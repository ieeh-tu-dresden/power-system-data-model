# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.quantities.multi_phase import ActivePower as ActivePowerSet
from psdm.quantities.multi_phase import CosPhi
from psdm.quantities.multi_phase import ReactivePower as ReactivePowerSet
from psdm.quantities.multi_phase import TanPhi
from psdm.quantities.multi_phase import Voltage
from psdm.quantities.single_phase import Frequency
from psdm.quantities.single_phase import PowerFactorDirection
from psdm.quantities.single_phase import SystemType
from psdm.steadystate_case.characteristic import Characteristic
from psdm.steadystate_case.controller import ControlCosPhiConst
from psdm.steadystate_case.controller import ControlCosPhiP
from psdm.steadystate_case.controller import ControlCosPhiU
from psdm.steadystate_case.controller import ControlledVoltageRef
from psdm.steadystate_case.controller import ControlPConst
from psdm.steadystate_case.controller import ControlPF
from psdm.steadystate_case.controller import ControlQConst
from psdm.steadystate_case.controller import ControlQP
from psdm.steadystate_case.controller import ControlQU
from psdm.steadystate_case.controller import ControlTanPhiConst
from psdm.steadystate_case.controller import ControlUConst
from psdm.steadystate_case.controller import Droop


class TestControlQConst:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            ((-500, -500, -500), does_not_raise()),
            ((500, 500, 500), does_not_raise()),
            ((500, 1000, 0), does_not_raise()),
            ((0, 0, 0), does_not_raise()),
            ((0, -500, 200), does_not_raise()),
            ((None, None, None), pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            ControlQConst(
                q_set=ReactivePowerSet(
                    value=value,
                    system_type=SystemType.NATURAL,
                ),
            )


class TestControlUConst:
    @pytest.mark.parametrize(
        (
            "value",
            "u_meas_ref",
            "expectation",
        ),
        [
            ((20000, 20000, 20000), ControlledVoltageRef.POS_SEQ, does_not_raise()),
            ((20000, 20000, 20000), ControlledVoltageRef.AVG, does_not_raise()),
            ((20000, 19000, 21000), ControlledVoltageRef.AVG, does_not_raise()),
            ((20000, 20000, 20000), None, pytest.raises(pydantic.ValidationError)),
            (None, ControlledVoltageRef.AVG, pytest.raises(pydantic.ValidationError)),
            (
                (-20000, -20000, -20000),
                ControlledVoltageRef.POS_SEQ,
                pytest.raises(pydantic.ValidationError),
            ),
        ],
    )
    def test_init(
        self,
        value,
        u_meas_ref,
        expectation,
    ) -> None:
        with expectation:
            ControlUConst(
                u_set=Voltage(
                    value=value,
                    system_type=SystemType.NATURAL,
                ),
                u_meas_ref=u_meas_ref,
                system_type=SystemType.NATURAL,
            )


class TestControlTanPhiConst:
    @pytest.mark.parametrize(
        (
            "direction",
            "value",
            "expectation",
        ),
        [
            (PowerFactorDirection.UE, (1, 1, 1), does_not_raise()),
            (PowerFactorDirection.UE, (0, 0, 0), does_not_raise()),
            (PowerFactorDirection.OE, (0.9, 0.9, 0.9), does_not_raise()),
            (PowerFactorDirection.OE, (0.9, 0.8, 1), does_not_raise()),
            (PowerFactorDirection.OE, (-0.9, -0.9, -0.9), pytest.raises(pydantic.ValidationError)),
            (PowerFactorDirection.OE, (-0.9, 0.9, 0.9), pytest.raises(pydantic.ValidationError)),
            (PowerFactorDirection.OE, (-0.6, 0.9, 0.9), pytest.raises(pydantic.ValidationError)),
            (PowerFactorDirection.OE, (None, None, None), pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        direction,
        value,
        expectation,
    ) -> None:
        with expectation:
            ControlTanPhiConst(
                tan_phi_set=TanPhi(
                    direction=direction,
                    value=value,
                    system_type=SystemType.NATURAL,
                ),
            )


class TestControlCosPhiConst:
    @pytest.mark.parametrize(
        (
            "direction",
            "value",
            "expectation",
        ),
        [
            (PowerFactorDirection.UE, (1, 1, 1), does_not_raise()),
            (PowerFactorDirection.UE, (0, 0, 0), does_not_raise()),
            (PowerFactorDirection.OE, (0.9, 0.9, 0.9), does_not_raise()),
            (PowerFactorDirection.OE, (0.9, 0.8, 1), does_not_raise()),
            (PowerFactorDirection.OE, (-0.9, -0.9, -0.9), pytest.raises(pydantic.ValidationError)),
            (PowerFactorDirection.OE, (-0.9, 0.9, 0.9), pytest.raises(pydantic.ValidationError)),
            (PowerFactorDirection.OE, (-0.6, 0.9, 0.9), pytest.raises(pydantic.ValidationError)),
            (PowerFactorDirection.OE, (2, 2, 2), pytest.raises(pydantic.ValidationError)),
            (PowerFactorDirection.OE, (None, None, None), pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        direction,
        value,
        expectation,
    ) -> None:
        with expectation:
            ControlCosPhiConst(
                cos_phi_set=CosPhi(
                    direction=direction,
                    value=value,
                    system_type=SystemType.NATURAL,
                ),
            )


class TestControlCosPhiP:
    @pytest.mark.parametrize(
        (
            "cos_phi_ue",
            "cos_phi_oe",
            "p_threshold_ue",
            "p_threshold_oe",
            "expectation",
        ),
        [
            (0.9, 0.9, -3, -6, does_not_raise()),
            (0.9, 0.9, 3, 6, does_not_raise()),
            (1, 0, -6, -3, does_not_raise()),
            (0.9, 1.1, -6, -3, pytest.raises(pydantic.ValidationError)),
            (1.1, 0.9, -6, -3, pytest.raises(pydantic.ValidationError)),
            (-0.9, 0.9, -6, -3, pytest.raises(pydantic.ValidationError)),
            (0.9, -0.9, -6, -3, pytest.raises(pydantic.ValidationError)),
            (None, 0.9, -3, -6, pytest.raises(pydantic.ValidationError)),
            (0.9, None, -3, -6, pytest.raises(pydantic.ValidationError)),
            (0.9, 0.9, None, -6, pytest.raises(pydantic.ValidationError)),
            (0.9, 0.9, -3, None, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        cos_phi_ue,
        cos_phi_oe,
        p_threshold_ue,
        p_threshold_oe,
        expectation,
    ) -> None:
        with expectation:
            pf_ue = CosPhi(
                value=[cos_phi_ue, cos_phi_ue, cos_phi_ue],
                direction=PowerFactorDirection.UE,
                system_type=SystemType.NATURAL,
            )
            pf_oe = CosPhi(
                value=[cos_phi_oe, cos_phi_oe, cos_phi_oe],
                direction=PowerFactorDirection.OE,
                system_type=SystemType.NATURAL,
            )
            if p_threshold_ue is not None:
                p_threshold_ue = ActivePowerSet(
                    value=[round(p_threshold_ue / 3, 3), round(p_threshold_ue / 3, 3), round(p_threshold_ue / 3, 3)],
                    system_type=SystemType.NATURAL,
                )
            if p_threshold_oe is not None:
                p_threshold_oe = ActivePowerSet(
                    value=[round(p_threshold_oe / 3, 3), round(p_threshold_oe / 3, 3), round(p_threshold_oe / 3, 3)],
                    system_type=SystemType.NATURAL,
                )
            ControlCosPhiP(
                cos_phi_ue=pf_ue,
                cos_phi_oe=pf_oe,
                p_threshold_ue=p_threshold_ue,
                p_threshold_oe=p_threshold_oe,
            )


class TestControlCosPhiU:
    @pytest.mark.parametrize(
        (
            "cos_phi_ue",
            "cos_phi_oe",
            "u_threshold_ue",
            "u_threshold_oe",
            "expectation",
        ),
        [
            (0.9, 0.9, 20000, 24000, does_not_raise()),
            (1, 0, 24000, 20000, does_not_raise()),
            (0.9, 1.1, 24000, 20000, pytest.raises(pydantic.ValidationError)),
            (1.1, 0.9, 24000, 20000, pytest.raises(pydantic.ValidationError)),
            (-0.9, 0.9, 24000, 20000, pytest.raises(pydantic.ValidationError)),
            (0.9, -0.9, 24000, 20000, pytest.raises(pydantic.ValidationError)),
            (0.9, 0.9, -24000, 20000, pytest.raises(pydantic.ValidationError)),
            (0.9, 0.9, 20000, -20000, pytest.raises(pydantic.ValidationError)),
            (None, 0.9, 20000, 24000, pytest.raises(pydantic.ValidationError)),
            (0.9, None, 20000, 24000, pytest.raises(pydantic.ValidationError)),
            (0.9, 0.9, None, 24000, pytest.raises(pydantic.ValidationError)),
            (0.9, 0.9, 20000, None, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        cos_phi_ue,
        cos_phi_oe,
        u_threshold_ue,
        u_threshold_oe,
        expectation,
    ) -> None:
        with expectation:
            pf_ue = CosPhi(
                value=[cos_phi_ue, cos_phi_ue, cos_phi_ue],
                direction=PowerFactorDirection.UE,
                system_type=SystemType.NATURAL,
            )
            pf_oe = CosPhi(
                value=[cos_phi_oe, cos_phi_oe, cos_phi_oe],
                direction=PowerFactorDirection.OE,
                system_type=SystemType.NATURAL,
            )
            voltage_ue = Voltage(
                value=[u_threshold_ue, u_threshold_ue, u_threshold_ue],
                system_type=SystemType.NATURAL,
            )
            voltage_oe = Voltage(
                value=[u_threshold_oe, u_threshold_oe, u_threshold_oe],
                system_type=SystemType.NATURAL,
            )
            ControlCosPhiU(
                cos_phi_ue=pf_ue,
                cos_phi_oe=pf_oe,
                u_threshold_ue=voltage_ue,
                u_threshold_oe=voltage_oe,
                node_ref_u="A",
            )


class TestControlQU:
    @pytest.mark.parametrize(
        (
            "droop_up",
            "droop_low",
            "u_q0",
            "u_deadband_up",
            "u_deadband_low",
            "q_max_ue",
            "q_max_oe",
            "expectation",
        ),
        [
            (5, 6, 110000, 1000, 1000, 10000, 10000, does_not_raise()),
            (6, 5, 110000, 1000, 2000, 20000, 10000, does_not_raise()),
            (5, 6, -110000, 1000, 2000, 20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, 110000, -1000, 2000, 20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, 110000, 1000, -2000, 20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, 110000, 1000, 2000, -20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, 110000, 1000, 2000, 20000, -10000, pytest.raises(pydantic.ValidationError)),
            (None, 6, 110000, 1000, 2000, 20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, None, 110000, 1000, 2000, 20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, None, 1000, 2000, 20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, 110000, None, 2000, 20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, 110000, 1000, None, 20000, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, 110000, 1000, 2000, None, 10000, pytest.raises(pydantic.ValidationError)),
            (5, 6, 110000, 1000, 2000, 20000, None, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        droop_up,
        droop_low,
        u_q0,
        u_deadband_up,
        u_deadband_low,
        q_max_ue,
        q_max_oe,
        expectation,
    ) -> None:
        with expectation:
            droop_up = Droop(
                value=[droop_up, droop_up, droop_up],
                system_type=SystemType.NATURAL,
            )
            droop_low = Droop(
                value=[droop_low, droop_low, droop_low],
                system_type=SystemType.NATURAL,
            )
            u_q0 = Voltage(
                value=[u_q0, u_q0, u_q0],
                system_type=SystemType.NATURAL,
            )
            u_deadband_up = Voltage(
                value=[u_deadband_up, u_deadband_up, u_deadband_up],
                system_type=SystemType.NATURAL,
            )
            u_deadband_low = Voltage(
                value=[u_deadband_low, u_deadband_low, u_deadband_low],
                system_type=SystemType.NATURAL,
            )
            if q_max_ue is not None:
                q_max_ue = ReactivePowerSet(
                    value=[round(q_max_ue / 3, 3), round(q_max_ue / 3, 3), round(q_max_ue / 3, 3)],
                    system_type=SystemType.NATURAL,
                )
            if q_max_oe is not None:
                q_max_oe = ReactivePowerSet(
                    value=[round(q_max_oe / 3, 3), round(q_max_oe / 3, 3), round(q_max_oe / 3, 3)],
                    system_type=SystemType.NATURAL,
                )

            ControlQU(
                droop_up=droop_up,
                droop_low=droop_low,
                u_q0=u_q0,
                u_deadband_up=u_deadband_up,
                u_deadband_low=u_deadband_low,
                q_max_ue=q_max_ue,
                q_max_oe=q_max_oe,
            )


class TestControlQP:
    @pytest.mark.parametrize(
        (
            "q_p_characteristic",
            "q_max_ue",
            "q_max_oe",
            "expectation",
        ),
        [
            (Characteristic(name="Q_P_Char"), 10000, 10000, does_not_raise()),
            (Characteristic(name="Q_P_Char"), 10000, 20000, does_not_raise()),
            (Characteristic(name="Q_P_Char"), None, None, does_not_raise()),
            (None, 10000, 10000, pytest.raises(pydantic.ValidationError)),
            (Characteristic(name="Q_P_Char"), -10000, 10000, pytest.raises(pydantic.ValidationError)),
            (Characteristic(name="Q_P_Char"), 10000, -10000, pytest.raises(pydantic.ValidationError)),
            (Characteristic(name="Q_P_Char"), -10000, -10000, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        q_p_characteristic,
        q_max_ue,
        q_max_oe,
        expectation,
    ) -> None:
        with expectation:
            if q_max_ue is not None:
                q_max_ue = ReactivePowerSet(
                    value=[round(q_max_ue / 3, 3), round(q_max_ue / 3, 3), round(q_max_ue / 3, 3)],
                    system_type=SystemType.NATURAL,
                )
            if q_max_oe is not None:
                q_max_oe = ReactivePowerSet(
                    value=[round(q_max_oe / 3, 3), round(q_max_oe / 3, 3), round(q_max_oe / 3, 3)],
                    system_type=SystemType.NATURAL,
                )

            ControlQP(
                q_p_characteristic=q_p_characteristic,
                q_max_ue=q_max_ue,
                q_max_oe=q_max_oe,
            )


class TestControlPF:
    @pytest.mark.parametrize(
        (
            "droop_over_freq",
            "droop_under_freq",
            "f_p0",
            "f_deadband_up",
            "f_deadband_low",
            "p_set",
            "expectation",
        ),
        [
            (40, 40, 50, 0.2, 0.2, 1, does_not_raise()),
            (40, 40, -50, 0.2, 0.2, 1, pytest.raises(pydantic.ValidationError)),
            (40, 40, 50, -0.2, 0.2, 1, pytest.raises(pydantic.ValidationError)),
            (40, 40, 50, 0.2, -0.2, 1, pytest.raises(pydantic.ValidationError)),
            (None, 40, 50, 0.2, 0.2, 1, pytest.raises(pydantic.ValidationError)),
            (40, None, 50, 0.2, 0.2, 1, pytest.raises(pydantic.ValidationError)),
            (40, 40, None, 0.2, 0.2, 1, pytest.raises(pydantic.ValidationError)),
            (40, 40, 50, None, 0.2, 1, pytest.raises(pydantic.ValidationError)),
            (40, 40, 50, 0.2, None, 1, pytest.raises(pydantic.ValidationError)),
            (40, 40, 50, 0.2, 0.2, None, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        droop_over_freq,
        droop_under_freq,
        f_p0,
        f_deadband_up,
        f_deadband_low,
        p_set,
        expectation,
    ) -> None:
        with expectation:
            ControlPF(
                droop_up=Droop(
                    value=[droop_over_freq, droop_over_freq, droop_over_freq],
                    system_type=SystemType.NATURAL,
                ),
                droop_low=Droop(
                    value=[droop_under_freq, droop_under_freq, droop_under_freq],
                    system_type=SystemType.NATURAL,
                ),
                f_p0=Frequency(
                    value=f_p0,
                    system_type=SystemType.NATURAL,
                ),
                f_deadband_up=Frequency(
                    value=f_deadband_up,
                    system_type=SystemType.NATURAL,
                ),
                f_deadband_low=Frequency(
                    value=f_deadband_low,
                    system_type=SystemType.NATURAL,
                ),
                p_set=ActivePowerSet(
                    value=[p_set, p_set, p_set],
                    system_type=SystemType.NATURAL,
                ),
            )


class TestControlPConst:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            ((-500, -500, -500), does_not_raise()),
            ((500, 500, 500), does_not_raise()),
            ((500, -500, 500), does_not_raise()),
            ((500, 1000, 0), does_not_raise()),
            ((0, 0, 0), does_not_raise()),
            ((None, None, None), pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            p_set = ActivePowerSet(
                value=value,
                system_type=SystemType.NATURAL,
            )
            ControlPConst(p_set=p_set)
