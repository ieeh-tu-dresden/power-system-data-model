# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from psdm.base import Base


class Coupler(Base):
    """This class represents physically existing switching element, e.g. a circuit breaker or a disconnector."""

    element: str
    node: str
    state: bool  # 0:opened; 1:closed
