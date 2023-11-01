# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.quantities import ActivePower
from psdm.quantities import ApparentPower
from psdm.quantities import Frequency
from psdm.quantities import Power
from psdm.quantities import PowerFactor
from psdm.quantities import PowerType
from psdm.quantities import ReactivePower
from psdm.quantities import Voltage


class TestFrequency:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (-2, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            Frequency(value=value)


class TestVoltage:
    @pytest.mark.parametrize(
        (
            "values",
            "is_symmetrical",
            "expectation",
        ),
        [
            ((0, 0, 0), True, does_not_raise()),
            ((1, 1, 1), True, does_not_raise()),
            ((2, 1, 1), False, does_not_raise()),
            ((1, 1, 1), False, pytest.raises(AssertionError)),
            ((-2, 1, 1), True, pytest.raises(pydantic.ValidationError)),
            ((2, 1, 1), True, pytest.raises(AssertionError)),
        ],
    )
    def test_init(
        self,
        values,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            v = Voltage(values=values)
            assert v.is_symmetrical == is_symmetrical


class TestPower:
    @pytest.mark.parametrize(
        (
            "value_total",
            "values",
            "power_type",
            "is_symmetrical",
            "expectation",
        ),
        [
            (0, (0, 0, 0), PowerType.AC_APPARENT, True, does_not_raise()),
            (3, (1, 1, 1), PowerType.AC_APPARENT, True, does_not_raise()),
            (4, (2, 1, 1), PowerType.AC_APPARENT, False, does_not_raise()),
            (0, (-2, 1, 1), PowerType.AC_APPARENT, False, does_not_raise()),
            (3, (1, 1, 1), PowerType.AC_APPARENT, False, pytest.raises(AssertionError)),
            (2, (2, 1, 1), PowerType.AC_APPARENT, False, pytest.raises(AssertionError)),
            (2, (-2, 1, 1), PowerType.AC_APPARENT, True, pytest.raises(AssertionError)),
            (4, (2, 1, 1), PowerType.AC_APPARENT, True, pytest.raises(AssertionError)),
            (0, (-2, 1, 1), PowerType.AC_APPARENT, True, pytest.raises(AssertionError)),
        ],
    )
    def test_init(
        self,
        value_total,
        values,
        power_type,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            p = Power(
                values=values,
                power_type=power_type,
            )
            assert p.is_symmetrical == is_symmetrical
            assert p.total == value_total


class TestReactivePower:
    def test_init(self) -> None:
        ReactivePower(values=(0, 0, 0))


class TestApparentPower:
    def test_init(self) -> None:
        ApparentPower(values=(0, 0, 0))


class TestActivePower:
    def test_init(self) -> None:
        ActivePower(values=(0, 0, 0))


class TestPowerFactor:
    @pytest.mark.parametrize(
        (
            "values",
            "is_symmetrical",
            "expectation",
        ),
        [
            ((0, 0, 0), True, does_not_raise()),
            ((1, 1, 1), True, does_not_raise()),
            ((0.9, 1, 1), False, does_not_raise()),
            ((1, 1, 1), False, pytest.raises(AssertionError)),
            ((1, 2, 1), False, pytest.raises(pydantic.ValidationError)),
            ((1, 2, 1), True, pytest.raises(pydantic.ValidationError)),
            ((1, -1, 1), True, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        values,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            pf = PowerFactor(values=values)
            assert pf.is_symmetrical == is_symmetrical
