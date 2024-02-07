# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum

import pydantic

from psdm.base import Base
from psdm.quantities.multi_phase import ActivePower
from psdm.quantities.multi_phase import CosPhi
from psdm.quantities.multi_phase import Droop
from psdm.quantities.multi_phase import ReactivePower
from psdm.quantities.multi_phase import TanPhi
from psdm.quantities.multi_phase import Voltage
from psdm.quantities.single_phase import Frequency
from psdm.steadystate_case.characteristic import Characteristic


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
    if power is not None and any(e < 0 for e in power.value):
        raise ValueError

    return power


class ControlQConst(Base):
    """Constant Q-setpoint control mode."""

    q_set: ReactivePower  # set point of reactive power
    control_strategy: QControlStrategy = QControlStrategy.Q_CONST

    @pydantic.field_validator("control_strategy")
    def check_control_strategy(cls, v: QControlStrategy) -> QControlStrategy:
        if v is not QControlStrategy.Q_CONST.value:
            msg = "Only QControlStrategy.Q_CONST is supported."
            raise ValueError(msg)

        return v


class ControlUConst(Base):
    """Constant U-setpoint control mode.

    The controller tries to keep the voltage at the setpoint via providing reactive power within the rated limits.
    """

    u_set: Voltage  # Setpoint of voltage.
    u_meas_ref: ControlledVoltageRef = ControlledVoltageRef.POS_SEQ  # voltage reference
    control_strategy: QControlStrategy = QControlStrategy.U_CONST

    @pydantic.field_validator("control_strategy")
    def check_control_strategy(cls, v: QControlStrategy) -> QControlStrategy:
        if v is not QControlStrategy.U_CONST.value:
            msg = "Only QControlStrategy.U_CONST is supported."
            raise ValueError(msg)

        return v


class ControlTanPhiConst(Base):
    """Constant tan(phi) control mode."""

    tan_phi_set: TanPhi  # set point of tan(phi)
    control_strategy: QControlStrategy = QControlStrategy.TANPHI_CONST

    @pydantic.field_validator("control_strategy")
    def check_control_strategy(cls, v: QControlStrategy) -> QControlStrategy:
        if v is not QControlStrategy.TANPHI_CONST.value:
            msg = "Only QControlStrategy.TANPHI_CONST is supported."
            raise ValueError(msg)

        return v


class ControlCosPhiConst(Base):
    """Constant cos(phi) control mode."""

    cos_phi_set: CosPhi  # set point of cos(phi)
    control_strategy: QControlStrategy = QControlStrategy.COSPHI_CONST

    @pydantic.field_validator("control_strategy")
    def check_control_strategy(cls, v: QControlStrategy) -> QControlStrategy:
        if v is not QControlStrategy.COSPHI_CONST.value:
            msg = "Only QControlStrategy.COSPHI_CONST is supported."
            raise ValueError(msg)

        return v


class ControlCosPhiP(Base):
    """cos(phi(P)) control mode.

    p >= p_threshold_oe: cos_phi = cos_phi_oe
    p_threshold_oe > u > p_threshold_ue: cos_phi is lineary interpolated between cos_phi_oe and cos_phi_ue
    p <= u_threshold_ue: cos_phi = cos_phi_ue
    """

    cos_phi_ue: CosPhi  # under excited: cos(phi) for calculation of Q in relation to P.
    cos_phi_oe: CosPhi  # over excited: cos(phi) for calculation of Q in relation to P.
    p_threshold_ue: ActivePower  # under excited: threshold for P.
    p_threshold_oe: ActivePower  # over excited: threshold for P.
    control_strategy: QControlStrategy = QControlStrategy.COSPHI_P

    @pydantic.field_validator("control_strategy")
    def check_control_strategy(cls, v: QControlStrategy) -> QControlStrategy:
        if v is not QControlStrategy.COSPHI_P.value:
            msg = "Only QControlStrategy.COSPHI_P is supported."
            raise ValueError(msg)

        return v


class ControlCosPhiU(Base):
    """cos(phi(U)) control mode.

    u >= u_threshold_ue: cos_phi = cos_phi_ue
    u_threshold_ue > u > u_threshold_oe: cos_phi is lineary interpolated between cos_phi_ue and cos_phi_oe
    u <= u_threshold_oe: cos_phi = cos_phi_oe
    """

    cos_phi_ue: CosPhi  # under excited: cos(phi) for calculation of Q in relation to P
    cos_phi_oe: CosPhi  # over excited: cos(phi) for calculation of Q in relation to P
    u_threshold_ue: Voltage  # under excited: threshold for U
    u_threshold_oe: Voltage  # over excited: threshold for U
    node_ref_u: str  # reference node at which the voltage is measured
    control_strategy: QControlStrategy = QControlStrategy.COSPHI_U

    @pydantic.field_validator("control_strategy")
    def check_control_strategy(cls, v: QControlStrategy) -> QControlStrategy:
        if v is not QControlStrategy.COSPHI_U.value:
            msg = "Only QControlStrategy.COSPHI_U is supported."
            raise ValueError(msg)

        return v


