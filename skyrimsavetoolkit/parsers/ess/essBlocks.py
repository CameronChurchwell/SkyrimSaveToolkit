from mothpriest import *
from mothpriest.references import *
from .essTypes import *

# single use blocks

header_info = BlockParser(
    'headerInfo',
    [
        MagicParser('TESV_SAVEGAME', 'magic'),
        uint32('headerSize')
    ],
)

header = BlockParser(
    'header',
    [
        uint32('version'),
        uint32('saveNumber'),
        wstring('playerName'),
        uint32('playerLevel'),
        wstring('playerLocation'),
        wstring('gameDate'),
        wstring('playerRace'),
        uint16('playerSex'),
        uint32('playerCurrentExp'),
        uint32('playerNeededExp'),
        uint32('fileDateLower'),
        uint32('fileDateUpper'),
        uint32('screenshotWidth'),
        uint32('screenshotHeight'),
        uint16('compressionType')
    ],
    ['headerInfo', 'headerSize'],
)

screenshot = ImageParser(
    width=['header', 'screenshotWidth'],
    height=['header', 'screenshotHeight'],
    id='screenshotData'
)

file_location = BlockParser(
    'fileLocationTable',
    [
        uint32('formIDArrayCountOffset'),
        uint32('unknownTable3Offset'),
        uint32('globalDataTable1Offset'),
        uint32('globalDataTable2Offset'),
        uint32('changeFormsOffset'),
        uint32('globalDataTable3Offset'),
        uint32('globalDataTable1Count'),
        uint32('globalDataTable2Count'),
        uint32('globalDataTable3Count'),
        uint32('changeFormCount'),
        ReferenceSizeParser('padding', 15*4)
    ]
)

# form/table entries

plugin_info = BlockParser('pluginInfo', [
    uint8('pluginInfoCount'),
    ReferenceCountParser('pluginCountEntries', 'pluginInfoCount', wstring)
])

def global_data_entry(id: Union[str, int]):
    return BlockParser(id, [
        uint32('type'),
        uint32('length'),
        ReferenceSizeParser('value', 'length')
    ])

def change_form_type_flags(id: Union[str, int]):
    return BlockParser(id, [
        # PDBParser('debug'),
        uint8('lengths_size'),
        uint8('form_type')
    ])

def change_form_type(id: Union[str, int]):
    return BytesExpansionParser(id, 1, [2, 6], change_form_type_flags('flags'))

def change_form_entry(id: Union[str, int]):
    return BlockParser(id, [
        refID('refid'),
        ReferenceSizeParser('changeFlags', 4),
        change_form_type('type'),
        uint8('version'),
        ReferenceMappedParser('length1', ['type', 'flags', 'lengths_size'], {
            0: uint8('length1'),
            1: uint16('length1'),
            2: uint32('length1')
        }),
        ReferenceMappedParser('length2', ['type', 'flags', 'lengths_size'], {
            0: uint8('length2'),
            1: uint16('length2'),
            2: uint32('length2')
        }),
        ReferenceSizeParser('data', 'length1'),
    ])

# tables

global_data_table_1 = ReferenceCountParser('globalDataTable1', ['fileLocationTable', 'globalDataTable1Count'], global_data_entry)
global_data_table_2 = ReferenceCountParser('globalDataTable2', ['fileLocationTable', 'globalDataTable2Count'], global_data_entry)
change_forms = ReferenceCountParser('changeForms', ['fileLocationTable', 'changeFormCount'], change_form_entry)
global_data_table_3 = ReferenceCountParser('globalDataTable3', ['_parent', 'fileLocationTable', 'globalDataTable3Count'], global_data_entry)

global_data_table_3_size = DifferenceReference(
    IDListReference(['fileLocationTable', 'formIDArrayCountOffset']),
    IDListReference(['fileLocationTable', 'globalDataTable3Offset']) 
)

global_data_table_3_debugged = BlockParser('globalDataTable3Chunk', [global_data_table_3], global_data_table_3_size)