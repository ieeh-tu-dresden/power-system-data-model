# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from __future__ import annotations

import enum

from psdm.base import Base
from psdm.base import UniqueTuple
from psdm.quantities.multi_phase import Phase
from psdm.quantities.single_phase import Angle
from psdm.quantities.single_phase import ImpedancePosSeq
from psdm.quantities.single_phase import ImpedanceZerSeq
from psdm.quantities.single_phase import Voltage
from psdm.topology.windings import Winding


class TapSide(enum.Enum):
    HV = "HV"
    MV = "MV"
    LV = "LV"


class TransformerPhaseTechnologyType(enum.Enum):
    SINGLE_PH_E = "SINGLE_PH_E"
    SINGLE_PH = "SINGLE_PH"
    THREE_PH = "THREE_PH"


class VectorGroup(enum.Enum):
    Dd0 = "Dd0"
    Yy0 = "Yy0"
    YNy0 = "YNy0"
    Yyn0 = "Yyn0"
    YNyn0 = "YNyn0"
    Dz0 = "Dz0"
    Dzn0 = "Dzn0"
    Zd0 = "Zd0"
    ZNd0 = "ZNd0"
    Dyn1 = "Dyn1"
    Dy5 = "Dy5"
    Dyn5 = "Dyn5"
    Yd5 = "Yd5"
    YNd5 = "YNd5"
    Yz5 = "Yz5"
    YNz5 = "YNz5"
    Yzn5 = "Yzn5"
    YNzn5 = "YNzn5"
    Dd6 = "Dd6"
    Yy6 = "Yy6"
    YNy6 = "YNy6"
    Yyn6 = "Yyn6"
    YNyn6 = "YNyn6"
    Dz6 = "Dz6"
    Dzn6 = "Dzn6"
    Zd6 = "Zd6"
    ZNd6 = "ZNd6"
    Dyn7 = "Dyn7"
    Dy11 = "Dy11"
    Dyn11 = "Dyn11"
    Yd11 = "Yd11"
    YNd11 = "YNd11"
    Yz11 = "Yz11"
    YNz11 = "YNz11"
    Yzn11 = "Yzn11"
    YNzn11 = "YNzn11"


class Transformer(Base):
    """This class represents a transformer and consists of winding elements.

    It is characterized by windings elements (2w or 3w), the vector group as well as the transformer tap control.
    """

    node_1: str
    node_2: str
    phases_1: UniqueTuple[Phase]
    phases_2: UniqueTuple[Phase]
    name: str
    number: int  # number of parallel units
    vector_group: VectorGroup  # specifier for wiring connection
    windings: UniqueTuple[Winding]  # winding object for each voltage leve
    r_fe1: ImpedancePosSeq  # positive sequence iron losses resistance
    x_h1: ImpedancePosSeq  # positive sequence magnetization reactance
    r_fe0: ImpedanceZerSeq | None = None  # zero sequence iron losses resistance
    x_h0: ImpedanceZerSeq | None = None  # zero sequence magnetisation reactance
    phase_technology_type: TransformerPhaseTechnologyType | None = None  # three- or single-phase-transformer
    description: str | None = None
    tap_u_mag: Voltage | None = None  # voltage deviation per tap position change
    tap_u_phi: Angle | None = None  # voltage angle deviation per tap position
    tap_max: int | None = None  # upper position of tap for tap control
    tap_min: int | None = None  # lower position of tap for tap control
    tap_neutral: int | None = None  # initial position where rated transformation ratio is specified
    tap_side: TapSide | None = None  # transformer side of where tap changer is installed
