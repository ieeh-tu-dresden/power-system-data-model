# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum
import json
import pathlib
import typing as t
import warnings

import annotated_types
import pydantic
from pydantic_core import PydanticCustomError

T = t.TypeVar("T")
U = t.TypeVar("U", bound=t.Hashable)


class VoltageSystemType(enum.Enum):
    AC = "AC"
    DC = "DC"


def _validate_unique_list(v: tuple[U]) -> tuple[U]:
    if len(v) != len(set(v)):
        error_type = "unique_list"
        message_template = "List must be unique"
        raise PydanticCustomError(error_type=error_type, message_template=message_template)
    return v


UniqueTuple = t.Annotated[
    tuple[U, ...],
    pydantic.AfterValidator(_validate_unique_list),
    pydantic.Field(json_schema_extra={"uniqueItems": True}),
]
UniqueNonEmptyTuple = t.Annotated[
    tuple[U, ...],
    annotated_types.Len(1, 2**126),
    pydantic.AfterValidator(_validate_unique_list),
    pydantic.Field(json_schema_extra={"uniqueItems": True}),
]
NonEmptyTuple = t.Annotated[tuple[T, ...], annotated_types.Len(1, 2**126)]


class Base(pydantic.BaseModel):
    model_config = {
        "frozen": True,
        "use_enum_values": True,
        "validate_default": True,
        "ser_json_inf_nan": "constants",
    }

    @classmethod
    def from_file(cls, file_path: str | pathlib.Path) -> Base:
        file_path = pathlib.Path(file_path)
        with file_path.open("r", encoding="utf-8") as file_handle:
            return cls.model_validate_json(file_handle.read())

    def to_json(self, file_path: str | pathlib.Path, indent: int = 2) -> None:
        file_path = pathlib.Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w+", encoding="utf-8") as file_handle:
            _json_data = self.model_dump_json()
            _data = json.loads(_json_data)
            json.dump(_data, file_handle, indent=indent, sort_keys=True)

    @classmethod
    def from_json(cls, json_str: str) -> Base:
        return cls.model_validate_json(json_str)


def validate_deprecated(self: U, attr_dpr: str, attr_new: str) -> U:
    if getattr(self, attr_dpr) is not None:
        msg = f"{attr_dpr} is deprecated. Use {attr_new} instead."
        warnings.warn(msg, DeprecationWarning, stacklevel=4)

    return self
