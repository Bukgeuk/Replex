from typing import Optional, Tuple, List
from screeninfo import screeninfo
from enum import Enum

__currentFps: Optional[float] = None
__windowSize: Tuple[int, int] = (0, 0)

__all__ = ['renewFramerate', 'getCurrentFramerate', 'getMonitorSize', 'DisplayMode', 'renewWindowSize', 'vw', 'vh']

def renewFramerate(value: float) -> None:
    global __currentFps
    __currentFps = value

def renewWindowSize(value: Tuple[int, int]) -> None:
    global __windowSize
    __windowSize = value

def getCurrentFramerate() -> Optional[float]:
    if not __currentFps is None:
        return __currentFps
    else:
        return None

def getMonitorSize() -> List[Tuple[int, int]]:
    '''
    Return:
        List of (width, height)
    '''
    return [(m.width, m.height) for m in screeninfo.get_monitors()]

def vw(radio: float) -> int:
    '''
    Parameter:
        radio: Float value between 0.0 to 1.0
    '''
    global __windowSize
    if radio >= 1.0:
        return __windowSize[0]
    elif radio <= 0.0:
        return 0
    else:
        return int(__windowSize[0] * radio)
    
def vh(radio: float) -> int:
    '''
    Parameter:
        radio: Float value between 0.0 to 1.0
    '''
    global __windowSize
    if radio >= 1.0:
        return __windowSize[1]
    elif radio <= 0.0:
        return 0
    else:
        return int(__windowSize[1] * radio)


class DisplayMode(Enum):
    WINDOWED = 0
    FULLSCREEN = 1
    NOFRAME = 2
    HIDDEN = 3
