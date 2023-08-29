# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import datetime
import typing as t
import uuid

import pydantic

from psdm.base import Base

VERSION = "1.6.0"


class Meta(Base):
    version: t.ClassVar[str] = VERSION
    name: str
    date: datetime.date
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)  # noqa: A003
    project: str | None = None
    case: str | None = None
