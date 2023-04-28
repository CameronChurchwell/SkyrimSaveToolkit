from pathlib import Path
from skyrimsavetoolkit.parsers import parse_ess

def validate_file(input_file: Path):
    parsed = parse_ess(input_file)
