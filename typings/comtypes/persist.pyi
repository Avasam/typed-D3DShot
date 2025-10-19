from ctypes import *
from ctypes.wintypes import WORD

from _typeshed import Incomplete
from comtypes import (
    COMMETHOD as COMMETHOD,
    GUID as GUID,
    HRESULT as HRESULT,
    COMObject as COMObject,
    IPersist as IPersist,
    IUnknown as IUnknown,
    dispid as dispid,
)
from comtypes.automation import VARIANT as VARIANT, tagEXCEPINFO as tagEXCEPINFO
from comtypes.hresult import *

WSTRING = c_wchar_p

class IErrorLog(IUnknown): ...
class IPropertyBag(IUnknown): ...
class IPersistPropertyBag(IPersist): ...

CLIPFORMAT = WORD
PROPBAG2_TYPE_UNDEFINED: int
PROPBAG2_TYPE_DATA: int
PROPBAG2_TYPE_URL: int
PROPBAG2_TYPE_OBJECT: int
PROPBAG2_TYPE_STREAM: int
PROPBAG2_TYPE_STORAGE: int
PROPBAG2_TYPE_MONIKER: int

class tagPROPBAG2(Structure): ...
class IPropertyBag2(IUnknown): ...
class IPersistPropertyBag2(IPersist): ...

STGM_READ: int
STGM_WRITE: int
STGM_READWRITE: int
STGM_SHARE_EXCLUSIVE: int
STGM_SHARE_DENY_WRITE: int
STGM_SHARE_DENY_READ: int
STGM_SHARE_DENY_NONE: int
STGM_PRIORITY: int
STGM_FAILIFTHERE: int
STGM_CREATE: int
STGM_CONVERT: int
STGM_DIRECT: int
STGM_TRANSACTED: int
STGM_NOSCRATCH: int
STGM_NOSNAPSHOT: int
STGM_SIMPLE: int
STGM_DIRECT_SWMR: int
STGM_DELETEONRELEASE: int
LPOLESTR = c_wchar_p
LPCOLESTR = c_wchar_p

class IPersistFile(IPersist): ...

class DictPropertyBag(COMObject):
    values: Incomplete
    def __init__(self, **kw) -> None: ...
    def Read(self, this, name, pVar, errorlog): ...
    def Write(self, this, name, var): ...

__known_symbols__: Incomplete
