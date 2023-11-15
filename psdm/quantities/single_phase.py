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
    POSITIVE_NEGATIVE_COUPLING = "POSITIVE_NEGATIVE_COUPLING"
    NEGATIVE_ZERO_COUPLING = "NEGATIVE_ZERO_COUPLING"
    ZERO_POSITIVE_COUPLING = "ZERO_POSITIVE_COUPLING"


class PowerFactorDirection(enum.Enum):
    UE = "UE"
    OE = "OE"
    ND = "ND"


class Unit(enum.Enum):
    WATT = "WATT"
    VOLT = "VOLT"
    AMPERE = "AMPERE"
    HERTZ = "HERTZ"
    OHM = "OHM"
    SIEMENS = "SIEMENS"
    METER = "METER"
    DEGREE = "DEGREE"
    PERCENT = "PERCENT"
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"
    KELVIN = "KELVIN"
    UNITLESS = "UNITLESS"


class Quantity(Base):
    system_type: SystemType
    precision: int = pydantic.Field(exclude=True)
    unit: Unit


class SinglePhaseQuantity(Quantity):
    value: float

    @pydantic.field_serializer("value")
    def serialize_value(self, value: float, _info: pydantic.FieldSerializationInfo) -> float:
        return round(value, self.precision)


class Frequency(SinglePhaseQuantity):
    """Frequency."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    precision: int = 3
    unit: Unit = Unit.HERTZ

    @model_validator_before
    def set_unit(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["unit"] = Unit.HERTZ.value
        return value


class Impedance(SinglePhaseQuantity):
    """Impedance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]

    @model_validator_before
    def set_unit(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["unit"] = Unit.OHM.value
        return value

    @model_validator_before
    def set_precision(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["precision"] = 6
        return value


class ImpedancePosSeq(Impedance):
    """Positive sequence impedance."""

    system_type: SystemType = SystemType.POSITIVE_SEQUENCE

    @model_validator_before
    def set_system_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["system_type"] = SystemType.POSITIVE_SEQUENCE.value
        return value


class ImpedanceNegSeq(Impedance):
    """Negative sequence impedance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.NEGATIVE_SEQUENCE

    @model_validator_before
    def set_system_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["system_type"] = SystemType.NEGATIVE_SEQUENCE.value
        return value


class ImpedanceZerSeq(Impedance):
    """Zero sequence impedance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.ZERO_SEQUENCE

    @model_validator_before
    def set_system_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["system_type"] = SystemType.ZERO_SEQUENCE.value
        return value


class ImpedanceNat(Impedance):
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


class AdmittancePosSeq(Admittance):
    """Positive sequence admittance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.POSITIVE_SEQUENCE

    @model_validator_before
    def set_system_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["system_type"] = SystemType.POSITIVE_SEQUENCE.value
        return value


class AdmittanceNegSeq(Admittance):
    """Negative sequence admittance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.NEGATIVE_SEQUENCE

    @model_validator_before
    def set_system_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["system_type"] = SystemType.NEGATIVE_SEQUENCE.value
        return value


class AdmittanceZerSeq(Admittance):
    """Zero sequence admittance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.ZERO_SEQUENCE

    @model_validator_before
    def set_system_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["system_type"] = SystemType.ZERO_SEQUENCE.value
        return value


class AdmittanceNat(Admittance):
    """Natural admittance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.NATURAL

    @model_validator_before
    def set_system_type(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        value["system_type"] = SystemType.NATURAL.value
        return value


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


class PowerFactor(Base):
    """Power factor, e.g. cos(phi), tan(phi)."""

    value: pydantic.confloat(ge=0, le=1)  # type: ignore[valid-type]
    direction: PowerFactorDirection = PowerFactorDirection.ND


class PhaseAngleClock(Base):
    """Phase shift between two windings in multiples of 30°."""

    value: pydantic.confloat(ge=0, lt=12)  # type: ignore[valid-type]

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def angle(self) -> float:
        return self.value * 30.0
