# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from enum import Enum

from psdm.base import Base
from psdm.base import UniqueTuple
from psdm.base import VoltageSystemType
from psdm.quantities.multi_phase import Phase
from psdm.quantities.single_phase import AdmittanceNat
from psdm.quantities.single_phase import AdmittancePosSeq
from psdm.quantities.single_phase import AdmittanceZerSeq
from psdm.quantities.single_phase import Current
from psdm.quantities.single_phase import Frequency
from psdm.quantities.single_phase import ImpedanceNat
from psdm.quantities.single_phase import ImpedancePosSeq
from psdm.quantities.single_phase import ImpedanceZerSeq
from psdm.quantities.single_phase import Length
from psdm.quantities.single_phase import Voltage


class BranchType(Enum):
    LINE = "LINE"
    COUPLER = "COUPLER"
    FUSE = "FUSE"


class Branch(Base):
    """This class represents a branch adn therefore includes lines, cables or branch fuses.

    It is characterized by a branch type (line, cable or fuse).
    """

    name: str
    node_1: str
    node_2: str
    phases_1: UniqueTuple[Phase]
    phases_2: UniqueTuple[Phase]
    u_n: Voltage  # nominal voltage of the branch connected nodes
    i_r: Current | None  # rated current of branch (thermal limit in continuous operation)
    type: BranchType
    voltage_system_type: VoltageSystemType
    r1: ImpedancePosSeq  # positive sequence values of PI-representation
    x1: ImpedancePosSeq  # positive sequence values of PI-representation
    g1: AdmittancePosSeq  # positive sequence values of PI-representation
    b1: AdmittancePosSeq  # positive sequence values of PI-representation
    r0: ImpedanceZerSeq | None = None  # zero sequence values of PI-representation
    x0: ImpedanceZerSeq | None = None  # zero sequence values of PI-representation
    g0: AdmittanceZerSeq | None = None  # zero sequence values of PI-representation
    b0: AdmittanceZerSeq | None = None  # zero sequence values of PI-representation
    f_n: Frequency | None = None  # nominal frequency the values x and b apply
    description: str | None = None
    energized: bool | None = None
    length: Length | None = None  # length of the line the impedance and admittance values apply
    rn: ImpedanceNat | None = None  # neutral natural values
    xn: ImpedanceNat | None = None  # neutral natural values
    gn: AdmittanceNat | None = None  # neutral natural values
    bn: AdmittanceNat | None = None  # neutral natural values
    rpn: ImpedanceNat | None = None  # neutral-line couple values
    xpn: ImpedanceNat | None = None  # neutral-line couple values
    gpn: AdmittanceNat | None = None  # neutral-line couple values
    bpn: AdmittanceNat | None = None  # neutral-line couple values
