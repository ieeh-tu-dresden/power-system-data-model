# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from psdm.base import Base
from psdm.topology.load_model import CONSTANT_POWER_LM
from psdm.topology.load_model import LoadModel


class ReactivePower(Base):
    load_model: LoadModel = CONSTANT_POWER_LM
