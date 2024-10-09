from __future__ import annotations

import gc
import os.path
import threading
import time
from collections import deque
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Literal, TypeVar, overload

from d3dshot._compat import override
from d3dshot.capture_output import CaptureOutput, CaptureOutputBackend, CaptureOutputs
from d3dshot.display import Display

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

    import numpy as np
    import numpy.typing as npt
    import torch
    from _typeshed import StrPath
    from PIL import Image

    from d3dshot.capture_outputs.numpy_capture_output import NumpyCaptureOutput
    from d3dshot.capture_outputs.numpy_float_capture_output import NumpyFloatCaptureOutput
    from d3dshot.capture_outputs.pil_capture_output import PILCaptureOutput
    from d3dshot.capture_outputs.pytorch_capture_output import PytorchCaptureOutput
    from d3dshot.capture_outputs.pytorch_float_capture_output import PytorchFloatCaptureOutput
    from d3dshot.capture_outputs.pytorch_float_gpu_capture_output import (
        PytorchFloatGPUCaptureOutput,
    )
    from d3dshot.capture_outputs.pytorch_gpu_capture_output import PytorchGPUCaptureOutput

_FloatT = TypeVar("_FloatT", bound=float)


class Singleton(type):
    _instances: ClassVar[dict[Singleton, Any]] = {}

    @override
    def __call__(
        cls, *args: object, **kwargs: object
    ) -> Any:  # TODO (Avasam): Try with object once everything is typed
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


