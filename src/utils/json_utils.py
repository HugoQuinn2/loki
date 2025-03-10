from email.policy import default
from typing import Any, List


def get_json_list(data: Any):
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        for key, value in data.items():
            result = get_json_list(value)
            if result is not None:
                return result

def _get_csv_json_headers_(data: Any):
    if isinstance(data, list):
        return data[0].keys()
    elif isinstance(data, dict):
        headers = []
        for key, value in data.items():
                headers.append(key)

        return headers


def get_csv_json_headers(data: Any, parent_key: str = "") -> List[str]:
    headers = []

    if isinstance(data, list):
        for key, value in data[0].items():
            if isinstance(value, dict):
                headers.extend(get_csv_json_headers(value, f"{parent_key}.{key}" if parent_key else key))
            else:
                headers.append(f"{parent_key}.{key}" if parent_key else key)
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                headers.extend(get_csv_json_headers(value, f"{parent_key}.{key}" if parent_key else key))
            elif isinstance(value, dict):
                headers.extend(get_csv_json_headers(value, f"{parent_key}.{key}" if parent_key else key))
            else:
                headers.append(f"{parent_key}.{key}" if parent_key else key)

    return headers

def get_nested_value(data: Any, path: str):
    keys = path.split(".")
    current = data

    print(current)
    for key in keys:
        if isinstance(current, list):
            current = current[key]
            print(f"list: {key} {current}")
        elif isinstance(current, dict):
            current = current.get(key)
            print(f"dict: {key} {current}")
        else:
            return ''

    return current
