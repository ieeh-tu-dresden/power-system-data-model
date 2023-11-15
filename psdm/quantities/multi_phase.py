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
from psdm.base import UniqueNonEmptyTuple
from psdm.base import model_validator_before
from psdm.quantities.single_phase import PowerFactorDirection
from psdm.quantities.single_phase import PowerType
from psdm.quantities.single_phase import Quantity
from psdm.quantities.single_phase import SystemType


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


def find_decimals(value: float) -> int:
    return len(([*str(value).split("."), ""])[1])


def round_avg(qty: MultiPhaseQuantity) -> float:
    return round(sum(qty.value) / qty.n_phases, find_decimals(qty.value[0]))


class MultiPhaseQuantity(Quantity):
    """Base class for multi phase quantities like voltage, current, power or charcteristic droops."""

    value: NonEmptyTuple[float]  # value (starting at first phase)

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
        return round_avg(self)

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


class Current(MultiPhaseQuantity):
    """Electrical currents."""


class Angle(MultiPhaseQuantity):
    """Angles of complex quantity."""

    value: NonEmptyTuple[pydantic.confloat(ge=0, le=360)]  # type: ignore[valid-type]


class Droop(MultiPhaseQuantity):
    """Droops of characteristics curves."""


class Impedance(MultiPhaseQuantity):
    """Natural impedance."""

    value: NonEmptyTuple[pydantic.confloat(ge=0)]  # type: ignore[valid-type]
    system_type: SystemType = SystemType.NATURAL

    @model_validator_before
    def set_system_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["system_type"] = SystemType.NATURAL.value
        return value


class Power(MultiPhaseQuantity):
    """Base class for power quantities.

    It comes with the computed property "total" that is the total power of all phases.
    This value should be used for symmetrical calculations.
    """

    power_type: PowerType

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def total(self) -> float:
        return round(sum(self.value), find_decimals(self.value[0]))


class ActivePower(Power):
    """Electrical active powers."""

    power_type: PowerType = PowerType.AC_ACTIVE

    @model_validator_before
    def set_power_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["power_type"] = PowerType.AC_ACTIVE.value
        return value


class ApparentPower(Power):
    """Electrical apparent powers."""

    power_type: PowerType = PowerType.AC_APPARENT

    @model_validator_before
    def set_power_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["power_type"] = PowerType.AC_APPARENT.value
        return value


class ReactivePower(Power):
    """Electrical reactive powers."""

    power_type: PowerType = PowerType.AC_REACTIVE

    @model_validator_before
    def set_power_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["power_type"] = PowerType.AC_REACTIVE.value
        return value


class PowerFactor(Base):
    """Power factors, e.g. cos(phi), tan(phi)."""

    value: NonEmptyTuple[pydantic.confloat(ge=0, le=1)]  # type: ignore[valid-type]
    direction: PowerFactorDirection = PowerFactorDirection.ND

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def is_symmetrical(self) -> bool:
        return len(list(itertools.groupby(self.value))) in (0, 1)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def n_phases(self) -> int:
        return len(self.value)

    def __len__(self) -> int:
        return self.n_phases


class PhaseConnections(Base):
    """Phases between which elements are connected, e.g. [(A,E). (B,E). (C,E)], [(A,B), (B,C), (C,A)]."""

    value: UniqueNonEmptyTuple[PhaseConnection]

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def n_phases(self) -> int:
        return len(self.value)

    def __len__(self) -> int:
        return self.n_phases
