from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np
import torch

from d3dshot._compat import override
from d3dshot.capture_outputs.pytorch_gpu_capture_output import PytorchGPUCaptureOutput

if TYPE_CHECKING:
    from ctypes import _CVoidConstPLike

    from PIL import Image


class PytorchFloatGPUCaptureOutput(PytorchGPUCaptureOutput):
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
        # https://github.com/pytorch/pytorch/issues/47027
        return image.type(torch.cuda.FloatTensor) / 255.0  # type: ignore[operator, return-value]

    @override
    def to_pil(self, frame: torch.Tensor) -> Image.Image:  # type: ignore[override]
        from PIL import Image

        return Image.fromarray(np.array(frame.cpu() * 255.0, dtype=np.uint8))
