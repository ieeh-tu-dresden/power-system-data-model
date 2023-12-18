import math

import pytest

from psdm.quantities.multi_phase import ActivePower
from psdm.quantities.multi_phase import ApparentPower
from psdm.quantities.multi_phase import CosPhi
from psdm.quantities.multi_phase import Power
from psdm.quantities.multi_phase import ReactivePower
from psdm.quantities.multi_phase import TanPhi
from psdm.quantities.single_phase import PowerType
from psdm.quantities.single_phase import Unit


class TestCosPhi:
    def test_average_ac_active_power(self) -> None:
        cp = CosPhi(value=(0.9, 0.8, 0.7))
        p = ActivePower(value=(100, 200, 300))
        assert cp.weighted_average(p) == 0.7597990  # noqa: PLR2004

    def test_average_ac_apparent_power(self) -> None:
        cp = CosPhi(value=(0.9, 0.8, 0.7))
        p = ApparentPower(value=(100, 200, 300))
        assert cp.weighted_average(p) == 0.7666667  # noqa: PLR2004

    def test_average_ac_reactive_power(self) -> None:
        cp = CosPhi(value=(0.9, 0.8, 0.7))
        p = ReactivePower(value=(100, 200, 300))
        assert cp.weighted_average(p) == 0.7806001  # noqa: PLR2004

    def test_average_power_type_mismatch(self) -> None:
        cp = CosPhi(value=(0.9, 0.8, 0.7))
        p = Power(value=(100, 200, 300), power_type=PowerType.DC, unit=Unit.WATT)
        assert math.isnan(cp.weighted_average(p))

    def test_average_dimension_mismatch(self) -> None:
        cp = CosPhi(value=(0.9, 0.8, 0.7))
        p = ActivePower(value=(100, 200))
        with pytest.raises(ValueError):  # noqa: PT011
            cp.weighted_average(p)

        cp = CosPhi(value=(0.9, 0.8))
        p = ActivePower(value=(100, 200, 300))
        with pytest.raises(ValueError):  # noqa: PT011
            cp.weighted_average(p)

    def test_average_nan(self) -> None:
        cp = CosPhi(value=(0.9, 0.8, float("nan")))
        p = ActivePower(value=(100, 200, 300))
        assert math.isnan(cp.weighted_average(p))

        cp = CosPhi(value=(0.9, 0.8, 0.7))
        p = ActivePower(value=(100, float("nan"), 300))
        assert math.isnan(cp.weighted_average(p))


class TestTanPhi:
    def test_average_ac_active_power(self) -> None:
        tp = TanPhi(value=(0.4843, 0.75, 1.0202))
        p = ActivePower(value=(100, 200, 300))
        assert tp.weighted_average(p) == 0.8408167  # noqa: PLR2004

    def test_average_ac_apparent_power(self) -> None:
        tp = TanPhi(value=(0.4843, 0.75, 1.0202))
        p = Power(value=(100, 200, 300), power_type=PowerType.AC_APPARENT, unit=Unit.VOLTAMPERE)
        assert tp.weighted_average(p) == 0.8213670  # noqa: PLR2004

    def test_average_ac_reactive_power(self) -> None:
        tp = TanPhi(value=(0.4843, 0.75, 1.0202))
        p = Power(value=(100, 200, 300), power_type=PowerType.AC_REACTIVE, unit=Unit.VOLTAMPERE_REACTIVE)
        assert tp.weighted_average(p) == 0.7820542  # noqa: PLR2004

    def test_average_power_type_mismatch(self) -> None:
        tp = TanPhi(value=(0.4843, 0.75, 1.0202))
        p = Power(value=(100, 200, 300), power_type=PowerType.DC, unit=Unit.WATT)
        assert math.isnan(tp.weighted_average(p))

    def test_average_dimension_mismatch(self) -> None:
        tp = TanPhi(value=(0.4843, 0.75, 1.0202))
        p = ActivePower(value=(100, 200))
        with pytest.raises(ValueError):  # noqa: PT011
            tp.weighted_average(p)

        tp = TanPhi(value=(0.4843, 0.75))
        p = ActivePower(value=(100, 200, 300))
        with pytest.raises(ValueError):  # noqa: PT011
            tp.weighted_average(p)

    def test_average_nan(self) -> None:
        tp = TanPhi(value=(0.4843, 0.75, float("nan")))
        p = ActivePower(value=(100, 200, 300))
        assert math.isnan(tp.weighted_average(p))

        tp = TanPhi(value=(0.4843, 0.75, 1.0202))
        p = ActivePower(value=(100, float("nan"), 300))
        assert math.isnan(tp.weighted_average(p))
