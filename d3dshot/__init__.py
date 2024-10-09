from d3dshot.capture_output import (
    CaptureOutputs,
    capture_output_mapping,  # noqa: F401 # Deprecated, make it still runtime available
    capture_outputs,  # noqa: F401 # Deprecated, make it still runtime available
)
from d3dshot.d3dshot import D3DShot

pil_is_available = importlib.util.find_spec("PIL") is not None
numpy_is_available = importlib.util.find_spec("numpy") is not None

pytorch_is_available = importlib.util.find_spec("torch") is not None and numpy_is_available

pytorch_gpu_is_available = False

if pytorch_is_available:
    import torch

    pytorch_gpu_is_available = torch.cuda.is_available()



def determine_available_capture_outputs():
    available_capture_outputs = []

    if pil_is_available:
        available_capture_outputs.append(CaptureOutputs.PIL)

    if numpy_is_available:
        available_capture_outputs.extend((CaptureOutputs.NUMPY, CaptureOutputs.NUMPY_FLOAT))

    if pytorch_is_available:
        available_capture_outputs.extend((CaptureOutputs.PYTORCH, CaptureOutputs.PYTORCH_FLOAT))

    if pytorch_gpu_is_available:
        available_capture_outputs.extend((
            CaptureOutputs.PYTORCH_GPU,
            CaptureOutputs.PYTORCH_FLOAT_GPU,
        ))

    return available_capture_outputs


def create(capture_output="pil", frame_buffer_size=60):
    capture_output = _validate_capture_output(capture_output)
    frame_buffer_size = _validate_frame_buffer_size(frame_buffer_size)

    return D3DShot(
        capture_output=capture_output,
        frame_buffer_size=frame_buffer_size,
        pil_is_available=pil_is_available,
        numpy_is_available=numpy_is_available,
        pytorch_is_available=pytorch_is_available,
        pytorch_gpu_is_available=pytorch_gpu_is_available,
    )


def _raise_invalid_output_name(
    capture_output_name: str,
    available_capture_outputs: Iterable[CaptureOutputs],
    error: KeyError | None,
) -> NoReturn:
    raise ValueError(
        f"Invalid Capture Output '{capture_output_name}'. Available Options: "
        + ", ".join([co.name.lower() for co in available_capture_outputs])
    ) from error


def _validate_capture_output_available(capture_output_name: str) -> CaptureOutputs:
    available_capture_outputs = determine_available_capture_outputs()

    try:
        capture_output = CaptureOutputs[capture_output_name.upper()]
    except KeyError as error:
        _raise_invalid_output_name(capture_output_name, available_capture_outputs, error)

    if capture_output not in available_capture_outputs:
        _raise_invalid_output_name(capture_output_name, available_capture_outputs, None)

    return capture_output


def _validate_frame_buffer_size(frame_buffer_size):
    if not isinstance(frame_buffer_size, int) or frame_buffer_size < 1:
        raise AttributeError("'frame_buffer_size' should be an int greater than 0")

    return frame_buffer_size
