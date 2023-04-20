from mothpriest import *
from .essBlocks import *
from .essTypes import *
from ..compression import *

file = BlockParser(
    'root',
    [
        header_info,
        header,
        screenshot,
        uint32('uncompressedSize'),
        uint32('compressedSize'),
        TransformationParser(
            'compressedContainer',
            'compressedSize',
            growingDecompress,
            compress,
            [
                uint8('formVersion'),
                uint32('pluginInfoSize'),
                plugin_info,
                file_location,
                global_data_table_1,
                global_data_table_2,
                change_forms,
                global_data_table_3_debugged,
                uint32('formIDArrayCount'),
                ReferenceCountParser('formIDArray', 'formIDArrayCount', formID),
                uint32('visitedWorldspaceArrayCount'),
                ReferenceCountParser('visitedWorldspaceArray', 'visitedWorldspaceArrayCount', formID),
                uint32('unknownTable3Size'),
                ReferenceSizeParser('unknownTable3', 'unknownTable3Size'),
                EOFParser()
            ]
        )
    ],
)