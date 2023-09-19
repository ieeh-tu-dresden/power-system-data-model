# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import datetime
import enum
import typing as t
import uuid

import pydantic

from psdm.base import Base

VERSION = "1.8.0"


class SignConvention(enum.Enum):
    PASSIVE = "PASSIVE"  # consumer load centered
    ACTIVE = "ACTIVE"  # producer load centered


class Meta(Base):
    """This class represents the meta data related to the grid export."""

    version: t.ClassVar[str] = VERSION
    name: str
    date: datetime.date
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)  # noqa: A003
    sign_convention: SignConvention | None = None
    project: str | None = None
    case: str | None = None
