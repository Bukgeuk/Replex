from __future__ import annotations
from typing import List, Optional, final, Callable, overload, TypeVar

from copy import deepcopy

import pygame

from Replex.components.Base import float2d, int2d
from Replex.components.Button import ButtonStyle

from ..utils.font import getFont
from ..utils.app import getCurrentFramerate, getWindowSize
from .Base import InteractiveComponent, int2d, float2d, Component
from ..utils.position import Position
from ..utils.font import Font
from ..utils.color import Color
from .Image import Image
from .Button import Button, Slider
from .TextBox import TextBox
from .TextInput import TextInput
from .CameraCapture import CameraCapture
from ..utils.color import Color, COLORS
from ..utils.style import ComponentStyle
from ..utils.event import EventType
from ..utils.mouse import getMousePos

__all__ = ['Surface', 'Container', 'ScrollBox', 'ScrollBoxStyle', 'Dropdown', 'DropdownStyle']


class Surface(InteractiveComponent):
    @overload
    def __init__(self, pos: float2d, size: int2d) -> None:
        ...

    @overload
    def __init__(self, pos: float2d, pygameSurface: pygame.Surface) -> None:
        ...

    def __init__(self, pos: float2d, value: int2d | pygame.Surface) -> None:
        if isinstance(value, pygame.Surface):
            super().__init__(pos, value.get_size())
            self.__surface = value
        else:
            super().__init__(pos, value)
            self.__surface = pygame.Surface(value)
        
        self.__tickObjects: List[Surface] = []
        self.__eventObjects: List[InteractiveComponent] = []
        self.__zIndexCallbackList: List[List[Callable[..., None]]] = []
        self.__zIndexLock: bool = False
    
    @final
    def render(self):
        self.__zIndexLock = True
        for index in self.__zIndexCallbackList:
            for callback in index:
                callback()
                
        self.__zIndexCallbackList.clear()
        self.__zIndexLock = False

    @final
    def __createTransparentPygameSurface(self) -> pygame.Surface:
        s = pygame.Surface(self.size, pygame.SRCALPHA)
        return s.convert_alpha()

    @final
    def registerDrawing(self, zindex: int, callback: Callable[..., None]):
        if zindex is None or callback is None:
            raise ValueError("Cannot register invalid value")
        elif zindex < 0:
            raise ValueError("z-index must be larger than 0")
        
        if zindex >= len(self.__zIndexCallbackList):
            for _ in range(zindex - len(self.__zIndexCallbackList) + 1):
                self.__zIndexCallbackList.append([])

        self.__zIndexCallbackList[zindex].append(callback)

    @final
    def getPygameSurface(self):
        return self.__surface

    @final
    def fill(self, color: Color, zindex: Optional[int] = None) -> None:
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.fill(color))
            return
        
        s = self.__createTransparentPygameSurface()
        s.fill(color.rgba)
        s.set_alpha(color.rgba[3])
        self.__surface.blit(s, (0,0))

    @final
    def flip(self, flip_x: bool, flip_y: bool) -> None:
        self.__surface = pygame.transform.flip(self.__surface, flip_x, flip_y)

    @final
    def scale(self, size: int2d) -> None:
        self.__surface = pygame.transform.scale(self.__surface, size)
        self.size = self.__surface.get_size()

    @final
    def scale_by(self, factor: float) -> None:
        self.__surface = pygame.transform.scale(self.__surface, (self.size[0] * factor, self.size[1] * factor))
        self.size = self.__surface.get_size()

    @final
    def scale2x(self) -> None:
        '''
        This will return a new image that is double the size of the original.
        It uses the AdvanceMAME Scale2X algorithm which does a 'jaggie-less' scale of bitmap graphics.
        '''
        self.__surface = pygame.transform.scale2x(self.__surface)
        self.size = self.__surface.get_size()

    @final
    def smoothscale(self, size: int2d) -> None:
        self.__surface = pygame.transform.smoothscale(self.__surface, size)
        self.size = self.__surface.get_size()

    @final
    def smoothscale_by(self, factor: float) -> None:
        self.__surface = pygame.transform.smoothscale(self.__surface, (self.size[0] * factor, self.size[1] * factor))
        self.size = self.__surface.get_size()

    @final
    def chop(self, pos: float2d, size: int2d) -> None:
        self.__surface = self.__surface.subsurface((int(pos[0]), int(pos[1]), size[0], size[1]))
        self.size = self.__surface.get_size()

    T = TypeVar("T")
    @final
    def clone(self: T) -> T:
        return deepcopy(self)

    @final
    def drawTextByFont(self, pos: float2d, text: str, font: Font, color: Color, antialias: bool = True, position: Position = Position.TOPLEFT, zindex: Optional[int] = None) -> None:
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawTextByFont(pos, text, font, color, antialias, position))
            return

        image = font.render(text, antialias, color.rgba)
        image.set_alpha(color.rgba[3])

        rect = image.get_rect()
        v = (round(pos[0]), round(pos[1]))

        if position == Position.CENTER:
            rect.center = v
        elif position == Position.TOPLEFT:
            rect.topleft = v
        elif position == Position.TOPRIGHT:
            rect.topright = v
        elif position == Position.BOTTOMLEFT:
            rect.bottomleft = v
        elif position == Position.BOTTOMRIGHT:
            rect.bottomright = v

        self.__surface.blit(image, rect)

    @final
    def drawTextByFontName(self, pos: float2d, text: str, fontName: str, color: Color, antialias: bool = True, position: Position = Position.TOPLEFT, zindex: Optional[int] = None) -> None:
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawTextByFontName(pos, text, fontName, color, antialias, position))
            return
        
        font = getFont(fontName)
        if font is None:
            raise ValueError("invalid font name")
        if font is not None:
            self.drawTextByFont(pos, text, font, color, antialias, position)

    @final
    def drawImage(self, image: Image, zindex: Optional[int] = None):
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawImage(image))
            return

        self.__surface.blit(image.getPygameImage(), image.pos)

    @final
    def drawRect(self, color: Color, pos: float2d, size: int2d, thickness: int = 0, radius: int = -1, top_left_radius: int = -1, top_right_radius: int = -1, bottom_left_radius: int = -1, bottom_right_radius: int = -1, zindex: Optional[int] = None) -> None:
        '''
        if thickness is 0, it will draw filled rectangle.\n
        if top_left_radius, top_right_radius, bottom_left_radius, bottom_right_radius < 0, it will use radius value.\n
        if radius < 1, it will draw rectangle without rounded corners.
        '''
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawRect(color, pos, size, thickness, radius, top_left_radius, top_right_radius, bottom_left_radius, bottom_right_radius))
            return

        s = self.__createTransparentPygameSurface()
        pygame.draw.rect(s, color.rgba, ((pos[0], pos[1]), (size[0], size[1])), thickness)
        s.set_alpha(color.rgba[3])
        self.__surface.blit(s, (0,0))

    @final
    def drawCircle(self, color: Color, pos: float2d, radius: int, thickness: int = 0, draw_top_right: Optional[bool] = None, draw_top_left: Optional[bool] = None, draw_bottom_left: Optional[bool] = None, draw_bottom_right: Optional[bool] = None, zindex: Optional[int] = None) -> None:
        '''
        if thickness is 0, it will draw filled circle.\n
        nothing will be drawn if the radius is less than 1
        '''
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawCircle(color, pos, radius, thickness, draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right))
            return

        s = self.__createTransparentPygameSurface()
        pygame.draw.circle(s, color.rgba, pos, radius, thickness, draw_top_right, draw_top_left, draw_bottom_right, draw_bottom_left)
        s.set_alpha(color.rgba[3])
        self.__surface.blit(s, (0,0))
    
    @final
    def drawEllipse(self, color: Color, pos: float2d, size: int2d, thickness: int = 0, zindex: Optional[int] = None) -> None:
        '''
        if thickness is 0, it will draw filled ellipse.
        '''
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawEllipse(color, pos, size, thickness))
            return

        s = self.__createTransparentPygameSurface()
        pygame.draw.ellipse(s, color.rgba, ((pos[0], pos[1]), (size[0], size[1])), thickness)
        s.set_alpha(color.rgba[3])
        self.__surface.blit(s, (0,0))

    @final
    def drawLine(self, color: Color, start_pos: float2d, end_pos: float2d, thickness: int = 1, zindex: Optional[int] = None) -> None:
        '''
        if thickness < 1, nothing will be drawn.
        '''
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawLine(color, start_pos, end_pos, thickness))
            return

        s = self.__createTransparentPygameSurface()
        pygame.draw.line(s, color.rgba, start_pos, end_pos, thickness)
        s.set_alpha(color.rgba[3])
        self.__surface.blit(s, (0,0))

    @final
    def drawLines(self, color: Color, points: List[float2d], closed: bool = False, thickness: int = 1, zindex: Optional[int] = None) -> None:
        '''
        if thickness < 1, nothing will be drawn.\n
        if closed is True, an additional line segment is drawn between the first and last points in the points sequence.
        '''
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawLines(color, points, closed, thickness))
            return

        s = self.__createTransparentPygameSurface()
        pygame.draw.lines(s, color.rgba, closed, points, thickness)
        s.set_alpha(color.rgba[3])
        self.__surface.blit(s, (0,0))

    @final
    def drawAntialiasedLine(self, color: Color, start_pos: float2d, end_pos: float2d, blend: int = 1, zindex: Optional[int] = None) -> None:
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawAntialiasedLine(color, start_pos, end_pos, blend))
            return

        s = self.__createTransparentPygameSurface()
        pygame.draw.aaline(s, color.rgba, start_pos, end_pos, blend)
        s.set_alpha(color.rgba[3])
        self.__surface.blit(s, (0,0))

    @final
    def drawAntialiasedLines(self, color: Color, points: List[float2d], closed: bool = False, blend: int = 1, zindex: Optional[int] = None) -> None:
        '''
        if closed is True, an additional line segment is drawn between the first and last points in the points sequence.
        '''
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawAntialiasedLines(color, points, closed, blend))
            return

        s = self.__createTransparentPygameSurface()
        pygame.draw.aalines(s, color.rgba, closed, points, blend)
        s.set_alpha(color.rgba[3])
        self.__surface.blit(s, (0,0))

    '''@final
    def drawDynamicObject(self, obj: DynamicObject):
        surface = obj.getPygameSurface()
        self.__surface.blit(surface, obj.getPos())
        self.__tickObjects.append(obj)'''

    @final
    def drawTextBox(self, textBox: TextBox, zindex: Optional[int] = None):
        if not self.__zIndexLock:
            textBox.zIndex = zindex

        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawTextBox(textBox))
            return

        size = textBox.size
        b = textBox.borderThickness
        pos = textBox.pos
        font = textBox.font
        r = textBox.radius
        if textBox.borderColor is not None:
            self.drawRect(textBox.borderColor, pos, (size[0] + (b * 2), size[1] + (b * 2)), radius=r)
        if textBox.backgroundColor is not None:
            self.drawRect(textBox.backgroundColor, (pos[0] + b, pos[1] + b), size, radius=r)
        if font is not None:
            self.drawTextByFont((pos[0] + (size[0] / 2), pos[1] + (size[1] / 2)), textBox.text, font, textBox.textColor, position=Position.CENTER)

        self.__eventObjects.append(textBox)

    @final
    def drawButton(self, button: Button, zindex: Optional[int] = None):
        if not self.__zIndexLock:
            button.zIndex = zindex

        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawButton(button))
            return

        size = button.size
        b = button.borderThickness
        pos = button.pos
        font = button.font
        r = button.radius
        if button.borderColor is not None:
            self.drawRect(button.borderColor, pos, (size[0] + (b * 2), size[1] + (b * 2)), radius=r)
        if button.backgroundRenderColor is not None:
            self.drawRect(button.backgroundRenderColor, (pos[0] + b, pos[1] + b), size, radius=r)
        if font is not None:
            self.drawTextByFont((pos[0] + (size[0] / 2), pos[1] + (size[1] / 2)), button.text, font, button.textRenderColor, position=Position.CENTER)

        self.__eventObjects.append(button)

    @final
    def drawTextInput(self, textInput: TextInput, zindex: Optional[int] = None):
        if not self.__zIndexLock:
            textInput.zIndex = zindex

        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawTextBox(textInput))
            return

        self.drawTextBox(textInput)

    @final
    def drawCameraCapture(self, capture: CameraCapture, zindex: Optional[int] = None):
        if not self.__zIndexLock:
            capture.zIndex = zindex

        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawCameraCapture(capture))
            return
        self.__surface.blit(capture.image, capture.pos)

    @final
    def drawContainer(self, container: Container, zindex: Optional[int] = None):
        if not self.__zIndexLock:
            container.zIndex = zindex

        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawContainer(container))
            return
        
        container.draw()
        container.render()
        self.__surface.blit(container.getPygameSurface(), container.pos)
        self.__tickObjects.append(container)
        self.__eventObjects.append(container)

    @final
    def drawScrollBox(self, scrollBox: ScrollBox, zindex: Optional[int] = None):
        if not self.__zIndexLock:
            scrollBox.zIndex = zindex

        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawScrollBox(scrollBox))
            return

        self.__surface.blit(scrollBox.render().getPygameSurface(), scrollBox.pos)
        self.__tickObjects.append(scrollBox)
        self.__eventObjects.append(scrollBox)
        self.addEventListener(EventType.onMouseUp, scrollBox.onScrollBarDragEnd)
        self.addEventListener(EventType.onMouseMove, scrollBox.onScrollBarDragging)

    @final
    def drawDropdown(self, dropdown: Dropdown, zindex: Optional[int] = None):
        if not self.__zIndexLock:
            dropdown.zIndex = zindex

        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawDropdown(dropdown))
            return
        
        btn = dropdown.getButton()
        self.drawButton(btn)
        if dropdown.isOpened:
            box = dropdown.getScrollBox()
            up = btn.pos[1]
            down = getWindowSize()[1] - btn.pos[1] - btn.size[1]

            if (down > box.size[1]) or (down < box.size[1] and up < box.size[1] and down > up):
                box.pos = (btn.pos[0], btn.pos[1] + btn.size[1])
            elif (up > box.size[1]) or (down < box.size[1] and up < box.size[1] and down < up):
                box.pos = (btn.pos[0], btn.pos[1] - box.size[1])

            box.contents = [Container.buildByCenteredText(box.elementSize, dropdown.items[i], dropdown.font, dropdown.itemTextColor, (dropdown.itemHoverColor if dropdown.hoveredIndex == i else dropdown.itemBackgroundColor)) for i in range(0, dropdown.numOfItems)]

            self.drawScrollBox(box)

    @final
    def drawSlider(self, slider: Slider, zindex: Optional[int] = None):
        if not self.__zIndexLock:
            slider.zIndex = zindex

        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawSlider(slider))
            return
        
        handle = slider.getHandle()
        p = slider.pos
        hs = slider.handleSize
        s = slider.size
        r = slider.sliderRadius
        drawpos = (p[0] - (hs[0] / 2), p[1])
        drawsize = (s[0] + hs[0], s[1])
        c = Container(drawpos, drawsize)
        c.drawRect(slider.sliderFilledColor, (0, 0), drawsize, radius=r)
        c.chop((0, 0), (s[0] * slider.value + (hs[0] / 2), s[1]))
        self.drawRect(slider.sliderColor, drawpos, drawsize, radius=r)
        self.drawContainer(c)
        
        self.addEventListener(EventType.onMouseMove, slider.onHandlerMouseMove)
        self.addEventListener(EventType.onMouseUp, slider.onHandlerMouseUp)
        self.__eventObjects.append(slider)

        self.drawButton(handle)

    def tick(self):
        for obj in self.__tickObjects:
            obj.tick()
        self.__tickObjects.clear()
        self.__eventObjects.clear()

    def onMouseDown(self, event) -> None:
        super().onMouseDown(event)

        temp: Optional[Component] = None

        for obj in self.__eventObjects:
            if obj.doEventSpread(event.pos):
                if temp is None:
                    temp = obj
                elif temp.zIndex is None:
                    temp = obj
                elif temp.zIndex is not None and obj.zIndex is not None:
                    if temp.zIndex <= obj.zIndex:
                        temp = obj
        
        if temp is not None:
            temp.onMouseDown(event)

    def onMouseUp(self, event) -> None:
        super().onMouseUp(event)

        temp: Optional[Component] = None

        for obj in self.__eventObjects:
            if obj.doEventSpread(event.pos):
                if temp is None:
                    temp = obj
                elif temp.zIndex is None:
                    temp = obj
                elif temp.zIndex is not None and obj.zIndex is not None:
                    if temp.zIndex <= obj.zIndex:
                        temp = obj
        
        if temp is not None:
            temp.onMouseUp(event)

    def onMouseWheel(self, event) -> None:
        super().onMouseWheel(event)
        
        temp: Optional[Component] = None

        for obj in self.__eventObjects:
            if obj.doEventSpread(getMousePos()):
                if temp is None:
                    temp = obj
                elif temp.zIndex is None:
                    temp = obj
                elif temp.zIndex is not None and obj.zIndex is not None:
                    if temp.zIndex <= obj.zIndex:
                        temp = obj
        
        if temp is not None:
            temp.onMouseWheel(event)

    def onMouseMove(self, event) -> None:
        super().onMouseMove(event)

        temp: Optional[Component] = None

        for obj in self.__eventObjects:
            if obj.doEventSpread(event.pos):
                if temp is None:
                    temp = obj
                elif temp.zIndex is None:
                    temp = obj
                elif temp.zIndex is not None and obj.zIndex is not None:
                    if temp.zIndex <= obj.zIndex:
                        temp = obj
            elif obj.isMouseEntered:
                obj.onMouseLeave(event)
        
        if temp is not None:
            temp.onMouseMove(event)
            if not temp.isMouseEntered:
                temp.onMouseEnter(event)

    def onMouseEnter(self, event) -> None:
        super().onMouseEnter(event)

    def onMouseLeave(self, event) -> None:
        super().onMouseLeave(event)

    def onKeyDown(self, event) -> None:
        super().onKeyDown(event)

        for obj in self.__eventObjects:
            obj.onKeyDown(event)

    def onKeyUp(self, event) -> None:
        super().onKeyUp(event)

        for obj in self.__eventObjects:
            obj.onKeyUp(event)

