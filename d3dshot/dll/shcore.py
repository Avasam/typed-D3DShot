import ctypes
from ctypes import wintypes


def get_scale_factor_for_monitor(hmonitor: int) -> float:
    scale_factor = wintypes.UINT()
    ctypes.windll.shcore.GetScaleFactorForMonitor(hmonitor, ctypes.byref(scale_factor))

    return scale_factor.value / 100.0
