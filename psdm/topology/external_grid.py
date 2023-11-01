# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from enum import Enum

from psdm.base import Base
from psdm.quantities import PhaseConnections
from psdm.quantities import Power


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
    phase_connections: PhaseConnections
    short_circuit_power_max: Power
    short_circuit_power_min: Power
    type: GridType  # noqa: A003
