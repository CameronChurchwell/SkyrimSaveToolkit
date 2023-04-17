from mothpriest import *
from mothpriest.macros import *

tes4_header = BlockParser('root', [
    float32('version'),
    uint32('numRecordsAndGroups'),
    uint32('nextAvailableObjectID')
])

record = BlockParser('record', [
    FixedSizeRawParser('type', 4),
    uint32('dataSize'),
    FixedSizeRawParser('flags', 4),
    FixedSizeRawParser('recordID', 4),
    uint16('timestamp'),
    uint16('versionControl'),
    uint16('internalVersion'),
    uint16('unknown'),
    ReferenceSizeRawParser('data', 'dataSize')
])