import csv
import yaml
import os.path
from enum import Enum
from typing import List, Any

from exceptions.ErrorParsingFile import ErrorParingFile
from exceptions.ExtensionNotSupported import ExtensionNotSupported
from exceptions.FileNotFound import FileNotFound
from utils.file_utils import get_file_extension

valid_files_type = ['csv', 'xml', 'yaml']

class Conversion(Enum):
    KEYED = 'keyed'
    JSON_ARRAY = 'array'
    JSON_COLUMN_ARRAY = 'colum-array'
    LIST = 'list'

def convert(input_file: str, conversion_type: Conversion):
    is_valid_file_in(input_file)
    file_in_type = get_file_extension(input_file)

    with open(input_file, 'r', encoding='utf-8') as read_file_in:
        if file_in_type == 'csv':
            file_in_content = csv.reader(read_file_in)
            headers = next(file_in_content)
            return _convert_csv_to_json(headers, file_in_content, conversion_type=conversion_type)
        elif file_in_type == 'yaml':
            file_in_content = yaml.safe_load(read_file_in)
            return _convert_yaml_to_json(file_in_content, conversion_type=conversion_type)



def _convert_csv_to_json(headers: List[str], csv_data: Any, conversion_type: Conversion) -> Any:
    if conversion_type == Conversion.KEYED:
        return {row[0]: dict(zip(headers[1:], row[1:])) for row in csv_data}
    elif conversion_type == Conversion.JSON_ARRAY:
        return list(csv_data)
    elif conversion_type == Conversion.JSON_COLUMN_ARRAY:
        columns = {header: [] for header in headers}
        for row in csv_data:
            for header, valor in zip(headers, row):
                columns[header].append(valor)
        return columns
    elif conversion_type == Conversion.LIST:
        return [dict(zip(headers, row)) for row in csv_data]
    else:
        raise ErrorParingFile(f"Type conversion {conversion_type} not valid.")

def _convert_yaml_to_json(yaml_data: Any, conversion_type: Conversion) -> Any:
    if conversion_type == Conversion.KEYED:
        if isinstance(yaml_data, dict):
            return yaml_data
        elif isinstance(yaml_data, list):
            return {i: item for i, item in enumerate(yaml_data)}

    elif conversion_type == Conversion.JSON_ARRAY:
        return list(yaml_data) if isinstance(yaml_data, (list, dict)) else [yaml_data]

    elif conversion_type == Conversion.JSON_COLUMN_ARRAY:
        if isinstance(yaml_data, dict):
            return {key: [value] for key, value in yaml_data.items()}
        elif isinstance(yaml_data, list) and all(isinstance(item, dict) for item in yaml_data):
            columns = {}
            for item in yaml_data:
                for key, value in item.items():
                    columns.setdefault(key, []).append(value)
            return columns
        else:
            raise ErrorParingFile("YAML data format is not suitable for column-array conversion.")

    elif conversion_type == Conversion.LIST:
        return yaml_data

    else:
        raise ErrorParingFile(f"Type conversion {conversion_type} not valid.")

def is_valid_file_in(file_in):
    if not os.path.exists(file_in):
        raise FileNotFound(f"File {file_in} does not exist.")

    file_type = get_file_extension(file_in)

    if not file_type in valid_files_type:
        raise ExtensionNotSupported(f"Fyle type {file_type} not supported.")