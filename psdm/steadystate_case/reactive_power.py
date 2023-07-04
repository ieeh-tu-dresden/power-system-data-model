# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import pydantic

from psdm.steadystate_case.controller import Controller
from psdm.topology.load import PowerBase
from psdm.topology.load import validate_symmetry
from psdm.topology.load import validate_total


class ReactivePower(PowerBase):
    controller: Controller | None = None

    @pydantic.model_validator(mode="after")  # type: ignore[arg-type]
    def _validate_symmetry(cls, power: ReactivePower) -> ReactivePower:
        return validate_symmetry(power)

    @pydantic.model_validator(mode="after")  # type: ignore[arg-type]
    def _validate_total(cls, power: ReactivePower) -> ReactivePower:
        return validate_total(power)
