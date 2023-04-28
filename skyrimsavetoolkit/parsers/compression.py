import lz4.block

def growingDecompress(data: bytes, size=None):
    """do lz4 block format decompress and double size of buffer until it fits"""
    if size is None:
        size = 2 ** 12
    try:
        return lz4.block.decompress(data, uncompressed_size=size)
    except lz4.block.LZ4BlockError:
        return growingDecompress(data, size=size*2)
    
def compress(record):
    """compress using lz4 block"""
    import pdb; pdb.set_trace()
    return lz4.block.compress(record, store_size=False)