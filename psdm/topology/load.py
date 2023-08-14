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
    STORAGE = "STORAGE"
    PROSUMER = "PROSUMER"


class SystemType(enum.Enum):
    COAL = "COAL"
    OIL = "OIL"
    GAS = "GAS"
    DIESEL = "DIESEL"
    NUCLEAR = "NUCLEAR"
    HYDRO = "HYDRO"
    PUMP_STORAGE = "PUMP_STORAGE"
    WIND = "WIND"
    BIOGAS = "BIOGAS"
    SOLAR = "SOLAR"
    PV = "PV"
    RENEWABLE_ENERGY = "RENEWABLE_ENERGY"
    FUELCELL = "FUELCELL"
    PEAT = "PEAT"
    STAT_GEN = "STAT_GEN"
    HVDC = "HVDC"
    REACTIVE_POWER_COMPENSATOR = "REACTIVE_POWER_COMPENSATOR"
    BATTERY_STORAGE = "BATTERY_STORAGE"
    EXTERNAL_GRID_EQUIVALENT = "EXTERNAL_GRID_EQUIVALENT"
    OTHER = "OTHER"
    NIGHT_STORAGE = "NIGHT_STORAGE"
    FIXED_CONSUMPTION = "FIXED_CONSUMPTION"
    VARIABLE_CONSUMPTION = "VARIABLE_CONSUMPTION"
    HEAT_PUMP = "HEAT_PUMP"
    CHARGING_POINT = "CHARGING_POINT"
    HVAC = "HVAC"


class PhaseConnectionType(enum.Enum):
    THREE_PH_D = "THREE_PH_D"
    THREE_PH_PH_E = "THREE_PH_PH_E"
    THREE_PH_YN = "THREE_PH_YN"
    TWO_PH_PH_E = "TWO_PH_PH_E"
    TWO_PH_YN = "TWO_PH_YN"
    ONE_PH_PH_PH = "ONE_PH_PH_PH"
    ONE_PH_PH_E = "ONE_PH_PH_E"
    ONE_PH_PH_N = "ONE_PH_PH_N"


class Phase(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    N = "N"


class PowerType(enum.Enum):
    AC_APPARENT = "AC_APPARENT"
    AC_ACTIVE = "AC_ACTIVE"
    AC_REACTIVE = "AC_REACTIVE"
    DC = "DC"
    THERMAL = "THERMAL"
    GAS = "GAS"
    MECHANICAL = "MECHANICAL"


THRESHOLD = 0.51  # acceptable rounding error (0.5 W) + epsilon for calculation accuracy (0.01 W)


class PowerBase(Base):
    value: float
    value_a: float
    value_b: float
    value_c: float
    is_symmetrical: bool


T = t.TypeVar("T", bound=PowerBase)


def validate_total(power: T) -> T:
    pow_total = power.value_a + power.value_b + power.value_c
    diff = abs(power.value - pow_total)
    if diff > THRESHOLD:
        msg = f"Power mismatch: Total power should be {pow_total}, is {power.value}."
        raise ValueError(msg)

    return power


def validate_symmetry(power: T) -> T:
    if power.value != 0:
        if power.is_symmetrical:
            if not (power.value_a == power.value_b == power.value_c):
                msg = "Power mismatch: Three-phase power of load is not symmetrical."
                raise ValueError(msg)

        elif power.value_a == power.value_b == power.value_c:
            msg = "Power mismatch: Three-phase power of load is symmetrical."
            raise ValueError(msg)

    return power


class RatedPower(PowerBase):
    value: float = pydantic.Field(..., ge=0)  # rated power; base for p.u. calculation
    value_a: float = pydantic.Field(..., ge=0)  # rated power (phase a)
    value_b: float = pydantic.Field(..., ge=0)  # rated power (phase b)
    value_c: float = pydantic.Field(..., ge=0)  # rated power (phase c)
    cosphi: float = pydantic.Field(1, ge=0, le=1)  # rated cos(phi) in relation to rated power
    cosphi_a: float = pydantic.Field(1, ge=0, le=1)  # rated cos(phi) (phase a)
    cosphi_b: float = pydantic.Field(1, ge=0, le=1)  # rated cos(phi) (phase b)
    cosphi_c: float = pydantic.Field(1, ge=0, le=1)  # rated cos(phi) (phase c)
    power_type: PowerType
    is_symmetrical: bool

    @pydantic.model_validator(mode="after")  # type: ignore[arg-type]
    def _validate_symmetry(cls, power: RatedPower) -> RatedPower:
        return validate_symmetry(power)

    @pydantic.model_validator(mode="after")  # type: ignore[arg-type]
    def _validate_total(cls, power: RatedPower) -> RatedPower:
        return validate_total(power)


class ConnectedPhases(Base):
    phases_a: tuple[Phase, Phase] | None
    phases_b: tuple[Phase, Phase] | None
    phases_c: tuple[Phase, Phase] | None

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def n_connected_phases(self) -> int:
        return sum([getattr(self, f"phases_{idx}") is not None for idx in ["a", "b", "c"]])


class Load(Base):  # including assets of type load and generator
    name: str
    node: str
    u_n: float  # nominal voltage of the connected node
    rated_power: RatedPower
    active_power: ActivePower
    reactive_power: ReactivePower
    type: LoadType  # noqa: A003
    connected_phases: ConnectedPhases
    system_type: SystemType
    phase_connection_type: PhaseConnectionType
    voltage_system_type: VoltageSystemType
    description: str | None = None
