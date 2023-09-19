# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from collections.abc import Sequence

import pydantic

from psdm.base import Base

variable_dimension = 2


def validate_dimension(
    value: Sequence[Sequence[float]] | None,
) -> Sequence[Sequence[float]] | None:
    if value is not None and len(value[0]) is not len(value[1]):
        raise ValueError
    if value is not None and len(value) > variable_dimension:
        raise ValueError

    return value


class Characteristic(Base):
    """This class represents a data point based characteristic of power injection for a load."""

    name: str
    description: str | None = None
    data: Sequence[Sequence[float]] | None = None  # intended to be a sequence of two lists, e.g. Q(P)-characteristic

    @pydantic.field_validator("data", mode="before")
    def validate_characteristic_dimension(
        cls,
        v: Sequence[Sequence[float]] | None,
    ) -> Sequence[Sequence[float]] | None:
        return validate_dimension(v)
