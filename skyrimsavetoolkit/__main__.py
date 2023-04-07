import argparse
from pathlib import Path
from .parsers.essFile import file
from io import BytesIO

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
        '--output-file',
        type=Path,
        help='output file',
        default=None
    )

    return parser.parse_args()

def parse_ess(input_file: Path, output_file: Path):
    """Parse an ess file and either return or print the output"""

    with open(input_file, 'rb') as f:
        input_content = f.read()

    parsed = file.parse(BytesIO(input_content))

    if output_file is None:
        print(parsed)
        return
    
    with open(output_file, 'w') as f:
        f.write(str(parsed))
    return


if __name__ == '__main__':
    parse_ess(**vars(parse_args()))
