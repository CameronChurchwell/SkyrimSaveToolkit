from mothpriest import *
# from .essBlocks import *
from .essTypes import *
from ..compression import *

def essFile():

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
        id='screenshotData',
        width=['header', 'screenshotWidth'],
        height=['header', 'screenshotHeight'],
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
            Parser('padding', 15*4)
        ]
    )

    # form/table entries

    plugin_info = BlockParser('pluginInfo', [
        uint8('pluginInfoCount'),
        ReferenceCountParser('pluginInfoEntries', 'pluginInfoCount', wstring),
        uint16('lightPluginInfoCount'),
        ReferenceCountParser('lightPluginInfoEntries', 'lightPluginInfoCount', wstring)
    ],
    size=['pluginInfoSize'])

    def global_data_entry(id: Union[str, int]):
        return BlockParser(id, [
            uint32('type'),
            uint32('length'),
            Parser('value', 'length')
        ])

    def change_form_type_flags(id: Union[str, int]):
        return BlockParser(id, [
            uint8('lengths_size'),
            uint8('form_type')
        ])

    def change_form_type(id: Union[str, int]):
        return BytesExpansionParser(id, 1, [2, 6], change_form_type_flags('flags'))

    def change_form_entry(id: Union[str, int]):
        return BlockParser(id, [
            refID('refid'),
            Parser('changeFlags', 4),
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
            Parser('data', 'length1'),
        ])

    # tables

    global_data_table_1 = ReferenceCountParser('globalDataTable1', ['fileLocationTable', 'globalDataTable1Count'], global_data_entry, position=['fileLocationTable', 'globalDataTable1Offset'])
    global_data_table_2 = ReferenceCountParser('globalDataTable2', ['fileLocationTable', 'globalDataTable2Count'], global_data_entry, position=['fileLocationTable', 'globalDataTable2Offset'])
    change_forms = ReferenceCountParser('changeForms', ['fileLocationTable', 'changeFormCount'], change_form_entry, position=['fileLocationTable', 'changeFormsOffset'])
    global_data_table_3 = ReferenceCountParser('globalDataTable3', ['fileLocationTable', 'globalDataTable3Count'], global_data_entry, position=['fileLocationTable', 'globalDataTable3Offset'])
    main_content_elements = [
        uint8('formVersion'),
        uint32('pluginInfoSize'),
        plugin_info,
        file_location,
        global_data_table_1,
        global_data_table_2,
        change_forms,
        global_data_table_3,
        # Parser('bug_catch', size=8), # bugged global_data_table_3 1005 entry
        uint32('formIDArrayCount', position=['fileLocationTable', 'formIDArrayCountOffset']),
        ReferenceCountParser('formIDArray', 'formIDArrayCount', formID),
        uint32('visitedWorldspaceArrayCount'),
        ReferenceCountParser('visitedWorldspaceArray', 'visitedWorldspaceArrayCount', formID),
        uint32('unknownTable3Size', position=['fileLocationTable', 'unknownTable3Offset']),
        Parser('unknownTable3', 'unknownTable3Size'),
        EOFParser()
    ]

    main_content = BlockParser(
        'main_content', main_content_elements, 
        size=['_parent', '_parent', 'uncompressedSize']
    )

    file = BlockParser(
        'root',
        [
            header_info,
            header,
            screenshot,
            ReferenceMappedParser(
                'mainContent',
                ['header', 'compressionType'],
                {
                    0: BlockParser('uncompressed', main_content_elements),
                    0: main_content,
                    1: ErrorParser('zlib', ValueError('Did not expect zlib compression')),
                    2: BlockParser('lz4', [
                        uint32('uncompressedSize'),
                        uint32('compressedSize'),
                        BackFoldingParser(
                            'compressedContainer',
                            [
                                TransformationParser(
                                    'compressedData',
                                    ['_parent', 'compressedSize'],
                                    growingDecompress,
                                    compress,
                                    [
                                        main_content
                                    ],
                                    in_place=True
                                )
                            ],
                            foldSize = 8
                        )
                    ])
                },
                transfer_record=False
            ),
        ],
    )

    return file