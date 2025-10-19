from collections.abc import Generator
from typing import Any, SupportsInt

from _typeshed import Incomplete

class Argument:
    atype: Incomplete
    name: Incomplete
    def __init__(self, atype, name) -> None: ...

class _HasArgs:
    arguments: Incomplete
    def __init__(self) -> None: ...
    def add_argument(self, arg) -> None: ...
    def iterArgTypes(self) -> Generator[Incomplete]: ...
    def iterArgNames(self) -> Generator[Incomplete]: ...
    def fixup_argtypes(self, typemap) -> None: ...

class Alias:
    name: Incomplete
    alias: Incomplete
    typ: Incomplete
    def __init__(self, name, alias, typ: Incomplete | None = None) -> None: ...

class Macro:
    name: Incomplete
    args: Incomplete
    body: Incomplete
    def __init__(self, name, args, body) -> None: ...

class File:
    name: Incomplete
    def __init__(self, name) -> None: ...

class Function(_HasArgs):
    location: Incomplete
    name: Incomplete
    returns: Incomplete
    attributes: Incomplete
    extern: Incomplete
    def __init__(self, name, returns, attributes, extern) -> None: ...

class Constructor(_HasArgs):
    location: Incomplete
    name: Incomplete
    def __init__(self, name) -> None: ...

class OperatorFunction(_HasArgs):
    location: Incomplete
    name: Incomplete
    returns: Incomplete
    def __init__(self, name, returns) -> None: ...

class FunctionType(_HasArgs):
    location: Incomplete
    returns: Incomplete
    attributes: Incomplete
    def __init__(self, returns, attributes) -> None: ...

class Method(_HasArgs):
    location: Incomplete
    name: Incomplete
    returns: Incomplete
    def __init__(self, name, returns) -> None: ...

class FundamentalType:
    location: Incomplete
    name: Incomplete
    size: Incomplete
    align: Incomplete
    def __init__(self, name, size, align) -> None: ...

class PointerType:
    location: Incomplete
    typ: Incomplete
    size: Incomplete
    align: Incomplete
    def __init__(self, typ, size, align) -> None: ...

class Typedef:
    location: Incomplete
    name: Incomplete
    typ: Incomplete
    def __init__(self, name, typ) -> None: ...

class ArrayType:
    location: Incomplete
    typ: Incomplete
    min: Incomplete
    max: Incomplete
    def __init__(self, typ: Any, min: int, max: int) -> None: ...

class StructureHead:
    location: Incomplete
    struct: Incomplete
    def __init__(self, struct: _Struct_Union_Base) -> None: ...

class StructureBody:
    location: Incomplete
    struct: Incomplete
    def __init__(self, struct: _Struct_Union_Base) -> None: ...

class _Struct_Union_Base:
    name: str
    align: int
    members: list[Field | Method | Constructor]
    bases: list[_Struct_Union_Base]
    artificial: Any | None
    size: int | None
    location: Incomplete
    struct_body: Incomplete
    struct_head: Incomplete
    def __init__(self) -> None: ...
    def get_body(self) -> StructureBody: ...
    def get_head(self) -> StructureHead: ...

class Structure(_Struct_Union_Base):
    name: Incomplete
    align: Incomplete
    members: Incomplete
    bases: Incomplete
    artificial: Incomplete
    size: Incomplete
    def __init__(
        self,
        name: str,
        align: SupportsInt,
        members: list[Field],
        bases: list[Any],
        size: SupportsInt | None,
        artificial: Any | None = None,
    ) -> None: ...

class Union(_Struct_Union_Base):
    name: Incomplete
    align: Incomplete
    members: Incomplete
    bases: Incomplete
    artificial: Incomplete
    size: Incomplete
    def __init__(
        self,
        name: str,
        align: SupportsInt,
        members: list[Field],
        bases: list[Any],
        size: SupportsInt | None,
        artificial: Any | None = None,
    ) -> None: ...

class Field:
    name: Incomplete
    typ: Incomplete
    bits: Incomplete
    offset: Incomplete
    def __init__(self, name: str, typ: Any, bits: Any | None, offset: SupportsInt) -> None: ...

class CvQualifiedType:
    typ: Incomplete
    const: Incomplete
    volatile: Incomplete
    def __init__(self, typ, const, volatile) -> None: ...

class Enumeration:
    location: Incomplete
    name: Incomplete
    size: Incomplete
    align: Incomplete
    values: Incomplete
    def __init__(self, name: str, size: SupportsInt, align: SupportsInt) -> None: ...
    def add_value(self, v: EnumValue) -> None: ...

class EnumValue:
    name: Incomplete
    value: Incomplete
    enumeration: Incomplete
    def __init__(self, name: str, value: int, enumeration: Enumeration) -> None: ...

class Variable:
    location: Incomplete
    name: Incomplete
    typ: Incomplete
    init: Incomplete
    def __init__(self, name, typ, init: Incomplete | None = None) -> None: ...
