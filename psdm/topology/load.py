# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum
import typing as t

import pydantic

from psdm.base import Base
from psdm.base import VoltageSystemType
from psdm.topology.active_power import ActivePower
from psdm.topology.reactive_power import ReactivePower


class LoadType(enum.Enum):
    CONSUMER = "CONSUMER"
    PRODUCER = "PRODUCER"
    PROSUMER = "PROSUMER"
    SHUNT = "SHUNT"
    STORAGE = "STORAGE"


class SystemType(enum.Enum):
    BATTERY_STORAGE = "BATTERY_STORAGE"
    BIOGAS = "BIOGAS"
    CHARGING_POINT = "CHARGING_POINT"
    COAL = "COAL"
    DIESEL = "DIESEL"
    EXTERNAL_GRID_EQUIVALENT = "EXTERNAL_GRID_EQUIVALENT"
    FILTER_C = "FILTER_C"
    FILTER_HARMONIC = "FILTER_HARMONIC"
    FILTER_RL = "FILTER_RL"
    FILTER_RLC = "FILTER_RLC"
    FILTER_RLCCRP = "FILTER_RLCCRP"
    FILTER_RLCRP = "FILTER_RLCRP"
    FIXED_CONSUMPTION = "FIXED_CONSUMPTION"
    FUELCELL = "FUELCELL"
    GAS = "GAS"
    HEAT_PUMP = "HEAT_PUMP"
    HVAC = "HVAC"
    HVDC = "HVDC"
    HYDRO = "HYDRO"
    NIGHT_STORAGE = "NIGHT_STORAGE"
    NUCLEAR = "NUCLEAR"
    OIL = "OIL"
    OTHER = "OTHER"
    PEAT = "PEAT"
    PUMP_STORAGE = "PUMP_STORAGE"
    PV = "PV"
    REACTIVE_POWER_COMPENSATOR = "REACTIVE_POWER_COMPENSATOR"
    RENEWABLE_ENERGY = "RENEWABLE_ENERGY"
    SOLAR = "SOLAR"
    STAT_GEN = "STAT_GEN"
    STATIC_VAR_SYSTEM = "STATIC_VAR_SYSTEM"
    VARIABLE_CONSUMPTION = "VARIABLE_CONSUMPTION"
    WIND = "WIND"


class PhaseConnectionType(enum.Enum):
    ONE_PH_PH_E = "ONE_PH_PH_E"
    ONE_PH_PH_N = "ONE_PH_PH_N"
    ONE_PH_PH_PH = "ONE_PH_PH_PH"
    THREE_PH_D = "THREE_PH_D"
    THREE_PH_PH_E = "THREE_PH_PH_E"
    THREE_PH_YN = "THREE_PH_YN"
    TWO_PH_PH_E = "TWO_PH_PH_E"
    TWO_PH_YN = "TWO_PH_YN"


class Phase(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    N = "N"


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


THRESHOLD = 0.51  # acceptable rounding error (0.5 W) + epsilon for calculation accuracy (0.01 W)


class Power(Base):
    value: float  # power (three-phase)
    value_a: float  # power (phase a)
    value_b: float  # power (phase b)
    value_c: float  # power (phase c)
    is_symmetrical: bool
    power_type: PowerType

    @pydantic.model_validator(mode="after")  # type: ignore[arg-type]
    def validate_total(cls, power: Power) -> Power:
        pow_total = power.value_a + power.value_b + power.value_c
        diff = abs(power.value - pow_total)
        if diff > THRESHOLD:
            msg = f"Power mismatch: Total power should be {pow_total}, is {power.value}."
            raise ValueError(msg)

        return power

    @pydantic.model_validator(mode="after")  # type: ignore[arg-type]
    def validate_symmetry(cls, power: Power) -> Power:
        if power.value != 0:
            if power.is_symmetrical:
                if not (power.value_a == power.value_b == power.value_c):
                    msg = "Power mismatch: Three-phase power of load is not symmetrical."
                    raise ValueError(msg)

            elif power.value_a == power.value_b == power.value_c:
                msg = "Power mismatch: Three-phase power of load is symmetrical."
                raise ValueError(msg)

        return power


class PowerFactor(Base):
    value: float  # cos(phi) (three-phase)
    value_a: float  # cos(phi) (phase a)
    value_b: float  # cos(phi) (phase b)
    value_c: float  # cos(phi) (phase c)
    is_symmetrical: bool
    direction: PowerFactorDirection

    @pydantic.model_validator(mode="after")  # type: ignore[arg-type]
    def _validate_symmetry(cls, power_factor: PowerFactor) -> PowerFactor:
        if power_factor.is_symmetrical:
            if not (power_factor.value == power_factor.value_a == power_factor.value_b == power_factor.value_c):
                msg = "Power factor mismatch: Three-phase power factor of load is not symmetrical."
                raise ValueError(msg)

        elif power_factor.value_a == power_factor.value_b == power_factor.value_c:
            msg = "Power factor mismatch: Three-phase power factor of load is symmetrical."
            raise ValueError(msg)

        return power_factor


class RatedPower(Base):
    power: Power
    cos_phi: PowerFactor


class ConnectedPhases(Base):
    phases_a: tuple[Phase, Phase] | None
    phases_b: tuple[Phase, Phase] | None
    phases_c: tuple[Phase, Phase] | None

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def n_connected_phases(self) -> int:
        return sum([getattr(self, f"phases_{idx}") is not None for idx in ["a", "b", "c"]])


class Load(Base):  # including assets of type load and generator
    """This class represents a load.

    It is mainly characterized by the load model of active and reactive power, the  connected phases and the load type itself (Producer, Consumer, Storage or passive shunt).
    """

    name: str
    node: str
    rated_power: RatedPower
    active_power: ActivePower
    reactive_power: ReactivePower
    connected_phases: ConnectedPhases
    phase_connection_type: PhaseConnectionType
    type: LoadType  # noqa: A003
    system_type: SystemType
    voltage_system_type: VoltageSystemType
    description: str | None = None
