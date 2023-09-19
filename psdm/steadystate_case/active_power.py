# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from psdm.steadystate_case.controller import PController
from psdm.topology.load import PowerBase


class ActivePower(PowerBase):
    """This class represents the three phase active power operating point of a load."""

    controller: PController
