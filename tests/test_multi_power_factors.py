import math

from psdm.quantities.multi_phase import CosPhi
from psdm.quantities.multi_phase import Power
from psdm.quantities.single_phase import PowerType
from psdm.quantities.single_phase import SystemType


class TestCosPhi:
    def test_average_ac_active(self) -> None:
        cp = CosPhi(value=(0.9, 0.8, 0.7))
        p = Power(value=(100, 200, 300), power_type=PowerType.AC_ACTIVE)
        assert cp.weighted_average(p) == 0.556

    def test_average_ac_apparent(self) -> None:
        cp = CosPhi(value=(0.9, 0.8, 0.7))
        p = Power(value=(100, 200, 300), power_type=PowerType.AC_APPARENT)
        assert cp.weighted_average(p) == 0.778

    def test_average_ac_reactive(self) -> None:
        cp = CosPhi(value=(0.9, 0.8, 0.7))
        p = Power(value=(100, 200, 300), power_type=PowerType.AC_REACTIVE)
        assert cp.weighted_average(p) == 0.875

    def test_average_nan(self) -> None:
        cp = CosPhi(value=(0.9, 0.8, 0.7))
        p = Power(value=(100, 200, 300), power_type=PowerType.DC)
        assert math.isnan(cp.weighted_average(p))
