# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.quantities.multi_phase import ActivePower
from psdm.quantities.multi_phase import Angle
from psdm.quantities.multi_phase import ApparentPower
from psdm.quantities.multi_phase import CosPhi
from psdm.quantities.multi_phase import Current
from psdm.quantities.multi_phase import Droop
from psdm.quantities.multi_phase import Impedance
from psdm.quantities.multi_phase import Phase
from psdm.quantities.multi_phase import PhaseConnections
from psdm.quantities.multi_phase import Power
from psdm.quantities.multi_phase import PowerFactor
from psdm.quantities.multi_phase import ReactivePower
from psdm.quantities.multi_phase import Voltage
from psdm.quantities.single_phase import PowerType
from psdm.quantities.single_phase import SystemType
from psdm.quantities.single_phase import Unit

N_PHASES = 3


class TestVoltage:
    @pytest.mark.parametrize(
        (
            "value",
            "is_symmetrical",
            "expectation",
        ),
        [
            ((0, 0, 0), True, does_not_raise()),
            ((1, 1, 1), True, does_not_raise()),
            ((2, 1, 1), False, does_not_raise()),
            ((1, 1, 1), False, pytest.raises(AssertionError)),
            ((-2, 1, 1), True, pytest.raises(pydantic.ValidationError)),
            ((-2, 1, 1), False, pytest.raises(pydantic.ValidationError)),
            ((2, 1, 1), True, pytest.raises(AssertionError)),
        ],
    )
    def test_init(
        self,
        value,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            v = Voltage(value=value, system_type=SystemType.NATURAL)
            assert v.is_symmetrical == is_symmetrical
            assert v.n_phases == N_PHASES
            assert len(v) == N_PHASES


class TestCurrent:
    @pytest.mark.parametrize(
        (
            "value",
            "is_symmetrical",
            "expectation",
        ),
        [
            ((0, 0, 0), True, does_not_raise()),
            ((1, 1, 1), True, does_not_raise()),
            ((2, 1, 1), False, does_not_raise()),
            ((1, 1, 1), False, pytest.raises(AssertionError)),
            ((-2, 1, 1), True, pytest.raises(AssertionError)),
            ((-2, 1, 1), False, does_not_raise()),
            ((2, 1, 1), True, pytest.raises(AssertionError)),
        ],
    )
    def test_init(
        self,
        value,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            c = Current(value=value, system_type=SystemType.NATURAL)
            assert c.is_symmetrical == is_symmetrical


class TestAngle:
    @pytest.mark.parametrize(
        (
            "value",
            "is_symmetrical",
            "expectation",
        ),
        [
            ((0, 0, 0), True, does_not_raise()),
            ((1, 1, 1), True, does_not_raise()),
            ((2, 1, 1), False, does_not_raise()),
            ((1, 1, 1), False, pytest.raises(AssertionError)),
            ((-2, 1, 1), True, pytest.raises(pydantic.ValidationError)),
            ((-2, 1, 1), False, pytest.raises(pydantic.ValidationError)),
            ((361, 1, 1), False, pytest.raises(pydantic.ValidationError)),
            ((2, 1, 1), True, pytest.raises(AssertionError)),
        ],
    )
    def test_init(
        self,
        value,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            a = Angle(value=value, system_type=SystemType.NATURAL)
            assert a.is_symmetrical == is_symmetrical


class TestDroop:
    @pytest.mark.parametrize(
        (
            "value",
            "is_symmetrical",
            "expectation",
        ),
        [
            ((0, 0, 0), True, does_not_raise()),
            ((1, 1, 1), True, does_not_raise()),
            ((2, 1, 1), False, does_not_raise()),
            ((1, 1, 1), False, pytest.raises(AssertionError)),
            ((-2, 1, 1), True, pytest.raises(AssertionError)),
            ((-2, 1, 1), False, does_not_raise()),
            ((2, 1, 1), True, pytest.raises(AssertionError)),
        ],
    )
    def test_init(
        self,
        value,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            d = Droop(value=value, system_type=SystemType.NATURAL)
            assert d.is_symmetrical == is_symmetrical


class TestImpedance:
    @pytest.mark.parametrize(
        (
            "value",
            "is_symmetrical",
            "expectation",
        ),
        [
            ((0, 0, 0), True, does_not_raise()),
            ((1, 1, 1), True, does_not_raise()),
            ((2, 1, 1), False, does_not_raise()),
            ((-2, 1, 1), False, does_not_raise()),
            ((1, 1, 1), False, pytest.raises(AssertionError)),
            ((-2, 1, 1), True, pytest.raises(AssertionError)),
            ((2, 1, 1), True, pytest.raises(AssertionError)),
        ],
    )
    def test_init(
        self,
        value,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            i = Impedance(value=value, system_type=SystemType.NATURAL)
            assert i.is_symmetrical == is_symmetrical
            assert i.system_type == SystemType.NATURAL.value


class TestPower:
    @pytest.mark.parametrize(
        (
            "value_total",
            "value",
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
        value,
        power_type,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            p = Power(
                value=value,
                power_type=power_type,
                system_type=SystemType.NATURAL,
                unit=Unit.VOLTAMPERE,
            )
            assert p.is_symmetrical == is_symmetrical
            assert p.total == value_total


class TestReactivePower:
    def test_init(self) -> None:
        p = ReactivePower(value=(0, 0, 0), system_type=SystemType.NATURAL)
        assert p.power_type == PowerType.AC_REACTIVE.value


class TestApparentPower:
    def test_init(self) -> None:
        p = ApparentPower(value=(0, 0, 0), system_type=SystemType.NATURAL)
        assert p.power_type == PowerType.AC_APPARENT.value


class TestActivePower:
    def test_init(self) -> None:
        p = ActivePower(value=(0, 0, 0), system_type=SystemType.NATURAL)
        assert p.power_type == PowerType.AC_ACTIVE.value


class TestPowerFactor:
    @pytest.mark.parametrize(
        (
            "value",
            "is_symmetrical",
            "expectation",
        ),
        [
            ((0, 0, 0), True, does_not_raise()),
            ((1, 1, 1), True, does_not_raise()),
            ((0.9, 1, 1), False, does_not_raise()),
            ((float("nan"), float("nan"), float("nan")), False, does_not_raise()),
            ((1, float("nan"), 1), False, does_not_raise()),
            ((1, float("nan"), 1), True, pytest.raises(AssertionError)),
            ((1, 1, 1), False, pytest.raises(AssertionError)),
            ((1, 0.9, 1), True, pytest.raises(AssertionError)),
            ((1, -1, 1), True, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        value,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            pf = PowerFactor(value=value, system_type=SystemType.NATURAL)
            assert pf.is_symmetrical == is_symmetrical
            assert len(pf) == N_PHASES


class TestCosPhi:
    @pytest.mark.parametrize(
        (
            "value",
            "is_symmetrical",
            "expectation",
        ),
        [
            ((1, 1.1, 1), False, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        value,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            pf = CosPhi(value=value, system_type=SystemType.NATURAL)
            assert pf.is_symmetrical == is_symmetrical
            assert len(pf) == N_PHASES


class TestPhaseConnections:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [(((Phase.A, Phase.B), (Phase.B, Phase.C), (Phase.C, Phase.A)), does_not_raise())],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            pf = PhaseConnections(value=value, system_type=SystemType.NATURAL)
            assert len(pf) == N_PHASES
