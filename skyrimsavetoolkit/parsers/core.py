from pathlib import Path
from .skse import file as skseFileParser
from .ess import file as essFileParser
from .esp import file as espFileParser
from io import BytesIO
from mothpriest.parsers import Parser

def parse_file(input_file: Path, output_file: Path, there_and_back: bool):
    extension = input_file.suffix.lower()
    if extension == '.ess':
        parsed = parse_ess(input_file)
    elif extension == '.skse':
        parsed = parse_skse(input_file)
    elif extension == '.esp':
        parsed = parse_esp(input_file)
    else:
        raise ValueError(f'extension {extension} does not match any known extension')

    if there_and_back:
        if extension == '.ess':
            # unparse_ess(output_file, parsed)
            buffer = BytesIO()
            essFileParser.unparse(buffer)
            buffer.seek(0)
            with open(output_file, 'wb') as f:
                f.write(buffer.read())
        return

    with open(output_file, 'w') as f:
        f.write(str(parsed))
    return

# TODO refactor to remove need for these somewhat redundant functions
def parse_ess(input_file: Path) -> Parser:
    """Read and parse an ess file from a path"""

    with open(input_file, 'rb') as f:
        input_content = f.read()

    essFileParser.parse(BytesIO(input_content))

    return essFileParser

def unparse_ess(output_file: Path, record):
    """Unparse a record back into an ess file"""

    if not 'root' in record:
        record = {'root': record}

    essFileParser.updateRecord
    buffer = BytesIO()
    essFileParser.unparse(buffer)
    buffer.seek(0)

    with open(output_file, 'wb') as f:
        f.write(buffer.read())

def parse_skse(input_file: Path):
    """Read and parse an skse file from a path"""

    with open(input_file, 'rb') as f:
        input_content = f.read()

    parsed = skseFileParser.parse(BytesIO(input_content))

    return parsed

def parse_esp(input_file: Path):
    """Read and parse an esp file from a path"""

    with open(input_file, 'rb') as f:
        input_content = f.read()

    parsed = espFileParser.parse(BytesIO(input_content))

    return parsed