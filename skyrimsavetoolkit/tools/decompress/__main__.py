import argparse
from pathlib import Path
from .core import decompress_file

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Parse a skyrim save into a readable file"
    )
    parser.add_argument(
        '--input-file',
        type=Path,
        help='input file'
    )
    parser.add_argument(
        '--output-file',
        type=Path,
        help='output file',
    )
    return parser.parse_args()

if __name__ == '__main__':
    decompress_file(**vars(parse_args()))