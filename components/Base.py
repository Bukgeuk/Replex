from enum import Enum
from typing import Tuple, final

class Positioning(Enum):
    CENTER = 0
    TOPLEFT = 1
    TOPRIGHT = 2
    BOTTOMLEFT = 3
    BOTTOMRIGHT = 4

class DisplayObject:
    def __init__(self, pos: Tuple[int, int]) -> None:
        self.__pos: Tuple[int, int] = pos

    @final
    def setPos(self, pos: Tuple[int, int]) -> None:
        self.__pos = pos

    @final
    def getPos(self) -> Tuple[int, int]:
        return self.__pos

    def doEventSpread(self, pos: Tuple[int, int]) -> bool:
        return False

class InteractiveDisplayObject(DisplayObject):
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int]) -> None:
        super().__init__(pos)
        self.__size: Tuple[int, int] = size

    @final
    def getSize(self) -> Tuple[int, int]:
        return self.__size

    @final
    def setSize(self, size: Tuple[int, int]) -> None:
        self.__size = size

    def doEventSpread(self, pos: Tuple[int, int]) -> bool:
        return (self.__pos[0] < pos[0] < self.__pos[0] + self.__size[0]) and (self.__pos[1] < pos[1] < self.__pos[1] + self.__size[1])


    def onMouseDown(self, event) -> None:
        pass

    def onMouseUp(self, event) -> None:
        pass

    def onMouseWheel(self, event) -> None:
        pass

    def onMouseMove(self, event) -> None:
        pass