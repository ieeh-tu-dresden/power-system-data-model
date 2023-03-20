# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from psdm.base import Base
from psdm.topology.characteristic import Characteristic
from psdm.topology.load_model import LoadModel


class ActivePower(Base):
    load_model: LoadModel | None = None
    characteristic: Characteristic | None = None
