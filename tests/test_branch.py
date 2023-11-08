# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from psdm.base import VoltageSystemType
from psdm.quantities.single_phase import Admittance
from psdm.quantities.single_phase import Current
from psdm.quantities.single_phase import Impedance
from psdm.quantities.single_phase import SystemType
from psdm.quantities.single_phase import Voltage
from psdm.topology.branch import Branch
from psdm.topology.branch import BranchType


class TestBranch:
    def test_init(self) -> None:
        Branch(
            node_1="asd",
            node_2="fgh",
            name="wqertasd",
            u_n=Voltage(value=1, system_type=SystemType.NATURAL),
            i_r=Current(value=1, system_type=SystemType.NATURAL),
            b1=Admittance(value=1, system_type=SystemType.NATURAL),
            g1=Admittance(value=1, system_type=SystemType.NATURAL),
            x1=Impedance(value=1, system_type=SystemType.NATURAL),
            r1=Impedance(value=1, system_type=SystemType.NATURAL),
            type=BranchType.LINE,
            voltage_system_type=VoltageSystemType.AC,
        )
