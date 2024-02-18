from enum import Enum


# Should this be in the type folder?
class ScriptType(Enum):
    P2PK = "P2PK"
    P2PKH = "P2PKH"
    P2SH = "P2SH"
    P2WPKH = "P2WPKH"
    P2WSH = "P2WSH"