class D3DShot(Generic[CaptureOutputBackend], metaclass=Singleton):  # noqa: PLR0904
    @overload
    def __init__(
        self: D3DShot[PILCaptureOutput],
        capture_output: Literal[CaptureOutputs.PIL] = CaptureOutputs.PIL,
        frame_buffer_size: int = 60,
        pil_is_available: bool = True,
        numpy_is_available: bool = False,
        pytorch_is_available: bool = False,
        pytorch_gpu_is_available: bool = False,
    ) -> None: ...
    @overload
    def __init__(
        self: D3DShot[NumpyCaptureOutput],
        capture_output: Literal[CaptureOutputs.NUMPY],
        frame_buffer_size: int = 60,
        pil_is_available: bool = True,
        numpy_is_available: bool = False,
        pytorch_is_available: bool = False,
        pytorch_gpu_is_available: bool = False,
    ) -> None: ...
    @overload
    def __init__(
        self: D3DShot[NumpyFloatCaptureOutput],
        capture_output: Literal[CaptureOutputs.NUMPY_FLOAT],
        frame_buffer_size: int = 60,
        pil_is_available: bool = True,
        numpy_is_available: bool = False,
        pytorch_is_available: bool = False,
        pytorch_gpu_is_available: bool = False,
    ) -> None: ...
    @overload
    def __init__(
        self: D3DShot[PytorchCaptureOutput],
        capture_output: Literal[CaptureOutputs.PYTORCH],
        frame_buffer_size: int = 60,
        pil_is_available: bool = True,
        numpy_is_available: bool = False,
        pytorch_is_available: bool = False,
        pytorch_gpu_is_available: bool = False,
    ) -> None: ...
    @overload
    def __init__(
        self: D3DShot[PytorchFloatCaptureOutput],
        capture_output: Literal[CaptureOutputs.PYTORCH_FLOAT],
        frame_buffer_size: int = 60,
        pil_is_available: bool = True,
        numpy_is_available: bool = False,
        pytorch_is_available: bool = False,
        pytorch_gpu_is_available: bool = False,
    ) -> None: ...
    @overload
    def __init__(
        self: D3DShot[PytorchGPUCaptureOutput],
        capture_output: Literal[CaptureOutputs.PYTORCH_GPU],
        frame_buffer_size: int = 60,
        pil_is_available: bool = True,
        numpy_is_available: bool = False,
        pytorch_is_available: bool = False,
        pytorch_gpu_is_available: bool = False,
    ) -> None: ...
    @overload
    def __init__(
        self: D3DShot[PytorchFloatGPUCaptureOutput],
        capture_output: Literal[CaptureOutputs.PYTORCH_FLOAT_GPU],
        frame_buffer_size: int = 60,
        pil_is_available: bool = True,
        numpy_is_available: bool = False,
        pytorch_is_available: bool = False,
        pytorch_gpu_is_available: bool = False,
    ) -> None: ...
    @overload
    def __init__(
        self,
        capture_output: CaptureOutputs,
        frame_buffer_size: int = 60,
        pil_is_available: bool = True,
        numpy_is_available: bool = False,
        pytorch_is_available: bool = False,
        pytorch_gpu_is_available: bool = False,
    ) -> None: ...
    def __init__(
        self,
        capture_output: CaptureOutputs = CaptureOutputs.PIL,
        frame_buffer_size: int = 60,
        pil_is_available: bool = True,
        numpy_is_available: bool = False,
        pytorch_is_available: bool = False,
        pytorch_gpu_is_available: bool = False,
    ) -> None:
        self.displays: list[Display] = []
        self.detect_displays()

        self.display = next(
            (display for display in self.displays if display.is_primary),
            self.displays[0],
        )

        self.capture_output = CaptureOutput(backend=capture_output)

        self.frame_buffer_size = frame_buffer_size
        self.frame_buffer: deque[
            npt.NDArray[np.uint8]
            | npt.NDArray[np.floating[npt.NBitBase]]
            | Image.Image
            | torch.Tensor
        ] = deque(maxlen=self.frame_buffer_size)

        self.previous_screenshot = None

        self.region = None

        self._pil_is_available = pil_is_available
        self._numpy_is_available = numpy_is_available
        self._pytorch_is_available = pytorch_is_available
        self._pytorch_gpu_is_available = pytorch_gpu_is_available

        self._capture_thread: threading.Thread | None = None
        self._is_capturing = False

    @property
    def is_capturing(self) -> bool:
        return self._is_capturing

    @overload
    def get_latest_frame(self: D3DShot[NumpyCaptureOutput]) -> npt.NDArray[np.uint8] | None: ...
    @overload
    def get_latest_frame(
        self: D3DShot[NumpyFloatCaptureOutput],
    ) -> npt.NDArray[np.floating[npt.NBitBase]] | None: ...
    @overload
    def get_latest_frame(self: D3DShot[PILCaptureOutput]) -> Image.Image | None: ...
    @overload
    def get_latest_frame(self: D3DShot[PytorchCaptureOutput]) -> torch.Tensor | None: ...
    def get_latest_frame(
        self,
    ) -> (
        npt.NDArray[np.uint8]
        | npt.NDArray[np.floating[npt.NBitBase]]
        | Image.Image
        | torch.Tensor
        | None
    ):
        return self.get_frame(0)

    @overload
    def get_frame(
        self: D3DShot[NumpyCaptureOutput], frame_index: int
    ) -> npt.NDArray[np.uint8] | None: ...
    @overload
    def get_frame(
        self: D3DShot[NumpyFloatCaptureOutput], frame_index: int
    ) -> npt.NDArray[np.floating[npt.NBitBase]] | None: ...
    @overload
    def get_frame(self: D3DShot[PILCaptureOutput], frame_index: int) -> Image.Image | None: ...
    @overload
    def get_frame(self: D3DShot[PytorchCaptureOutput], frame_index: int) -> torch.Tensor | None: ...
    @overload
    def get_frame(
        self, frame_index: int
    ) -> (
        npt.NDArray[np.uint8]
        | npt.NDArray[np.floating[npt.NBitBase]]
        | Image.Image
        | torch.Tensor
        | None
    ): ...
    def get_frame(
        self, frame_index: int
    ) -> (
        npt.NDArray[np.uint8]
        | npt.NDArray[np.floating[npt.NBitBase]]
        | Image.Image
        | torch.Tensor
        | None
    ):
        if frame_index < 0 or (frame_index + 1) > len(self.frame_buffer):
            return None

        return self.frame_buffer[frame_index]

    @overload
    def get_frames(
        self: D3DShot[NumpyCaptureOutput],
        frame_indices: Iterable[int],
    ) -> list[npt.NDArray[np.uint8]]: ...
    @overload
    def get_frames(
        self: D3DShot[NumpyFloatCaptureOutput],
        frame_indices: Iterable[int],
    ) -> list[npt.NDArray[np.floating[npt.NBitBase]]]: ...
    @overload
    def get_frames(
        self: D3DShot[PILCaptureOutput],
        frame_indices: Iterable[int],
    ) -> list[Image.Image]: ...
    @overload
    def get_frames(
        self: D3DShot[PytorchCaptureOutput],
        frame_indices: Iterable[int],
    ) -> list[torch.Tensor]: ...
    @overload
    def get_frames(
        self, frame_indices: Iterable[int]
    ) -> (
        list[npt.NDArray[np.uint8]]
        | list[npt.NDArray[np.floating[npt.NBitBase]]]
        | list[Image.Image]
        | list[torch.Tensor]
    ): ...
    def get_frames(
        self, frame_indices: Iterable[int]
    ) -> (
        list[npt.NDArray[np.uint8]]
        | list[npt.NDArray[np.floating[npt.NBitBase]]]
        | list[Image.Image]
        | list[torch.Tensor]
    ):
        # The proper arg-type is encoded as the generic
        frames: list[Any] = []

        for frame_index in frame_indices:
            frame = self.get_frame(frame_index)

            if frame is not None:
                frames.append(frame)

        return frames

    @overload
    def get_frame_stack(
        self: D3DShot[NumpyCaptureOutput],
        frame_indices: Iterable[int],
        stack_dimension: Literal["first", "last"] | None = None,
    ) -> npt.NDArray[np.uint8]: ...
    @overload
    def get_frame_stack(
        self: D3DShot[NumpyFloatCaptureOutput],
        frame_indices: Iterable[int],
        stack_dimension: Literal["first", "last"] | None = None,
    ) -> npt.NDArray[np.floating[npt.NBitBase]]: ...
    @overload
    def get_frame_stack(
        self: D3DShot[PILCaptureOutput],
        frame_indices: Iterable[int],
        stack_dimension: Literal["first", "last"] | None = None,
    ) -> list[Image.Image]: ...
    @overload
    def get_frame_stack(
        self: D3DShot[PytorchCaptureOutput],
        frame_indices: Iterable[int],
        stack_dimension: Literal["first", "last"] | None = None,
    ) -> torch.Tensor: ...
    def get_frame_stack(
        self, frame_indices: Iterable[int], stack_dimension: Literal["first", "last"] | None = None
    ) -> (
        npt.NDArray[np.uint8]
        | npt.NDArray[np.floating[npt.NBitBase]]
        | Sequence[Image.Image]
        | torch.Tensor
    ):
        if stack_dimension not in {"first", "last"}:
            stack_dimension = "first"

        frames = self.get_frames(frame_indices)

        return self.capture_output.stack(frames, stack_dimension)

    @overload
    def screenshot(
        self: D3DShot[NumpyCaptureOutput],
        region: Sequence[int] | None = None,
        *,
        skip_region_validation: bool = False,
    ) -> npt.NDArray[np.uint8]: ...
    @overload
    def screenshot(
        self: D3DShot[NumpyFloatCaptureOutput],
        region: Sequence[int] | None = None,
        *,
        skip_region_validation: bool = False,
    ) -> npt.NDArray[np.floating[npt.NBitBase]]: ...
    @overload
    def screenshot(
        self: D3DShot[PILCaptureOutput],
        region: Sequence[int] | None = None,
        *,
        skip_region_validation: bool = False,
    ) -> Image.Image: ...
    @overload
    def screenshot(
        self: D3DShot[PytorchCaptureOutput],
        region: Sequence[int] | None = None,
        *,
        skip_region_validation: bool = False,
    ) -> torch.Tensor: ...
    @overload
    def screenshot(
        self,
        region: Sequence[int] | None = None,
        *,
        skip_region_validation: bool = False,
    ) -> (
        npt.NDArray[np.uint8] | npt.NDArray[np.floating[npt.NBitBase]] | Image.Image | torch.Tensor
    ): ...
    def screenshot(
        self,
        region: Sequence[int] | None = None,
        *,
        skip_region_validation: bool = False,
    ) -> (
        npt.NDArray[np.uint8] | npt.NDArray[np.floating[npt.NBitBase]] | Image.Image | torch.Tensor
    ):
        if not skip_region_validation:
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

    def screenshot_to_disk(
        self,
        directory: StrPath | None = None,
        file_name: str | None = None,
        region: Sequence[int] | None = None,
        *,
        skip_region_validation: bool = False,
    ) -> str:
        directory = self._validate_directory(directory)
        file_name = self._validate_file_name(file_name)

        file_path = f"{directory}/{file_name}"

        frame = self.screenshot(region=region, skip_region_validation=skip_region_validation)

        frame_pil = self.capture_output.to_pil(frame)
        frame_pil.save(file_path)

        return file_path

    def frame_buffer_to_disk(self, directory: StrPath | None = None) -> None:
        directory = self._validate_directory(directory)

        # tuple cast to ensure an immutable frame buffer
        for i, frame in enumerate(tuple(self.frame_buffer)):
            frame_pil = self.capture_output.to_pil(frame)
            frame_pil.save(f"{directory}/{i + 1}.png")

    def capture(self, target_fps: int = 60, region: Sequence[int] | None = None) -> bool:
        target_fps = self._validate_target_fps(target_fps)

        if self.is_capturing:
            return False

        self._is_capturing = True

        self._capture_thread = threading.Thread(target=self._capture, args=(target_fps, region))
        self._capture_thread.start()

        return True

    def screenshot_every(self, interval: float, region: Sequence[int] | None = None) -> bool:
        if self.is_capturing:
            return False

        interval = self._validate_interval(interval)

        self._is_capturing = True

        self._capture_thread = threading.Thread(
            target=self._screenshot_every, args=(interval, region)
        )
        self._capture_thread.start()

        return True

    def screenshot_to_disk_every(
        self, interval: float, directory: StrPath | None = None, region: Sequence[int] | None = None
    ) -> bool:
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
        self.frame_buffer = deque(maxlen=self.frame_buffer_size)

    @overload
    def _validate_region(self, region: tuple[()] | None) -> None: ...  # type: ignore[overload-overlap]
    @overload
    def _validate_region(self, region: Sequence[int]) -> tuple[int, int, int, int]: ...
    def _validate_region(self, region: Sequence[int] | None) -> tuple[int, int, int, int] | None:
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

        return region  # type: ignore[return-value] # This method typeguards

    @staticmethod
    def _validate_target_fps(target_fps: int) -> int:
        if not isinstance(target_fps, int) or target_fps < 1:
            raise AttributeError("'target_fps' should be an int greater than 0")

        return target_fps

    @staticmethod
    def _validate_directory(directory: StrPath | None) -> str:
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
    def _validate_interval(interval: _FloatT) -> _FloatT:
        if not isinstance(interval, (int, float)) or interval < 1.0:
            raise AttributeError("'interval' should be one of (int, float) and be >= 1.0")

        return interval

    def _capture(self, target_fps: int, region: Sequence[int] | None) -> None:
        self._reset_frame_buffer()

        frame_time = 1 / target_fps
        region = self._validate_region(region)
        while self.is_capturing:
            cycle_start = time.time()

            frame = self.display.capture(self.capture_output.process, region=region)

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

    def _screenshot_every(self, interval: float, region: Sequence[int] | None) -> None:
        self._reset_frame_buffer()
        region = self._validate_region(region)

        while self.is_capturing:
            cycle_start = time.time()

            frame = self.screenshot(region=region, skip_region_validation=True)
            self.frame_buffer.appendleft(frame)

            cycle_end = time.time()

            time_left = interval - (cycle_end - cycle_start)

            if time_left > 0:
                time.sleep(time_left)

        self._is_capturing = False

    def _screenshot_to_disk_every(
        self, interval: float, directory: StrPath | None, region: Sequence[int] | None
    ) -> None:
        region = self._validate_region(region)
        while self.is_capturing:
            cycle_start = time.time()

            self.screenshot_to_disk(directory=directory, region=region, skip_region_validation=True)

            cycle_end = time.time()

            time_left = interval - (cycle_end - cycle_start)

            if time_left > 0:
                time.sleep(time_left)

        self._is_capturing = False
