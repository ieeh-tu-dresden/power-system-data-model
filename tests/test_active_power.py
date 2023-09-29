# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.steadystate_case.active_power import ActivePower
from psdm.steadystate_case.controller import ControlPConst
from psdm.steadystate_case.controller import PController
from psdm.topology.load import ActivePower as ActivePowerSet


class TestActivePower:
    @pytest.mark.parametrize(
        (
            "controller",
            "expectation",
        ),
        [
            (
                PController(
                    node_target="Node_A",
                    control_type=ControlPConst(
                        p_set=ActivePowerSet(
                            values=(0, 0, 0),
                        ),
                    ),
                ),
                does_not_raise(),
            ),
            (None, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(
        self,
        controller,
        expectation,
    ) -> None:
        with expectation:
            ActivePower(controller=controller)
