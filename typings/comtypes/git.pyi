from ctypes import *

from _typeshed import Incomplete
from comtypes import IUnknown

__all__ = ["GetInterfaceFromGlobal", "RegisterInterfaceInGlobal", "RevokeInterfaceFromGlobal"]

DWORD = c_ulong

class IGlobalInterfaceTable(IUnknown):
    def RegisterInterfaceInGlobal(self, obj, interface=...): ...
    def GetInterfaceFromGlobal(self, cookie, interface=...): ...
    def RevokeInterfaceFromGlobal(self, cookie) -> None: ...

RevokeInterfaceFromGlobal: Incomplete
RegisterInterfaceInGlobal: Incomplete
GetInterfaceFromGlobal: Incomplete
