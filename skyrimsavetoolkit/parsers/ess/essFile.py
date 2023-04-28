from mothpriest import *
from .essBlocks import *
from .essTypes import *
from ..compression import *

main_content_elements = [
    uint8('formVersion'),
    uint32('pluginInfoSize'),
    plugin_info,
    file_location,
    # ReferencePositionParser('globalDataTable1Start', ['fileLocationTable', 'globalDataTable1Offset']),
    global_data_table_1,
    # ReferencePositionParser('globalDataTable2Start', ['fileLocationTable', 'globalDataTable2Offset']),
    global_data_table_2,
    # ReferencePositionParser('changeFormsStart', ['fileLocationTable', 'changeFormsOffset']),
    change_forms,
    # ReferencePositionParser('globalDataTable3Start', ['fileLocationTable', 'globalDataTable3Offset']),
    global_data_table_3_debugged,
    # ReferencePositionParser('formIDArrayCountStart', ['fileLocationTable', 'formIDArrayCountOffset']),
    uint32('formIDArrayCount'),
    ReferenceCountParser('formIDArray', 'formIDArrayCount', formID),
    uint32('visitedWorldspaceArrayCount'),
    ReferenceCountParser('visitedWorldspaceArray', 'visitedWorldspaceArrayCount', formID),
    # ReferencePositionParser('unknownTable3Start', ['fileLocationTable', 'unknownTable3Offset']),
    uint32('unknownTable3Size'),
    Parser('unknownTable3', 'unknownTable3Size'),
    EOFParser()
]

file = BlockParser(
    'root',
    [
        header_info,
        header,
        screenshot,
        ReferenceMappedParser('mainContent', ['header', 'compressionType'], {
            0: BlockParser('uncompressed', main_content_elements),
            1: ErrorParser('zlib', ValueError('Did not expect zlib compression')),
            2: BlockParser('lz4', [
                SourceDeletingParser('compressionSizes', [
                    uint32('uncompressedSize'),
                    uint32('compressedSize'),
                ]),
                TransformationParser(
                    'compressedContainer',
                    ['compressionSizes', 'compressedSize'],
                    growingDecompress,
                    compress,
                    main_content_elements,
                    in_place=True
                )
            ])
        }),
    ],
)