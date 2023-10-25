# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

import datetime as dt
import warnings
from contextlib import nullcontext as does_not_raise

import pytest

from psdm.meta import Meta


class TestMeta:
    @pytest.mark.parametrize(
        ("name", "grid", "result", "expectation", "warning"),
        [
            ("a", None, "a", does_not_raise(), True),
            (None, "a", "a", does_not_raise(), False),
            ("a", "b", "b", does_not_raise(), True),
            (None, None, "a", pytest.raises(ValueError, match="grid\nField required"), False),
        ],
    )
    def test_depr(
        self,
        *,
        name: str | None,
        grid: str | None,
        result: str,
        expectation,
        warning: bool,
    ) -> None:
        with expectation, warnings.catch_warnings(record=True) as w:
            m = Meta(name=name, grid=grid, date=dt.date(2020, 1, 1))
            assert m.grid == result
            if warning:
                assert len(w) == 1
                assert w[0].category is DeprecationWarning
                assert str(w[0].message) == "name is deprecated. Use grid instead."
