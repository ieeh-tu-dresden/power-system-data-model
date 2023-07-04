# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import pydantic

from psdm.base import Base
from psdm.meta import Meta
from psdm.topology.branch import Branch
from psdm.topology.external_grid import ExternalGrid
from psdm.topology.load import Load
from psdm.topology.node import Node
from psdm.topology.transformer import Transformer


class Topology(Base):
    meta: Meta
    branches: pydantic.conset(Branch)  # type: ignore[valid-type]
    nodes: pydantic.conset(Node)  # type: ignore[valid-type]
    loads: pydantic.conset(Load)  # type: ignore[valid-type]
    transformers: pydantic.conset(Transformer)  # type: ignore[valid-type]
    external_grids: pydantic.conset(ExternalGrid)  # type: ignore[valid-type]
