# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum
import itertools
import typing as t

import pydantic

from psdm.base import Base
from psdm.base import NonEmptyTuple
from psdm.base import UniqueTuple
from psdm.base import model_validator_before


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


class PowerType(enum.Enum):
    AC_ACTIVE = "AC_ACTIVE"
    AC_APPARENT = "AC_APPARENT"
    AC_REACTIVE = "AC_REACTIVE"
    CURRENT = "CURRENT"
    DC = "DC"
    GAS = "GAS"
    IMPEDANCE = "IMPEDANCE"
    MECHANICAL = "MECHANICAL"
    THERMAL = "THERMAL"


class PowerFactorDirection(enum.Enum):
    UE = "UE"
    OE = "OE"
    ND = "ND"


PhaseConnection = tuple[Phase, Phase] | None


def find_decimals(value: float) -> int:
    return len(([*str(value).split("."), ""])[1])


def round_avg(qty: MultiPhaseQuantity) -> float:
    return round(sum(qty.values) / qty.n_phases, find_decimals(qty.values[0]))  # noqa: PD011


class Frequency(Base):
    value: float = pydantic.Field(..., ge=0)  # voltage (three-phase)


class Impedance(Base):
    value: float = pydantic.Field(..., ge=0)  # resistance


class Admittance(Base):
    value: float = pydantic.Field(..., ge=0)  # admittance


class Length(Base):
    value: float = pydantic.Field(..., ge=0)  # length


class PhaseAngleClock(Base):
    value: float = pydantic.Field(..., ge=0, lt=12)  # admittance

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def angle(self) -> float:
        return self.value * 30.0


class MultiPhaseQuantity(Base):
    """Base class for multi phase quantities like voltage, current, power or charcteristic droops."""

    values: NonEmptyTuple[float]  # values (starting at phase a)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def is_symmetrical(self) -> bool:
        return len(list(itertools.groupby(self.values))) in (0, 1)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def n_phases(self) -> int:
        return len(self.values)

    def __len__(self) -> int:
        return self.n_phases


class Voltage(MultiPhaseQuantity):
    values: NonEmptyTuple[pydantic.confloat(ge=0)]  # type: ignore[valid-type]  # values (starting at phase a)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def average(self) -> float:
        return round_avg(self)


class Current(MultiPhaseQuantity):
    @pydantic.computed_field  # type: ignore[misc]
    @property
    def average(self) -> float:
        return round_avg(self)


class Angle(MultiPhaseQuantity):
    values: NonEmptyTuple[pydantic.confloat(ge=0, le=360)]  # type: ignore[valid-type]  # values (starting at phase a)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def average(self) -> float:
        return round_avg(self)


class Droop(MultiPhaseQuantity):
    @pydantic.computed_field  # type: ignore[misc]
    @property
    def average(self) -> float:
        return round_avg(self)


class Power(MultiPhaseQuantity):
    """Base class for power quantities.

    It comes with the computed property "total" that is the total power of all phases.
    This value should be used for symmetrical calculations.
    """

    power_type: PowerType

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def total(self) -> float:
        return round(sum(self.values), find_decimals(self.values[0]))


class ActivePower(Power):
    power_type: PowerType = PowerType.AC_ACTIVE

    @model_validator_before
    def set_power_type(cls, values: dict[str, t.Any]) -> dict[str, t.Any]:
        values["power_type"] = PowerType.AC_ACTIVE.value
        return values


class ApparentPower(Power):
    power_type: PowerType = PowerType.AC_APPARENT

    @model_validator_before
    def set_power_type(cls, values: dict[str, t.Any]) -> dict[str, t.Any]:
        values["power_type"] = PowerType.AC_APPARENT.value
        return values


class ReactivePower(Power):
    power_type: PowerType = PowerType.AC_REACTIVE

    @model_validator_before
    def set_power_type(cls, values: dict[str, t.Any]) -> dict[str, t.Any]:
        values["power_type"] = PowerType.AC_REACTIVE.value
        return values


class PowerFactor(MultiPhaseQuantity):
    values: NonEmptyTuple[pydantic.confloat(ge=0, le=1)]  # type: ignore[valid-type] # values (starting at phase a)
    direction: PowerFactorDirection = PowerFactorDirection.ND

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def average(self) -> float:
        return round_avg(self)


class PhaseConnections(Base):
    values: UniqueTuple[PhaseConnection]

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def n_phases(self) -> int:
        return len(self.values)
