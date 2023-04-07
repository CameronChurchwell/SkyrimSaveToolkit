from mothpriest import *
from .essBlocks import *
from .essTypes import *
from .compression import *

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
            # PDBParser('debug')
            BlockParser('compressedContent', [
                uint8('formVersion'),
                uint32('pluginInfoSize'),
                plugin_info,
                file_location,
                ReferenceCountParser('globalDataTable1', ['fileLocationTable', 'globalDataTable1Count'], global_data_entry),
                ReferenceCountParser('globalDataTable2', ['fileLocationTable', 'globalDataTable2Count'], global_data_entry),
                ReferenceCountParser('changeForms', ['fileLocationTable', 'changeFormCount'], change_form_entry),
                ReferenceCountParser('globalDataTable3', ['fileLocationTable', 'globalDataTable3Count'], global_data_entry),
                uint32('formIDArrayCount'),
                ReferenceCountParser('formIDArray', 'formIDArrayCount', form_id_entry)
                # ReferenceCountParser('debug', ['fileLocationTable', 'changeFormCount'], FixedSizeRawParser('', 1))
                # DebugRemainderParser(100)
                # RawParser('remainder')
            ])
        )
    ],
)