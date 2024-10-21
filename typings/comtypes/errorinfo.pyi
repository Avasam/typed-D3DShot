from ctypes import *

from _typeshed import Incomplete
from comtypes import IUnknown
from comtypes.hresult import *

__all__ = [
    "CreateErrorInfo",
    "GetErrorInfo",
    "ICreateErrorInfo",
    "IErrorInfo",
    "ISupportErrorInfo",
    "ReportError",
    "ReportException",
    "SetErrorInfo",
]

LPCOLESTR = c_wchar_p
DWORD = c_ulong

class ICreateErrorInfo(IUnknown): ...
class IErrorInfo(IUnknown): ...
class ISupportErrorInfo(IUnknown): ...

def CreateErrorInfo(): ...
def GetErrorInfo(): ...
def SetErrorInfo(errinfo): ...
def ReportError(
    text,
    iid,
    clsid: Incomplete | None = None,
    helpfile: Incomplete | None = None,
    helpcontext: int = 0,
    hresult=...,
): ...
def ReportException(
    hresult,
    iid,
    clsid: Incomplete | None = None,
    helpfile: Incomplete | None = None,
    helpcontext: Incomplete | None = None,
    stacklevel: Incomplete | None = None,
): ...
