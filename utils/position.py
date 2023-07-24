from typing import Tuple
from enum import Enum

__all__ = ['float2d', 'int2d', 'Position']

float2d = Tuple[float, float]
int2d = Tuple[int, int]

class Position(Enum):
    CENTER = 0
    TOPLEFT = 1
    TOPRIGHT = 2
    BOTTOMLEFT = 3
    BOTTOMRIGHT = 4