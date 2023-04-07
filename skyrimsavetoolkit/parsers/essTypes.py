from mothpriest import IntegerParser, BlockParser, ReferenceSizeStringParser, FixedSizeRawParser
from functools import partial

# unsigned integer sizes
uint8 = partial(IntegerParser, 1)
uint16 = partial(IntegerParser, 2)
uint32 = partial(IntegerParser, 4)

# strings
wstring = partial(BlockParser, elements=[
    uint16('length'), 
    ReferenceSizeStringParser('value', 'length')
])

# IDs
refID = FixedSizeRawParser('RefID', 3)

formID = BlockParser('formID', [
    FixedSizeRawParser('objectID', 3),
    uint8('pluginID')
])