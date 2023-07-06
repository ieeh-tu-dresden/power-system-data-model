# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum
import json
import pathlib
import typing as t

import pydantic

T = t.TypeVar("T")


class VoltageSystemType(enum.Enum):
    AC = "AC"
    DC = "DC"


class CosphiDir(enum.Enum):
    UE = "UE"
    OE = "OE"


class Base(pydantic.BaseModel):
    model_config = {
        "frozen": True,
        "use_enum_values": True,
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
