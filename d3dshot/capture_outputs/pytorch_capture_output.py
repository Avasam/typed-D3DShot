from __future__ import annotations

import ctypes
from typing import TYPE_CHECKING, Literal

import numpy as np
import torch

from d3dshot._compat import override
from d3dshot.capture_output import CaptureOutput

if TYPE_CHECKING:
    from collections.abc import Sequence
    from ctypes import _CVoidConstPLike

    import numpy.typing as npt
    from PIL import Image
    from typing_extensions import Self


class PytorchCaptureOutput(CaptureOutput):
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
    ) -> torch.Tensor:
        # We proxy through numpy's ctypes interface because making
        # a PyTorch tensor from a bytearray is HORRIBLY slow...
        image: npt.NDArray[np.uint8] = np.empty((size,), dtype=np.uint8)
        ctypes.memmove(image.ctypes.data, pointer, size)

        pitch_per_channel = pitch // 4

        # Use match-case in Python 3.10
        if rotation == 0:
            image = np.reshape(image, (height, pitch_per_channel, 4))[..., [2, 1, 0]]
        elif rotation == 90:
            image = np.reshape(image, (width, pitch_per_channel, 4))[..., [2, 1, 0]]
            image = np.rot90(image, axes=(1, 0)).copy()
        elif rotation == 180:
            image = np.reshape(image, (height, pitch_per_channel, 4))[..., [2, 1, 0]]
            image = np.rot90(image, k=2, axes=(0, 1)).copy()
        elif rotation == 270:
            image = np.reshape(image, (width, pitch_per_channel, 4))[..., [2, 1, 0]]
            image = np.rot90(image, axes=(0, 1)).copy()

        # Trim pitch padding
        if rotation in {0, 180} and pitch_per_channel != width:
            image = image[:, :width, :]
        elif rotation in {90, 270} and pitch_per_channel != height:
            image = image[:height, :, :]

        # Region slicing
        if region[2] - region[0] != width or region[3] - region[1] != height:
            image = image[region[1] : region[3], region[0] : region[2], :]

        return torch.from_numpy(image)

    @override
    def to_pil(self, frame: npt.ArrayLike) -> Image.Image:
        from PIL import Image

        return Image.fromarray(np.array(frame))

    @override
    def stack(
        self,
        frames: Sequence[torch.Tensor],
        stack_dimension: Literal["first", "last"],
    ) -> torch.Tensor:
        if stack_dimension == "first":
            dimension = 0
        elif stack_dimension == "last":
            dimension = -1
        else:
            raise ValueError(f"stack_dimension must be 'first' or 'last', got {stack_dimension!r}")

        # I assume torch's type is wrong and it can take any sequence
        # If untrue, let's coerce it to a tuple/list
        return torch.stack(frames, dim=dimension)  # type: ignore[arg-type]
