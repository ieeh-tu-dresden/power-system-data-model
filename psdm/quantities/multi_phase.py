# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum
import itertools
import math
import typing as t

import pydantic

from psdm.base import Base
from psdm.base import NonEmptyTuple
from psdm.base import UniqueNonEmptyTuple
from psdm.quantities.single_phase import PowerFactorDirection
from psdm.quantities.single_phase import PowerType
from psdm.quantities.single_phase import Precision
from psdm.quantities.single_phase import Quantity
from psdm.quantities.single_phase import SystemType
from psdm.quantities.single_phase import Unit

if t.TYPE_CHECKING:
    import collections.abc as cabc


class Phase(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    N = "N"
    E = "E"
    U = "U"
    V = "V"
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"


PhaseConnection = tuple[Phase, Phase] | None


class MultiPhaseQuantity(Quantity):
    """Base class for multi phase quantities like voltage, current, power or characteristic droops."""

    value: NonEmptyTuple[float]  # value (starting at first phase)
    system_type: SystemType = SystemType.NATURAL

    @pydantic.field_validator("system_type")
    def check_system_type(cls, v: SystemType) -> SystemType:
        if v is not SystemType.NATURAL.value:
            msg = "Input should be SystemType.NATURAL."
            raise ValueError(msg)

        return v

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def is_symmetrical(self) -> bool:
        return len(list(itertools.groupby(self.value))) in (0, 1)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def n_phases(self) -> int:
        return len(self.value)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def average(self) -> float:
        return round(sum(self.rounded) / self.n_phases, self.precision)

    def __len__(self) -> int:
        return self.n_phases

    @pydantic.field_serializer("value")
    def serialize_value(
        self,
        _value: pydantic.FieldSerializationInfo,
        _info: pydantic.FieldSerializationInfo,
    ) -> NonEmptyTuple[float]:
        return tuple(self.rounded)

    @property
    def rounded(self) -> cabc.Generator[float, None, None]:
        return (round(e, self.precision) for e in self.value)


class Voltage(MultiPhaseQuantity):
    """Electrical Voltage."""

    value: NonEmptyTuple[pydantic.confloat(ge=0)]  # type: ignore[valid-type]
    precision: int = Precision.VOLTAGE
    unit: Unit = Unit.VOLT

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.VOLT.value:
            msg = "Input should be Unit.VOLT."
            raise ValueError(msg)

        return v


class Current(MultiPhaseQuantity):
    """Electrical currents."""

    precision: int = Precision.CURRENT
    unit: Unit = Unit.AMPERE

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.AMPERE.value:
            msg = "Input should be Unit.AMPERE."
            raise ValueError(msg)

        return v


class Angle(MultiPhaseQuantity):
    """Angles of complex quantity."""

    value: NonEmptyTuple[pydantic.confloat(ge=0, le=360)]  # type: ignore[valid-type]
    precision: int = Precision.ANGLE
    unit: Unit = Unit.DEGREE

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.DEGREE.value:
            msg = "Input should be Unit.DEGREE."
            raise ValueError(msg)

        return v


class Droop(MultiPhaseQuantity):
    """Droops of characteristics curves."""

    precision: int = Precision.PU
    unit: Unit = Unit.UNITLESS

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.UNITLESS.value:
            msg = "Input should be Unit.UNITLESS."
            raise ValueError(msg)

        return v


class Impedance(MultiPhaseQuantity):
    """Natural impedance."""

    precision: int = Precision.IMPEDANCE
    unit: Unit = Unit.OHM

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.OHM.value:
            msg = "Input should be Unit.OHM."
            raise ValueError(msg)

        return v


class Admittance(MultiPhaseQuantity):
    """Natural admittance."""

    precision: int = Precision.ADMITTANCE
    unit: Unit = Unit.SIEMENS

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.SIEMENS.value:
            msg = "Input should be Unit.SIEMENS."
            raise ValueError(msg)

        return v


class Power(MultiPhaseQuantity):
    """Base class for power quantities.

    It comes with the computed property "total" that is the total power of all phases.
    This value should be used for symmetrical calculations.
    """

    power_type: PowerType
    precision: int = Precision.POWER
    unit: Unit = Unit.WATT

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v not in (Unit.WATT.value, Unit.VOLTAMPERE.value, Unit.VOLTAMPERE_REACTIVE.value):
            msg = "Input should be Unit.WATT, Unit.VOLTAMPERE or Unit.VOLTAMPERE_REACTIVE."
            raise ValueError(msg)

        return v

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def total(self) -> float:
        return round(sum(self.rounded), self.precision)


class ActivePower(Power):
    """Electrical active powers."""

    power_type: PowerType = PowerType.AC_ACTIVE
    unit: Unit = Unit.WATT

    @pydantic.field_validator("power_type")
    def check_power_type(cls, v: PowerType) -> PowerType:
        if v is not PowerType.AC_ACTIVE.value:
            msg = "Input should be PowerType.AC_ACTIVE."
            raise ValueError(msg)

        return v

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.WATT.value:
            msg = "Input should be Unit.WATT."
            raise ValueError(msg)

        return v


class ApparentPower(Power):
    """Electrical apparent powers."""

    power_type: PowerType = PowerType.AC_APPARENT
    unit: Unit = Unit.VOLTAMPERE

    @pydantic.field_validator("power_type")
    def check_power_type(cls, v: PowerType) -> PowerType:
        if v is not PowerType.AC_APPARENT.value:
            msg = "Input should be PowerType.AC_APPARENT."
            raise ValueError(msg)

        return v

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.VOLTAMPERE.value:
            msg = "Input should be Unit.VOLTAMPERE."
            raise ValueError(msg)

        return v


class ReactivePower(Power):
    """Electrical reactive powers."""

    power_type: PowerType = PowerType.AC_REACTIVE
    unit: Unit = Unit.VOLTAMPERE_REACTIVE

    @pydantic.field_validator("power_type")
    def check_power_type(cls, v: PowerType) -> PowerType:
        if v is not PowerType.AC_REACTIVE.value:
            msg = "Input should be PowerType.AC_REACTIVE."
            raise ValueError(msg)

        return v

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.VOLTAMPERE_REACTIVE.value:
            msg = "Input should be Unit.VOLTAMPERE_REACTIVE."
            raise ValueError(msg)

        return v


class PowerFactor(MultiPhaseQuantity):
    """Power factors, e.g. cos(phi), tan(phi)."""

    value: NonEmptyTuple[float]
    direction: PowerFactorDirection = PowerFactorDirection.ND
    precision: int = Precision.POWERFACTOR
    unit: Unit = Unit.UNITLESS

    @pydantic.field_validator("value")
    def check_value(cls, value: NonEmptyTuple[float]) -> NonEmptyTuple[float]:
        for v in value:
            if not math.isnan(v) and v < 0:
                msg = "Input should be greater than 0."
                raise ValueError(msg)

        return value

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.UNITLESS.value:
            msg = "Input should be Unit.UNITLESS."
            raise ValueError(msg)

        return v

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def average(self) -> float:
        if not self.is_symmetrical:
            return float("nan")

        return round(sum(self.rounded) / self.n_phases, self.precision)


class CosPhi(PowerFactor):
    @pydantic.field_validator("value")
    def check_value(cls, value: NonEmptyTuple[float]) -> NonEmptyTuple[float]:
        for v in value:
            if not math.isnan(v) and not (0 <= v <= 1):
                msg = "Input should be between 0 and 1."
                raise ValueError(msg)

        return value

    def weighted_average(self, power: Power) -> float:
        """Calculate the weighted average power factor depending of the power type of the provided power."""
        match power.power_type:
            case PowerType.AC_ACTIVE.value:
                return round(
                    power.total / sum(pw / cp for pw, cp in zip(power.value, self.value, strict=True)),
                    self.precision,
                )
            case PowerType.AC_APPARENT.value:
                return round(
                    sum(pw * cp for pw, cp in zip(power.value, self.value, strict=True)) / power.total,
                    self.precision,
                )
            case PowerType.AC_REACTIVE.value:
                return round(
                    sum(pw / math.tan(math.acos(cp)) for pw, cp in zip(power.value, self.value, strict=True))
                    / sum(pw / math.sin(math.acos(cp)) for pw, cp in zip(power.value, self.value, strict=True)),
                    self.precision,
                )
            case _:
                return float("nan")


class TanPhi(PowerFactor):
    def weighted_average(self, power: Power) -> float:
        """Calculate the weighted average power factor depending of the power type of the provided power."""
        match power.power_type:
            case PowerType.AC_ACTIVE.value:
                return round(
                    sum(pw * tp for pw, tp in zip(power.value, self.value, strict=True)) / power.total,
                    self.precision,
                )
            case PowerType.AC_APPARENT.value:
                return round(
                    sum(pw * math.sin(math.atan(cp)) for pw, cp in zip(power.value, self.value, strict=True))
                    / sum(pw * math.cos(math.atan(cp)) for pw, cp in zip(power.value, self.value, strict=True)),
                    self.precision,
                )
            case PowerType.AC_REACTIVE.value:
                return round(
                    power.total / sum(pw / tp for pw, tp in zip(power.value, self.value, strict=True)),
                    self.precision,
                )
            case _:
                return float("nan")


class PhaseConnections(Base):
    """Phases between which elements are connected, e.g. [(A,E). (B,E). (C,E)], [(A,B), (B,C), (C,A)]."""

    value: UniqueNonEmptyTuple[PhaseConnection]

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def n_phases(self) -> int:
        return len(self.value)

    def __len__(self) -> int:
        return self.n_phases
