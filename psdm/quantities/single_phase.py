# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum
import math

import pydantic

from psdm.base import Base


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
    UE = "UE"  # under excited
    OE = "OE"  # over excited
    ND = "ND"  # not defined


class Unit(enum.Enum):
    AMPERE = "AMPERE"
    DAY = "DAY"
    DEGREE = "DEGREE"
    HERTZ = "HERTZ"
    HOUR = "HOUR"
    KELVIN = "KELVIN"
    METER = "METER"
    MINUTE = "MINUTE"
    OHM = "OHM"
    VOLT = "VOLT"
    VOLTAMPERE = "VA"
    VOLTAMPERE_REACTIVE = "VAR"
    WATT = "WATT"
    PERCENT = "PERCENT"
    SECOND = "SECOND"
    SIEMENS = "SIEMENS"
    UNITLESS = "UNITLESS"


class Precision:
    """Count of decimal digits."""

    ADMITTANCE: int = 13
    ANGLE: int = 5
    CURRENT: int = 2
    FREQUENCY: int = 4
    IMPEDANCE: int = 7
    LENGTH: int = 0
    POWER: int = 1
    POWERFACTOR: int = 7
    PU: int = 5
    VOLTAGE: int = 2


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

    system_type: SystemType = SystemType.NATURAL
    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    precision: int = Precision.FREQUENCY
    unit: Unit = Unit.HERTZ

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.HERTZ.value:
            msg = "Input should be Unit.HERTZ."
            raise ValueError(msg)

        return v


class Impedance(SinglePhaseQuantity):
    """Impedance."""

    system_type: SystemType = SystemType.NATURAL
    precision: int = Precision.IMPEDANCE
    unit: Unit = Unit.OHM

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.OHM.value:
            msg = "Input should be Unit.OHM."
            raise ValueError(msg)

        return v


class ImpedancePosSeq(Impedance):
    """Positive sequence impedance."""

    system_type: SystemType = SystemType.POSITIVE_SEQUENCE

    @pydantic.field_validator("system_type")
    def check_system_type(cls, v: SystemType) -> SystemType:
        if v is not SystemType.POSITIVE_SEQUENCE.value:
            msg = "Input should be SystemType.POSITIVE_SEQUENCE."
            raise ValueError(msg)

        return v


class ImpedanceNegSeq(Impedance):
    """Negative sequence impedance."""

    system_type: SystemType = SystemType.NEGATIVE_SEQUENCE

    @pydantic.field_validator("system_type")
    def check_system_type(cls, v: SystemType) -> SystemType:
        if v is not SystemType.NEGATIVE_SEQUENCE.value:
            msg = "Input should be SystemType.NEGATIVE_SEQUENCE."
            raise ValueError(msg)

        return v


class ImpedanceZerSeq(Impedance):
    """Zero sequence impedance."""

    system_type: SystemType = SystemType.ZERO_SEQUENCE

    @pydantic.field_validator("system_type")
    def check_system_type(cls, v: SystemType) -> SystemType:
        if v is not SystemType.ZERO_SEQUENCE.value:
            msg = "Input should be SystemType.ZERO_SEQUENCE."
            raise ValueError(msg)

        return v


class ImpedanceNat(Impedance):
    """Natural impedance."""

    system_type: SystemType = SystemType.NATURAL

    @pydantic.field_validator("system_type")
    def check_system_type(cls, v: SystemType) -> SystemType:
        if v is not SystemType.NATURAL.value:
            msg = "Input should be SystemType.NATURAL."
            raise ValueError(msg)

        return v


class Admittance(SinglePhaseQuantity):
    """Admittance."""

    precision: int = Precision.ADMITTANCE
    unit: Unit = Unit.SIEMENS

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.SIEMENS.value:
            msg = "Input should be Unit.SIEMENS."
            raise ValueError(msg)

        return v


class AdmittancePosSeq(Admittance):
    """Positive sequence admittance."""

    system_type: SystemType = SystemType.POSITIVE_SEQUENCE

    @pydantic.field_validator("system_type")
    def check_system_type(cls, v: SystemType) -> SystemType:
        if v is not SystemType.POSITIVE_SEQUENCE.value:
            msg = "Input should be SystemType.POSITIVE_SEQUENCE."
            raise ValueError(msg)

        return v


