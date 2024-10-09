from __future__ import annotations

from typing import TYPE_CHECKING, Literal, NoReturn, overload

from d3dshot._compat import (
    numpy_is_available as numpy_is_available,
    pil_is_available as pil_is_available,
    pytorch_gpu_is_available as pytorch_gpu_is_available,
    pytorch_is_available as pytorch_is_available,
)
from d3dshot.capture_output import (
    CaptureOutputs,
    capture_output_mapping,  # noqa: F401 # Deprecated, make it still runtime available
    capture_outputs,  # noqa: F401 # Deprecated, make it still runtime available
)
from d3dshot.d3dshot import D3DShot

if TYPE_CHECKING:
    from collections.abc import Iterable

    from d3dshot.capture_output import CaptureOutput
    from d3dshot.capture_outputs.numpy_capture_output import NumpyCaptureOutput
    from d3dshot.capture_outputs.numpy_float_capture_output import NumpyFloatCaptureOutput
    from d3dshot.capture_outputs.pil_capture_output import PILCaptureOutput
    from d3dshot.capture_outputs.pytorch_capture_output import PytorchCaptureOutput
    from d3dshot.capture_outputs.pytorch_float_capture_output import PytorchFloatCaptureOutput
    from d3dshot.capture_outputs.pytorch_float_gpu_capture_output import (
        PytorchFloatGPUCaptureOutput,
    )
    from d3dshot.capture_outputs.pytorch_gpu_capture_output import PytorchGPUCaptureOutput


def determine_available_capture_outputs() -> list[CaptureOutputs]:
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


@overload
def create(  # pyright: ignore[reportOverlappingOverload]
    capture_output: Literal["numpy"], frame_buffer_size: int = 60
) -> D3DShot[NumpyCaptureOutput]: ...
@overload
def create(
    capture_output: Literal["numpy_float"], frame_buffer_size: int = 60
) -> D3DShot[NumpyFloatCaptureOutput]: ...
@overload
def create(
    capture_output: Literal["pytorch"], frame_buffer_size: int = 60
) -> D3DShot[PytorchCaptureOutput]: ...
@overload
def create(
    capture_output: Literal["pytorch_float"], frame_buffer_size: int = 60
) -> D3DShot[PytorchFloatCaptureOutput]: ...
@overload
def create(
    capture_output: Literal["pytorch_gpu"], frame_buffer_size: int = 60
) -> D3DShot[PytorchFloatGPUCaptureOutput]: ...
@overload
def create(
    capture_output: Literal["pytorch_float_gpu"], frame_buffer_size: int = 60
) -> D3DShot[PytorchGPUCaptureOutput]: ...
@overload
def create(
    capture_output: Literal["pil"] = "pil", frame_buffer_size: int = 60
) -> D3DShot[PILCaptureOutput]: ...
@overload
def create(capture_output: str, frame_buffer_size: int = 60) -> D3DShot[CaptureOutput]: ...
def create(capture_output: str = "pil", frame_buffer_size: int = 60) -> D3DShot[CaptureOutput]:  # type: ignore[misc]
    capture_output_enum = _validate_capture_output_available(capture_output)
    frame_buffer_size = _validate_frame_buffer_size(frame_buffer_size)

    return D3DShot(
        capture_output=capture_output_enum,
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


def _validate_frame_buffer_size(frame_buffer_size: int) -> int:
    if not isinstance(frame_buffer_size, int) or frame_buffer_size < 1:
        raise AttributeError("'frame_buffer_size' should be an int greater than 0")

    return frame_buffer_size
