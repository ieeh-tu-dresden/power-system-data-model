# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from psdm.base import VoltageSystemType
from psdm.topology.branch import Branch
from psdm.topology.branch import BranchType
from psdm.topology.quantities import Admittance
from psdm.topology.quantities import Current
from psdm.topology.quantities import Impedance
from psdm.topology.quantities import Voltage


class TestBranch:
    def test_init(self) -> None:
        Branch(
            node_1="asd",
            node_2="fgh",
            name="wqertasd",
            u_n=Voltage(values=(1,)),
            i_r=Current(values=(1,)),
            b1=Admittance(value=1),
            g1=Admittance(value=1),
            x1=Impedance(value=1),
            r1=Impedance(value=1),
            type=BranchType.LINE,
            voltage_system_type=VoltageSystemType.AC,
        )
