import argparse
from pathlib import Path
from .core import validate_file

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
    return parser.parse_args()

if __name__ == '__main__':
    validate_file(**vars(parse_args()))