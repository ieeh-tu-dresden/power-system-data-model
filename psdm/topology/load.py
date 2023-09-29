# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import collections.abc as cabc
import enum
import itertools
import typing as t

import pydantic

from psdm.base import Base
from psdm.base import VoltageSystemType
from psdm.topology.load_model import LoadModel


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
    ND = "ND"


PhaseConnection = tuple[Phase, Phase] | None


THRESHOLD = 0.51  # acceptable rounding error (0.5 W) + epsilon for calculation accuracy (0.01 W)


class Frequency(Base):
    value: float = pydantic.Field(..., ge=0)  # voltage (three-phase)


class MultiPhaseQuantity(Base):
    values: cabc.Sequence[float]  # values (starting at phase a)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def is_symmetrical(self) -> bool:
        return len(list(itertools.groupby(self.values))) in (0, 1)


class Voltage(MultiPhaseQuantity):
    values: cabc.Sequence[pydantic.confloat(ge=0)]  # type: ignore[valid-type]  # values (starting at phase a)


class Droop(MultiPhaseQuantity):
    values: cabc.Sequence[pydantic.confloat(ge=0)]  # type: ignore[valid-type]  # values (starting at phase a)


class Power(MultiPhaseQuantity):
    @pydantic.computed_field  # type: ignore[misc]
    @property
    def total(self) -> float:
        return sum(self.values)


class ActivePower(Power):
    @pydantic.model_validator(mode="before")
    def set_power_type(cls, values: dict[str, t.Any]) -> dict[str, t.Any]:
        values["power_type"] = PowerType.AC_ACTIVE.value
        return values


class ApparentPower(Power):
    @pydantic.model_validator(mode="before")
    def set_power_type(cls, values: dict[str, t.Any]) -> dict[str, t.Any]:
        values["power_type"] = PowerType.AC_APPARENT.value
        return values


class ReactivePower(Power):
    @pydantic.model_validator(mode="before")
    def set_power_type(cls, values: dict[str, t.Any]) -> dict[str, t.Any]:
        values["power_type"] = PowerType.AC_REACTIVE.value
        return values


class PowerFactor(MultiPhaseQuantity):
    values: cabc.Sequence[pydantic.confloat(ge=0, le=1)]  # type: ignore[valid-type] # values (starting at phase a)
    direction: PowerFactorDirection = PowerFactorDirection.ND

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def n_phases(self) -> int:
        return len(self.values)


class RatedPower(Base):
    power: Power
    cos_phi: PowerFactor

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def is_symmetrical(self) -> bool:
        return self.power.is_symmetrical and self.cos_phi.is_symmetrical


class PhaseConnections(Base):
    values: cabc.Sequence[PhaseConnections]

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def n_connected_phases(self) -> int:
        return sum(e is not None for e in self.values)


class Load(Base):  # including assets of type load and generator
    """This class represents a load.

    It is mainly characterized by the load model of active and reactive power, the  connected phases and the load type itself (Producer, Consumer, Storage or passive shunt).
    """

    name: str
    node: str
    rated_power: RatedPower
    active_power_model: LoadModel
    reactive_power_model: LoadModel
    phase_connections: PhaseConnections
    phase_connection_type: PhaseConnectionType
    type: LoadType  # noqa: A003
    system_type: SystemType
    voltage_system_type: VoltageSystemType
    description: str | None = None
