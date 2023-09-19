# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from psdm.base import Base
from psdm.base import UniqueTuple
from psdm.meta import Meta
from psdm.topology.branch import Branch
from psdm.topology.external_grid import ExternalGrid
from psdm.topology.load import Load
from psdm.topology.node import Node
from psdm.topology.transformer import Transformer


class Topology(Base):
    """This class represents operating point independent topology of a grid.

    It is characterized by list of branches, nodes, loads, transformers and external grids.
    """

    meta: Meta
    branches: UniqueTuple[Branch]
    nodes: UniqueTuple[Node]
    loads: UniqueTuple[Load]
    transformers: UniqueTuple[Transformer]
    external_grids: UniqueTuple[ExternalGrid]
