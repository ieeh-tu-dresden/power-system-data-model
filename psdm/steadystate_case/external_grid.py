# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from psdm.base import Base


class ExternalGrid(Base):
    """This class represents the operating point of an external grid or a grid subsitute equivalent respectively."""

    name: str
    u_0: float | None = None
    phi_0: float | None = None
    p_0: float | None = None
    q_0: float | None = None
