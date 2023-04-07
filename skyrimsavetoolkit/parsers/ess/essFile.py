from mothpriest import *
from .essBlocks import *
from .essTypes import *
from ..compression import *

file = BlockParser(
    'file',
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
            BlockParser('compressedContent', [
                uint8('formVersion'),
                uint32('pluginInfoSize'),
                plugin_info,
                file_location,
                global_data_table_1,
                global_data_table_2,
                change_forms,
                global_data_table_3_debugged,
                uint32('formIDArrayCount'),
                ReferenceCountParser('formIDArray', 'formIDArrayCount', form_id_entry),
                uint32('visitedWorldspaceArrayCount'),
                ReferenceCountParser('visitedWorldspaceArray', 'visitedWorldspaceArrayCount', form_id_entry),
                uint32('unknownTable3Size'),
                ReferenceSizeRawParser('unknownTable3', 'unknownTable3Size'),
                EOFParser('eof')
            ])
        )
    ],
)