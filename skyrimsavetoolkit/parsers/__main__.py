import argparse
from pathlib import Path
from .core import parse_file

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
        default=None
    )
    parser.add_argument(
        '--there-and-back',
        action='store_true',
        help='if this flag is set, parse and unparse in one action'
    )
    return parser.parse_args()

if __name__ == '__main__':
    parse_file(**vars(parse_args()))
