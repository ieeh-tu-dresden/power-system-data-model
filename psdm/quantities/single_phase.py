# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum

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
    POSITIVE_NEGATIVE_COUPLING = "POSITIVE_NEGATIVE_COUPLING"
    NEGATIVE_ZERO_COUPLING = "NEGATIVE_ZERO_COUPLING"
    ZERO_POSITIVE_COUPLING = "ZERO_POSITIVE_COUPLING"


class PowerFactorDirection(enum.Enum):
    UE = "UE"
    OE = "OE"
    ND = "ND"


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
    VOLT_AMPERE = "VA"
    VOLT_AMPERE_REACTIVE = "VAR"
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

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    precision: int = Precision.FREQUENCY
    unit: Unit = Unit.HERTZ

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def unit(self) -> Unit:
        return Unit.HERTZ


class Impedance(SinglePhaseQuantity):
    """Impedance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    precision: int = Precision.IMPEDANCE
    unit: Unit = Unit.OHM

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def unit(self) -> Unit:
        return Unit.OHM


class ImpedancePosSeq(Impedance):
    """Positive sequence impedance."""

    system_type: SystemType = SystemType.POSITIVE_SEQUENCE

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def system_type(self) -> SystemType:
        return SystemType.POSITIVE_SEQUENCE


class ImpedanceNegSeq(Impedance):
    """Negative sequence impedance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.NEGATIVE_SEQUENCE

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def system_type(self) -> SystemType:
        return SystemType.NEGATIVE_SEQUENCE


class ImpedanceZerSeq(Impedance):
    """Zero sequence impedance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.ZERO_SEQUENCE

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def system_type(self) -> SystemType:
        return SystemType.ZERO_SEQUENCE


class ImpedanceNat(Impedance):
    """Natural impedance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.NATURAL

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def system_type(self) -> SystemType:
        return SystemType.NATURAL


class Admittance(SinglePhaseQuantity):
    """Admittance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    precision: int = Precision.ADMITTANCE
    unit: Unit = Unit.SIEMENS


class AdmittancePosSeq(Admittance):
    """Positive sequence admittance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.POSITIVE_SEQUENCE

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def system_type(self) -> SystemType:
        return SystemType.POSITIVE_SEQUENCE


class AdmittanceNegSeq(Admittance):
    """Negative sequence admittance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.NEGATIVE_SEQUENCE

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def system_type(self) -> SystemType:
        return SystemType.NEGATIVE_SEQUENCE


class AdmittanceZerSeq(Admittance):
    """Zero sequence admittance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.ZERO_SEQUENCE

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def system_type(self) -> SystemType:
        return SystemType.ZERO_SEQUENCE


class AdmittanceNat(Admittance):
    """Natural admittance."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    system_type: SystemType = SystemType.NATURAL

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def system_type(self) -> SystemType:
        return SystemType.NATURAL


class Length(SinglePhaseQuantity):
    """Length."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    precision: int = Precision.LENGTH
    unit: Unit = Unit.METER


class Voltage(SinglePhaseQuantity):
    """Electrical Voltage."""

    precision: int = Precision.VOLTAGE
    unit: Unit = Unit.VOLT


class Current(SinglePhaseQuantity):
    """Electrical current."""

    precision: int = Precision.CURRENT
    unit: Unit = Unit.AMPERE


class Angle(SinglePhaseQuantity):
    """Angle of complex quantity."""

    value: pydantic.confloat(ge=0, le=360)  # type: ignore[valid-type]
    precision: int = Precision.ANGLE
    unit: Unit = Unit.DEGREE


class Droop(SinglePhaseQuantity):
    """Droop of characteristics curves."""

    precision: int = Precision.PU
    unit: Unit = Unit.UNITLESS


class Power(SinglePhaseQuantity):
    """Base class for power quantities."""

    power_type: PowerType
    precision: int = Precision.POWER


class ActivePower(Power):
    """Electrical active power."""

    power_type: PowerType = PowerType.AC_ACTIVE
    unit: Unit = Unit.WATT

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def power_type(self) -> PowerType:
        return PowerType.AC_ACTIVE


class ApparentPower(Power):
    """Electrical apparent power."""

    power_type: PowerType = PowerType.AC_APPARENT
    unit: Unit = Unit.VOLT_AMPERE

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def power_type(self) -> PowerType:
        return PowerType.AC_APPARENT


class ReactivePower(Power):
    """Electrical reactive power."""

    power_type: PowerType = PowerType.AC_REACTIVE
    unit: Unit = Unit.VOLT_AMPERE_REACTIVE

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def power_type(self) -> PowerType:
        return PowerType.AC_REACTIVE


class PowerFactor(Base):
    """Power factor, e.g. cos(phi), tan(phi)."""

    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]
    direction: PowerFactorDirection = PowerFactorDirection.ND
    precision: int = Precision.POWERFACTOR
    unit: Unit = Unit.UNITLESS


class CosPhi(PowerFactor):
    value: pydantic.confloat(ge=0, le=1)  # type: ignore[valid-type]


class TanPhi(PowerFactor):
    value: pydantic.confloat(ge=0)  # type: ignore[valid-type]


class PhaseAngleClock(Base):
    """Phase shift between two windings in multiples of 30°."""

    value: pydantic.confloat(ge=0, lt=12)  # type: ignore[valid-type]

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def angle(self) -> float:
        return self.value * 30.0
