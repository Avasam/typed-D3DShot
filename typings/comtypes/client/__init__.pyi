from typing import Any, TypeVar, overload

import comtypes
from comtypes import GUID, CoClass, IUnknown, hints
from comtypes.client._events import (
    GetEvents as GetEvents,
    PumpEvents as PumpEvents,
    ShowEvents as ShowEvents,
)
from comtypes.client._generate import GetModule as GetModule
from comtypes.hresult import *

__all__ = [
    "CoGetObject",
    "CreateObject",
    "GetActiveObject",
    "GetClassObject",
    "GetEvents",
    "GetModule",
    "PumpEvents",
    "ShowEvents",
]

def wrap_outparam(punk: Any) -> Any: ...
def GetBestInterface(punk: Any) -> Any: ...

wrap = GetBestInterface
_T_IUnknown = TypeVar("_T_IUnknown", bound=IUnknown)

@overload
def GetActiveObject(progid: str | CoClass | GUID) -> Any: ...
@overload
def GetActiveObject(progid: str | CoClass | GUID, interface: type[_T_IUnknown]) -> _T_IUnknown: ...
@overload
def GetClassObject(
    progid: str | CoClass | GUID,
    clsctx: int | None = None,
    pServerInfo: comtypes.COSERVERINFO | None = None,
) -> hints.IClassFactory: ...
@overload
def GetClassObject(
    progid: str | CoClass | GUID,
    clsctx: int | None = None,
    pServerInfo: comtypes.COSERVERINFO | None = None,
    interface: type[_T_IUnknown] | None = None,
) -> _T_IUnknown: ...
@overload
def CreateObject(progid: str | type[CoClass] | GUID) -> Any: ...
@overload
def CreateObject(
    progid: str | type[CoClass] | GUID,
    clsctx: int | None = None,
    machine: str | None = None,
    interface: type[_T_IUnknown] | None = None,
    dynamic: bool = ...,
    pServerInfo: comtypes.COSERVERINFO | None = None,
) -> _T_IUnknown: ...
@overload
def CoGetObject(displayname: str, interface: type[_T_IUnknown]) -> _T_IUnknown: ...
@overload
def CoGetObject(displayname: str, interface: None = None, dynamic: bool = False) -> Any: ...
