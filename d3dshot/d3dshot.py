import collections
import gc
import os
import threading
import time

from d3dshot.capture_output import CaptureOutput, CaptureOutputs
from d3dshot.display import Display


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        else:
            import warnings

            warnings.warn(
                f"Only 1 instance of {cls.__name__} is allowed per process!"
                + "Returning the existing instance...",
                stacklevel=1,
            )

        return cls._instances[cls]


class D3DShot(metaclass=Singleton):
    def __init__(
        self,
        capture_output=CaptureOutputs.PIL,
        frame_buffer_size=60,
        pil_is_available=True,
        numpy_is_available=False,
        pytorch_is_available=False,
        pytorch_gpu_is_available=False,
    ) -> None:
        self.displays = None
        self.detect_displays()

        self.display = next(
            (display for display in self.displays if display.is_primary),
            self.displays[0],
        )

        self.capture_output = CaptureOutput(backend=capture_output)

        self.frame_buffer_size = frame_buffer_size
        self.frame_buffer = collections.deque([], self.frame_buffer_size)

        self.previous_screenshot = None

        self.region = None

        self._pil_is_available = pil_is_available
        self._numpy_is_available = numpy_is_available
        self._pytorch_is_available = pytorch_is_available
        self._pytorch_gpu_is_available = pytorch_gpu_is_available

        self._capture_thread = None
        self._is_capturing = False

    @property
    def is_capturing(self):
        return self._is_capturing

    def get_latest_frame(self):
        return self.get_frame(0)

    def get_frame(self, frame_index):
        if frame_index < 0 or (frame_index + 1) > len(self.frame_buffer):
            return None

        return self.frame_buffer[frame_index]

    def get_frames(self, frame_indices):
        frames = []

        for frame_index in frame_indices:
            frame = self.get_frame(frame_index)

            if frame is not None:
                frames.append(frame)

        return frames

    def get_frame_stack(self, frame_indices, stack_dimension=None):
        if stack_dimension not in {"first", "last"}:
            stack_dimension = "first"

        frames = self.get_frames(frame_indices)

        return self.capture_output.stack(frames, stack_dimension)

    def screenshot(self, region=None):
        region = self._validate_region(region)

        if self.previous_screenshot is None:
            frame = None

            while frame is None:
                frame = self.display.capture(self.capture_output.process, region=region)

            self.previous_screenshot = frame
            return frame
        for _ in range(300):
            frame = self.display.capture(self.capture_output.process, region=region)

            if frame is not None:
                self.previous_screenshot = frame
                return frame

        return self.previous_screenshot

    def screenshot_to_disk(self, directory=None, file_name=None, region=None):
        directory = self._validate_directory(directory)
        file_name = self._validate_file_name(file_name)

        file_path = f"{directory}/{file_name}"

        frame = self.screenshot(region=region)

        frame_pil = self.capture_output.to_pil(frame)
        frame_pil.save(file_path)

        return file_path

    def frame_buffer_to_disk(self, directory=None) -> None:
        directory = self._validate_directory(directory)

        # tuple cast to ensure an immutable frame buffer
        for i, frame in enumerate(tuple(self.frame_buffer)):
            frame_pil = self.capture_output.to_pil(frame)
            frame_pil.save(f"{directory}/{i + 1}.png")

    def capture(self, target_fps=60, region=None) -> bool:
        target_fps = self._validate_target_fps(target_fps)

        if self.is_capturing:
            return False

        self._is_capturing = True

        self._capture_thread = threading.Thread(target=self._capture, args=(target_fps, region))
        self._capture_thread.start()

        return True

    def screenshot_every(self, interval, region=None) -> bool:
        if self.is_capturing:
            return False

        interval = self._validate_interval(interval)

        self._is_capturing = True

        self._capture_thread = threading.Thread(
            target=self._screenshot_every, args=(interval, region)
        )
        self._capture_thread.start()

        return True

    def screenshot_to_disk_every(self, interval, directory=None, region=None) -> bool:
        if self.is_capturing:
            return False

        interval = self._validate_interval(interval)
        directory = self._validate_directory(directory)

        self._is_capturing = True

        self._capture_thread = threading.Thread(
            target=self._screenshot_to_disk_every, args=(interval, directory, region)
        )
        self._capture_thread.start()

        return True

    def stop(self) -> bool:
        if not self.is_capturing:
            return False

        self._is_capturing = False

        if self._capture_thread is not None:
            self._capture_thread.join(timeout=1)
            self._capture_thread = None

        return True

    def benchmark(self) -> None:
        print("Preparing Benchmark...")
        print()
        print(f"Capture Output: {self.capture_output.backend.__class__.__name__}")
        print(f"Display: {self.display}")
        print()

        frame_count = 0

        start_time = time.time()
        end_time = start_time + 60

        print("Capturing as many frames as possible in the next 60 seconds... Go!")

        while time.time() <= end_time:
            self.screenshot()
            frame_count += 1

        print(f"Done! Results: {round(frame_count / 60, 3)} FPS")

    def detect_displays(self) -> None:
        self._reset_displays()
        self.displays = Display.discover_displays()

    def _reset_displays(self) -> None:
        self.displays = []

    def _reset_frame_buffer(self) -> None:
        self.frame_buffer = collections.deque([], self.frame_buffer_size)

    def _validate_region(self, region):
        region = region or self.region or None

        if region is None:
            return None

        error_message = "'region' is expected to be a 4-length iterable"

        if not isinstance(region, tuple):
            try:
                region = tuple(region)
            except TypeError:
                raise AttributeError(error_message, region) from None

        valid = True

        for i, value in enumerate(region):
            if not isinstance(value, int):
                valid = False
                break

            if i == 2:
                if value <= region[0]:
                    valid = False
                    break
                continue
            if i == 3:
                if value <= region[1]:
                    valid = False
                    break
                continue
            if i == 4:
                raise AttributeError(error_message, region)

        if not valid:
            error_message = (
                "Invalid 'region' tuple. Make sure all values are ints and that 'right' and "
                + "'bottom' values are greater than their 'left' and 'top' counterparts"
            )
            raise AttributeError(error_message)

        return region

    @staticmethod
    def _validate_target_fps(target_fps: int) -> int:
        if not isinstance(target_fps, int) or target_fps < 1:
            raise AttributeError("'target_fps' should be an int greater than 0")

        return target_fps

    @staticmethod
    def _validate_directory(directory):
        if directory is None:
            directory = "."
        if not isinstance(directory, str):
            directory = str(directory)

        # We don't need to pull in pathlib just for this
        if not os.path.isdir(directory):  # noqa: PTH112
            raise NotADirectoryError(directory)

        return directory

    @staticmethod
    def _validate_file_name(file_name: str | None) -> str:
        if file_name is None or not isinstance(file_name, str):
            file_name = f"{time.time()}.png"

        file_extension = file_name.split(".")[-1]

        if file_extension not in {"png", "jpg", "jpeg"}:
            raise AttributeError("'file_name' needs to end in .png, .jpg or .jpeg")

        return file_name

    @staticmethod
    def _validate_interval(interval):
        if not isinstance(interval, (int, float)) or interval < 1.0:
            raise AttributeError("'interval' should be one of (int, float) and be >= 1.0")

        return interval

    def _capture(self, target_fps, region) -> None:
        self._reset_frame_buffer()

        frame_time = 1 / target_fps

        while self.is_capturing:
            cycle_start = time.time()

            frame = self.display.capture(
                self.capture_output.process, region=self._validate_region(region)
            )

            if frame is not None:
                self.frame_buffer.appendleft(frame)
            elif len(self.frame_buffer):
                self.frame_buffer.appendleft(self.frame_buffer[0])

            gc.collect()

            cycle_end = time.time()

            frame_time_left = frame_time - (cycle_end - cycle_start)

            if frame_time_left > 0:
                time.sleep(frame_time_left)

        self._is_capturing = False

    def _screenshot_every(self, interval, region) -> None:
        self._reset_frame_buffer()

        while self.is_capturing:
            cycle_start = time.time()

            frame = self.screenshot(region=self._validate_region(region))
            self.frame_buffer.appendleft(frame)

            cycle_end = time.time()

            time_left = interval - (cycle_end - cycle_start)

            if time_left > 0:
                time.sleep(time_left)

        self._is_capturing = False

    def _screenshot_to_disk_every(self, interval, directory, region) -> None:
        while self.is_capturing:
            cycle_start = time.time()

            self.screenshot_to_disk(directory=directory, region=self._validate_region(region))

            cycle_end = time.time()

            time_left = interval - (cycle_end - cycle_start)

            if time_left > 0:
                time.sleep(time_left)

        self._is_capturing = False
