# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest
from psdm.steadystate_case.controller import QController
from psdm.steadystate_case.controller import ControlQConst

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
                        value=0,
                        value_a=0,
                        value_b=0,
                        value_c=0,
                        is_symmetrical=True,
                    ),
                ),
                does_not_raise(),
            ),
            (None, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(  # noqa: PLR0913
        self,
        controller,
        expectation,
    ) -> None:
        with expectation:
            ReactivePower(
                controller=controller,
            )
