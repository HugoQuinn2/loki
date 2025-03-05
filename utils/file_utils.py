import os
from pathlib import Path


def get_file_extension(file):
    return os.path.splitext(file)[1].lower().replace('.', '')

def create_output_file_name(file: str, extension: str):
    input_path = Path(file)
    output_file_name = str(input_path.with_suffix(f'{extension}'))

    if not os.path.exists(output_file_name):
        return output_file_name

    base, ext = os.path.splitext(output_file_name)
    counter = 1

    while True:
        new_path = f"{base} ({counter}){ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1