from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np

from d3dshot._compat import override
from d3dshot.capture_outputs.numpy_capture_output import NumpyCaptureOutput

if TYPE_CHECKING:
    from ctypes import _CVoidConstPLike

    import numpy.typing as npt
    from PIL import Image


class NumpyFloatCaptureOutput(NumpyCaptureOutput):
    @override
    def process(  # type: ignore[override]
        self,
        pointer: _CVoidConstPLike,
        pitch: int,
        size: int,
        width: int,
        height: int,
        region: tuple[int, int, int, int],
        rotation: Literal[0, 90, 180, 270],
    ) -> npt.NDArray[np.floating[npt.NBitBase]]:
        image = super().process(pointer, pitch, size, width, height, region, rotation)
        return np.divide(image, 255.0)

    @override
    def to_pil(self, frame: npt.NDArray[np.floating[npt.NBitBase]]) -> Image.Image:  # type: ignore[override]
        from PIL import Image

        return Image.fromarray(np.array(frame * 255.0, dtype=np.uint8))
