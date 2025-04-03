# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2025.
# :license: BSD 3-Clause

from __future__ import annotations

import pydantic

from psdm.base import Base
from psdm.quantities.multi_phase import Power
from psdm.quantities.multi_phase import Voltage


class LoadModel(Base):
    """Load representation based on polynomial model without frequency dependency.

    power = power_0*(c_p*(U/U_0)^exp_p + c_i*(U/U_0)^exp_i + (c_z)*(U/U_0)^exp_z)
    The component c_z is computed automatically based on c_z = 1 - c_p - c_i.
    Assuming the exponents exp_p=0, exp_i=1 and exp_z=2 for a ZIP equivalent model.
    """

    u_0: Voltage
    name: str | None = None
    c_p: float = 1.0
    c_i: float = 0.0
    exp_p: float = 0.0
    exp_i: float = 1.0
    exp_z: float = 2.0

    @pydantic.computed_field  # type: ignore[prop-decorator]
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
        return Power(
            power_type=power.power_type,
            system_type=power.system_type,
            value=value,
            unit=power.unit,
        )
