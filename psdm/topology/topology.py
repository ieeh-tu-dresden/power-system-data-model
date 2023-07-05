# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import pydantic

from psdm.base import Base
from psdm.base import validate_set
from psdm.meta import Meta
from psdm.topology.branch import Branch
from psdm.topology.external_grid import ExternalGrid
from psdm.topology.load import Load
from psdm.topology.node import Node
from psdm.topology.transformer import Transformer


class Topology(Base):
    meta: Meta
    branches: list[Branch]
    nodes: list[Node]
    loads: list[Load]
    transformers: list[Transformer]
    external_grids: list[ExternalGrid]

    @pydantic.field_validator("branches")
    def validate_branches(cls, value: list[Branch]) -> list[Branch]:
        return validate_set(value)

    @pydantic.field_validator("nodes")
    def validate_nodes(cls, value: list[Node]) -> list[Node]:
        return validate_set(value)

    @pydantic.field_validator("loads")
    def validate_loads(cls, value: list[Load]) -> list[Load]:
        return validate_set(value)

    @pydantic.field_validator("transformers")
    def validate_transformers(cls, value: list[Transformer]) -> list[Transformer]:
        return validate_set(value)

    @pydantic.field_validator("external_grids")
    def validate_external_grids(cls, value: list[ExternalGrid]) -> list[ExternalGrid]:
        return validate_set(value)
