import logging
from ctypes import *
from ctypes import _CData as _CData, _Pointer, _SimpleCData
from typing import TypeVar, overload

from _typeshed import Incomplete
from comtypes import hints as hints, patcher as patcher
from comtypes._comobject import COMObject as COMObject
from comtypes._memberspec import (
    ComMemberGenerator as ComMemberGenerator,
    DispMemberGenerator as DispMemberGenerator,
    _ComMemberSpec,
    _DispMemberSpec,
)
from comtypes._meta import _coclass_meta
from comtypes.GUID import GUID as GUID
from typing_extensions import TypeAlias

__version__: str
msg: Incomplete

class NullHandler(logging.Handler):
    def emit(self, record) -> None: ...

logger: Incomplete
PyInstanceMethod_Type: Incomplete

def instancemethod(func, inst, cls): ...

class ReturnHRESULT(Exception): ...

IID = GUID
DWORD = c_ulong
wireHWND = c_ulong
CLSCTX_INPROC_SERVER: int
CLSCTX_INPROC_HANDLER: int
CLSCTX_LOCAL_SERVER: int
CLSCTX_INPROC: int
CLSCTX_SERVER: int
CLSCTX_ALL: int
CLSCTX_INPROC_SERVER16: int
CLSCTX_REMOTE_SERVER: int
CLSCTX_INPROC_HANDLER16: int
CLSCTX_RESERVED1: int
CLSCTX_RESERVED2: int
CLSCTX_RESERVED3: int
CLSCTX_RESERVED4: int
CLSCTX_NO_CODE_DOWNLOAD: int
CLSCTX_RESERVED5: int
CLSCTX_NO_CUSTOM_MARSHAL: int
CLSCTX_ENABLE_CODE_DOWNLOAD: int
CLSCTX_NO_FAILURE_LOG: int
CLSCTX_DISABLE_AAA: int
CLSCTX_ENABLE_AAA: int
CLSCTX_FROM_DEFAULT_CONTEXT: int
tagCLSCTX = c_int
CLSCTX = tagCLSCTX
SEC_WINNT_AUTH_IDENTITY_UNICODE: int
RPC_C_AUTHN_WINNT: int
RPC_C_AUTHZ_NONE: int
RPC_C_AUTHN_LEVEL_CONNECT: int
RPC_C_IMP_LEVEL_IMPERSONATE: int
EOAC_NONE: int
COINIT_MULTITHREADED: int
COINIT_APARTMENTTHREADED: int
COINIT_DISABLE_OLE1DDE: int
COINIT_SPEED_OVER_MEMORY: int

def CoInitialize(): ...
def CoInitializeEx(flags: Incomplete | None = None) -> None: ...
def CoUninitialize() -> None: ...

com_interface_registry: Incomplete
com_coclass_registry: Incomplete

class _cominterface_meta(type):
    def __new__(cls, name, bases, namespace): ...
    def __setattr__(self, name, value) -> None: ...

class _compointer_meta(Incomplete, _cominterface_meta): ...

class _compointer_base(c_void_p, metaclass=_compointer_meta):
    def __del__(self, _debug=...) -> None: ...
    def __cmp__(self, other): ...
    def __eq__(self, other): ...
    def __hash__(self): ...
    value: Incomplete
    @classmethod
    def from_param(cls, value): ...

class BSTR(_SimpleCData):  # type: ignore[type-arg]
    def __ctypes_from_outparam__(self): ...
    def __del__(self, _free=...) -> None: ...
    @classmethod
    def from_param(cls, value): ...

class helpstring(str): ...

class defaultvalue:
    value: Incomplete
    def __init__(self, value) -> None: ...

class dispid(int): ...

def STDMETHOD(restype, name, argtypes=()) -> _ComMemberSpec: ...
def DISPMETHOD(idlflags, restype, name, *argspec) -> _DispMemberSpec: ...
def DISPPROPERTY(idlflags, proptype, name) -> _DispMemberSpec: ...
def COMMETHOD(idlflags, restype, methodname, *argspec) -> _ComMemberSpec: ...