class ControlQU(Base):
    """Q(U) characteristic control mode.

    u >= (u_q0 + u_deadband_up): q has to be increased with droop_up until q_max_ue is reached
    (u_q0 + u_deadband_up) > u > (u_q0 - u_deadband_low): q = 0
    u <= (u_q0 - u_deadband_low): q has to be decreased with droop_low until q_max_oe is reached
    """

    droop_up: Droop  # Droop/Slope for q if voltage is above the u_deadband_up
    droop_low: Droop  # Droop/Slope for q if voltage is below the u_deadband_low
    u_q0: Voltage  # Voltage value, where Q=0: absolut value in V
    u_deadband_up: Voltage  # Width of upper deadband (U_1_up - U_Q0): absolut value in V
    u_deadband_low: Voltage  # Width of lower deadband (U_Q0 - U_1_low): absolut value in V
    q_max_ue: ReactivePower  # Under excited limit of Q: absolut value in var
    q_max_oe: ReactivePower  # Over excited limit of Q: absolut value in var
    control_strategy: QControlStrategy = QControlStrategy.Q_U

    @pydantic.field_validator("q_max_ue")
    def validate_q_max_ue(cls, power_limit: ReactivePower | None) -> ReactivePower | None:
        return validate_pos(power_limit)

    @pydantic.field_validator("q_max_oe")
    def validate_q_max_oe(cls, power_limit: ReactivePower | None) -> ReactivePower | None:
        return validate_pos(power_limit)

    @pydantic.field_validator("control_strategy")
    def check_control_strategy(cls, v: QControlStrategy) -> QControlStrategy:
        if v is not QControlStrategy.Q_U.value:
            msg = "Only QControlStrategy.Q_U is supported."
            raise ValueError(msg)

        return v


class ControlQP(Base):
    """Q(P) characteristic control mode.

    This is the general case of ControlCosPhiP, ControlCosPhiConst, ControlTanPhiConst.
    """

    q_p_characteristic: Characteristic
    q_max_ue: ReactivePower | None  # Under excited limit of Q: absolut value
    q_max_oe: ReactivePower | None  # Over excited limit of Q: absolut value
    control_strategy: QControlStrategy = QControlStrategy.Q_P

    @pydantic.field_validator("q_max_ue")
    def validate_q_max_ue(cls, power_limit: ReactivePower | None) -> ReactivePower | None:
        return validate_pos(power_limit)

    @pydantic.field_validator("q_max_oe")
    def validate_q_max_oe(cls, power_limit: ReactivePower | None) -> ReactivePower | None:
        return validate_pos(power_limit)

    @pydantic.field_validator("control_strategy")
    def check_control_strategy(cls, v: QControlStrategy) -> QControlStrategy:
        if v is not QControlStrategy.Q_P.value:
            msg = "Only QControlStrategy.Q_P is supported."
            raise ValueError(msg)

        return v


class ControlPConst(Base):
    """Constant P-setpoint control mode."""

    p_set: ActivePower  # set point of active power
    control_strategy: PControlStrategy = PControlStrategy.P_CONST

    @pydantic.field_validator("control_strategy")
    def check_control_strategy(cls, v: PControlStrategy) -> PControlStrategy:
        if v is not PControlStrategy.P_CONST.value:
            msg = "Only PControlStrategy.P_CONST is supported."
            raise ValueError(msg)

        return v


class ControlPF(Base):
    """P(f) characteristic control mode.

    f >= (f_p0+ f_deadband_up): p_set has to be decreased with droop_up
    (f_p0+ f_deadband_up) > f > (f_p0 - f_deadband_low): p = p_set
    f <= (f_p0 - f_deadband_low): p_set has to be increased with droop_low
    """

    droop_up: Droop  # Droop/Slope of power infeed reduction if frequency is above f_deadband_up: '%/Hz'
    droop_low: Droop  # Droop/Slope of power infeed increase if frequency is below f_deadband_low: '%/Hz'
    f_p0: Frequency  # Nominal frequency value: absolut value in Hz
    f_deadband_up: Frequency  # Width of upper deadband (f_up - f_P0): absolut value in Hz
    f_deadband_low: Frequency  # Width of lower deadband (f_P0 - f_low): absolut value in Hz
    p_set: ActivePower  # set point of active power
    control_strategy: PControlStrategy = PControlStrategy.P_F

    @pydantic.field_validator("control_strategy")
    def check_control_strategy(cls, v: PControlStrategy) -> PControlStrategy:
        if v is not PControlStrategy.P_F.value:
            msg = "Only PControlStrategy.P_F is supported."
            raise ValueError(msg)

        return v


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
