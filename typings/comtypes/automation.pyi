from ctypes import *
from ctypes import _Pointer
from ctypes.wintypes import DWORD, LONG, WCHAR as WCHAR
from typing import Any, ClassVar

from _typeshed import Incomplete
from comtypes import (
    BSTR as BSTR,
    COMMETHOD as COMMETHOD,
    GUID as GUID,
    IID as IID,
    STDMETHOD as STDMETHOD,
    COMError as COMError,
    IUnknown as IUnknown,
    hints as hints,
)
from comtypes.hresult import *

class _safearray:
    tagSAFEARRAY: Incomplete

LCID = DWORD
DISPID = LONG
SCODE = LONG
VARTYPE = c_ushort
DISPATCH_METHOD: int
DISPATCH_PROPERTYGET: int
DISPATCH_PROPERTYPUT: int
DISPATCH_PROPERTYPUTREF: int
tagINVOKEKIND = c_int
INVOKE_FUNC = DISPATCH_METHOD
INVOKE_PROPERTYGET = DISPATCH_PROPERTYGET
INVOKE_PROPERTYPUT = DISPATCH_PROPERTYPUT
INVOKE_PROPERTYPUTREF = DISPATCH_PROPERTYPUTREF
INVOKEKIND = tagINVOKEKIND
IID_NULL: Incomplete
riid_null: Incomplete
VARENUM = c_int
VT_EMPTY: int
VT_NULL: int
VT_I2: int
VT_I4: int
VT_R4: int
VT_R8: int
VT_CY: int
VT_DATE: int
VT_BSTR: int
VT_DISPATCH: int
VT_ERROR: int
VT_BOOL: int
VT_VARIANT: int
VT_UNKNOWN: int
VT_DECIMAL: int
VT_I1: int
VT_UI1: int
VT_UI2: int
VT_UI4: int
VT_I8: int
VT_UI8: int
VT_INT: int
VT_UINT: int
VT_VOID: int
VT_HRESULT: int
VT_PTR: int
VT_SAFEARRAY: int
VT_CARRAY: int
VT_USERDEFINED: int
VT_LPSTR: int
VT_LPWSTR: int
VT_RECORD: int
VT_INT_PTR: int
VT_UINT_PTR: int
VT_FILETIME: int
VT_BLOB: int
VT_STREAM: int
VT_STORAGE: int
VT_STREAMED_OBJECT: int
VT_STORED_OBJECT: int
VT_BLOB_OBJECT: int
VT_CF: int
VT_CLSID: int
VT_VERSIONED_STREAM: int
VT_BSTR_BLOB: int
VT_VECTOR: int
VT_ARRAY: int
VT_BYREF: int
VT_RESERVED: int
VT_ILLEGAL: int
VT_ILLEGALMASKED: int
VT_TYPEMASK: int

class tagCY(Structure): ...

CY = tagCY
CURRENCY = CY

class tagDEC(Structure):
    def as_decimal(self): ...

DECIMAL = tagDEC

class tagVARIANT(Structure):
    vt: int
    _: U_VARIANT1.__tagVARIANT.U_VARIANT2
    null: ClassVar[VARIANT]
    empty: ClassVar[VARIANT]
    missing: ClassVar[VARIANT]
    class U_VARIANT1(Union):
        class __tagVARIANT(Structure):
            class U_VARIANT2(Union):
                class _tagBRECORD(Structure): ...

    value: Incomplete
    def __init__(self, *args) -> None: ...
    def __del__(self) -> None: ...
    @classmethod
    def from_param(cls, value): ...
    def __setitem__(self, index, value) -> None: ...
    def __getitem__(self, index): ...
    def __ctypes_from_outparam__(self): ...
    def ChangeType(self, typecode) -> None: ...

VARIANT = tagVARIANT
VARIANTARG = VARIANT
v: Incomplete

class _:
    @classmethod
    def from_param(cls, arg): ...
    def __setitem__(self, index, value) -> None: ...

class IEnumVARIANT(IUnknown):
    def __iter__(self): ...
    def __next__(self): ...
    def __getitem__(self, index): ...
    def Next(self, celt): ...

class tagEXCEPINFO(Structure):
    wCode: int
    wReserved: int
    bstrSource: str
    bstrDescription: str
    bstrHelpFile: str
    dwHelpContext: int
    pvReserved: int | None
    pfnDeferredFillIn: int | None
    scode: int

EXCEPINFO = tagEXCEPINFO

class tagDISPPARAMS(Structure):
    rgvarg: Array[VARIANT]
    rgdispidNamedArgs: _Pointer[DISPID]
    cArgs: int
    cNamedArgs: int
    def __del__(self) -> None: ...

DISPPARAMS = tagDISPPARAMS
DISPID_VALUE: int
DISPID_UNKNOWN: int
DISPID_PROPERTYPUT: int
DISPID_NEWENUM: int
DISPID_EVALUATE: int
DISPID_CONSTRUCTOR: int
DISPID_DESTRUCTOR: int
DISPID_COLLECT: int
RawGetIDsOfNamesFunc: Incomplete
RawInvokeFunc: Incomplete

class IDispatch(IUnknown):
    def GetTypeInfo(self, index: int, lcid: int = 0) -> hints.ITypeInfo: ...
    def GetIDsOfNames(self, *names: str, **kw: Any) -> list[int]: ...
    def Invoke(self, dispid: int, *args: Any, **kw: Any) -> Any: ...

__known_symbols__: Incomplete
