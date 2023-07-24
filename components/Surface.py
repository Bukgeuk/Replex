from __future__ import annotations
from typing import List, Optional, final, Callable
from copy import deepcopy

import pygame

from ..utils.font import getFont
from .Base import InteractiveComponent, int2d, float2d
from ..utils.position import Position
from ..utils.font import Font
from ..utils.color import Color
from .Image import Image
from .Button import Button
from .TextBox import TextBox
from .TextInput import TextInput
from .CameraCapture import CameraCapture
from .Container import Container

__all__ = ['Surface']

class Surface(InteractiveComponent):
    def __init__(self, pos: float2d, size: int2d) -> None:
        super().__init__(pos, size)
        self.__surface = pygame.Surface(size)
        self.__tickObjects: List[Surface] = []
        self.__eventObjects: List[InteractiveComponent] = []
        self.__zIndex: List[List[Callable[..., None]]] = []

    @final
    def render(self):
        for index in self.__zIndex:
            for callback in index:
                callback()
                
        self.__zIndex.clear()

    @final
    def registerDrawing(self, zindex: int, callback: Callable[..., None]):
        if zindex is None or callback is None:
            raise ValueError("Cannot register invalid value")
        
        if self.__zIndex[zindex] is None:
            self.__zIndex[zindex] = []

        self.__zIndex[zindex].append(callback)

    @final
    def getPygameSurface(self):
        return self.__surface

    @final
    def fill(self, color: Color, zindex: Optional[int] = None) -> None:
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.fill(color))
            return

        self.__surface.fill(color.rgba)

    @final
    def drawTextByFont(self, pos: float2d, text: str, font: Font, color: Color, antialias: bool = True, position: Position = Position.TOPLEFT, zindex: Optional[int] = None) -> None:
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawTextByFont(pos, text, font, color, antialias, position))
            return

        image = font.render(text, antialias, color.rgba)
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

        pygame.draw.rect(self.__surface, color.rgba, ((pos[0], pos[1]), (size[0], size[1])), thickness)

    @final
    def drawCircle(self, color: Color, pos: float2d, radius: int, thickness: int = 0, draw_top_right: Optional[bool] = None, draw_top_left: Optional[bool] = None, draw_bottom_left: Optional[bool] = None, draw_bottom_right: Optional[bool] = None, zindex: Optional[int] = None) -> None:
        '''
        if thickness is 0, it will draw filled circle.\n
        nothing will be drawn if the radius is less than 1
        '''
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawCircle(color, pos, radius, thickness, draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right))
            return

        pygame.draw.circle(self.__surface, color.rgba, pos, radius, thickness, draw_top_right, draw_top_left, draw_bottom_right, draw_bottom_left)
    
    @final
    def drawEllipse(self, color: Color, pos: float2d, size: int2d, thickness: int = 0, zindex: Optional[int] = None) -> None:
        '''
        if thickness is 0, it will draw filled ellipse.
        '''
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawEllipse(color, pos, size, thickness))
            return

        pygame.draw.ellipse(self.__surface, color.rgba, ((pos[0], pos[1]), (size[0], size[1])), thickness)

    @final
    def drawLine(self, color: Color, start_pos: float2d, end_pos: float2d, thickness: int = 1, zindex: Optional[int] = None) -> None:
        '''
        if thickness < 1, nothing will be drawn.
        '''
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawLine(color, start_pos, end_pos, thickness))
            return

        pygame.draw.line(self.__surface, color.rgba, start_pos, end_pos, thickness)

    @final
    def drawLines(self, color: Color, points: List[float2d], closed: bool = False, thickness: int = 1, zindex: Optional[int] = None) -> None:
        '''
        if thickness < 1, nothing will be drawn.\n
        if closed is True, an additional line segment is drawn between the first and last points in the points sequence.
        '''
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawLines(color, points, closed, thickness))
            return

        pygame.draw.lines(self.__surface, color.rgba, closed, points, thickness)

    @final
    def drawAntialiasedLine(self, color: Color, start_pos: float2d, end_pos: float2d, blend: int = 1, zindex: Optional[int] = None) -> None:
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawAntialiasedLine(color, start_pos, end_pos, blend))
            return

        pygame.draw.aaline(self.__surface, color.rgba, start_pos, end_pos, blend)

    @final
    def drawAntialiasedLines(self, color: Color, points: List[float2d], closed: bool = False, blend: int = 1, zindex: Optional[int] = None) -> None:
        '''
        if closed is True, an additional line segment is drawn between the first and last points in the points sequence.
        '''
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawAntialiasedLines(color, points, closed, blend))
            return

        pygame.draw.aalines(self.__surface, color.rgba, closed, points, blend)

    '''@final
    def drawDynamicObject(self, obj: DynamicObject):
        surface = obj.getPygameSurface()
        self.__surface.blit(surface, obj.getPos())
        self.__tickObjects.append(obj)'''

    @final
    def drawTextBox(self, textBox: TextBox, zindex: Optional[int] = None):
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawTextBox(textBox))
            return

        size = textBox.size
        b = textBox.borderThickness
        pos = textBox.pos
        font = textBox.font
        self.drawRect(textBox.borderColor, pos, (size[0] + (b * 2), size[1] + (b * 2)))
        self.drawRect(textBox.backgroundColor, (pos[0] + b, pos[1] + b), size)
        if not font is None:
            self.drawTextByFont((pos[0] + (size[0] / 2), pos[1] + (size[1] / 2)), textBox.text, font, textBox.textColor, position=Position.CENTER)

        self.__eventObjects.append(textBox)

    @final
    def drawButton(self, button: Button, zindex: Optional[int] = None):
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawButton(button))
            return

        size = button.size
        b = button.borderThickness
        pos = button.pos
        font = button.font
        self.drawRect(button.borderColor, pos, (size[0] + (b * 2), size[1] + (b * 2)))
        self.drawRect(button.backgroundRenderColor, (pos[0] + b, pos[1] + b), size)
        if not font is None:
            self.drawTextByFont((pos[0] + (size[0] / 2), pos[1] + (size[1] / 2)), button.text, font, button.textRenderColor, position=Position.CENTER)

        self.__eventObjects.append(button)

    @final
    def drawTextInput(self, textInput: TextInput, zindex: Optional[int] = None):
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawTextBox(textInput))
            return

        self.drawTextBox(textInput)

    @final
    def drawCameraCapture(self, capture: CameraCapture, zindex: Optional[int] = None):
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawCameraCapture(capture))
            return
        self.__surface.blit(capture.image, capture.pos)

    @final
    def drawContainer(self, container: Container, zindex: Optional[int] = None):
        if zindex is not None:
            self.registerDrawing(zindex, lambda: self.drawContainer(container))
            return
        
        container.draw()
        container.render()
        self.__surface.blit(container.getPygameSurface(), container.pos)
        self.__tickObjects.append(container)
        self.__eventObjects.append(container)

    def tick(self):
        for obj in self.__tickObjects:
            obj.tick()
        self.__tickObjects.clear()
        self.__eventObjects.clear()

    def onMouseDown(self, event) -> None:
        super().onMouseDown(event)

        for obj in self.__eventObjects:
            if obj.doEventSpread(event.pos):
                obj.onMouseDown(event)

    def onMouseUp(self, event) -> None:
        super().onMouseUp(event)

        for obj in self.__eventObjects:
            if obj.doEventSpread(event.pos):
                obj.onMouseUp(event)

    def onMouseWheel(self, event) -> None:
        super().onMouseWheel(event)
        
        for obj in self.__eventObjects:
            if obj.doEventSpread(event.pos):
                obj.onMouseWheel(event)

    def onMouseMove(self, event) -> None:
        super().onMouseMove(event)

        for obj in self.__eventObjects:
            if obj.doEventSpread(event.pos):
                obj.onMouseMove(event)
                if not obj.isMouseEntered:
                    obj.onMouseEnter(event)
            elif obj.isMouseEntered:
                obj.onMouseLeave(event)

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