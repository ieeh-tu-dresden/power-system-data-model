# :author: Sebastian Krahmer <sebastian.krahmer@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2024.
# :license: BSD 3-Clause

import datetime as dt

from psdm.meta import Meta
from psdm.steadystate_case.case import Case as SteadystateCase
from psdm.topology.topology import Topology
from psdm.topology_case.case import Case as TopologyCase

meta = Meta(
    grid="test_grid",
    date=dt.datetime.now().astimezone().date(),
)


class TestFullSchema:
    def test_init(self) -> None:
        SteadystateCase(meta=meta, loads=[], transformers=[], external_grids=[])

        Topology(
            meta=meta,
            branches=[],
            nodes=[],
            loads=[],
            transformers=[],
            external_grids=[],
        )

        TopologyCase(meta=meta, elements=[])
