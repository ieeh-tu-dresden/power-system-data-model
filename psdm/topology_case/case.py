# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from psdm.base import Base
from psdm.base import UniqueTuple
from psdm.meta import Meta
from psdm.topology_case.element_state import ElementState


class Case(Base):
    """This class represents a unique topology case of the grid.

    It is characterized by a list of element which are out of service.
    """

    meta: Meta
    elements: UniqueTuple[ElementState]
