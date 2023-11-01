# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.quantities import ActivePower as ActivePowerSet
from psdm.quantities import ReactivePower as ReactivePowerSet
from psdm.steadystate_case.controller import ControlPConst
from psdm.steadystate_case.controller import ControlQConst
from psdm.steadystate_case.controller import PController
from psdm.steadystate_case.controller import QController
from psdm.steadystate_case.reactive_power import ReactivePower


class TestReactivePower:
    @pytest.mark.parametrize(
        (
            "controller",
            "expectation",
        ),
        [
            (
                QController(
                    node_target="Node_A",
                    control_type=ControlQConst(
                        q_set=ReactivePowerSet(
                            values=[0, 0, 0],
                        ),
                    ),
                ),
                does_not_raise(),
            ),
            (None, pytest.raises(pydantic.ValidationError)),
            (
                PController(
                    node_target="Node_A",
                    control_type=ControlPConst(
                        p_set=ActivePowerSet(
                            values=(0, 0, 0),
                        ),
                    ),
                ),
                pytest.raises(pydantic.ValidationError),
            ),
        ],
    )
    def test_init(
        self,
        controller,
        expectation,
    ) -> None:
        with expectation:
            ReactivePower(controller=controller)
