from typing import Any, Sequence

from _typeshed import Incomplete
from comtypes import typeinfo as typeinfo
from comtypes.tools.typedesc_base import *
from comtypes.typeinfo import TLIBATTR as TLIBATTR, ITypeLib as ITypeLib
from typing_extensions import TypeAlias

class TypeLib:
    name: Incomplete
    guid: Incomplete
    major: Incomplete
    minor: Incomplete
    doc: Incomplete
    def __init__(
        self, name: str, guid: str, major: int, minor: int, doc: str | None = None
    ) -> None: ...

class Constant:
    name: Incomplete
    typ: Incomplete
    value: Incomplete
    doc: Incomplete
    def __init__(
        self, name: str, typ: Typedef | FundamentalType, value: Any, doc: str | None
    ) -> None: ...

class External:
    tlib: Incomplete
    symbol_name: Incomplete
    size: Incomplete
    align: Incomplete
    docs: Incomplete
    def __init__(
        self, tlib: ITypeLib, name: str, size: int, align: int, docs: tuple[str, str] | None = None
    ) -> None: ...
    def get_head(self) -> External: ...

class SAFEARRAYType:
    typ: Incomplete
    align: Incomplete
    def __init__(self, typ: Any) -> None: ...

class ComMethod:
    invkind: Incomplete
    name: Incomplete
    returns: Incomplete
    idlflags: Incomplete
    memid: Incomplete
    doc: Incomplete
    arguments: Incomplete
    def __init__(
        self,
        invkind: int,
        memid: int,
        name: str,
        returns: Any,
        idlflags: list[str],
        doc: str | None,
    ) -> None: ...
    def add_argument(
        self, typ: Any, name: str, idlflags: list[str], default: Any | None
    ) -> None: ...

class DispMethod:
    dispid: Incomplete
    invkind: Incomplete
    name: Incomplete
    returns: Incomplete
    idlflags: Incomplete
    doc: Incomplete
    arguments: Incomplete
    def __init__(
        self,
        dispid: int,
        invkind: int,
        name: str,
        returns: Any,
        idlflags: list[str],
        doc: str | None,
    ) -> None: ...
    def add_argument(
        self, typ: Any, name: str, idlflags: list[str], default: Any | None
    ) -> None: ...

class DispProperty:
    dispid: Incomplete
    name: Incomplete
    typ: Incomplete
    idlflags: Incomplete
    doc: Incomplete
    def __init__(
        self, dispid: int, name: str, typ: Any, idlflags: list[str], doc: Any | None
    ) -> None: ...

class DispInterfaceHead:
    itf: Incomplete
    def __init__(self, itf: DispInterface) -> None: ...

class DispInterfaceBody:
    itf: Incomplete
    def __init__(self, itf: DispInterface) -> None: ...

class DispInterface:
    name: Incomplete
    members: Incomplete
    base: Incomplete
    iid: Incomplete
    idlflags: Incomplete
    itf_head: Incomplete
    itf_body: Incomplete
    doc: Incomplete
    def __init__(
        self, name: str, base: Any, iid: str, idlflags: list[str], doc: str | None
    ) -> None: ...
    def add_member(self, member: DispMethod | DispProperty) -> None: ...
    def get_body(self) -> DispInterfaceBody: ...
    def get_head(self) -> DispInterfaceHead: ...

class ComInterfaceHead:
    itf: Incomplete
    def __init__(self, itf: ComInterface) -> None: ...

class ComInterfaceBody:
    itf: Incomplete
    def __init__(self, itf: ComInterface) -> None: ...

class ComInterface:
    name: Incomplete
    members: Incomplete
    base: Incomplete
    iid: Incomplete
    idlflags: Incomplete
    itf_head: Incomplete
    itf_body: Incomplete
    doc: Incomplete
    def __init__(
        self, name: str, base: ComInterface | None, iid: str, idlflags: list[str], doc: str | None
    ) -> None: ...
    def extend_members(self, members: Sequence[ComMethod]) -> None: ...
    def get_body(self) -> ComInterfaceBody: ...
    def get_head(self) -> ComInterfaceHead: ...

_ImplTypeFlags = int
_Interface: TypeAlias = ComInterface | DispInterface

class CoClass:
    name: Incomplete
    clsid: Incomplete
    idlflags: Incomplete
    tlibattr: Incomplete
    interfaces: Incomplete
    doc: Incomplete
    def __init__(
        self, name: str, clsid: str, idlflags: list[str], tlibattr: TLIBATTR, doc: str | None
    ) -> None: ...
    def add_interface(self, itf: _Interface, idlflags: _ImplTypeFlags) -> None: ...

_ImplementedInterfaces: TypeAlias = Sequence[_Interface]
_SourceInterfaces: TypeAlias = Sequence[_Interface]

def groupby_impltypeflags(
    seq: Sequence[tuple[_Interface, _ImplTypeFlags]],
) -> tuple[_ImplementedInterfaces, _SourceInterfaces]: ...
