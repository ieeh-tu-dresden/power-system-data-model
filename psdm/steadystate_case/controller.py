# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum

import pydantic

from psdm.base import Base
from psdm.base import CosphiDir
from psdm.steadystate_case.characteristic import Characteristic


class ControlStrategy(enum.Enum):
    U_CONST = "U_CONST"
    COSPHI_CONST = "COSPHI_CONST"
    Q_CONST = "Q_CONST"
    Q_U = "Q_U"
    Q_P = "Q_P"
    COSPHI_P = "COSPHI_P"
    COSPHI_U = "COSPHI_U"
    TANPHI_CONST = "TANPHI_CONST"
    P_F = "P_F"
    ND = "ND"


class ControlledVoltageRef(enum.Enum):
    POS_SEQ = "POS_SEQ"
    AVG = "AVG"
    A = "A"
    B = "B"
    C = "C"
    AB = "AB"
    BC = "BC"
    CA = "CA"


class ControlQConst(Base):
    # q-setpoint control mode
    q_set: float  # Setpoint of reactive power. Counted demand based.

    control_strategy: ControlStrategy = ControlStrategy.Q_CONST


class ControlUConst(Base):
    # u-setpoint control mode
    u_set: float = pydantic.Field(ge=0)  # Setpoint of voltage.
    u_meas_ref: ControlledVoltageRef = ControlledVoltageRef.POS_SEQ  # voltage reference

    control_strategy: ControlStrategy = ControlStrategy.U_CONST


class ControlTanphiConst(Base):
    # cos(phi) control mode
    cosphi_dir: CosphiDir
    cosphi: float = pydantic.Field(ge=0, le=1)  # cos(phi) for calculation of Q in relation to P.

    control_strategy: ControlStrategy = ControlStrategy.TANPHI_CONST


class ControlCosphiConst(Base):
    # cos(phi) control mode
    cosphi_dir: CosphiDir
    cosphi: float = pydantic.Field(ge=0, le=1)  # cos(phi) for calculation of Q in relation to P.

    control_strategy: ControlStrategy = ControlStrategy.COSPHI_CONST


class ControlCosphiP(Base):
    # cos(phi(P)) control mode
    cosphi_ue: float = pydantic.Field(
        ge=0,
        le=1,
    )  # under excited: cos(phi) for calculation of Q in relation to P.
    cosphi_oe: float = pydantic.Field(
        ge=0,
        le=1,
    )  # over excited: cos(phi) for calculation of Q in relation to P.
    p_threshold_ue: float = pydantic.Field(le=0)  # under excited: threshold for P.
    p_threshold_oe: float = pydantic.Field(le=0)  # over excited: threshold for P.

    control_strategy: ControlStrategy = ControlStrategy.COSPHI_P


class ControlCosphiU(Base):
    # cos(phi(U)) control mode
    cosphi_ue: float = pydantic.Field(
        ...,
        ge=0,
        le=1,
    )  # under excited: cos(phi) for calculation of Q in relation to P.
    cosphi_oe: float = pydantic.Field(
        ...,
        ge=0,
        le=1,
    )  # over excited: cos(phi) for calculation of Q in relation to P.
    u_threshold_ue: float = pydantic.Field(..., ge=0)  # under excited: threshold for U.
    u_threshold_oe: float = pydantic.Field(..., ge=0)  # over excited: threshold for U.

    control_strategy: ControlStrategy = ControlStrategy.COSPHI_U


class ControlQU(Base):
    # Q(U) characteristic control mode
    droop_tg_2015: float = pydantic.Field(
        ...,
        ge=0,
    )  # Droop/Slope based on technical guideline VDE-AR-N 4120:2015: '%/kV'-value --> Q = m_% * Pr * dU_kV
    droop_tg_2018: float = pydantic.Field(
        ...,
        ge=0,
    )  # Droop/Slope based on technical guideline VDE-AR-N 4120:2018: '%/pu'-value --> Q = m_% * Pr * dU_(% of Un)
    u_q0: float = pydantic.Field(..., ge=0)  # Voltage value, where Q=0: absolut value in V
    u_deadband_up: float = pydantic.Field(
        ...,
        ge=0,
    )  # Width of upper deadband (U_1_up - U_Q0): absolut value in V
    u_deadband_low: float = pydantic.Field(
        ...,
        ge=0,
    )  # Width of lower deadband (U_Q0 - U_1_low): absolut value in V
    q_max_ue: float = pydantic.Field(..., ge=0)  # Under excited limit of Q: absolut value in var
    q_max_oe: float = pydantic.Field(..., ge=0)  # Over excited limit of Q: absolut value in var

    control_strategy: ControlStrategy = ControlStrategy.Q_U


def validate_pos(value: float | None) -> float | None:
    if value is not None and value < 0:
        raise ValueError

    return value


class ControlQP(Base):
    # Q(P) characteristic control mode
    q_p_characteristic: Characteristic
    q_max_ue: float | None = None  # Under excited limit of Q: absolut value
    q_max_oe: float | None = None  # Over excited limit of Q: absolut value

    control_strategy: ControlStrategy = ControlStrategy.Q_P

    @pydantic.field_validator("q_max_ue", mode="before")
    def validate_q_max_ue(cls, v: float | None) -> float | None:
        return validate_pos(v)

    @pydantic.field_validator("q_max_oe", mode="before")
    def validate_q_max_oe(cls, v: float | None) -> float | None:
        return validate_pos(v)


class ControlPF(Base):
    # P(f) characteristic control mode
    droop_over_freq: float = pydantic.Field(
        ...,
        ge=0,
    )  # Droop/Slope of power infeed reduction if freqeuncy is above f_deadband_up: '%/Hz'
    droop_under_freq: float = pydantic.Field(
        ...,
        ge=0,
    )  # Droop/Slope of power infeed increase if freqeuncy is below f_deadband_low: '%/Hz'
    f_p0: float = pydantic.Field(..., ge=0)  # Nominal freqeuncy value: absolut value in Hz
    f_deadband_up: float = pydantic.Field(
        ...,
        ge=0,
    )  # Width of upper deadband (f_up - f_P0): absolut value in Hz
    f_deadband_low: float = pydantic.Field(
        ...,
        ge=0,
    )  # Width of lower deadband (f_P0 - f_low): absolut value in Hz

    control_strategy: ControlStrategy = ControlStrategy.P_F


ControlType = (
    ControlQConst
    | ControlUConst
    | ControlTanphiConst
    | ControlCosphiConst
    | ControlCosphiP
    | ControlCosphiU
    | ControlQU
    | ControlQP
    | ControlPF
)


class Controller(Base):
    node_target: str  # the controlled node (which can be differ from node the load is connected to)
    control_type: ControlType | None = None
    external_controller_name: str | None = None  # if external controller is specified --> name
