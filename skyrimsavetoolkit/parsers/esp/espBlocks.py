from mothpriest import *
from mothpriest.macros import *

tes4_header = BlockParser('root', [
    float32('version'),
    uint32('numRecordsAndGroups'),
    uint32('nextAvailableObjectID')
])

record = BlockParser('record', [
    Parser('type', 4),
    uint32('dataSize'),
    Parser('flags', 4),
    Parser('recordID', 4),
    uint16('timestamp'),
    uint16('versionControl'),
    uint16('internalVersion'),
    uint16('unknown'),
    Parser('data', 'dataSize')
])