# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from psdm.base import AttributeData
from psdm.base import Base
from psdm.base import UniqueNonEmptyTuple


class Switch(Base):
    """This class represents an imaginary switching element."""

    element: str
    node: str
    state: bool  # 0:opened; 1:closed
    meta: UniqueNonEmptyTuple[AttributeData] | None = None
