# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import datetime as dt
import enum
import typing as t
import uuid

import pydantic

from psdm.base import Base
from psdm.base import model_validator_after
from psdm.base import model_validator_before
from psdm.base import validate_deprecated

VERSION = "1.9.0"


class SignConvention(enum.Enum):
    PASSIVE = "PASSIVE"  # consumer load centered
    ACTIVE = "ACTIVE"  # producer load centered


class Meta(Base):
    """This class represents the meta data related to the grid export."""

    name: str | None = pydantic.Field(None, repr=False)

    @model_validator_after
    def _validate_deprecated(self) -> Meta:
        return validate_deprecated(self, attr_dpr="name", attr_new="grid")

    grid: str | None = None

    @model_validator_before
    def _validate_naming(cls, data: t.Any) -> t.Any:  # noqa: ANN401
        if data.get("grid") is None and data.get("name") is None:
            msg = "grid\nField required"
            raise ValueError(msg)

        if data.get("grid") is None:
            data["grid"] = data["name"]

        return data

    date: dt.date

    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)  # noqa: A003
    sign_convention: SignConvention | None = None
    project: str | None = None
    case: str | None = None

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def version(self) -> str:
        return VERSION
