# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from psdm.base import Base
from psdm.base import UniqueTuple
from psdm.meta import Meta
from psdm.topology_case.element_state import ElementState

if TYPE_CHECKING:
    from psdm.topology.topology import Topology


class Case(Base):
    """This class represents a unique topology case of the grid.

    It is characterized by a list of element which are out of service.
    """

    meta: Meta
    elements: UniqueTuple[ElementState]

    def matches_topology(self, topology: Topology) -> bool:
        logger.info("Verifying topology case ...")
        if topology.meta != self.meta:
            logger.error("Metadata does not match.")
            return False

        if not self._is_proper_elements(topology):
            return False

        logger.info("Verifying topology case was successful.")
        return True

    def _is_proper_elements(self, topology: Topology) -> bool:
        topology_elements = (
            topology.loads + topology.transformers + topology.nodes + topology.branches + topology.external_grids
        )
        topology_element_names = [e.name for e in topology_elements]
        for e in self.elements:
            if e.name not in topology_element_names:
                logger.error("Element {element_name} is not in topology.", element_name=e.name)
                return False

        return True
