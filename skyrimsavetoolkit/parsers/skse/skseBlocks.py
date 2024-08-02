from mothpriest import *
from mothpriest.macros import *
from functools import partial

header = BlockParser('header', [
    MagicParser('SKSE', 'magic'),
    uint32('formatVersion'),
    uint32('skseVersion'),
    uint32('runtimeVersion'),
    uint32('numPlugins')
])

def chunk(id):
    chunk_header = BlockParser('chunkHeader', [
        uint32('type'),
        uint32('version'),
        uint32('length')
    ])

    return BlockParser(id, [
        chunk_header,
        ReferenceCountParser('data', ['chunkHeader', 'length'], uint8)
    ])


def plugin(id):
    plugin_header = BlockParser('pluginHeader', [
        uint32('signature'),
        uint32('numChunks'),
        uint32('length')
    ])
    return BlockParser(id, [
        plugin_header,
        ReferenceCountParser('chunks', ['pluginHeader', 'numChunks'], chunk)
    ])