# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

from enum import Enum

from psdm.base import Base
from psdm.base import VoltageSystemType


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
    u_n: float  # nominal voltage of the branch connected nodes
    i_r: float | None  # rated current of branch (thermal limit in continuous operation)
    r1: float  # positive sequence values of PI-representation
    x1: float  # positive sequence values of PI-representation
    g1: float  # positive sequence values of PI-representation
    b1: float  # positive sequence values of PI-representation
    type: BranchType  # noqa: A003
    voltage_system_type: VoltageSystemType
    r0: float | None = None  # zero sequence values of PI-representation
    x0: float | None = None  # zero sequence values of PI-representation
    g0: float | None = None  # zero sequence values of PI-representation
    b0: float | None = None  # zero sequence values of PI-representation
    f_n: float | None = None  # nominal frequency the values x and b apply
    description: str | None = None
    energized: bool | None = None
    length: float | None = None  # length of the line the impedance and admittance values apply
    rn: float | None = None  # neutral natural values
    xn: float | None = None  # neutral natural values
    gn: float | None = None  # neutral natural values
    bn: float | None = None  # neutral natural values
    rpn: float | None = None  # neutral-line couple values
    xpn: float | None = None  # neutral-line couple values
    gpn: float | None = None  # neutral-line couple values
    bpn: float | None = None  # neutral-line couple values
