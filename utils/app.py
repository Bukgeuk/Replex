from typing import Optional, Tuple, List
from screeninfo import screeninfo
from enum import Enum

__currentFps: Optional[float] = None

__all__ = ['renewFramerate', 'getCurrentFramerate', 'getMonitorInfo', 'DisplayMode']

def renewFramerate(value: float) -> None:
    global __currentFps
    __currentFps = value

def getCurrentFramerate() -> Optional[float]:
    if not __currentFps is None:
        return __currentFps
    else:
        return None

def getMonitorInfo() -> List[Tuple[int, int]]:
    '''
    Return:
        List of (width, height)
    '''
    return [(m.width, m.height) for m in screeninfo.get_monitors()]

class DisplayMode(Enum):
    WINDOWED = 0
    FULLSCREEN = 1
    NOFRAME = 2
    HIDDEN = 3
