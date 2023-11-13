from skyrimsavetoolkit.parsers import parse_ess
from pathlib import Path
from mothpriest import Parser, ReferenceMappedParser

def decompress_file(input_file: Path, output_file: Path):
    """Decompresses an ess file and writes the output to another ess file"""

    if input_file == output_file:
        raise RuntimeError('input file and output file cannot be the same value (to protect you from yourself)')
    
    # parse input file
    parser = parse_ess(input_file)
    
    decompress(parser)

    with open(output_file, 'wb+') as f:
        parser.unparse(f)

def decompress(parser: Parser):
    """Decompresses an ess parser"""

    # switch from compression to no compression
    # here a key of 0 means no compression, and 2 means compression
    # this also updates the compressionType field and removes the compression lengths``
    switchParser = parser.getReference('mainContent')
    assert isinstance(switchParser, ReferenceMappedParser)
    # import pdb; pdb.set_trace()
    switchParser.setKey(0)