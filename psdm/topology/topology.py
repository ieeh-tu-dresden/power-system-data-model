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
    branches: pydantic.conlist(Branch, unique_items=True)  # type: ignore[valid-type]
    nodes: pydantic.conlist(Node, unique_items=True)  # type: ignore[valid-type]
    loads: pydantic.conlist(Load, unique_items=True)  # type: ignore[valid-type]
    transformers: pydantic.conlist(Transformer, unique_items=True)  # type: ignore[valid-type]
    external_grids: pydantic.conlist(ExternalGrid, unique_items=True)  # type: ignore[valid-type]
