# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import pydantic

from psdm.base import Base
from psdm.meta import Meta
from psdm.topology_case.element_state import ElementState


class Case(Base):
    meta: Meta
    elements: pydantic.conlist(ElementState, unique_items=True)  # type: ignore[valid-type]
