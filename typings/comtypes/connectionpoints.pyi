from ctypes import *

from comtypes import (
    COMMETHOD as COMMETHOD,
    GUID as GUID,
    HRESULT as HRESULT,
    IUnknown as IUnknown,
    dispid as dispid,
)

class tagCONNECTDATA(Structure): ...

CONNECTDATA = tagCONNECTDATA

class IConnectionPointContainer(IUnknown): ...
class IConnectionPoint(IUnknown): ...

class IEnumConnections(IUnknown):
    def __iter__(self): ...
    def __next__(self): ...

class IEnumConnectionPoints(IUnknown):
    def __iter__(self): ...
    def __next__(self): ...