class Container(Surface):
    @overload
    def __init__(self, pos: float2d, size: int2d) -> None:
        ...

    @overload
    def __init__(self, pos: float2d, image: Image) -> None:
        ...

    @overload
    def __init__(self, pos: float2d, pygameSurface: pygame.Surface) -> None:
        ...

    def __init__(self, pos: float2d, value: int2d | pygame.Surface | Image) -> None:
        if isinstance(value, Image):
            super().__init__(pos, value.getPygameImage())
        else:
            super().__init__(pos, value)

    @staticmethod
    @final
    def buildByText(size: int2d, textPos: float2d, text: str, font: Font | str, textColor: Color, backgroundColor: Optional[Color] = None, antialias: bool = True, position: Position = Position.TOPLEFT) -> Container:
        obj = Container((0, 0), size)
        if backgroundColor is not None:
            obj.fill(backgroundColor)

        if isinstance(font, str):
            obj.drawTextByFontName(textPos, text, font, textColor, antialias, position)
        else:
            obj.drawTextByFont(textPos, text, font, textColor, antialias, position)

        return obj
    
    @staticmethod
    @final
    def buildByCenteredText(size: int2d, text: str, font: Font | str, textColor: Color, backgroundColor: Optional[Color] = None, antialias: bool = True) -> Container:
        return Container.buildByText(size, (size[0] / 2, size[1] / 2), text, font, textColor, backgroundColor, antialias, Position.CENTER)

    def draw(self):
        pass

    def tick(self):
        super().tick()

