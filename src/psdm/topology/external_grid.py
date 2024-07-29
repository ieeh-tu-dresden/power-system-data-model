# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from enum import Enum

from psdm.base import Base
from psdm.base import UniqueTuple
from psdm.quantities.multi_phase import Phase
from psdm.quantities.single_phase import ApparentPower


class GridType(Enum):
    SL = "SL"  # slack node: voltage amplitude and phase angle is fixed
    PV = "PV"  # active power and voltage amplitude is fixed
    PQ = "PQ"  # active power and reactive power is fixed


class ExternalGrid(Base):
    """This class represents an external grid or a grid subsitute equivalent respectively.

    It is characterized by a grid type (slack, P-V-node, P-Q-node).
    """

    description: str | None
    name: str
    node: str
    phases: UniqueTuple[Phase]
    short_circuit_power_max: ApparentPower
    short_circuit_power_min: ApparentPower
    type: GridType
