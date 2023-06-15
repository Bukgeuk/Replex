from typing import Tuple
from enum import Enum

__all__ = ['Pos', 'Position']

Pos = Tuple[float, float]

class Position(Enum):
    CENTER = 0
    TOPLEFT = 1
    TOPRIGHT = 2
    BOTTOMLEFT = 3
    BOTTOMRIGHT = 4