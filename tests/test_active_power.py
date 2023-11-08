# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.quantities.multi_phase import ActivePower as ActivePowerSet
from psdm.quantities.multi_phase import ReactivePower as ReactivePowerSet
from psdm.quantities.single_phase import SystemType
from psdm.steadystate_case.active_power import ActivePower
from psdm.steadystate_case.controller import ControlPConst
from psdm.steadystate_case.controller import ControlQConst
from psdm.steadystate_case.controller import PController
from psdm.steadystate_case.controller import QController


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
                            value=(0, 0, 0),
                            system_type=SystemType.NATURAL,
                        ),
                    ),
                ),
                does_not_raise(),
            ),
            (None, pytest.raises(pydantic.ValidationError)),
            (
                QController(
                    node_target="Node_A",
                    control_type=ControlQConst(
                        q_set=ReactivePowerSet(
                            value=(0, 0, 0),
                            system_type=SystemType.NATURAL,
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
            ActivePower(controller=controller)
