import os

from exceptions.ExtensionNotSupported import ExtensionNotSupported
from exceptions.FileNotFound import FileNotFound
from utils.file_utils import get_file_extension

valid_files_type = ['csv', 'xml', 'yaml']

def is_valid_file_in(file_in):
    if not os.path.exists(file_in):
        raise FileNotFound(f"File {file_in} does not exist.")

    file_type = get_file_extension(file_in)

    if not file_type in valid_files_type:
        raise ExtensionNotSupported(f"Fyle type {file_type} not supported.")