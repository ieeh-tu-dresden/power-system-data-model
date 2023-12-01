# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High VoltagePhasePhase, VoltagePhaseEarth Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import pydantic

from psdm.base import Base
from psdm.quantities.multi_phase import Power
from psdm.quantities.multi_phase import Voltage


class LoadModel(Base):
    """Load representation based on polynomial model.

    power = power_0*(c_p*(U/U_0)^exp_p + c_i*(U/U_0)^exp_i + (c_z)*(U/U_0)^exp_z)
    c_z = 1 - c_p - c_i
    """

    u_0: Voltage
    name: str | None = None
    c_p: pydantic.confloat(ge=0, le=1) = 1.0  # type: ignore[valid-type]
    c_i: pydantic.confloat(ge=0, le=1) = 0.0  # type: ignore[valid-type]
    exp_p: int = 0
    exp_i: int = 1
    exp_z: int = 2

    @pydantic.model_validator(mode="after")
    def validate_range_c(self) -> LoadModel:
        name = self.name
        c_p = self.c_p
        c_i = self.c_i
        if c_p + c_i > 1:
            msg = f"Load model {name!r}: Sum of components must not exceed 1, but {(c_p + c_i)=}."
            raise ValueError(msg)

        return self

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def c_z(self) -> float:
        return 1 - self.c_p - self.c_i

    def calc_power(self, u: Voltage, power: Power) -> Power:
        value = tuple(
            p
            * (
                self.c_p * (_u / _u_0) ** self.exp_p
                + self.c_i * (_u / _u_0) ** self.exp_i
                + self.c_z * (_u / _u_0) ** self.exp_z
            )
            for p, _u, _u_0 in zip(power.value, u.value, self.u_0.value, strict=True)
        )
        return Power(power_type=power.power_type, system_type=power.system_type, value=value, unit=power.unit)
