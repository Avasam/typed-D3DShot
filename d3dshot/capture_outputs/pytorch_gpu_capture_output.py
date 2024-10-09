from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np
import torch

from d3dshot._compat import override
from d3dshot.capture_outputs.pytorch_capture_output import PytorchCaptureOutput

if TYPE_CHECKING:
    from ctypes import _CVoidConstPLike

    from PIL import Image


class PytorchGPUCaptureOutput(PytorchCaptureOutput):
    def __init__(self) -> None:
        self.device = torch.device("cuda")
        torch.tensor([0], device=self.device)  # Warm up CUDA

    @override
    def process(
        self,
        pointer: _CVoidConstPLike,
        pitch: int,
        size: int,
        width: int,
        height: int,
        region: tuple[int, int, int, int],
        rotation: Literal[0, 90, 180, 270],
    ) -> torch.Tensor:
        image = super().process(pointer, pitch, size, width, height, region, rotation)
        return image.to(self.device)

    @override
    def to_pil(self, frame: torch.Tensor) -> Image.Image:  # type: ignore[override]
        from PIL import Image

        return Image.fromarray(np.array(frame.cpu()))
