# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum
import itertools
import math
import typing as t

import pydantic

from psdm.base import Base
from psdm.base import UniqueTuple
from psdm.base import VoltageSystemType
from psdm.base import model_validator_after
from psdm.base import model_validator_before
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


def find_decimals(value: float) -> int:
    return len(str(value).split(".")[1])


class Frequency(Base):
    value: float = pydantic.Field(..., ge=0)  # voltage (three-phase)


class MultiPhaseQuantity(Base):
    """Base class for multi phase quantities like voltage, current, power or charcteristic droops."""

    values: tuple[float, ...]  # values (starting at phase a)

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
    values: tuple[pydantic.confloat(ge=0), ...]  # type: ignore[valid-type]  # values (starting at phase a)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def average(self) -> float:
        return round(sum(self.values) / self.n_phases, find_decimals(self.values[0]))


class Current(MultiPhaseQuantity):
    @pydantic.computed_field  # type: ignore[misc]
    @property
    def average(self) -> float:
        return round(sum(self.values) / self.n_phases, find_decimals(self.values[0]))


class Angle(MultiPhaseQuantity):
    values: tuple[pydantic.confloat(ge=0, le=360), ...]  # type: ignore[valid-type]  # values (starting at phase a)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def average(self) -> float:
        return round(sum(self.values) / self.n_phases, find_decimals(self.values[0]))


class Droop(MultiPhaseQuantity):
    @pydantic.computed_field  # type: ignore[misc]
    @property
    def average(self) -> float:
        return round(sum(self.values) / self.n_phases, find_decimals(self.values[0]))


class Power(MultiPhaseQuantity):
    """Base class for power quantities.

    It comes with the computed property "total" that is the total power of all phases.
    This value should be used for symmetrical calculations.
    """

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
    values: tuple[pydantic.confloat(ge=0, le=1), ...]  # type: ignore[valid-type] # values (starting at phase a)
    direction: PowerFactorDirection = PowerFactorDirection.ND

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def average(self) -> float:
        return round(sum(self.values) / self.n_phases, find_decimals(self.values[0]))


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
        return round(
            sum(self.active_power.values) / sum(self.apparent_power.values),
            find_decimals(self.cos_phi.values[0]),  # noqa: PD011
        )

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


class PhaseConnections(Base):
    values: UniqueTuple[PhaseConnection]

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def n_phases(self) -> int:
        return len(self.values)


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
    phase_connection_type: PhaseConnectionType
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
