# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import pydantic

from psdm.base import Base
from psdm.steadystate_case.controller import Controller
from psdm.topology.load import validate_symmetry
from psdm.topology.load import validate_total


class ReactivePower(Base):
    value: float  # actual reactive power (three-phase)
    value_a: float  # actual reactive power (phase a)
    value_b: float  # actual reactive power (phase b)
    value_c: float  # actual reactive power (phase c)
    is_symmetrical: bool
    controller: Controller | None = None

    @pydantic.root_validator(skip_on_failure=True)
    def _validate_symmetry(cls, values: dict[str, float]) -> dict[str, float]:
        return validate_symmetry(values)

    @pydantic.root_validator(skip_on_failure=True)
    def _validate_total(cls, values: dict[str, float]) -> dict[str, float]:
        return validate_total(values)
