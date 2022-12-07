from typing import Optional

_currentFps: Optional[float] = None

def renewFramerate(value: float) -> None:
    global _currentFps
    _currentFps = value

def getCurrentFramerate() -> Optional[float]:
    if not _currentFps is None:
        return _currentFps
    else:
        return None