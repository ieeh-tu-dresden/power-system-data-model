# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import pydantic

from psdm.base import Base


class LoadModel(Base):
    """Load representation based on polynomial model.

    load = load_0*(c_p*(U/U_0)^exp_p + c_i*(U/U_0)^exp_i + (c_z)*(U/U_0)^exp_z)
    c_z = 1 - c_p - c_i
    """

    name: str | None = None
    c_p: pydantic.confloat(ge=0, le=1) = 1.0  # type: ignore[valid-type]
    c_i: pydantic.confloat(ge=0, le=1) = 0.0  # type: ignore[valid-type]
    exp_p: int = 0
    exp_i: int = 1
    exp_z: int = 2

    @pydantic.model_validator(mode="after")  # type: ignore[arg-type]
    def validate_range_c(cls, load_model: LoadModel) -> LoadModel:
        name = load_model.name
        c_p = load_model.c_p
        c_i = load_model.c_i
        if c_p + c_i > 1:
            msg = f"Load model {name!r}: Sum of components must not exceed 1, but {(c_p + c_i)=}."
            raise ValueError(msg)

        return load_model

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def c_z(self) -> float:
        return 1 - self.c_p - self.c_i


CONSTANT_POWER_LM = LoadModel(name="constant_power")
