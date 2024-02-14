import json
import os.path
from typing import Dict


def read_json(filename: str) -> Dict[str, object]:
    if not os.path.exists(filename):
        return {}

    with open(filename, encoding="utf8") as f:
        data = json.load(f)
        assert isinstance(data, dict)
        return data


def write_json(filename: str, data: object) -> None:
    with open(filename, "w", encoding="utf8") as f:
        json.dump(data, f, sort_keys=True)
