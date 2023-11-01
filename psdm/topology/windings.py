# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum

from psdm.base import Base
from psdm.quantities import ApparentPower
from psdm.quantities import Impedance
from psdm.quantities import PhaseAngleClock
from psdm.quantities import Voltage


class VectorGroup(enum.Enum):
    Y = "Y"
    YN = "YN"
    Z = "Z"
    ZN = "ZN"
    D = "D"


class Winding(Base):
    """This class represents a winding of a transformer.

    For example, a 2-winding transformer has a high and low voltage level winding.
    Each windings is characterized by vector group, which defines the interconnection of the three phases.
    """

    node: str
    s_r: ApparentPower
    u_n: Voltage  # Nominal Voltage of connected nodes (CIM: BaseVoltage)
    u_r: Voltage  # Rated Voltage of the transformer windings itself (CIM: ratedU)
    r1: Impedance  # positive sequence values of transformer T-representation
    x1: Impedance
    r0: Impedance | None = None  # zero sequence values of transformer T-representation
    x0: Impedance | None = None
    re: Impedance | None = None  # earthing of neutral point
    xe: Impedance | None = None  # earthing of neutral point
    phase_angle_clock: PhaseAngleClock | None = None
    vector_group: VectorGroup | None = None
    neutral_connected: bool = False  # indicates if neutral line is connected to winding object
