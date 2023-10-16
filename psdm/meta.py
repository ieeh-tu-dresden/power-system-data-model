# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import datetime
import enum
import uuid

import pydantic

from psdm.base import Base
from psdm.base import validate_deprecated

VERSION = "1.8.1"


class SignConvention(enum.Enum):
    PASSIVE = "PASSIVE"  # consumer load centered
    ACTIVE = "ACTIVE"  # producer load centered


class Meta(Base):
    """This class represents the meta data related to the grid export."""

    name: str | None = None

    @pydantic.model_validator(mode="after")  # type: ignore[arg-type]
    def _validate_deprecated(cls, meta: Meta) -> Meta:
        return validate_deprecated(cls, obj=meta, attr_dpr="name", attr_new="grid")  # type: ignore[arg-type]

    grid: str | None = None

    @pydantic.model_validator(mode="after")  # type: ignore[arg-type]
    def _validate_naming(cls, meta: Meta) -> Meta:
        if meta.name is None and meta.grid is None:
            msg = "grid\nField required"
            raise ValueError(msg)

        return meta

    date: datetime.date
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)  # noqa: A003
    sign_convention: SignConvention | None = None
    project: str | None = None
    case: str | None = None

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def version(self) -> str:
        return VERSION
