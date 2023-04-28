from mothpriest import *
from mothpriest.macros import *
from functools import partial
from typing import Union

# strings
def wstring(id: Union[int, str]):
    return BlockParser(id, elements=[
        uint16('length'),
        StringParser('value', 'length')
    ])

# IDs
def refID(id: Union[int, str]):
    return BlockParser(id, elements=[
        BytesExpansionParser(
            'splitter',
            3,
            [2, 22],
            parser=BlockParser('RefID', elements=[
                uint8('type'),
                Parser('value', 3)
            ])
        )
    ])

def formID(id: Union[int, str]): 
    return BlockParser(id, [
        HexParser('objectID', 3),
        uint8('pluginID')
    ])