from enum import Enum

__all__ = ['EventType']

class EventType(Enum):
    RUN = 0
    QUIT = 1
    onMouseDown = 2
    onMouseUp = 3
    onMouseWheel = 4
    onMouseMove = 5
    onMouseEnter = 6
    onMouseLeave = 7
    onKeyDown = 8
    onKeyUp = 9
    onClick = 10