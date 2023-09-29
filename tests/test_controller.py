# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

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
from psdm.topology.load import ActivePower as ActivePowerSet
from psdm.topology.load import Frequency
from psdm.topology.load import PowerFactor
from psdm.topology.load import PowerFactorDirection
from psdm.topology.load import ReactivePower as ReactivePowerSet
from psdm.topology.load import Voltage


class TestControlQConst:
    @pytest.mark.parametrize(
        (
            "values",
            "expectation",
        ),
        [
            ((-500, -500, -500), does_not_raise()),
            ((500, 500, 500), does_not_raise()),
            ((500, 1000, 0), does_not_raise()),
            ((0, 0, 0), does_not_raise()),
            ((None, None, None), pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        values,
        expectation,
    ) -> None:
        with expectation:
            ControlQConst(
                q_set=ReactivePowerSet(
                    values=values,
                ),
            )


class TestControlUConst:
    @pytest.mark.parametrize(
        (
            "values",
            "u_meas_ref",
            "expectation",
        ),
        [
            ((20000, 20000, 20000), ControlledVoltageRef.POS_SEQ, does_not_raise()),
            ((20000, 20000, 20000), ControlledVoltageRef.AVG, does_not_raise()),
            ((20000, 19000, 21000), ControlledVoltageRef.AVG, does_not_raise()),
            ((20000, 20000, 20000), None, pytest.raises(pydantic.ValidationError)),
            (
                (-20000, -20000, -20000),
                ControlledVoltageRef.POS_SEQ,
                pytest.raises(pydantic.ValidationError),
            ),
        ],
    )
    def test_init(
        self,
        values,
        u_meas_ref,
        expectation,
    ) -> None:
        with expectation:
            ControlUConst(
                u_set=Voltage(
                    values=values,
                ),
                u_meas_ref=u_meas_ref,
            )


class TestControlTanphiConst:
    @pytest.mark.parametrize(
        (
            "direction",
            "values",
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
        values,
        expectation,
    ) -> None:
        with expectation:
            ControlTanPhiConst(
                tan_phi_set=PowerFactor(
                    direction=direction,
                    values=values,
                ),
            )


class TestControlCosPhiConst:
    @pytest.mark.parametrize(
        (
            "direction",
            "values",
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
        values,
        expectation,
    ) -> None:
        with expectation:
            ControlCosPhiConst(
                cos_phi_set=PowerFactor(
                    direction=direction,
                    values=values,
                ),
            )


class TestControlCosPhiP:
    @pytest.mark.parametrize(
        (
            "cos_phi_ue",
            "cos_phi_ue_is_symmetrical",
            "cos_phi_oe",
            "cos_phi_oe_is_symmetrical",
            "p_threshold_ue",
            "p_threshold_ue_is_symmetrical",
            "p_threshold_oe",
            "p_threshold_oe_is_symmetrical",
            "expectation",
        ),
        [
            (0.9, True, 0.9, True, -3, True, -6, True, does_not_raise()),
            (0.9, True, 0.9, True, 3, True, 6, True, does_not_raise()),
            (1, True, 0, True, -6, True, -3, True, does_not_raise()),
            (0.9, True, 1.1, True, -6, True, -3, True, pytest.raises(pydantic.ValidationError)),
            (1.1, True, 0.9, True, -6, True, -3, True, pytest.raises(pydantic.ValidationError)),
            (-0.9, True, 0.9, True, -6, True, -3, True, pytest.raises(pydantic.ValidationError)),
            (0.9, True, -0.9, True, -6, True, -3, True, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        cos_phi_ue,
        cos_phi_ue_is_symmetrical,
        cos_phi_oe,
        cos_phi_oe_is_symmetrical,
        p_threshold_ue,
        p_threshold_ue_is_symmetrical,
        p_threshold_oe,
        p_threshold_oe_is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            if cos_phi_ue_is_symmetrical:
                pf_ue = PowerFactor(values=[cos_phi_ue, cos_phi_ue, cos_phi_ue], direction=PowerFactorDirection.UE)
            if cos_phi_oe_is_symmetrical:
                pf_oe = PowerFactor(values=[cos_phi_oe, cos_phi_oe, cos_phi_oe], direction=PowerFactorDirection.OE)
            if p_threshold_ue_is_symmetrical:
                power_ue = ActivePowerSet(
                    values=[round(p_threshold_ue / 3, 3), round(p_threshold_ue / 3, 3), round(p_threshold_ue / 3, 3)],
                )
            if p_threshold_oe_is_symmetrical:
                power_oe = ActivePowerSet(
                    values=[round(p_threshold_oe / 3, 3), round(p_threshold_oe / 3, 3), round(p_threshold_oe / 3, 3)],
                )
            ControlCosPhiP(
                cos_phi_ue=pf_ue,
                cos_phi_oe=pf_oe,
                p_threshold_ue=power_ue,
                p_threshold_oe=power_oe,
            )


class TestControlCosPhiU:
    @pytest.mark.parametrize(
        (
            "cos_phi_ue",
            "cos_phi_ue_is_symmetrical",
            "cos_phi_oe",
            "cos_phi_oe_is_symmetrical",
            "u_threshold_ue",
            "u_threshold_ue_is_symmetrical",
            "u_threshold_oe",
            "u_threshold_oe_is_symmetrical",
            "expectation",
        ),
        [
            (0.9, True, 0.9, True, 20000, True, 24000, True, does_not_raise()),
            (1, True, 0, True, 24000, True, 20000, True, does_not_raise()),
            (0.9, True, 1.1, True, 24000, True, 20000, True, pytest.raises(pydantic.ValidationError)),
            (1.1, True, 0.9, True, 24000, True, 20000, True, pytest.raises(pydantic.ValidationError)),
            (-0.9, True, 0.9, True, 24000, True, 20000, True, pytest.raises(pydantic.ValidationError)),
            (0.9, True, -0.9, True, 24000, True, 20000, True, pytest.raises(pydantic.ValidationError)),
            (0.9, True, 0.9, True, -24000, True, 20000, True, pytest.raises(pydantic.ValidationError)),
            (0.9, True, 0.9, True, 20000, True, -20000, True, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        cos_phi_ue,
        cos_phi_ue_is_symmetrical,
        cos_phi_oe,
        cos_phi_oe_is_symmetrical,
        u_threshold_ue,
        u_threshold_ue_is_symmetrical,
        u_threshold_oe,
        u_threshold_oe_is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            if cos_phi_ue_is_symmetrical:
                pf_ue = PowerFactor(values=[cos_phi_ue, cos_phi_ue, cos_phi_ue], direction=PowerFactorDirection.UE)
            if cos_phi_oe_is_symmetrical:
                pf_oe = PowerFactor(values=[cos_phi_oe, cos_phi_oe, cos_phi_oe], direction=PowerFactorDirection.OE)
            if u_threshold_ue_is_symmetrical:
                voltage_ue = Voltage(values=[u_threshold_ue, u_threshold_ue, u_threshold_ue])
            if u_threshold_oe_is_symmetrical:
                voltage_oe = Voltage(values=[u_threshold_oe, u_threshold_oe, u_threshold_oe])
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
            "droop_up_is_symmetrical",
            "droop_low",
            "droop_low_is_symmetrical",
            "u_q0",
            "u_q0_is_symmetrical",
            "u_deadband_up",
            "u_deadband_up_is_symmetrical",
            "u_deadband_low",
            "u_deadband_low_is_symmetrical",
            "q_max_ue",
            "q_max_ue_is_symmetrical",
            "q_max_oe",
            "q_max_oe_is_symmetrical",
            "expectation",
        ),
        [
            (5, True, 6, True, 110000, True, 1000, True, 1000, True, 10000, True, 10000, True, does_not_raise()),
            (6, True, 5, True, 110000, True, 1000, True, 2000, True, 20000, True, 10000, True, does_not_raise()),
            (
                -5,
                True,
                6,
                True,
                110000,
                True,
                1000,
                True,
                2000,
                True,
                20000,
                True,
                10000,
                True,
                pytest.raises(pydantic.ValidationError),
            ),
            (
                5,
                True,
                -6,
                True,
                110000,
                True,
                1000,
                True,
                2000,
                True,
                20000,
                True,
                10000,
                True,
                pytest.raises(pydantic.ValidationError),
            ),
            (
                5,
                False,
                6,
                True,
                110000,
                True,
                1000,
                True,
                2000,
                True,
                20000,
                True,
                10000,
                True,
                pytest.raises(pydantic.ValidationError),
            ),
            (
                5,
                True,
                6,
                False,
                110000,
                True,
                1000,
                True,
                2000,
                True,
                20000,
                True,
                10000,
                True,
                pytest.raises(pydantic.ValidationError),
            ),
            (
                5,
                True,
                6,
                True,
                -110000,
                True,
                1000,
                True,
                2000,
                True,
                20000,
                True,
                10000,
                True,
                pytest.raises(pydantic.ValidationError),
            ),
            (
                5,
                True,
                6,
                True,
                110000,
                False,
                1000,
                True,
                2000,
                True,
                20000,
                True,
                10000,
                True,
                pytest.raises(pydantic.ValidationError),
            ),
            (
                5,
                True,
                6,
                True,
                110000,
                False,
                -1000,
                True,
                2000,
                True,
                20000,
                True,
                10000,
                True,
                pytest.raises(pydantic.ValidationError),
            ),
            (
                5,
                True,
                6,
                True,
                110000,
                True,
                1000,
                False,
                2000,
                True,
                20000,
                True,
                10000,
                True,
                pytest.raises(pydantic.ValidationError),
            ),
            (
                5,
                True,
                6,
                True,
                110000,
                True,
                1000,
                True,
                -2000,
                True,
                20000,
                True,
                10000,
                True,
                pytest.raises(pydantic.ValidationError),
            ),
            (
                5,
                True,
                6,
                True,
                110000,
                True,
                1000,
                True,
                2000,
                False,
                20000,
                True,
                10000,
                True,
                pytest.raises(pydantic.ValidationError),
            ),
            (
                5,
                True,
                6,
                True,
                110000,
                True,
                1000,
                True,
                2000,
                True,
                -20000,
                True,
                10000,
                True,
                pytest.raises(pydantic.ValidationError),
            ),
            (
                5,
                True,
                6,
                True,
                110000,
                True,
                1000,
                True,
                2000,
                True,
                20000,
                True,
                -10000,
                True,
                pytest.raises(pydantic.ValidationError),
            ),
        ],
    )
    def test_init(
        self,
        droop_up,
        droop_up_is_symmetrical,
        droop_low,
        droop_low_is_symmetrical,
        u_q0,
        u_q0_is_symmetrical,
        u_deadband_up,
        u_deadband_up_is_symmetrical,
        u_deadband_low,
        u_deadband_low_is_symmetrical,
        q_max_ue,
        q_max_ue_is_symmetrical,
        q_max_oe,
        q_max_oe_is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            if droop_up_is_symmetrical:
                droop_up = Droop(values=[droop_up, droop_up, droop_up])

            if droop_low_is_symmetrical:
                droop_low = Droop(values=[droop_low, droop_low, droop_low])

            if u_q0_is_symmetrical:
                u_q0 = Voltage(values=[u_q0, u_q0, u_q0])

            if u_deadband_up_is_symmetrical:
                u_deadband_up = Voltage(values=[u_deadband_up, u_deadband_up, u_deadband_up])

            if u_deadband_low_is_symmetrical:
                u_deadband_low = Voltage(values=[u_deadband_low, u_deadband_low, u_deadband_low])

            if q_max_ue is not None:
                if q_max_ue_is_symmetrical:
                    q_max_ue = ReactivePowerSet(
                        values=[round(q_max_ue / 3, 3), round(q_max_ue / 3, 3), round(q_max_ue / 3, 3)],
                    )
                else:
                    q_max_ue = None

            if q_max_oe is not None:
                if q_max_oe_is_symmetrical:
                    q_max_oe = ReactivePowerSet(
                        values=[round(q_max_oe / 3, 3), round(q_max_oe / 3, 3), round(q_max_oe / 3, 3)],
                    )
                else:
                    q_max_oe = None

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
            "q_max_ue_is_symmetrical",
            "q_max_oe",
            "q_max_oe_is_symmetrical",
            "expectation",
        ),
        [
            (Characteristic(name="Q_P_Char"), 10000, True, 10000, True, does_not_raise()),
            (Characteristic(name="Q_P_Char"), 10000, True, 20000, True, does_not_raise()),
            (Characteristic(name="Q_P_Char"), None, True, None, True, does_not_raise()),
            (Characteristic(name="Q_P_Char"), None, False, None, False, does_not_raise()),
            (None, 10000, True, 10000, True, pytest.raises(pydantic.ValidationError)),
            (Characteristic(name="Q_P_Char"), -10000, True, 10000, True, pytest.raises(pydantic.ValidationError)),
            (Characteristic(name="Q_P_Char"), 10000, True, -10000, True, pytest.raises(pydantic.ValidationError)),
            (Characteristic(name="Q_P_Char"), -10000, True, -10000, True, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        q_p_characteristic,
        q_max_ue,
        q_max_ue_is_symmetrical,
        q_max_oe,
        q_max_oe_is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            if q_max_ue is not None:
                if q_max_ue_is_symmetrical:
                    q_max_ue = ReactivePowerSet(
                        values=[round(q_max_ue / 3, 3), round(q_max_ue / 3, 3), round(q_max_ue / 3, 3)],
                    )
                else:
                    q_max_ue = None

            if q_max_oe is not None:
                if q_max_oe_is_symmetrical:
                    q_max_oe = ReactivePowerSet(
                        values=[round(q_max_oe / 3, 3), round(q_max_oe / 3, 3), round(q_max_oe / 3, 3)],
                    )
                else:
                    q_max_oe = None

            ControlQP(
                q_p_characteristic=q_p_characteristic,
                q_max_ue=q_max_ue,
                q_max_oe=q_max_oe,
            )


class TestControlPF:
    @pytest.mark.parametrize(
        (
            "droop_over_freq",
            "droop_over_freq_is_symmetrical",
            "droop_under_freq",
            "droop_under_freq_is_symmetrical",
            "f_p0",
            "f_deadband_up",
            "f_deadband_low",
            "expectation",
        ),
        [
            (40, True, 40, True, 50, 0.2, 0.2, does_not_raise()),
            (-40, True, 40, True, 50, 0.2, 0.2, pytest.raises(pydantic.ValidationError)),
            (40, True, -40, True, 50, 0.2, 0.2, pytest.raises(pydantic.ValidationError)),
            (40, True, 40, True, -50, 0.2, 0.2, pytest.raises(pydantic.ValidationError)),
            (40, True, 40, True, 50, -0.2, 0.2, pytest.raises(pydantic.ValidationError)),
            (40, True, 40, True, 50, 0.2, -0.2, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        droop_over_freq,
        droop_over_freq_is_symmetrical,
        droop_under_freq,
        droop_under_freq_is_symmetrical,
        f_p0,
        f_deadband_up,
        f_deadband_low,
        expectation,
    ) -> None:
        with expectation:
            if droop_over_freq_is_symmetrical:
                droop_over_freq = Droop(values=[droop_over_freq, droop_over_freq, droop_over_freq])
            else:
                droop_over_freq = None
            if droop_under_freq_is_symmetrical:
                droop_under_freq = Droop(values=[droop_under_freq, droop_under_freq, droop_under_freq])
            else:
                droop_under_freq = None
            ControlPF(
                droop_up=droop_over_freq,
                droop_low=droop_under_freq,
                f_p0=Frequency(value=f_p0),
                f_deadband_up=Frequency(value=f_deadband_up),
                f_deadband_low=Frequency(value=f_deadband_low),
            )


class TestControlPConst:
    @pytest.mark.parametrize(
        (
            "values",
            "expectation",
        ),
        [
            ((-500, -500, -500), does_not_raise()),
            ((500, 500, 500), does_not_raise()),
            ((500, 1000, 0), does_not_raise()),
            ((0, 0, 0), does_not_raise()),
            ((None, None, None), pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        values,
        expectation,
    ) -> None:
        with expectation:
            p_set = ActivePowerSet(values=values)
            ControlPConst(p_set=p_set)
