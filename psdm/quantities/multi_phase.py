# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum
import itertools
import math

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
            msg = "Only SystemType.NATURAL is supported."
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
        return round(sum(self.value) / self.n_phases, self.precision)

    def __len__(self) -> int:
        return self.n_phases

    @pydantic.field_serializer("value")
    def serialize_value(
        self,
        value: NonEmptyTuple[float],
        _info: pydantic.FieldSerializationInfo,
    ) -> NonEmptyTuple[float]:
        return tuple(round(e, self.precision) for e in value)


class Voltage(MultiPhaseQuantity):
    """Electrical Voltage."""

    value: NonEmptyTuple[pydantic.confloat(ge=0)]  # type: ignore[valid-type]
    precision: int = Precision.VOLTAGE
    unit: Unit = Unit.VOLT


class Current(MultiPhaseQuantity):
    """Electrical currents."""

    precision: int = Precision.CURRENT
    unit: Unit = Unit.AMPERE


class Angle(MultiPhaseQuantity):
    """Angles of complex quantity."""

    value: NonEmptyTuple[pydantic.confloat(ge=0, le=360)]  # type: ignore[valid-type]
    precision: int = Precision.ANGLE
    unit: Unit = Unit.DEGREE


class Droop(MultiPhaseQuantity):
    """Droops of characteristics curves."""

    precision: int = Precision.PU
    unit: Unit = Unit.UNITLESS


class Impedance(MultiPhaseQuantity):
    """Natural impedance."""

    value: NonEmptyTuple[pydantic.confloat(ge=0)]  # type: ignore[valid-type]

    precision: int = Precision.IMPEDANCE
    unit: Unit = Unit.OHM


class Power(MultiPhaseQuantity):
    """Base class for power quantities.

    It comes with the computed property "total" that is the total power of all phases.
    This value should be used for symmetrical calculations.
    """

    power_type: PowerType
    precision: int = Precision.POWER

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def total(self) -> float:
        return round(sum(self.value), self.precision)


class ActivePower(Power):
    """Electrical active powers."""

    power_type: PowerType = PowerType.AC_ACTIVE
    unit: Unit = Unit.WATT

    @pydantic.field_validator("power_type")
    def check_power_type(cls, v: PowerType) -> PowerType:
        if v is not PowerType.AC_ACTIVE.value:
            msg = "Only PowerType.AC_ACTIVE is supported."
            raise ValueError(msg)

        return v

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.WATT.value:
            msg = "Only Unit.WATT is supported."
            raise ValueError(msg)

        return v


class ApparentPower(Power):
    """Electrical apparent powers."""

    power_type: PowerType = PowerType.AC_APPARENT
    unit: Unit = Unit.VOLT_AMPERE

    @pydantic.field_validator("power_type")
    def check_power_type(cls, v: PowerType) -> PowerType:
        if v is not PowerType.AC_APPARENT.value:
            msg = "Only PowerType.AC_APPARENT is supported."
            raise ValueError(msg)

        return v

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.VOLT_AMPERE.value:
            msg = "Only Unit.VOLT_AMPERE is supported."
            raise ValueError(msg)

        return v


class ReactivePower(Power):
    """Electrical reactive powers."""

    power_type: PowerType = PowerType.AC_REACTIVE
    unit: Unit = Unit.VOLTAMPERE_REACTIVE

    @pydantic.field_validator("power_type")
    def check_power_type(cls, v: PowerType) -> PowerType:
        if v is not PowerType.AC_REACTIVE.value:
            msg = "Only PowerType.AC_REACTIVE is supported."
            raise ValueError(msg)

        return v

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.VOLTAMPERE_REACTIVE.value:
            msg = "Only Unit.VOLTAMPERE_REACTIVE is supported."
            raise ValueError(msg)

        return v


class PowerFactor(MultiPhaseQuantity):
    """Power factors, e.g. cos(phi), tan(phi)."""

    value: NonEmptyTuple[pydantic.confloat(ge=0)]  # type: ignore[valid-type]
    direction: PowerFactorDirection = PowerFactorDirection.ND
    precision: int = Precision.POWERFACTOR
    unit: Unit = Unit.UNITLESS

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.UNITLESS.value:
            msg = "Only Unit.UNITLESS is supported."
            raise ValueError(msg)

        return v


class CosPhi(PowerFactor):
    value: NonEmptyTuple[pydantic.confloat(ge=0, le=1)]  # type: ignore[valid-type]

    def weighted_average(self, power: Power) -> pydantic.confloat(ge=0, le=1):  # type: ignore[valid-type]
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
    value: NonEmptyTuple[pydantic.confloat(ge=0)]  # type: ignore[valid-type]

    def weighted_average(self, power: Power) -> pydantic.confloat(ge=0):  # type: ignore[valid-type]
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
