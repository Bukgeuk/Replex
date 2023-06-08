from typing import Optional, Tuple, List
from screeninfo import screeninfo

_currentFps: Optional[float] = None

def renewFramerate(value: float) -> None:
    global _currentFps
    _currentFps = value

def getCurrentFramerate() -> Optional[float]:
    if not _currentFps is None:
        return _currentFps
    else:
        return None

def getMonitorInfo() -> List[Tuple[int, int]]:
    return [(m.width, m.height) for m in screeninfo.get_monitors()]
