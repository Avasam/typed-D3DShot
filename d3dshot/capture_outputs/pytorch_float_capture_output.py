from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np

from d3dshot._compat import override
from d3dshot.capture_outputs.pytorch_capture_output import PytorchCaptureOutput

if TYPE_CHECKING:
    from ctypes import _CVoidConstPLike

    import torch
    from numpy._typing._array_like import _ArrayLikeFloat_co
    from PIL import Image


class PytorchFloatCaptureOutput(PytorchCaptureOutput):
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
        return image / 255.0

    @override
    def to_pil(self, frame: _ArrayLikeFloat_co) -> Image.Image:  # type: ignore[override]
        from PIL import Image

        # torch.Tensor doesn't match npt.NDArray[np.floating[npt.NBitBase]]
        # idk what's the right type here
        return Image.fromarray(np.array(frame * 255.0, dtype=np.uint8))  # type: ignore[operator]
