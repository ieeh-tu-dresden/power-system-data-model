# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.quantities import ActivePower as ActivePowerSet
from psdm.quantities import Droop
from psdm.quantities import PowerFactor
from psdm.quantities import PowerFactorDirection
from psdm.quantities import ReactivePower as ReactivePowerSet
from psdm.quantities import Voltage
from psdm.steadystate_case.characteristic import Characteristic
from psdm.steadystate_case.controller import ControlCosPhiConst
from psdm.steadystate_case.controller import ControlCosPhiP
from psdm.steadystate_case.controller import ControlCosPhiU
from psdm.steadystate_case.controller import ControlledVoltageRef
from psdm.steadystate_case.controller import ControlPConst
from psdm.steadystate_case.controller import ControlQConst
from psdm.steadystate_case.controller import ControlQP
from psdm.steadystate_case.controller import ControlQU
from psdm.steadystate_case.controller import ControlTanPhiConst
from psdm.steadystate_case.controller import ControlUConst
from psdm.steadystate_case.controller import QController


class TestReactivePower:
    @pytest.mark.parametrize(
        (
            "node_target",
            "control_type",
            "expectation",
        ),
        [
            (
                "Node_A",
                ControlQConst(
                    q_set=ReactivePowerSet(values=[0, 0, 0]),
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlCosPhiConst(
                    cos_phi_set=PowerFactor(values=[0.9, 0.9, 0.9], direction=PowerFactorDirection.UE),
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlTanPhiConst(
                    tan_phi_set=PowerFactor(values=[0.9, 0.9, 0.9], direction=PowerFactorDirection.UE),
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlCosPhiP(
                    cos_phi_ue=PowerFactor(values=[0.9, 0.9, 0.9], direction=PowerFactorDirection.UE),
                    cos_phi_oe=PowerFactor(values=[0.9, 0.9, 0.9], direction=PowerFactorDirection.UE),
                    p_threshold_ue=ActivePowerSet(values=[3, 3, 3]),
                    p_threshold_oe=ActivePowerSet(values=[3, 3, 3]),
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlUConst(
                    u_set=Voltage(values=[20000, 20000, 20000]),
                    u_meas_ref=ControlledVoltageRef.POS_SEQ,
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlCosPhiU(
                    cos_phi_ue=PowerFactor(values=[0.9, 0.9, 0.9], direction=PowerFactorDirection.UE),
                    cos_phi_oe=PowerFactor(values=[0.9, 0.9, 0.9], direction=PowerFactorDirection.UE),
                    u_threshold_ue=Voltage(values=[20000, 20000, 20000]),
                    u_threshold_oe=Voltage(values=[20000, 20000, 20000]),
                    node_ref_u="Node_B",
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlQP(
                    q_p_characteristic=Characteristic(name="Q(P)-Char"),
                    q_max_ue=None,
                    q_max_oe=None,
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlQU(
                    droop_low=Droop(values=[8, 8, 8]),
                    droop_up=Droop(values=[8, 8, 8]),
                    u_q0=Voltage(values=[20000, 20000, 20000]),
                    u_deadband_low=Voltage(values=[500, 500, 500]),
                    u_deadband_up=Voltage(values=[500, 500, 500]),
                    q_max_ue=ReactivePowerSet(values=[3000, 3000, 3000]),
                    q_max_oe=ReactivePowerSet(values=[3000, 3000, 3000]),
                ),
                does_not_raise(),
            ),
            (
                None,
                ControlUConst(
                    u_set=Voltage(values=[20000, 20000, 20000]),
                    u_meas_ref=ControlledVoltageRef.POS_SEQ,
                ),
                pytest.raises(pydantic.ValidationError),
            ),
            ("Node_A", None, pytest.raises(TypeError)),
            (
                "Node_A",
                ControlPConst(
                    p_set=ActivePowerSet(values=[0, 0, 0]),
                ),
                pytest.raises(TypeError),
            ),
        ],
    )
    def test_init(
        self,
        node_target,
        control_type,
        expectation,
    ) -> None:
        with expectation:
            QController(
                node_target=node_target,
                control_type=control_type,
            )
