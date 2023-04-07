from mothpriest import *
from mothpriest.macros import *
from functools import partial

# strings
wstring = partial(BlockParser, elements=[
    uint16('length'), 
    ReferenceSizeStringParser('value', 'length')
])

# IDs
refID = partial(BlockParser, elements=[
    BytesExpansionParser(
        'splitter',
        3, 
        [2, 6, 8, 8],
        parser=BlockParser('RefID', elements=[
            uint8('type'),
            FixedSizeRawParser('value', 3)
        ])
    )
])

formID = BlockParser('formID', [
    FixedSizeRawParser('objectID', 3),
    uint8('pluginID')
])