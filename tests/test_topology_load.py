# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.topology.load import RatedPower
from psdm.topology.load import PowerType


class TestRatedPower:
    @pytest.mark.parametrize(
        (
            "value",
            "value_a",
            "value_b",
            "value_c",
            "cosphi",
            "cosphi_a",
            "cosphi_b",
            "cosphi_c",
            "power_type",
            "is_symmetrical",
            "expectation",
        ),
        [
            (0, 0, 0, 0, 0, 0, 0, 0, PowerType.AC_APPARENT, True, does_not_raise()),
            (3, 1, 1, 1, 1, 1, 1, 1, PowerType.AC_APPARENT, True, does_not_raise()),
            (4, 2, 1, 1, 1, 1, 1, 1, PowerType.AC_APPARENT, False, does_not_raise()),
            (2, 2, 1, 1, 1, 1, 2, 1, PowerType.AC_APPARENT, False, pytest.raises(pydantic.ValidationError)),
            (2, -2, 1, 1, 1, 1, 1, 1, PowerType.AC_APPARENT, True, pytest.raises(pydantic.ValidationError)),
            (0, -2, 1, 1, 1, 1, 1, 1, PowerType.AC_APPARENT, False, pytest.raises(pydantic.ValidationError)),
            (4, 2, 1, 1, 1, 1, 2, 1, PowerType.AC_APPARENT, True, pytest.raises(pydantic.ValidationError)),
            (0, -2, 1, 1, 1, 1, 1, 1, PowerType.AC_APPARENT, True, pytest.raises(pydantic.ValidationError)),
            (3, 1, 1, 1, 1, 1, 1, 1, PowerType.AC_APPARENT, False, pytest.raises(pydantic.ValidationError)),
        ],
    )
    def test_init(  # noqa: PLR0913
        self,
        value,
        value_a,
        value_b,
        value_c,
        cosphi,
        cosphi_a,
        cosphi_b,
        cosphi_c,
        power_type,
        is_symmetrical,
        expectation,
    ) -> None:
        with expectation:
            RatedPower(
                value=value,
                value_a=value_a,
                value_b=value_b,
                value_c=value_c,
                cosphi=cosphi,
                cosphi_a=cosphi_a,
                cosphi_b=cosphi_b,
                cosphi_c=cosphi_c,
                power_type=power_type,
                is_symmetrical=is_symmetrical,
            )