class ScrollBoxStyle(ComponentStyle):
    scrollbarWidth: int
    elementHeight: int
    radius: int
    scrollbarColor: Color
    backgroundColor: Optional[Color]

    def __init__(self, scrollbarColor: Color = COLORS.GRAY, scrollbarWidth: int = 5, elementHeight: int = 100, radius: int = -1, backgroundColor: Optional[Color] = None) -> None:
        super().__init__()
        self.scrollbarColor = scrollbarColor
        self.scrollbarWidth = scrollbarWidth
        self.elementHeight = elementHeight
        self.backgroundColor = backgroundColor
        self.radius = radius

class ScrollBox(InteractiveComponent):
    def __init__(self, pos: float2d, size: int2d, style: ScrollBoxStyle, friction: float = 50, wheel: float = 50, contents: List[Container] = []) -> None:
        super().__init__(pos, size)
        self.__scrollbarWidth = style.scrollbarWidth
        self.__scrollbarColor = style.scrollbarColor
        self.__backgroundColor = style.backgroundColor
        self.__elementSize = (size[0] - style.scrollbarWidth, style.elementHeight)
        self.__friction = friction
        self.__wheel = wheel
        self.__radius = style.radius
        self.__contents: List[Container] = []
        for content in contents:
            if (content.size[0] > self.__elementSize[0]) or (content.size[1] > self.__elementSize[1]):
                self.__contents.append(content.chop((0, 0), self.__elementSize))
            else:
                self.__contents.append(content)

        self.__offset: float = 0

        self.__startpos: Optional[tuple[int, int]] = None
        self.__dragpos: Optional[tuple[int, int]] = None
        self.__bardragpos: Optional[tuple[int, int]] = None
        self.__tickcount: int = 0
        self.__speedPerTick: float = 0

        self.__clickHandler: Optional[Callable[[int], None]] = None
        self.__hoverHandler: Optional[Callable[[Optional[int]], None]] = None
        self.__lastHoveredIdx: Optional[int] = None

    def clone(self) -> ScrollBox:
        return deepcopy(self)

    @property
    def numOfContents(self) -> int:
        return len(self.__contents)
    
    @property
    def contents(self) -> List[Container]:
        return self.__contents
    
    @contents.setter
    def contents(self, contents: List[Container]) -> None:
        self.__contents = contents

    @property
    def scrollbarWidth(self) -> int:
        return self.__scrollbarWidth
    
    @scrollbarWidth.setter
    def scrollbarWidth(self, value: int):
        self.__scrollbarWidth = value

    @property
    def scrollbarColor(self) -> Color:
        return self.__scrollbarColor
    
    @scrollbarColor.setter
    def scrollbarColor(self, value: Color):
        self.__scrollbarColor = value

    @property
    def contentBackgroundColor(self) -> Optional[Color]:
        return self.__contentBackgroundColor
    
    @contentBackgroundColor.setter
    def contentBackgroundColor(self, value: Optional[Color]):
        self.__contentBackgroundColor = value

    @property
    def elementSize(self) -> int2d:
        return self.__elementSize
    
    @property
    def offset(self) -> int:
        return int(self.__offset)
    
    @property
    def maxOffset(self) -> int:
        value = self.numOfContents * self.elementSize[1] - self.size[1]
        return 0 if value < 0 else value
    
    @property
    def scrollBarLength(self) -> int:
        if self.maxOffset == 0: return self.size[1]
        else: return int(self.size[1] / (self.maxOffset / self.size[1]))
    
    @property
    def scrollBarOffset(self) -> int:
        if self.maxOffset == 0: return 0
        else: return (self.offset / self.maxOffset) * (self.size[1] - self.scrollBarLength)
    
    @final
    def setClickHandler(self, handler: Callable[[int], None]) -> None:
        self.__clickHandler = handler

    @final
    def setHoverHandler(self, handler: Callable[[Optional[int]], None]) -> None:
        self.__hoverHandler = handler
    
    @final
    def append(self, content: Container) -> None:
        self.__contents.append(content)

    @final
    def pop(self, idx: int) -> None:
        if (idx >= 0 and idx >= len(self.__contents)) or (idx < 0 and idx < -len(self.__contents)):
            raise IndexError("list index out of range")
        else:
            self.__contents.pop(idx)
        
    @final
    def remove(self, content: Container) -> None:
        self.__contents.remove(content)

    def onMouseWheel(self, event) -> None:
        boxMove = -(event.y * self.__wheel)

        if self.offset + boxMove < 0: self.__offset = 0
        elif self.offset + boxMove > self.maxOffset: self.__offset = self.maxOffset
        else: self.__offset += boxMove

        return super().onMouseWheel(event)

    def onMouseLeave(self, event) -> None:
        if self.__startpos is not None:
            self.__speedPerTick = (self.__startpos[1] - event.pos[1]) / self.__tickcount
        self.__startpos = None
        self.__dragpos = None
        return super().onMouseLeave(event)
    
    def onMouseMove(self, event) -> None:
        if (self.pos[0] < event.pos[0] < self.pos[0] + self.elementSize[0]) and (self.pos[1] < event.pos[1] < self.pos[1] + self.size[1]):
            idx = int(self.offset + (event.pos[1] - self.pos[1]) / self.elementSize[1])
            if self.__hoverHandler is not None:            
                self.__hoverHandler(idx)
                self.__lastHoveredIdx = idx

            if self.__dragpos is not None:
                boxMove = self.__dragpos[1] - event.pos[1]
                if self.offset + boxMove < 0: self.__offset = 0
                elif self.offset + boxMove > self.maxOffset: self.__offset = self.maxOffset
                else: self.__offset += boxMove
                self.__dragpos = event.pos
        elif self.__lastHoveredIdx is not None and self.__hoverHandler is not None:
            self.__hoverHandler(None)
            self.__lastHoveredIdx = None

        return super().onMouseMove(event)
    
    @final
    def onScrollBarDragEnd(self, event) -> None:
        if event.button == 1:
            self.__bardragpos = None

    @final
    def onScrollBarDragging(self, event) -> None:
        if self.__bardragpos is not None:
            barMove = event.pos[1] - self.__bardragpos[1]
            boxMove = barMove * (self.maxOffset / self.size[1])
            if self.scrollBarOffset + barMove < 0: self.__offset = 0
            elif self.scrollBarOffset + barMove > self.size[1] - self.scrollBarLength : self.__offset = self.maxOffset
            else: self.__offset += boxMove
            self.__bardragpos = event.pos
    
    def onMouseDown(self, event) -> None:
        if event.button == 1 and (self.pos[1] < event.pos[1] < self.pos[1] + self.size[1]):
            if self.pos[0] < event.pos[0] < self.pos[0] + self.elementSize[0]:
                self.__tickcount = 1
                self.__speedPerTick = 0
                self.__startpos = event.pos
                self.__dragpos = event.pos
            elif self.pos[0] + self.elementSize[0] < event.pos[0] < self.pos[0] + self.size[0]:
                self.__bardragpos = event.pos
        
        return super().onMouseDown(event)
    
    def onClick(self, event) -> None:
        if event.button == 1 and (self.pos[0] < event.pos[0] < self.pos[0] + self.elementSize[0]) and (self.pos[1] < event.pos[1] < self.pos[1] + self.size[1]) and self.__clickHandler is not None:
            idx = int(self.offset + (event.pos[1] - self.pos[1]) / self.elementSize[1])                        
            self.__clickHandler(idx)
        return super().onClick(event)
    
    def onMouseUp(self, event) -> None:
        if event.button == 1:
            if (self.pos[0] < event.pos[0] < self.pos[0] + self.elementSize[0]) and (self.pos[1] < event.pos[1] < self.pos[1] + self.size[1]) and self.__startpos is not None:
                self.__speedPerTick = (self.__startpos[1] - event.pos[1]) / self.__tickcount       
            
            self.__startpos = None
            self.__dragpos = None
        
        return super().onMouseUp(event)
    
    def tick(self) -> None:
        if self.__startpos is not None:
            self.__tickcount += 1

        if self.__speedPerTick > 0 and (self.__offset + self.__speedPerTick > self.maxOffset):
            self.__offset = self.maxOffset
            self.__speedPerTick = 0
        elif self.__speedPerTick < 0 and (self.__offset + self.__speedPerTick < 0):
            self.__offset = 0
            self.__speedPerTick = 0
        else:
            framerate = getCurrentFramerate()
            if framerate == 0: return
            friction = self.__friction / framerate
            self.__offset += self.__speedPerTick

            if self.__speedPerTick > 0:
                if self.__speedPerTick < friction: self.__speedPerTick = 0
                else: self.__speedPerTick -= friction
            elif self.__speedPerTick < 0:
                if -self.__speedPerTick < friction: self.__speedPerTick = 0
                else: self.__speedPerTick += friction

    def render(self) -> Container:
        l = self.elementSize[1] * self.numOfContents
        box = Container(self.pos, (self.size[0], l if l > self.size[1] else self.size[1]))
        if self.__backgroundColor is not None:
            box.fill(self.__backgroundColor)

        for i in range(0, self.numOfContents):
            content = self.__contents[i]
            if content.size[0] > self.elementSize[0] or content.size[1] > self.elementSize[1]:
                raise ValueError("Size of Element doesn't match elementSize")
            content.pos = (0, self.elementSize[1] * i)
            box.drawContainer(content)
        
        box.chop((0, self.offset), self.size)
        box.drawRect(self.scrollbarColor, (self.elementSize[0], self.scrollBarOffset), (self.scrollbarWidth, self.scrollBarLength), radius=self.__radius)

        return box

