from mothpriest import *
from mothpriest.macros import *

header = BlockParser('header', [
    MagicParser('SKSE', 'magic'),
    uint32('formatVersion'),
    uint32('skseVersion'),
    uint32('runtimeVersion'),
    uint32('numPlugins')
])

plugin_header = BlockParser('pluginHeader', [
    uint32('signature'),
    uint32('numChunks'),
    uint32('length')
])

chunk_header = BlockParser('chunkHeader', [
    uint32('type'),
    uint32('version'),
    uint32('length')
])

plugin_data = uint8('data')

chunk = BlockParser('chunk', [
    chunk_header,
    ReferenceCountParser('data', ['chunkHeader', 'length'], plugin_data)
])

plugin = BlockParser('plugin', [
    plugin_header,
    ReferenceCountParser('chunk', ['pluginHeader', 'numChunks'], chunk)
])