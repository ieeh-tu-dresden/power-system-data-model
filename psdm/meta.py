# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import datetime as dt
import enum
import uuid

import pydantic

from psdm.base import Base

VERSION = "2.0.1"


class SignConvention(enum.Enum):
    PASSIVE = "PASSIVE"  # consumer load centered
    ACTIVE = "ACTIVE"  # producer load centered


class Meta(Base):
    """This class represents the meta data related to the grid export."""

    grid: str
    date: dt.date

    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)  # noqa: A003
    sign_convention: SignConvention | None = None
    project: str | None = None
    case: str | None = None

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def version(self) -> str:
        return VERSION