class DropdownStyle(ComponentStyle):
    buttonStyle: ButtonStyle
    scrollBoxStyle: ScrollBoxStyle
    font: Font | str
    itemTextColor: Color
    itemBackgroundColor: Color
    itemHoverColor: Color

    def __init__(self, buttonStyle: ButtonStyle, scrollBoxStyle: ScrollBoxStyle, font: Font | str, itemTextColor: Color, itemBackgroundColor: Color, itemHoverColor: Color) -> None:
        self.buttonStyle = buttonStyle
        self.scrollBoxStyle = scrollBoxStyle
        self.font = font
        self.itemBackgroundColor = itemBackgroundColor
        self.itemHoverColor = itemHoverColor
        self.itemTextColor = itemTextColor

class Dropdown(Component):
    def __init__(self, pos: float2d, buttonSize: int2d, scrollBoxSize: int2d, style: DropdownStyle, items: List[str], default: int = 0) -> None:
        if len(items) == 0:
            raise ValueError("Dropdown must have at least one item")

        super().__init__(pos, (0, 0))
        self.__items: List[str] = items
        self.__value: int = default
        self.__itemTextColor = style.itemTextColor
        self.__itemHoverColor = style.itemHoverColor
        self.__itemBackgroundColor = style.itemBackgroundColor
        self.__font: Font | None

        if type(style.font) is str:
            self.__font = getFont(style.font)
        elif type(style.font) is Font:
            self.__font = style.font

        self.__btn = Button(pos, buttonSize, style.buttonStyle, items[default])
        self.__box = ScrollBox((0, 0), scrollBoxSize, style.scrollBoxStyle, contents=[])

        self.__hoveridx: Optional[int] = None
        self.__box.setHoverHandler(self.onItemHover)
        self.__box.setClickHandler(self.onItemClick)
        self.__btn.addEventListener(EventType.onClick, self.onButtonClick)

        self.__isOpened: bool = False

    def onItemHover(self, idx: Optional[int]) -> None:
        self.__hoveridx = idx

    def onItemClick(self, idx: int) -> None:
        self.__value = idx
        self.__btn.text = self.__items[idx]
        self.__isOpened = False

    def onButtonClick(self, event) -> None:
        self.__isOpened = True
        self.__hoveridx = None

    @final
    def getButton(self) -> Button:
        return self.__btn
    
    @final
    def getScrollBox(self) -> ScrollBox:
        return self.__box
    
    @property
    def numOfItems(self) -> int:
        return len(self.__items)

    @property
    def items(self) -> List[str]:
        return self.__items
    
    @property
    def indexValue(self) -> int:
        return self.__value
    
    @property
    def strValue(self) -> str:
        return self.__items[self.__value]
    
    @property
    def isOpened(self) -> bool:
        return self.__isOpened
    
    @property
    def hoveredIndex(self) -> int:
        return self.__hoveridx
     
    @property
    def font(self) -> Optional[Font]:
        return self.__font
    
    @font.setter
    def font(self, font: Font | str):
        if type(font) is str:
            self.__font = getFont(font)
        elif type(font) is Font:
            self.__font = font

    @property
    def itemTextColor(self) -> Color:
        return self.__itemTextColor
    
    @itemTextColor.setter
    def itemTextColor(self, color: Color) -> None:
        self.__itemTextColor = color

    @property
    def itemHoverColor(self) -> Color:
        return self.__itemHoverColor
    
    @itemHoverColor.setter
    def itemHoverColor(self, color: Color) -> None:
        self.__itemHoverColor = color

    @property
    def itemBackgroundColor(self) -> Color:
        return self.__itemBackgroundColor
    
    @itemBackgroundColor.setter
    def itemBackgroundColor(self, color: Color) -> None:
        self.__itemBackgroundColor = color
    
    @final
    def append(self, item: str) -> None:
        self.__items.append(item)

    @final
    def pop(self, idx: int) -> None:
        if (idx >= 0 and idx >= len(self.__items)) or (idx < 0 and idx < -len(self.__items)):
            raise IndexError("list index out of range")
        else:
            self.__items.pop(idx)
    
    @final
    def remove(self, item: Container) -> None:
        self.__items.remove(item)