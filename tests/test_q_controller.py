# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.quantities.multi_phase import ActivePower as ActivePowerSet
from psdm.quantities.multi_phase import CosPhi
from psdm.quantities.multi_phase import Droop
from psdm.quantities.multi_phase import ReactivePower as ReactivePowerSet
from psdm.quantities.multi_phase import TanPhi
from psdm.quantities.multi_phase import Voltage
from psdm.quantities.single_phase import PowerFactorDirection
from psdm.quantities.single_phase import SystemType
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
                    q_set=ReactivePowerSet(
                        value=[0, 0, 0],
                        system_type=SystemType.NATURAL,
                    ),
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlCosPhiConst(
                    cos_phi_set=CosPhi(
                        value=[0.9, 0.9, 0.9],
                        direction=PowerFactorDirection.UE,
                        system_type=SystemType.NATURAL,
                    ),
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlTanPhiConst(
                    tan_phi_set=TanPhi(
                        value=[0.9, 0.9, 0.9],
                        direction=PowerFactorDirection.UE,
                        system_type=SystemType.NATURAL,
                    ),
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlCosPhiP(
                    cos_phi_ue=CosPhi(
                        value=[0.9, 0.9, 0.9],
                        direction=PowerFactorDirection.UE,
                        system_type=SystemType.NATURAL,
                    ),
                    cos_phi_oe=CosPhi(
                        value=[0.9, 0.9, 0.9],
                        direction=PowerFactorDirection.UE,
                        system_type=SystemType.NATURAL,
                    ),
                    p_threshold_ue=ActivePowerSet(
                        value=[3, 3, 3],
                        system_type=SystemType.NATURAL,
                    ),
                    p_threshold_oe=ActivePowerSet(
                        value=[3, 3, 3],
                        system_type=SystemType.NATURAL,
                    ),
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlUConst(
                    u_set=Voltage(
                        value=[20000, 20000, 20000],
                        system_type=SystemType.NATURAL,
                    ),
                    u_meas_ref=ControlledVoltageRef.POS_SEQ,
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlCosPhiU(
                    cos_phi_ue=CosPhi(
                        value=[0.9, 0.9, 0.9],
                        direction=PowerFactorDirection.UE,
                        system_type=SystemType.NATURAL,
                    ),
                    cos_phi_oe=CosPhi(
                        value=[0.9, 0.9, 0.9],
                        direction=PowerFactorDirection.UE,
                        system_type=SystemType.NATURAL,
                    ),
                    u_threshold_ue=Voltage(
                        value=[20000, 20000, 20000],
                        system_type=SystemType.NATURAL,
                    ),
                    u_threshold_oe=Voltage(
                        value=[20000, 20000, 20000],
                        system_type=SystemType.NATURAL,
                    ),
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
                    droop_low=Droop(
                        value=[8, 8, 8],
                        system_type=SystemType.NATURAL,
                    ),
                    droop_up=Droop(
                        value=[8, 8, 8],
                        system_type=SystemType.NATURAL,
                    ),
                    u_q0=Voltage(
                        value=[20000, 20000, 20000],
                        system_type=SystemType.NATURAL,
                    ),
                    u_deadband_low=Voltage(
                        value=[500, 500, 500],
                        system_type=SystemType.NATURAL,
                    ),
                    u_deadband_up=Voltage(
                        value=[500, 500, 500],
                        system_type=SystemType.NATURAL,
                    ),
                    q_max_ue=ReactivePowerSet(
                        value=[3000, 3000, 3000],
                        system_type=SystemType.NATURAL,
                    ),
                    q_max_oe=ReactivePowerSet(
                        value=[3000, 3000, 3000],
                        system_type=SystemType.NATURAL,
                    ),
                ),
                does_not_raise(),
            ),
            (
                None,
                ControlUConst(
                    u_set=Voltage(
                        value=[20000, 20000, 20000],
                        system_type=SystemType.NATURAL,
                    ),
                    u_meas_ref=ControlledVoltageRef.POS_SEQ,
                ),
                pytest.raises(pydantic.ValidationError),
            ),
            ("Node_A", None, pytest.raises(pydantic.ValidationError)),
            (
                "Node_A",
                ControlPConst(
                    p_set=ActivePowerSet(
                        value=[0, 0, 0],
                        system_type=SystemType.NATURAL,
                    ),
                ),
                pytest.raises(pydantic.ValidationError),
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
