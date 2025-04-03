# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2024.
# :license: BSD 3-Clause

from contextlib import nullcontext as does_not_raise

import pydantic
import pytest

from psdm.base import AttributeData


class TestAttributeData:
    @pytest.mark.parametrize(
        (
            "value",
            "expectation",
        ),
        [
            (1, does_not_raise()),
            (1.1, does_not_raise()),
            (True, does_not_raise()),
            ("value", does_not_raise()),
            ([1, 1], does_not_raise()),
            ([1, "value"], does_not_raise()),
            ([], does_not_raise()),
            (None, pytest.raises(pydantic.ValidationError)),
            (
                {"key": "value"},
                pytest.raises(pydantic.ValidationError),
            ),  # dict is forbidden as is not hashable
            ([1, {"key": "value"}], pytest.raises(pydantic.ValidationError)),
            (
                AttributeData(name="test2", value=1),
                pytest.raises(pydantic.ValidationError),
            ),
            (
                [AttributeData(name="test2", value=2)],
                does_not_raise(),
            ),
            (
                [
                    AttributeData(name="test2", value=2),
                    AttributeData(name="test3", value=3),
                ],
                does_not_raise(),
            ),
            (
                [
                    AttributeData(name="test2", value=2),
                    AttributeData(name="test2", value=2),
                ],
                pytest.raises(pydantic.ValidationError),  # not unique
            ),
            (
                (
                    AttributeData(name="test2", value=2),
                    "string",
                ),
                pytest.raises(
                    pydantic.ValidationError,
                ),  # not tuple of AttributeData only
            ),
        ],
    )
    def test_init(
        self,
        value,
        expectation,
    ) -> None:
        with expectation:
            AttributeData(name="test", value=value)
