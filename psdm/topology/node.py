# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from psdm.base import Base


class Node(Base):
    """This class represents a terminal within the grid."""

    name: str
    u_n: float
    description: str | None = None
