# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum
import typing as t

import pydantic

from psdm.base import Base
from psdm.base import model_validator_before


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


class SystemType(enum.Enum):
    POSITIVE_SEQUENCE = "POSITIVE_SEQUENCE"
    NEGATIVE_SEQUENCE = "NEGATIVE_SEQUENCE"
    ZERO_SEQUENCE = "ZERO_SEQUENCE"
    NATURAL = "NATURAL"


class PowerFactorDirection(enum.Enum):
    UE = "UE"
    OE = "OE"
    ND = "ND"


class Quantity(Base):
    system_type: SystemType


class SinglePhaseQuantity(Quantity):
    value: float


class Frequency(SinglePhaseQuantity):
    """Frequency."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]


class Impedance(SinglePhaseQuantity):
    """Impedance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]


class ImpedancePosSeq(SinglePhaseQuantity):
    """Positive sequence impedance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.POSITIVE_SEQUENCE

    @model_validator_before
    def set_system_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["system_type"] = SystemType.POSITIVE_SEQUENCE.value
        return value


class ImpedanceNegSeq(SinglePhaseQuantity):
    """Negative sequence impedance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.NEGATIVE_SEQUENCE

    @model_validator_before
    def set_system_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["system_type"] = SystemType.NEGATIVE_SEQUENCE.value
        return value


class ImpedanceZerSeq(SinglePhaseQuantity):
    """Zero sequence impedance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.ZERO_SEQUENCE

    @model_validator_before
    def set_system_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["system_type"] = SystemType.ZERO_SEQUENCE.value
        return value


class ImpedanceNat(SinglePhaseQuantity):
    """Natural impedance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.NATURAL

    @model_validator_before
    def set_system_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["system_type"] = SystemType.NATURAL.value
        return value


class Admittance(SinglePhaseQuantity):
    """Admittance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]


class Length(SinglePhaseQuantity):
    """Length."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]


class Voltage(SinglePhaseQuantity):
    """Electrical Voltage."""


class Current(SinglePhaseQuantity):
    """Electrical current."""


class Angle(SinglePhaseQuantity):
    """Angle of complex quantity."""

    value: pydantic.confloat(ge=0, le=360)  # type: ignore[valid-type]


class Droop(SinglePhaseQuantity):
    """Droop of characteristics curves."""


class Power(SinglePhaseQuantity):
    """Base class for power quantities."""

    power_type: PowerType


class ActivePower(Power):
    """Electrical active power."""

    power_type: PowerType = PowerType.AC_ACTIVE

    @model_validator_before
    def set_power_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["power_type"] = PowerType.AC_ACTIVE.value
        return value


class ApparentPower(Power):
    """Electrical apparent power."""

    power_type: PowerType = PowerType.AC_APPARENT

    @model_validator_before
    def set_power_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["power_type"] = PowerType.AC_APPARENT.value
        return value


class ReactivePower(Power):
    """Electrical reactive power."""

    power_type: PowerType = PowerType.AC_REACTIVE

    @model_validator_before
    def set_power_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["power_type"] = PowerType.AC_REACTIVE.value
        return value


class PowerFactor(Quantity):
    """Power factor, e.g. cos(phi), tan(phi)."""

    value: pydantic.confloat(ge=0, le=1)  # type: ignore[valid-type]
    direction: PowerFactorDirection = PowerFactorDirection.ND


class PhaseAngleClock(Quantity):
    """Phase shift between two windings in multiples of 30°."""

    value: pydantic.confloat(ge=0, lt=12)  # type: ignore[valid-type]

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def angle(self) -> float:
        return self.value * 30.0
