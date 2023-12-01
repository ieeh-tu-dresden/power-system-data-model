# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from psdm.base import VoltageSystemType
from psdm.quantities.multi_phase import Phase
from psdm.quantities.single_phase import AdmittancePosSeq
from psdm.quantities.single_phase import Current
from psdm.quantities.single_phase import ImpedancePosSeq
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
            phases_1=(Phase.A, Phase.B),
            phases_2=(Phase.A, Phase.B),
            u_n=Voltage(value=1, system_type=SystemType.NATURAL),
            i_r=Current(value=1, system_type=SystemType.NATURAL),
            b1=AdmittancePosSeq(value=1, system_type=SystemType.POSITIVE_SEQUENCE),
            g1=AdmittancePosSeq(value=1, system_type=SystemType.POSITIVE_SEQUENCE),
            x1=ImpedancePosSeq(value=1, system_type=SystemType.POSITIVE_SEQUENCE),
            r1=ImpedancePosSeq(value=1, system_type=SystemType.POSITIVE_SEQUENCE),
            type=BranchType.LINE,
            voltage_system_type=VoltageSystemType.AC,
        )
