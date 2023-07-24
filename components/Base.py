from __future__ import annotations

from typing import final, Callable, Dict, List, Optional
from ..utils.event import EventType
from ..utils.position import int2d, float2d

__all__ = ['Component', 'InteractiveComponent']

class Component:
    def __init__(self, pos: float2d, size: int2d) -> None:
        self.__pos: float2d = pos
        self.__size: int2d = size
        self.__zIndex: Optional[int] = None

    @final
    @property
    def pos(self) -> float2d:
        return self.__pos

    @final
    @pos.setter
    def pos(self, pos: float2d):
        self.__pos = pos

    @final
    @property
    def size(self) -> int2d:
        return self.__size

    @final
    @size.setter
    def size(self, size: int2d):
        self.__size = size
       
    @final
    @property
    def zIndex(self) -> Optional[int]:
        return self.__zIndex
    
    @final
    @zIndex.setter
    def zIndex(self, zindex: Optional[int]):
        self.__zIndex = zindex

    @final
    def vw(self, radio: float) -> int:
        '''
        Parameter:
            radio: Float value between 0.0 to 1.0
        '''
        if radio >= 1.0:
            return int(self.size[0])
        elif radio <= 0.0:
            return 0
        else:
            return int(self.size[0] * radio)
    
    @final
    def vh(self, radio: float) -> int:
        '''
        Parameter:
            radio: Float value between 0.0 to 1.0
        '''
        if radio >= 1.0:
            return int(self.size[1])
        elif radio <= 0.0:
            return 0
        else:
            return int(self.size[1] * radio)
    
    def doEventSpread(self, pos: float2d) -> bool:
        return False
    

class InteractiveComponent(Component):
    def __init__(self, pos: float2d, size: int2d) -> None:
        super().__init__(pos, size)
        self.__isMouseEntered: bool = False
        self.__eventListeners: Dict[EventType, List[Callable[..., None]]] = {}
        for type in EventType:
            self.__eventListeners[type] = []
    
    @final
    @property
    def isMouseEntered(self) -> bool:
        return self.__isMouseEntered
    
    @final
    def addEventListener(self, eventType: EventType, callback: Callable[..., None]) -> InteractiveComponent:
        self.__eventListeners[eventType].append(callback)
        return self
    
    @final
    def removeEventListener(self, eventType: EventType, callback: Callable[..., None]) -> InteractiveComponent:
        self.__eventListeners[eventType].remove(callback)
        return self

    @final
    def clearEventListeners(self, eventType: EventType) -> InteractiveComponent:
        self.__eventListeners[eventType].clear()
        return self

    def doEventSpread(self, pos: float2d) -> bool:
        cpos = self.pos
        size = self.size
        return (cpos[0] < pos[0] < cpos[0] + size[0]) and (cpos[1] < pos[1] < cpos[1] + size[1])

    def onMouseDown(self, event) -> None:
        for callback in self.__eventListeners[EventType.onMouseDown]:
            callback(event)

    def onMouseUp(self, event) -> None:
        for callback in self.__eventListeners[EventType.onMouseUp]:
            callback(event)

    def onMouseWheel(self, event) -> None:
        for callback in self.__eventListeners[EventType.onMouseWheel]:
            callback(event)

    def onMouseMove(self, event) -> None:
        for callback in self.__eventListeners[EventType.onMouseMove]:
            callback(event)
    
    def onMouseEnter(self, event) -> None:
        '''
        * This event doesn't work on Scene
        '''
        self.__isMouseEntered = True

        for callback in self.__eventListeners[EventType.onMouseEnter]:
            callback(event)

    def onMouseLeave(self, event) -> None:
        '''
        * This event doesn't work on Scene
        '''
        self.__isMouseEntered = False

        for callback in self.__eventListeners[EventType.onMouseLeave]:
            callback(event)

    def onKeyDown(self, event) -> None:
        for callback in self.__eventListeners[EventType.onKeyDown]:
            callback(event)

    def onKeyUp(self, event) -> None:
        for callback in self.__eventListeners[EventType.onKeyUp]:
            callback(event)
    
'''class DynamicObject(DisplayObject, metaclass=ABCMeta):
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
        return self'''