# utils/validation.py

from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Tuple, Type

def validate_data(data: dict, dataclass_type: Type) -> Tuple[bool, str]:
    if not is_dataclass(dataclass_type):
        return False, "Provided type is not a dataclass."

    dataclass_fields = {field.name: field.type for field in fields(dataclass_type)}

    for field_name, field_type in dataclass_fields.items():
        if field_name not in data and not isinstance(None, field_type):
            return False, f"Missing required field: {field_name}"
        if field_name in data and not isinstance(data[field_name], field_type):
            return False, f"Invalid type for field '{field_name}', expected {field_type.__name__}"

    return True, None
