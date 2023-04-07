from mothpriest import *
from .essTypes import *

# single use blocks

header_info = BlockParser(
    'headerInfo',
    [
        MagicParser('TESV_SAVEGAME', 'magic'),
        IntegerParser(4, 'headerSize')
    ],
)

header = ReferenceSizeBlockParser(
    'header',
    ['headerInfo', 'headerSize'],
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
    ]
)

screenshot = ReferenceSizeImageParser(
    width_id=['header', 'screenshotWidth'],
    height_id=['header', 'screenshotHeight'],
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
        FixedPaddingParser(15*4)
    ]
)

# form/table entries

plugin_info = BlockParser('pluginInfo', [
    uint8('pluginInfoCount'),
    ReferenceCountParser('pluginCountEntries', 'pluginInfoCount', wstring('plugin'))
])

global_data_entry = BlockParser('globalData', [
    uint32('type'),
    uint32('length'),
    ReferenceSizeRawParser('value', 'length')
])

change_form_type_flags = BlockParser('flags', [
    uint8('lengths_size'),
    uint8('form_type')
])
change_form_type = BytesExpansionParser('type', 1, [2, 6], change_form_type_flags)
change_form_entry = BlockParser('changeFormEntry', [
    refID('refid'),
    FixedSizeRawParser('changeFlags', 4),
    change_form_type,
    uint8('version'),
    ReferenceMappedParser('length1', ['type', 'lengths_size'], {
        0: uint8(None),
        1: uint16(None),
        2: uint32(None)
    }),
    ReferenceMappedParser('length2', ['type', 'lengths_size'], {
        0: uint8(None),
        1: uint16(None),
        2: uint32(None)
    }),
    ReferenceSizeRawParser('data', 'length1')
])

form_id_entry = BlockParser('formID', [
    FixedSizeRawParser('objectID', 3),
    uint8('pluginID'),
])
