from typing import Any, List


def _get_json_list(data: Any):
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        for key, value in data.items():
            result = _get_json_list(value)
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

def _get_csv_json_headers(data: Any, parent_key: str = "") -> List[str]:
    headers = []

    if isinstance(data, list):
        # Si es una lista, extrae los encabezados del primer elemento
        if data and isinstance(data[0], dict):
            headers.extend(data[0].keys())
        return headers

    elif isinstance(data, dict):
        # Si es un diccionario, recorre sus claves y valores
        for key, value in data.items():
            new_key = f"{parent_key}/{key}" if parent_key else key
            if isinstance(value, dict):
                # Si el valor es un diccionario, llama recursivamente
                headers.extend(_get_csv_json_headers(value, new_key))
            elif isinstance(value, list):
                # Si el valor es una lista, llama recursivamente
                headers.extend(_get_csv_json_headers(value, new_key))
            else:
                # Si es un valor simple, agrega la clave como encabezado
                headers.append(new_key)
        return headers

    else:
        # Si no es ni lista ni diccionario, devuelve una lista vacía
        return headers