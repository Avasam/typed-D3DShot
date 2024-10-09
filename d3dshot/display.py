from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypeVar, overload

import d3dshot.dll.d3d
import d3dshot.dll.dxgi
import d3dshot.dll.shcore
import d3dshot.dll.user32
from d3dshot._compat import override

if TYPE_CHECKING:
    from _ctypes import _Pointer
    from collections.abc import Callable, Sequence
    from ctypes import _CVoidConstPLike

    from typing_extensions import Self

_T = TypeVar("_T")


class DisplayCaptureError(Exception):
    pass


class DisplayCaptureWarning(DisplayCaptureError, Warning):  # noqa: N818
    pass


class Display:
    @overload
    def __init__(
        self,
        name: str | None,
        adapter_name: str | None,
        resolution: tuple[int, int] | None,
        position: d3dshot.dll.dxgi.PositionDict | None,
        rotation: Literal[0, 90, 180, 270] | None,
        scale_factor: float | None,
        is_primary: bool,
        hmonitor: int | None,
        dxgi_output: _Pointer[d3dshot.dll.dxgi.IDXGIOutput1],
        dxgi_adapter: _Pointer[d3dshot.dll.dxgi.IDXGIAdapter]
        | _Pointer[d3dshot.dll.dxgi.IDXGIAdapter1],
    ) -> None: ...
    @overload
    def __init__(
        self,
        name: str | None = None,
        adapter_name: str | None = None,
        resolution: tuple[int, int] | None = None,
        position: d3dshot.dll.dxgi.PositionDict | None = None,
        rotation: Literal[0, 90, 180, 270] | None = None,
        scale_factor: float | None = None,
        is_primary: bool = False,
        hmonitor: int | None = None,
        *,
        dxgi_output: _Pointer[d3dshot.dll.dxgi.IDXGIOutput1],
        dxgi_adapter: _Pointer[d3dshot.dll.dxgi.IDXGIAdapter]
        | _Pointer[d3dshot.dll.dxgi.IDXGIAdapter1],
    ) -> None: ...
    def __init__(  # noqa: PLR0913, PLR0917
        self,
        name: str | None = None,
        adapter_name: str | None = None,
        resolution: tuple[int, int] | None = None,
        position: d3dshot.dll.dxgi.PositionDict | None = None,
        rotation: Literal[0, 90, 180, 270] | None = None,
        scale_factor: float | None = None,
        is_primary: bool = False,
        hmonitor: int | None = None,
        dxgi_output: _Pointer[d3dshot.dll.dxgi.IDXGIOutput1] | None = None,
        # Mypy doesn't support _ctypes._Pointer subclasses,
        # so we must specify a union of all subclasses in param
        dxgi_adapter: _Pointer[d3dshot.dll.dxgi.IDXGIAdapter]
        | _Pointer[d3dshot.dll.dxgi.IDXGIAdapter1]
        | None = None,
    ) -> None:
        if dxgi_output is None or dxgi_adapter is None:
            # TODO (Avasam): Consider removing default param in an update
            raise TypeError("dxgi_output and dxgi_adapter parameters for Display() cannot be None")
        self.name = name or "Unknown"
        self.adapter_name = adapter_name or "Unknown Adapter"

        self.resolution = resolution or (0, 0)

        self.position = position or d3dshot.dll.dxgi.PositionDict(left=0, top=0, right=0, bottom=0)
        self.rotation: Literal[0, 90, 180, 270] = rotation or 0
        self.scale_factor = scale_factor or 1.0

        self.is_primary = is_primary
        self.hmonitor = hmonitor or 0

        self.dxgi_output = dxgi_output
        self.dxgi_adapter = dxgi_adapter

        self.dxgi_output_duplication = self._initialize_dxgi_output_duplication()

    @override
    def __repr__(self) -> str:
        name = self.name
        adapter = self.adapter_name
        resolution = f"{self.resolution[0]}x{self.resolution[1]}"
        rotation = self.rotation
        scale_factor = {self.scale_factor}
        primary = {self.is_primary}
        return f"<Display {name=} {adapter=} {resolution=} {rotation=} {scale_factor=} {primary=}>"

    def capture(
        self,
        process_func: Callable[
            [
                _CVoidConstPLike,
                int,
                int,
                int,
                int,
                tuple[int, int, int, int],
                Literal[0, 90, 180, 270],
            ],
            _T,
        ],
        region: Sequence[int] | None = None,
    ) -> _T | None:
        region = self._get_clean_region(region)

        try:
            return d3dshot.dll.dxgi.get_dxgi_output_duplication_frame(
                self.dxgi_output_duplication,
                self.d3d_device,
                process_func=process_func,
                width=self.resolution[0],
                height=self.resolution[1],
                region=region,
                rotation=self.rotation,
            )
        except Exception as _error:  # noqa: BLE001 # See warning. We want more precise exceptions eventually
            import traceback
            import warnings

            warnings.warn(
                "Caught an Error in Display.capture, downgrading to Warning. "
                + "This may become a CaptureOutputError in the future:\n"
                + traceback.format_exc(),
                DisplayCaptureWarning,
                stacklevel=2,
            )
            # raise DisplayCaptureError(*error.args) from _error
            return None

    def _initialize_dxgi_output_duplication(
        self,
    ) -> _Pointer[d3dshot.dll.dxgi.IDXGIOutputDuplication]:
        (
            self.d3d_device,
            self.d3d_device_context,
        ) = d3dshot.dll.d3d.initialize_d3d_device(self.dxgi_adapter)

        return d3dshot.dll.dxgi.initialize_dxgi_output_duplication(
            self.dxgi_output, self.d3d_device
        )

    def _get_clean_region(self, region: Sequence[int] | None) -> tuple[int, int, int, int]:
        if region is None:
            return (0, 0, self.resolution[0], self.resolution[1])

        return (
            0 if region[0] < 0 or region[0] > self.resolution[0] else region[0],
            0 if region[1] < 0 or region[1] > self.resolution[1] else region[1],
            self.resolution[0] if region[2] < 0 or region[2] > self.resolution[0] else region[2],
            self.resolution[1] if region[3] < 0 or region[3] > self.resolution[1] else region[3],
        )

    @classmethod
    def discover_displays(cls) -> list[Self]:
        display_device_name_mapping = d3dshot.dll.user32.get_display_device_name_mapping()

        dxgi_factory = d3dshot.dll.dxgi.initialize_dxgi_factory()
        dxgi_adapters = d3dshot.dll.dxgi.discover_dxgi_adapters(dxgi_factory)

        displays = []

        for dxgi_adapter in dxgi_adapters:
            dxgi_adapter_description = d3dshot.dll.dxgi.describe_dxgi_adapter(dxgi_adapter)

            for dxgi_output in d3dshot.dll.dxgi.discover_dxgi_outputs(dxgi_adapter):
                dxgi_output_description = d3dshot.dll.dxgi.describe_dxgi_output(dxgi_output)

                if dxgi_output_description["is_attached_to_desktop"]:
                    display_device = display_device_name_mapping.get(
                        dxgi_output_description["name"]
                    )

                    if display_device is None:
                        display_device = ("Unknown", False)

                    hmonitor = d3dshot.dll.user32.get_hmonitor_by_point(
                        dxgi_output_description["position"]["left"],
                        dxgi_output_description["position"]["top"],
                    )

                    scale_factor = d3dshot.dll.shcore.get_scale_factor_for_monitor(hmonitor)

                    display = cls(
                        name=display_device[0],
                        adapter_name=dxgi_adapter_description,
                        resolution=dxgi_output_description["resolution"],
                        position=dxgi_output_description["position"],
                        rotation=dxgi_output_description["rotation"],
                        scale_factor=scale_factor,
                        is_primary=display_device[1],
                        hmonitor=hmonitor,
                        dxgi_output=dxgi_output,
                        dxgi_adapter=dxgi_adapter,
                    )

                    displays.append(display)

        return displays
