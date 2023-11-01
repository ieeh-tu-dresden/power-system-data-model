# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from enum import Enum

from psdm.base import Base
from psdm.base import VoltageSystemType
from psdm.quantities import Admittance
from psdm.quantities import Current
from psdm.quantities import Frequency
from psdm.quantities import Impedance
from psdm.quantities import Length
from psdm.quantities import Voltage


class BranchType(Enum):
    LINE = "LINE"
    COUPLER = "COUPLER"
    FUSE = "FUSE"


class Branch(Base):
    """This class represents a branch adn therefore includes lines, cables or branch fuses.

    It is characterized by a branch type (line, cable or fuse).
    """

    node_1: str
    node_2: str
    name: str
    u_n: Voltage  # nominal voltage of the branch connected nodes
    i_r: Current | None  # rated current of branch (thermal limit in continuous operation)
    r1: Impedance  # positive sequence values of PI-representation
    x1: Impedance  # positive sequence values of PI-representation
    g1: Admittance  # positive sequence values of PI-representation
    b1: Admittance  # positive sequence values of PI-representation
    type: BranchType  # noqa: A003
    voltage_system_type: VoltageSystemType
    r0: Impedance | None = None  # zero sequence values of PI-representation
    x0: Impedance | None = None  # zero sequence values of PI-representation
    g0: Admittance | None = None  # zero sequence values of PI-representation
    b0: Admittance | None = None  # zero sequence values of PI-representation
    f_n: Frequency | None = None  # nominal frequency the values x and b apply
    description: str | None = None
    energized: bool | None = None
    length: Length | None = None  # length of the line the impedance and admittance values apply
    rn: Impedance | None = None  # neutral natural values
    xn: Impedance | None = None  # neutral natural values
    gn: Admittance | None = None  # neutral natural values
    bn: Admittance | None = None  # neutral natural values
    rpn: Impedance | None = None  # neutral-line couple values
    xpn: Impedance | None = None  # neutral-line couple values
    gpn: Admittance | None = None  # neutral-line couple values
    bpn: Admittance | None = None  # neutral-line couple values
