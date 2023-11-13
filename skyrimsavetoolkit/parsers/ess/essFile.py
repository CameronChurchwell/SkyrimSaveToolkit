from mothpriest import *
from .essBlocks import *
from .essTypes import *
from ..compression import *

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