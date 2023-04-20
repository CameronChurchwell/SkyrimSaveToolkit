from mothpriest import *
from mothpriest.macros import *

tes4_header = BlockParser('root', [
    float32('version'),
    uint32('numRecordsAndGroups'),
    uint32('nextAvailableObjectID')
])

record = BlockParser('record', [
    ReferenceSizeParser('type', 4),
    uint32('dataSize'),
    ReferenceSizeParser('flags', 4),
    ReferenceSizeParser('recordID', 4),
    uint16('timestamp'),
    uint16('versionControl'),
    uint16('internalVersion'),
    uint16('unknown'),
    ReferenceSizeParser('data', 'dataSize')
])