from ctypes import *

from _typeshed import Incomplete
from comtypes import COMObject
from comtypes.hresult import *

__all__ = ["VARIANTEnumerator"]

class VARIANTEnumerator(COMObject):
    items: Incomplete
    seq: Incomplete
    def __init__(self, items) -> None: ...
    def Next(self, this, celt, rgVar, pCeltFetched): ...
    def Skip(self, this, celt): ...
    def Reset(self, this): ...

class COMCollection(COMObject):
    collection: Incomplete
    itemtype: Incomplete
    def __init__(self, itemtype, collection) -> None: ...
