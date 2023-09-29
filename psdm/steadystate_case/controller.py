# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum

import pydantic

from psdm.base import Base
from psdm.steadystate_case.characteristic import Characteristic
from psdm.topology.load import ActivePower
from psdm.topology.load import Droop
from psdm.topology.load import Frequency
from psdm.topology.load import PowerFactor
from psdm.topology.load import ReactivePower
from psdm.topology.load import Voltage


class QControlStrategy(enum.Enum):
    COSPHI_CONST = "COSPHI_CONST"
    COSPHI_P = "COSPHI_P"
    COSPHI_U = "COSPHI_U"
    ND = "ND"
    Q_CONST = "Q_CONST"
    Q_P = "Q_P"
    Q_U = "Q_U"
    TANPHI_CONST = "TANPHI_CONST"
    U_CONST = "U_CONST"


class PControlStrategy(enum.Enum):
    ND = "ND"
    P_CONST = "P_CONST"
    P_F = "P_F"


class ControlledVoltageRef(enum.Enum):
    A = "A"
    AB = "AB"
    AVG = "AVG"
    B = "B"
    BC = "BC"
    C = "C"
    CA = "CA"
    POS_SEQ = "POS_SEQ"


def validate_pos(power: ReactivePower | None) -> ReactivePower | None:
    if power is not None and any(e < 0 for e in power.values):  # noqa: PD011
        raise ValueError

    return power


class ControlQConst(Base):
    # q-setpoint control mode
    q_set: ReactivePower  # set point of reactive power

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def control_strategy(self) -> QControlStrategy:
        return QControlStrategy.Q_CONST


class ControlUConst(Base):
    # u-setpoint control mode
    u_set: Voltage  # Setpoint of voltage.
    u_meas_ref: ControlledVoltageRef = ControlledVoltageRef.POS_SEQ  # voltage reference

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def control_strategy(self) -> QControlStrategy:
        return QControlStrategy.U_CONST


class ControlTanPhiConst(Base):
    # tan(phi) control mode
    tan_phi_set: PowerFactor  # set point of tan(phi)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def control_strategy(self) -> QControlStrategy:
        return QControlStrategy.TANPHI_CONST


class ControlCosPhiConst(Base):
    # cos(phi) control mode
    cos_phi_set: PowerFactor  # set point of cos(phi)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def control_strategy(self) -> QControlStrategy:
        return QControlStrategy.COSPHI_CONST


class ControlCosPhiP(Base):
    # cos(phi(P)) control mode
    cos_phi_ue: PowerFactor  # under excited: cos(phi) for calculation of Q in relation to P.
    cos_phi_oe: PowerFactor  # over excited: cos(phi) for calculation of Q in relation to P.
    p_threshold_ue: ActivePower  # under excited: threshold for P.
    p_threshold_oe: ActivePower  # over excited: threshold for P.

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def control_strategy(self) -> QControlStrategy:
        return QControlStrategy.COSPHI_P


class ControlCosPhiU(Base):
    # cos(phi(U)) control mode
    cos_phi_ue: PowerFactor  # under excited: cos(phi) for calculation of Q in relation to P
    cos_phi_oe: PowerFactor  # over excited: cos(phi) for calculation of Q in relation to P
    u_threshold_ue: Voltage  # under excited: threshold for U
    u_threshold_oe: Voltage  # over excited: threshold for U
    node_ref_u: str  # reference node at which the voltage is measured

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def control_strategy(self) -> QControlStrategy:
        return QControlStrategy.COSPHI_U


class ControlQU(Base):
    # Q(U) characteristic control mode
    droop_up: Droop  # Droop/Slope for voltage above the u_deadband_up
    droop_low: Droop  # Droop/Slope for voltage above the u_deadband_low
    u_q0: Voltage  # Voltage value, where Q=0: absolut value in V
    u_deadband_up: Voltage  # Width of upper deadband (U_1_up - U_Q0): absolut value in V
    u_deadband_low: Voltage  # Width of lower deadband (U_Q0 - U_1_low): absolut value in V
    q_max_ue: ReactivePower  # Under excited limit of Q: absolut value in var
    q_max_oe: ReactivePower  # Over excited limit of Q: absolut value in var

    @pydantic.field_validator("q_max_ue", mode="before")
    def validate_q_max_ue(cls, power_limit: ReactivePower | None) -> ReactivePower | None:
        return validate_pos(power_limit)

    @pydantic.field_validator("q_max_oe", mode="before")
    def validate_q_max_oe(cls, power_limit: ReactivePower | None) -> ReactivePower | None:
        return validate_pos(power_limit)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def control_strategy(self) -> QControlStrategy:
        return QControlStrategy.Q_U


class ControlQP(Base):
    # Q(P) characteristic control mode
    q_p_characteristic: Characteristic
    q_max_ue: ReactivePower | None  # Under excited limit of Q: absolut value
    q_max_oe: ReactivePower | None  # Over excited limit of Q: absolut value

    @pydantic.field_validator("q_max_ue", mode="before")
    def validate_q_max_ue(cls, power_limit: ReactivePower | None) -> ReactivePower | None:
        return validate_pos(power_limit)

    @pydantic.field_validator("q_max_oe", mode="before")
    def validate_q_max_oe(cls, power_limit: ReactivePower | None) -> ReactivePower | None:
        return validate_pos(power_limit)

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def control_strategy(self) -> QControlStrategy:
        return QControlStrategy.Q_P


class ControlPConst(Base):
    # p-setpoint control mode
    p_set: ActivePower  # set point of active power

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def control_strategy(self) -> PControlStrategy:
        return PControlStrategy.P_CONST


class ControlPF(Base):
    # P(f) characteristic control mode
    droop_up: Droop  # Droop/Slope of power infeed reduction if frequency is above f_deadband_up: '%/Hz'
    droop_low: Droop  # Droop/Slope of power infeed increase if frequency is below f_deadband_low: '%/Hz'
    f_p0: Frequency  # Nominal frequency value: absolut value in Hz
    f_deadband_up: Frequency  # Width of upper deadband (f_up - f_P0): absolut value in Hz
    f_deadband_low: Frequency  # Width of lower deadband (f_P0 - f_low): absolut value in Hz

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def control_strategy(self) -> PControlStrategy:
        return PControlStrategy.P_F


QControlType = (
    ControlQConst
    | ControlUConst
    | ControlTanPhiConst
    | ControlCosPhiConst
    | ControlCosPhiP
    | ControlCosPhiU
    | ControlQU
    | ControlQP
)

PControlType = ControlPConst | ControlPF


class Controller(Base):
    node_target: str  # the controlled node (which can be differ from node the load is connected to)
    external_controller_name: str | None = None  # if external controller is specified --> name


class PController(Controller):
    """This class represents a controller of active power of a load.

    It is characterized by the control type, which comes with different controller parameters.
    """

    control_type: PControlType


class QController(Controller):
    """This class represents a controller of reactive power of a load.

    It is characterized by the control type, which comes with different controller parameters.
    """

    control_type: QControlType
