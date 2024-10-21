import comtypes
from _typeshed import Incomplete

class IClassFactory(comtypes.IUnknown):
    def CreateInstance(
        self,
        punkouter: Incomplete | None = None,
        interface: Incomplete | None = None,
        dynamic: bool = False,
    ): ...

ACTIVEOBJECT_STRONG: int
ACTIVEOBJECT_WEAK: int
oleaut32: Incomplete

def RegisterActiveObject(comobj, weak: bool = True): ...
def RevokeActiveObject(handle) -> None: ...
