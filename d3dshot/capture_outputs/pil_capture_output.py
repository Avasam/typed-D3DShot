from __future__ import annotations

import ctypes
from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal, TypeVar

from PIL import Image

from d3dshot._compat import override
from d3dshot.capture_output import CaptureOutput

if TYPE_CHECKING:
    from ctypes import _CVoidConstPLike

    from typing_extensions import Self

_ImageT = TypeVar("_ImageT", bound=Image.Image)
_ImageTs = TypeVar("_ImageTs", bound=Sequence[Image.Image])


class PILCaptureOutput(CaptureOutput):
    def __new__(cls) -> Self:
        return super(CaptureOutput, cls).__new__(cls)  # type: ignore[return-value]

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
    ) -> Image.Image:
        raw_bytes = ctypes.string_at(pointer, size=size)

        pitch_per_channel = pitch // 4

        # Use match-case in Python 3.10
        if rotation == 0:
            image = Image.frombytes("RGBA", (pitch_per_channel, height), raw_bytes)
        elif rotation == 90:
            image = Image.frombytes("RGBA", (pitch_per_channel, width), raw_bytes)
            image = image.transpose(Image.Transpose.ROTATE_270)
        elif rotation == 180:
            image = Image.frombytes("RGBA", (pitch_per_channel, height), raw_bytes)
            image = image.transpose(Image.Transpose.ROTATE_180)
        elif rotation == 270:
            image = Image.frombytes("RGBA", (pitch_per_channel, width), raw_bytes)
            image = image.transpose(Image.Transpose.ROTATE_90)
        else:
            raise ValueError(f"Invalid rotation {rotation}°")

        b, g, r, _ = image.split()
        image = Image.merge("RGB", (r, g, b))

        # Trim pitch padding
        if (rotation in {0, 180} and pitch_per_channel != width) or (
            rotation in {90, 270} and pitch_per_channel != height
        ):
            image = image.crop((0, 0, width, height))

        # Region slicing
        if region[2] - region[0] != width or region[3] - region[1] != height:
            image = image.crop(region)

        return image

    @override
    def to_pil(self, frame: _ImageT) -> _ImageT:
        return frame

    @override
    def stack(self, frames: _ImageTs, stack_dimension: object) -> _ImageTs:
        return frames
