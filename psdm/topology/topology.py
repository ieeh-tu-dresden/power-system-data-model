# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from psdm.base import Base
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
