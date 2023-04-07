from mothpriest import *
from .skseBlocks import *

file = BlockParser('root', [
    header,
    ReferenceCountParser('plugins', ['header', 'numPlugins'], plugin),
    EOFParser()
])