class AdmittanceNegSeq(Admittance):
    """Negative sequence admittance."""

    system_type: SystemType = SystemType.NEGATIVE_SEQUENCE

    @pydantic.field_validator("system_type")
    def check_system_type(cls, v: SystemType) -> SystemType:
        if v is not SystemType.NEGATIVE_SEQUENCE.value:
            msg = "Input should be SystemType.NEGATIVE_SEQUENCE."
            raise ValueError(msg)

        return v


class AdmittanceZerSeq(Admittance):
    """Zero sequence admittance."""

    system_type: SystemType = SystemType.ZERO_SEQUENCE

    @pydantic.field_validator("system_type")
    def check_system_type(cls, v: SystemType) -> SystemType:
        if v is not SystemType.ZERO_SEQUENCE.value:
            msg = "Input should be SystemType.ZERO_SEQUENCE."
            raise ValueError(msg)

        return v


class AdmittanceNat(Admittance):
    """Natural admittance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.NATURAL

    @pydantic.field_validator("system_type")
    def check_system_type(cls, v: SystemType) -> SystemType:
        if v is not SystemType.NATURAL.value:
            msg = "Input should be SystemType.NATURAL."
            raise ValueError(msg)

        return v


class Length(SinglePhaseQuantity):
    """Length."""

    system_type: SystemType = SystemType.NATURAL
    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    precision: int = Precision.LENGTH
    unit: Unit = Unit.METER

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.METER.value:
            msg = "Input should be Unit.METER."
            raise ValueError(msg)

        return v


class Voltage(SinglePhaseQuantity):
    """Electrical Voltage."""

    precision: int = Precision.VOLTAGE
    unit: Unit = Unit.VOLT

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.VOLT.value:
            msg = "Input should be Unit.VOLT."
            raise ValueError(msg)

        return v


class Current(SinglePhaseQuantity):
    """Electrical current."""

    precision: int = Precision.CURRENT
    unit: Unit = Unit.AMPERE

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.AMPERE.value:
            msg = "Input should be Unit.AMPERE."
            raise ValueError(msg)

        return v


class Angle(SinglePhaseQuantity):
    """Angle of complex quantity."""

    value: pydantic.confloat(ge=0, le=360)  # type: ignore[valid-type]
    precision: int = Precision.ANGLE
    unit: Unit = Unit.DEGREE

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.DEGREE.value:
            msg = "Input should be Unit.DEGREE."
            raise ValueError(msg)

        return v


class Droop(SinglePhaseQuantity):
    """Droop of characteristics curves."""

    precision: int = Precision.PU
    unit: Unit = Unit.UNITLESS

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.UNITLESS.value:
            msg = "Input should be Unit.UNITLESS."
            raise ValueError(msg)

        return v


class Power(SinglePhaseQuantity):
    """Base class for power quantities."""

    power_type: PowerType
    precision: int = Precision.POWER


class ActivePower(Power):
    """Electrical active power."""

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
    """Electrical apparent power."""

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
    """Electrical reactive power."""

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


class PowerFactor(Base):
    """Power factor, e.g. cos(phi), tan(phi)."""

    value: float
    direction: PowerFactorDirection = PowerFactorDirection.ND
    precision: int = Precision.POWERFACTOR
    unit: Unit = Unit.UNITLESS

    @pydantic.field_validator("value")
    def check_value(cls, value: float) -> float:
        if not math.isnan(value) and value < 0:
            msg = "Input should be greater than 0."
            raise ValueError(msg)

        return value

    @pydantic.field_validator("unit")
    def check_unit(cls, v: Unit) -> Unit:
        if v is not Unit.UNITLESS.value:
            msg = "Input should be Unit.UNITLESS."
            raise ValueError(msg)

        return v


class CosPhi(PowerFactor):
    value: float

    @pydantic.field_validator("value")
    def check_value(cls, value: float) -> float:
        if not math.isnan(value) and not (0 <= value <= 1):
            msg = "Input should be between 0 and 1."
            raise ValueError(msg)

        return value


class TanPhi(PowerFactor): ...


class PhaseAngleClock(Base):
    """Phase shift between two windings in multiples of 30°."""

    value: pydantic.confloat(ge=0, lt=12)  # type: ignore[valid-type]

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def angle(self) -> float:
        return self.value * 30.0
