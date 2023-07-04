# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import pydantic

from psdm.topology.load import PowerBase
from psdm.topology.load import validate_symmetry
from psdm.topology.load import validate_total


class ActivePower(PowerBase):
    value: float  # actual active power (three-phase)
    value_a: float  # actual active power (phase a)
    value_b: float  # actual active power (phase b)
    value_c: float  # actual active power (phase c)
    is_symmetrical: bool

    @pydantic.model_validator(mode="after")  # type: ignore[arg-type]
    def _validate_symmetry(cls, power: ActivePower) -> ActivePower:
        return validate_symmetry(power)

    @pydantic.model_validator(mode="after")  # type: ignore[arg-type]
    def _validate_total(cls, power: ActivePower) -> ActivePower:
        return validate_total(power)
