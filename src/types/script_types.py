from enum import Enum


class ScriptType(Enum):
    P2PK = "P2PK"
    P2PKH = "P2PKH"
    P2SH = "P2SH"
    P2WPKH = "P2WPKH"
    P2WSH = "P2WSH"
