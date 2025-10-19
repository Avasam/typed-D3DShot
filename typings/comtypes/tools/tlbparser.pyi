from typing import Any

from _typeshed import Incomplete
from comtypes import (
    BSTR as BSTR,
    COMError as COMError,
    automation as automation,
    typeinfo as typeinfo,
)
from comtypes.tools import typedesc as typedesc

is_64bits: Incomplete

def PTR(typ): ...

char_type: Incomplete
uchar_type: Incomplete
wchar_t_type: Incomplete
short_type: Incomplete
ushort_type: Incomplete
int_type: Incomplete
uint_type: Incomplete
long_type: Incomplete
ulong_type: Incomplete
longlong_type: Incomplete
ulonglong_type: Incomplete
float_type: Incomplete
double_type: Incomplete
BSTR_type: Incomplete
SCODE_type: Incomplete
VARIANT_BOOL_type: Incomplete
HRESULT_type: Incomplete
VARIANT_type: Incomplete
IDISPATCH_type: Incomplete
IUNKNOWN_type: Incomplete
DECIMAL_type: Incomplete

def midlSAFEARRAY(typ): ...

CURRENCY_type = longlong_type
DATE_type = double_type
COMTYPES: Incomplete

class Parser:
    tlib: typeinfo.ITypeLib
    items: dict[str, Any]
    def make_type(self, tdesc: typeinfo.TYPEDESC, tinfo: typeinfo.ITypeInfo) -> Any: ...
    def ParseEnum(
        self, tinfo: typeinfo.ITypeInfo, ta: typeinfo.TYPEATTR
    ) -> typedesc.Enumeration: ...
    def ParseRecord(
        self, tinfo: typeinfo.ITypeInfo, ta: typeinfo.TYPEATTR
    ) -> typedesc.Structure: ...
    def ParseModule(self, tinfo: typeinfo.ITypeInfo, ta: typeinfo.TYPEATTR) -> None: ...
    def ParseInterface(
        self, tinfo: typeinfo.ITypeInfo, ta: typeinfo.TYPEATTR
    ) -> typedesc.ComInterface | None: ...
    def ParseDispatch(
        self, tinfo: typeinfo.ITypeInfo, ta: typeinfo.TYPEATTR
    ) -> typedesc.DispInterface: ...
    def inv_kind(self, invkind: int) -> list[str]: ...
    def func_flags(self, flags: int) -> list[str]: ...
    def param_flags(self, flags: int) -> list[str]: ...
    def coclass_type_flags(self, flags: int) -> list[str]: ...
    def interface_type_flags(self, flags: int) -> list[str]: ...
    def var_flags(self, flags: int) -> list[str]: ...
    def ParseCoClass(
        self, tinfo: typeinfo.ITypeInfo, ta: typeinfo.TYPEATTR
    ) -> typedesc.CoClass: ...
    def ParseAlias(self, tinfo: typeinfo.ITypeInfo, ta: typeinfo.TYPEATTR) -> typedesc.Typedef: ...
    def ParseUnion(self, tinfo: typeinfo.ITypeInfo, ta: typeinfo.TYPEATTR) -> typedesc.Union: ...
    def parse_typeinfo(self, tinfo: typeinfo.ITypeInfo) -> Any: ...
    def parse_LibraryDescription(self) -> None: ...
    def parse(self): ...

class TlbFileParser(Parser):
    tlib: Incomplete
    items: Incomplete
    def __init__(self, path) -> None: ...

class TypeLibParser(Parser):
    tlib: Incomplete
    items: Incomplete
    def __init__(self, tlib) -> None: ...

def get_tlib_filename(tlib): ...
