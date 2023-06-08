from __future__ import annotations

from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Tuple, final, Union
import pygame
from ..api.app import getCurrentFramerate

Pos = Tuple[float, float]
Color = Union[Tuple[int, int, int], Tuple[int, int, int, int]]

class Positioning(Enum):
    CENTER = 0
    TOPLEFT = 1
    TOPRIGHT = 2
    BOTTOMLEFT = 3
    BOTTOMRIGHT = 4

class DisplayObject:
    def __init__(self, pos: Pos) -> None:
        self.__pos: Pos = pos

    @final
    def setPos(self, pos: Pos) -> DisplayObject:
        self.__pos = pos
        return self

    @final
    def getPos(self) -> Pos:
        return self.__pos

    def doEventSpread(self, pos: Pos) -> bool:
        return False

class InteractiveDisplayObject(DisplayObject):
    def __init__(self, pos: Pos, size: Pos) -> None:
        super().__init__(pos)
        self.__size: Pos = size

    @final
    def getSize(self) -> Pos:
        return self.__size

    @final
    def setSize(self, size: Pos) -> InteractiveDisplayObject:
        self.__size = size
        return self

    def doEventSpread(self, pos: Pos) -> bool:
        cpos = self.getPos()
        return (cpos[0] < pos[0] < cpos[0] + self.__size[0]) and (cpos[1] < pos[1] < cpos[1] + self.__size[1])

    def onMouseDown(self, event) -> None:
        pass

    def onMouseUp(self, event) -> None:
        pass

    def onMouseWheel(self, event) -> None:
        pass

    def onMouseMove(self, event) -> None:
        pass

    def onKeyDown(self, event) -> None:
        pass

    def onKeyUp(self, event) -> None:
        pass

'''class DynamicBase(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.__velocity: Pos = (0, 0)

    @abstractmethod'''
    
class DynamicObject(DisplayObject, metaclass=ABCMeta):
    def __init__(self, pos: Pos) -> None:
        super().__init__(pos)
        self.__velocity: Pos = (0, 0)

    def tick(self):
        pos = self.getPos()
        fps = getCurrentFramerate()
        if fps != None and fps != 0:
            self.setPos((pos[0] + (self.__velocity[0] / fps), pos[1] + (self.__velocity[1] / fps)))

    @abstractmethod
    def getPygameSurface() -> pygame.surface.Surface:
        pass

    @final
    def getVelocity(self) -> Pos:
        return self.__velocity

    @final
    def setVelocity(self, velocity: Pos) -> DynamicObject:
        self.__velocity = velocity
        return self

    @final
    def addVelocity(self, velocity: Pos) -> DynamicObject:
        self.__velocity = (self.__velocity[0] + velocity[0], self.__velocity[1] + velocity[1])
        return self