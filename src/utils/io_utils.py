import json
from pathlib import Path
from urllib.parse import quote, unquote
import base64


def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def url_encode(cadena):
    return quote(cadena, safe="")


def url_decode(cadena):
    return unquote(cadena)


def base64_decode(cadena):
    return base64.b64decode(cadena).decode("utf-8")


def base64_encode(cadena):
    return base64.b64encode(cadena.encode("utf-8"))
