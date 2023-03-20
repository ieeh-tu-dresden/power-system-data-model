# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from psdm.base import Base
from psdm.steadystate_case.active_power import ActivePower
from psdm.steadystate_case.reactive_power import ReactivePower


class Load(Base):  # including assets of type load and generator
    name: str
    active_power: ActivePower
    reactive_power: ReactivePower
