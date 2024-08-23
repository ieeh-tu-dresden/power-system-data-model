# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.quantities.multi_phase import ActivePower as ActivePowerSet
from psdm.quantities.multi_phase import Droop
from psdm.quantities.multi_phase import ReactivePower as ReactivePowerSet
from psdm.quantities.single_phase import Frequency
from psdm.quantities.single_phase import SystemType
from psdm.steadystate_case.controller import ControlPConst
from psdm.steadystate_case.controller import ControlPF
from psdm.steadystate_case.controller import ControlQConst
from psdm.steadystate_case.controller import PController


class TestActivePower:
    @pytest.mark.parametrize(
        (
            "node_target",
            "control_type",
            "expectation",
        ),
        [
            (
                "Node_A",
                ControlPConst(
                    p_set=ActivePowerSet(
                        value=[0, 0, 0],
                        system_type=SystemType.NATURAL,
                    ),
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlPF(
                    droop_up=Droop(
                        value=[2, 2, 2],
                        system_type=SystemType.NATURAL,
                    ),
                    droop_low=Droop(
                        value=[3, 3, 3],
                        system_type=SystemType.NATURAL,
                    ),
                    f_p0=Frequency(
                        value=50,
                        system_type=SystemType.NATURAL,
                    ),
                    f_deadband_up=Frequency(
                        value=0.1,
                        system_type=SystemType.NATURAL,
                    ),
                    f_deadband_low=Frequency(
                        value=0.2,
                        system_type=SystemType.NATURAL,
                    ),
                    p_set=ActivePowerSet(
                        value=[0, 0, 0],
                        system_type=SystemType.NATURAL,
                    ),
                ),
                does_not_raise(),
            ),
            (
                None,
                ControlPConst(
                    p_set=ActivePowerSet(
                        value=[0, 0, 0],
                        system_type=SystemType.NATURAL,
                    ),
                ),
                pytest.raises(pydantic.ValidationError),
            ),
            (
                "Node_A",
                None,
                pytest.raises(pydantic.ValidationError),
            ),
            (
                "Node_A",
                ControlQConst(
                    q_set=ReactivePowerSet(
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
            PController(
                node_target=node_target,
                control_type=control_type,
            )
