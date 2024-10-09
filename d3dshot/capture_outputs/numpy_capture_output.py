from __future__ import annotations

import ctypes
from typing import TYPE_CHECKING, Literal, TypeVar

import numpy as np

from d3dshot._compat import override
from d3dshot.capture_output import CaptureOutput

if TYPE_CHECKING:
    from collections.abc import Sequence
    from ctypes import _CVoidConstPLike

    import numpy.typing as npt
    from numpy._typing._array_like import _ArrayLike
    from PIL import Image
    from typing_extensions import Self

    # Same as numpy._core.shape_base._SCT, which was as numpy.core.shape_base._SCT before numpy 2
    _SCT = TypeVar("_SCT", bound=np.generic)


class NumpyCaptureOutput(CaptureOutput):
    def __new__(cls) -> Self:
        return super(CaptureOutput, cls).__new__(cls)  # type: ignore[misc]

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
    ) -> npt.NDArray[np.uint8]:
        image: npt.NDArray[np.uint8] = np.empty((size,), dtype=np.uint8)
        ctypes.memmove(image.ctypes.data, pointer, size)

        pitch_per_channel = pitch // 4

        # Use match-case in Python 3.10
        if rotation == 0:
            image = np.reshape(image, (height, pitch_per_channel, 4))[..., [2, 1, 0]]
        elif rotation == 90:
            image = np.reshape(image, (width, pitch_per_channel, 4))[..., [2, 1, 0]]
            image = np.rot90(image, axes=(1, 0))
        elif rotation == 180:
            image = np.reshape(image, (height, pitch_per_channel, 4))[..., [2, 1, 0]]
            image = np.rot90(image, k=2, axes=(0, 1))
        elif rotation == 270:
            image = np.reshape(image, (width, pitch_per_channel, 4))[..., [2, 1, 0]]
            image = np.rot90(image, axes=(0, 1))

        # Trim pitch padding
        if rotation in {0, 180} and pitch_per_channel != width:
            image = image[:, :width, :]
        elif rotation in {90, 270} and pitch_per_channel != height:
            image = image[:height, :, :]

        # Region slicing
        if region[2] - region[0] != width or region[3] - region[1] != height:
            image = image[region[1] : region[3], region[0] : region[2], :]

        return image

    @override
    def to_pil(self, frame: Image.SupportsArrayInterface) -> Image.Image:
        from PIL import Image

        return Image.fromarray(frame)

    @override
    # use of generics allows us to be more precise,
    # even if realistically we'll only get uint8 or floating
    def stack(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, frames: Sequence[_ArrayLike[_SCT]], stack_dimension: Literal["first", "last"]
    ) -> npt.NDArray[_SCT]:
        if stack_dimension == "first":
            dimension = 0
        elif stack_dimension == "last":
            dimension = -1
        else:
            raise ValueError(f"stack_dimension must be 'first' or 'last', got {stack_dimension!r}")

        return np.stack(frames, axis=dimension)
