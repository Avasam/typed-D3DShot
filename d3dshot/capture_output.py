from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING, Any, Final, Literal, TypeVar, overload

if TYPE_CHECKING:
    from collections.abc import Sequence
    from ctypes import _CVoidConstPLike

    import numpy as np
    import numpy.typing as npt
    import torch
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


class CaptureOutputs(Enum):
    PIL = auto()
    NUMPY = auto()
    NUMPY_FLOAT = auto()
    PYTORCH = auto()
    PYTORCH_FLOAT = auto()
    PYTORCH_GPU = auto()
    PYTORCH_FLOAT_GPU = auto()


capture_output_mapping: Final = {
    capture_output.name.lower(): capture_output for capture_output in CaptureOutputs
}
"""Deprecated, use `CaptureOutputs[key.upper()]` instead of `capture_output_mapping[key]`"""
capture_outputs: Final = [capture_output.name.lower() for capture_output in CaptureOutputs]
"""
Deprecated,
  use `CaptureOutputs.PIL.name` instead of `capture_outputs[CaptureOutputs.PIL.value]`
  use `CaptureOutputs(value).name` instead of `capture_outputs[value]`
"""


class CaptureOutput:
    @overload
    def __new__(
        cls, backend: Literal[CaptureOutputs.PIL] = CaptureOutputs.PIL
    ) -> PILCaptureOutput: ...
    @overload
    def __new__(cls, backend: Literal[CaptureOutputs.NUMPY]) -> NumpyCaptureOutput: ...
    @overload
    def __new__(cls, backend: Literal[CaptureOutputs.NUMPY_FLOAT]) -> NumpyFloatCaptureOutput: ...
    @overload
    def __new__(cls, backend: Literal[CaptureOutputs.PYTORCH]) -> PytorchCaptureOutput: ...
    @overload
    def __new__(
        cls, backend: Literal[CaptureOutputs.PYTORCH_FLOAT]
    ) -> PytorchFloatCaptureOutput: ...
    @overload
    def __new__(cls, backend: Literal[CaptureOutputs.PYTORCH_GPU]) -> PytorchGPUCaptureOutput: ...
    @overload
    def __new__(
        cls, backend: Literal[CaptureOutputs.PYTORCH_FLOAT_GPU]
    ) -> PytorchFloatGPUCaptureOutput: ...
    @overload
    def __new__(cls, backend: CaptureOutputs) -> CaptureOutput: ...
    def __new__(cls, backend: CaptureOutputs = CaptureOutputs.PIL) -> CaptureOutput:  # noqa: PYI034
        return cls._initialize_backend(backend)

    def process(
        self,
        pointer: _CVoidConstPLike,
        pitch: int,
        size: int,
        width: int,
        height: int,
        region: tuple[int, int, int, int],
        rotation: Literal[0, 90, 180, 270],
    ) -> (
        # Include the full union for all subtypes
        npt.NDArray[np.uint8] | npt.NDArray[np.floating[npt.NBitBase]] | Image.Image | torch.Tensor
    ):
        raise NotImplementedError

    def to_pil(self, frame: Any) -> Image.Image:  # noqa: ANN401
        raise NotImplementedError

    def stack(
        self, frames: Sequence[Any], stack_dimension: Literal["first", "last"]
    ) -> (
        # Include the full union for all subtypes
        npt.NDArray[np.uint8]
        | npt.NDArray[np.floating[npt.NBitBase]]
        | Sequence[Image.Image]
        | torch.Tensor
    ):
        raise NotImplementedError

    @staticmethod
    def _initialize_backend(backend: CaptureOutputs) -> CaptureOutput:  # noqa: PLR0911
        # Use match-case in Python 3.10
        if backend == CaptureOutputs.PIL:
            from d3dshot.capture_outputs.pil_capture_output import PILCaptureOutput

            return PILCaptureOutput()
        if backend == CaptureOutputs.NUMPY:
            from d3dshot.capture_outputs.numpy_capture_output import NumpyCaptureOutput

            return NumpyCaptureOutput()
        if backend == CaptureOutputs.NUMPY_FLOAT:
            from d3dshot.capture_outputs.numpy_float_capture_output import NumpyFloatCaptureOutput

            return NumpyFloatCaptureOutput()
        if backend == CaptureOutputs.PYTORCH:
            from d3dshot.capture_outputs.pytorch_capture_output import PytorchCaptureOutput

            return PytorchCaptureOutput()
        if backend == CaptureOutputs.PYTORCH_FLOAT:
            from d3dshot.capture_outputs.pytorch_float_capture_output import (
                PytorchFloatCaptureOutput,
            )

            return PytorchFloatCaptureOutput()
        if backend == CaptureOutputs.PYTORCH_GPU:
            from d3dshot.capture_outputs.pytorch_gpu_capture_output import PytorchGPUCaptureOutput

            return PytorchGPUCaptureOutput()
        if backend == CaptureOutputs.PYTORCH_FLOAT_GPU:
            from d3dshot.capture_outputs.pytorch_float_gpu_capture_output import (
                PytorchFloatGPUCaptureOutput,
            )

            return PytorchFloatGPUCaptureOutput()
        raise ValueError("The specified backend is invalid!")


CaptureOutputBackend = TypeVar("CaptureOutputBackend", bound=CaptureOutput)
