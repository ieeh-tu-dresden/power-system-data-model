# :author: Sasan Jacob Rasti <sasan_jacob.rasti@tu-dresden.de>
# :copyright: Copyright (c) Institute of Electrical Power Systems and High Voltage Engineering - TU Dresden, 2022-2023.
# :license: BSD 3-Clause

from pydantic import Field

from psdm.base import Base


class ElementState(Base):
    """This class represents the state of an element which is (partly) disconnected or out of service."""

    name: str
    disabled: bool = False
    open_switches: tuple[str, ...] = Field(default_factory=tuple)
