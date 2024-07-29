# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from psdm.base import Base
from psdm.quantities.multi_phase import ActivePower
from psdm.quantities.multi_phase import Angle
from psdm.quantities.multi_phase import ReactivePower
from psdm.quantities.multi_phase import Voltage


class ExternalGrid(Base):
    """This class represents the operating point of an external grid or a grid subsitute equivalent respectively."""

    name: str
    u_0: Voltage | None = None
    phi_0: Angle | None = None
    p_0: ActivePower | None = None
    q_0: ReactivePower | None = None
