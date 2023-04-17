import argparse
from pathlib import Path
from .core import patchSaveMerge

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Parse a skyrim save into a json file"
    )
    parser.add_argument(
        '--input-file',
        type=Path,
        help='input file'
    )
    parser.add_argument(
        '--map-file',
        type=Path,
        help='map file created by zMerge'
    )
    parser.add_argument(
        '--merge-name',
        type=str,
        help='the name of the new merged plugin file (esp?), must match exactly including capitalization'
    )
    parser.add_argument(
        '--output-file',
        type=Path,
        help='output file, leaving this blank is equivalent to a dry run',
        default=None
    )
    return parser.parse_args()

if __name__ == '__main__':
    patchSaveMerge(**vars(parse_args()))