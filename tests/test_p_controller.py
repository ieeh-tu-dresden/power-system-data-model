# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.quantities import ActivePower as ActivePowerSet
from psdm.quantities import Droop
from psdm.quantities import Frequency
from psdm.quantities import ReactivePower as ReactivePowerSet
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
                    p_set=ActivePowerSet(values=[0, 0, 0]),
                ),
                does_not_raise(),
            ),
            (
                "Node_A",
                ControlPF(
                    droop_up=Droop(values=[2, 2, 2]),
                    droop_low=Droop(values=[3, 3, 3]),
                    f_p0=Frequency(value=50),
                    f_deadband_up=Frequency(value=0.1),
                    f_deadband_low=Frequency(value=0.2),
                ),
                does_not_raise(),
            ),
            (
                None,
                ControlPConst(
                    p_set=ActivePowerSet(values=[0, 0, 0]),
                ),
                pytest.raises(pydantic.ValidationError),
            ),
            (
                "Node_A",
                None,
                pytest.raises(TypeError),
            ),
            (
                "Node_A",
                ControlQConst(
                    q_set=ReactivePowerSet(values=[0, 0, 0]),
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
            PController(
                node_target=node_target,
                control_type=control_type,
            )
