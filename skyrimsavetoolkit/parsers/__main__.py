import argparse
from pathlib import Path
from .skse import file as skseFileParser
from .ess import file as essFileParser
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

def parse_file(input_file: Path, output_file: Path):
    extension = input_file.suffix
    if extension.lower() == '.ess':
        parsed = parse_ess(input_file)
    elif extension.lower() == '.skse':
        parsed = parse_skse(input_file)

    if output_file is None:
        print(parsed)
        return
    
    with open(output_file, 'w') as f:
        f.write(str(parsed))
    return

# TODO refactor to remove need for these somewhat redundant functions
def parse_ess(input_file: Path):
    """Read and parse an ess file from a path"""

    with open(input_file, 'rb') as f:
        input_content = f.read()

    parsed = essFileParser.parse(BytesIO(input_content))

    return parsed

def parse_skse(input_file: Path):
    """Read and parse an skse file from a path"""

    with open(input_file, 'rb') as f:
        input_content = f.read()

    parsed = skseFileParser.parse(BytesIO(input_content))

    return parsed

if __name__ == '__main__':
    parse_file(**vars(parse_args()))
