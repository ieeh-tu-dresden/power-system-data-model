# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.quantities.single_phase import ActivePower
from psdm.quantities.single_phase import Admittance
from psdm.quantities.single_phase import ApparentPower
from psdm.quantities.single_phase import Current
from psdm.quantities.single_phase import Frequency
from psdm.quantities.single_phase import Impedance
from psdm.quantities.single_phase import ImpedanceNat
from psdm.quantities.single_phase import ImpedanceNegSeq
from psdm.quantities.single_phase import ImpedancePosSeq
from psdm.quantities.single_phase import ImpedanceZerSeq
from psdm.quantities.single_phase import Length
from psdm.quantities.single_phase import PhaseAngleClock
from psdm.quantities.single_phase import PowerFactor
from psdm.quantities.single_phase import PowerType
from psdm.quantities.single_phase import ReactivePower
from psdm.quantities.single_phase import SystemType
from psdm.quantities.single_phase import Voltage


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
            Frequency(value=value, system_type=SystemType.NATURAL)


class TestImpedance:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (-2, does_not_raise()),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            Impedance(value=value, system_type=SystemType.NATURAL)


class TestImpedancePosSeq:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (-2, does_not_raise()),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            i = ImpedancePosSeq(value=value)
            assert i.system_type == SystemType.POSITIVE_SEQUENCE.value


class TestImpedanceNegSeq:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (-2, does_not_raise()),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            i = ImpedanceNegSeq(value=value)
            assert i.system_type == SystemType.NEGATIVE_SEQUENCE.value


class TestImpedanceZerSeq:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (-2, does_not_raise()),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            i = ImpedanceZerSeq(value=value)
            assert i.system_type == SystemType.ZERO_SEQUENCE.value


class TestImpedanceNat:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (-2, does_not_raise()),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            i = ImpedanceNat(value=value)
            assert i.system_type == SystemType.NATURAL.value


class TestAdmittance:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (-2, does_not_raise()),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            Admittance(value=value, system_type=SystemType.NATURAL)


class TestLength:
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
            Length(value=value, system_type=SystemType.NATURAL)


class TestVoltage:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (-2, does_not_raise()),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            Voltage(value=value, system_type=SystemType.NATURAL)


class TestCurrent:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (-2, does_not_raise()),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            Current(value=value, system_type=SystemType.NATURAL)


class TestReactivePower:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (-2, does_not_raise()),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            p = ReactivePower(value=value, system_type=SystemType.NATURAL)
            assert p.power_type == PowerType.AC_REACTIVE.value


class TestApparentPower:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (-2, does_not_raise()),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            p = ApparentPower(value=value, system_type=SystemType.NATURAL)
            assert p.power_type == PowerType.AC_APPARENT.value


class TestActivePower:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (-2, does_not_raise()),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            p = ActivePower(value=value, system_type=SystemType.NATURAL)
            assert p.power_type == PowerType.AC_ACTIVE.value


class TestPhaseAngleClock:
    @pytest.mark.parametrize(
        (
            "value",
            "angle",
            "expectation",
        ),
        [
            (0, 0, does_not_raise()),
            (1, 30, does_not_raise()),
            (1.5, 45, does_not_raise()),
            (13, 390, pytest.raises(pydantic.ValidationError)),
            (-2, -60, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        value,
        angle,
        expectation,
    ) -> None:
        with expectation:
            p = PhaseAngleClock(value=value, system_type=SystemType.NATURAL)
            assert round(p.angle) == angle


class TestPowerFactor:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (0, does_not_raise()),
            (0.5, does_not_raise()),
            (1, does_not_raise()),
            (float("nan"), does_not_raise()),
            (-1, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            PowerFactor(value=value, system_type=SystemType.NATURAL)
