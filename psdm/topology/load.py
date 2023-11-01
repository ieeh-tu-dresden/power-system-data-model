# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum
import math

import pydantic

from psdm.base import Base
from psdm.base import VoltageSystemType
from psdm.base import model_validator_after
from psdm.quantities import ActivePower
from psdm.quantities import ApparentPower
from psdm.quantities import PhaseConnections
from psdm.quantities import PowerFactor
from psdm.quantities import ReactivePower
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


THRESHOLD = 0.51  # acceptable rounding error (0.5 W) + epsilon for calculation accuracy (0.01 W)


def find_decimals(value: float) -> int:
    return len(str(value).split(".")[1])


class RatedPower(Base):
    """Rated power of a load specified by rated apparent power and power factor.

    A RatedPower object should be created via the class method "from_apparent_power(apparent_power, power_factor)"
    as active and reactive power will be automatically computed based on rated power and powerfactor.
    """

    apparent_power: ApparentPower
    active_power: ActivePower
    reactive_power: ReactivePower
    cos_phi: PowerFactor

    @model_validator_after
    def validate_length(self) -> RatedPower:
        if (
            self.apparent_power.n_phases
            == self.active_power.n_phases
            == self.reactive_power.n_phases
            == self.cos_phi.n_phases
        ):
            return self

        msg = "Length mismatch."
        raise ValueError(msg)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def is_symmetrical(self) -> bool:
        return self.apparent_power.is_symmetrical and self.cos_phi.is_symmetrical

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def cos_phi_total(self) -> float:
        try:
            return round(
                sum(self.active_power.values) / sum(self.apparent_power.values),
                find_decimals(self.cos_phi.values[0]),  # noqa: PD011
            )
        except ZeroDivisionError:
            return float("nan")

    @classmethod
    def from_apparent_power(cls, apparent_power: ApparentPower, cos_phi: PowerFactor) -> RatedPower:
        active_power = ActivePower(
            values=[round(p * c, find_decimals(p)) for p, c in zip(apparent_power.values, cos_phi.values, strict=True)],
        )
        reactive_power = ReactivePower(
            values=[
                round(p * math.sin(math.acos(c)), find_decimals(p))
                for p, c in zip(apparent_power.values, cos_phi.values, strict=True)
            ],
        )
        return RatedPower(
            apparent_power=apparent_power,
            active_power=active_power,
            reactive_power=reactive_power,
            cos_phi=cos_phi,
        )

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def n_phases(self) -> int:
        return len(self.cos_phi.values)

    def __len__(self) -> int:
        return self.n_phases


class Load(Base):  # including assets of type load and generator
    """This class represents a load.

    It is mainly characterized by the load model of active and reactive power, the connected phases and the load type itself (Producer, Consumer, Storage or passive shunt).
    """

    name: str
    node: str
    rated_power: RatedPower
    active_power_model: LoadModel
    reactive_power_model: LoadModel
    phase_connections: PhaseConnections
    type: LoadType  # noqa: A003
    system_type: SystemType
    voltage_system_type: VoltageSystemType
    description: str | None = None

    @model_validator_after
    def validate_length(self) -> Load:
        if self.rated_power.n_phases == self.phase_connections.n_phases:
            return self

        msg = "Length mismatch."
        raise ValueError(msg)
