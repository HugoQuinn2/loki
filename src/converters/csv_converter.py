import json
import os
from enum import Enum
from typing import Any

import xmltodict
import yaml

from exceptions.ErrorParsingFile import ErrorParingFile
from exceptions.ExtensionNotSupported import ExtensionNotSupported
from exceptions.FileNotFound import FileNotFound
from utils.file_utils import get_file_extension
from utils.json_utils import get_json_list, get_csv_json_headers

from utils.json_utils import get_nested_value

valid_files_type = ['json', 'xml', 'yaml']

class CsvConverter(Enum):
    LIST = 'list'
    KEYED = 'keyed'
    ARRAY = 'array'
    NESTED = 'nested'

def csv_convert(input_file: str, conversion_type: CsvConverter):
    is_valid_file_in(input_file)
    file_in_type = get_file_extension(input_file)

    with open(input_file, 'r', encoding='utf-8') as read_file_in:
        if file_in_type == 'json':
            file_in_content = json.load(read_file_in)
            return _convert_json_to_csv(file_in_content, conversion_type=conversion_type)
        elif file_in_type == 'yaml':
            file_in_content = yaml.safe_load(read_file_in)
        elif file_in_type == 'xml':
            file_in_content = xmltodict.parse(read_file_in.read())
        else:
            raise ExtensionNotSupported(f"File type {file_in_type} not supported.")


def is_valid_file_in(file_in):
    if not os.path.exists(file_in):
        raise FileNotFound(f"File {file_in} does not exist.")
    file_type = get_file_extension(file_in)
    if file_type not in valid_files_type:
        raise ExtensionNotSupported(f"File type {file_type} not supported.")


def _convert_json_to_csv(data: Any, conversion_type: CsvConverter):
    if conversion_type == CsvConverter.LIST:
        headers = get_csv_json_headers(data)
        output = [','.join(headers)]
        output.extend([','.join(str(get_nested_value(data, h)) for h in headers) for d in data])
        return '\n'.join(output)
    elif conversion_type == CsvConverter.KEYED:
        print()
    elif conversion_type == CsvConverter.ARRAY:
        print()
    elif conversion_type == CsvConverter.NESTED:
        print()
    else:
        raise ErrorParingFile(f"CSV {conversion_type} Convertion not valid.")