_T_IUnknown = TypeVar("_T_IUnknown", bound=IUnknown)

class _IUnknown_Base(c_void_p, metaclass=_cominterface_meta): ...  # pyright: ignore[reportGeneralTypeIssues]

class IUnknown(_IUnknown_Base, metaclass=_cominterface_meta):
    def QueryInterface(
        self, interface: type[_T_IUnknown], iid: GUID | None = None
    ) -> _T_IUnknown: ...
    def AddRef(self) -> int: ...
    def Release(self) -> int: ...

class IPersist(IUnknown):
    def GetClassID(self) -> GUID: ...

class IServiceProvider(IUnknown):
    def QueryService(self, serviceIID: GUID, interface: type[_T_IUnknown]) -> _T_IUnknown: ...

@overload
def CoGetObject(displayname: str, interface: None) -> IUnknown: ...
@overload
def CoGetObject(displayname: str, interface: type[_T_IUnknown]) -> _T_IUnknown: ...

_pUnkOuter: TypeAlias = type[_Pointer[IUnknown]]

@overload
def CoCreateInstance(
    clsid: GUID,
    interface: None = None,
    clsctx: int | None = None,
    punkouter: _pUnkOuter | None = None,
) -> IUnknown: ...
@overload
def CoCreateInstance(
    clsid: GUID,
    interface: type[_T_IUnknown],
    clsctx: int | None = None,
    punkouter: _pUnkOuter | None = None,
) -> _T_IUnknown: ...
@overload
def CoGetClassObject(
    clsid: GUID,
    clsctx: int | None = None,
    pServerInfo: COSERVERINFO | None = None,
    interface: None = None,
) -> hints.IClassFactory: ...
@overload
def CoGetClassObject(
    clsid: GUID,
    clsctx: int | None = None,
    pServerInfo: COSERVERINFO | None = None,
    interface: type[_T_IUnknown] | None = None,
) -> _T_IUnknown: ...
@overload
def GetActiveObject(clsid: GUID, interface: None = None) -> IUnknown: ...
@overload
def GetActiveObject(clsid: GUID, interface: type[_T_IUnknown]) -> _T_IUnknown: ...

class MULTI_QI(Structure):
    pIID: GUID
    pItf: _Pointer[c_void_p]
    hr: HRESULT

class _COAUTHIDENTITY(Structure): ...

COAUTHIDENTITY: Incomplete

class _COAUTHINFO(Structure): ...

COAUTHINFO: Incomplete

class _COSERVERINFO(Structure):
    dwReserved1: int
    pwszName: str | None
    pAuthInfo: _COAUTHINFO
    dwReserved2: int

COSERVERINFO: Incomplete

class tagBIND_OPTS(Structure): ...

BIND_OPTS = tagBIND_OPTS

class tagBIND_OPTS2(Structure): ...

BINDOPTS2 = tagBIND_OPTS2

class _SEC_WINNT_AUTH_IDENTITY(Structure): ...

SEC_WINNT_AUTH_IDENTITY: Incomplete

class _SOLE_AUTHENTICATION_INFO(Structure): ...

SOLE_AUTHENTICATION_INFO: Incomplete

class _SOLE_AUTHENTICATION_LIST(Structure): ...

SOLE_AUTHENTICATION_LIST: Incomplete

@overload
def CoCreateInstanceEx(
    clsid: GUID,
    interface: None = None,
    clsctx: int | None = None,
    machine: str | None = None,
    pServerInfo: COSERVERINFO | None = None,
) -> IUnknown: ...
@overload
def CoCreateInstanceEx(
    clsid: GUID,
    interface: type[_T_IUnknown],
    clsctx: int | None = None,
    machine: str | None = None,
    pServerInfo: COSERVERINFO | None = None,
) -> _T_IUnknown: ...

class CoClass(COMObject, metaclass=_coclass_meta): ...

__known_symbols__: Incomplete
