from __future__ import annotations

from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Tuple, final, Union, Callable, Dict, List
import pygame
from ..utils.app import getCurrentFramerate

Pos = Tuple[float, float]
Color = Union[Tuple[int, int, int], Tuple[int, int, int, int]]

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

class Positioning(Enum):
    CENTER = 0
    TOPLEFT = 1
    TOPRIGHT = 2
    BOTTOMLEFT = 3
    BOTTOMRIGHT = 4

class DisplayObject:
    def __init__(self, pos: Pos, size: Pos) -> None:
        self.__pos: Pos = pos
        self.__size: Pos = size

    @final
    def setPos(self, pos: Pos) -> DisplayObject:
        self.__pos = pos
        return self
    
    @final
    def getPos(self) -> Pos:
        return self.__pos

    @final
    def setSize(self, size: Pos) -> InteractiveDisplayObject:
        self.__size = size
        return self
    
    @final
    def getSize(self) -> Pos:
        return self.__size
    
    def doEventSpread(self, pos: Pos) -> bool:
        return False

class InteractiveDisplayObject(DisplayObject):
    def __init__(self, pos: Pos, size: Pos) -> None:
        super().__init__(pos, size)
        self.__isMouseEntered: bool = False
        self.__eventHandlers: Dict[EventType, List[Callable[[any]]]] = {}
        for type in EventType:
            self.__eventHandlers[type] = []
    
    @final
    def isMouseEntered(self) -> bool:
        return self.__isMouseEntered
    
    @final
    def addEventHandler(self, eventType: EventType, callback: Callable[[any]]) -> InteractiveDisplayObject:
        self.__eventHandlers[eventType].append(callback)
        return self

    def doEventSpread(self, pos: Pos) -> bool:
        cpos = self.getPos()
        return (cpos[0] < pos[0] < cpos[0] + self.__size[0]) and (cpos[1] < pos[1] < cpos[1] + self.__size[1])

    def onMouseDown(self, event) -> None:
        for callback in self.__eventHandlers[EventType.onMouseDown]:
            callback(event)

    def onMouseUp(self, event) -> None:
        for callback in self.__eventHandlers[EventType.onMouseUp]:
            callback(event)

    def onMouseWheel(self, event) -> None:
        for callback in self.__eventHandlers[EventType.onMouseWheel]:
            callback(event)

    def onMouseMove(self, event) -> None:
        for callback in self.__eventHandlers[EventType.onMouseMove]:
            callback(event)
    
    def onMouseEnter(self, event) -> None:
        '''
        * This event doesn't work on Scene
        '''
        self.__isMouseEntered = True

        for callback in self.__eventHandlers[EventType.onMouseEnter]:
            callback(event)

    def onMouseLeave(self, event) -> None:
        '''
        * This event doesn't work on Scene
        '''
        self.__isMouseEntered = False

        for callback in self.__eventHandlers[EventType.onMouseLeave]:
            callback(event)

    def onKeyDown(self, event) -> None:
        for callback in self.__eventHandlers[EventType.onKeyDown]:
            callback(event)

    def onKeyUp(self, event) -> None:
        for callback in self.__eventHandlers[EventType.onKeyUp]:
            callback(event)

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