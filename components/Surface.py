from __future__ import annotations
from typing import List, Optional, final

import pygame

from ..utils.font import getFont
from .Base import InteractiveComponent, Pos
from ..utils.position import Position
from ..utils.font import Font
from ..utils.color import Color
from .Image import Image
from .Button import Button
from .TextBox import TextBox
from .TextInput import TextInput

__all__ = ['Surface']

class Surface(InteractiveComponent):
    def __init__(self, pos: Pos, size: Pos) -> None:
        super().__init__(pos, size)
        self.__surface = pygame.Surface(size)
        self.__tickObjects: List[Surface] = []
        self.__eventObjects: List[InteractiveComponent] = []

    @final
    def getPygameSurface(self):
        return self.__surface

    @final
    def fill(self, color: Color) -> None:
        self.__surface.fill(color.rgba)

    @final
    def drawTextByFont(self, pos: Pos, text: str, font: Font, color: Color, antialias: bool = True, position: Position = Position.TOPLEFT) -> None:
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
    def drawTextByFontName(self, pos: Pos, text: str, fontName: str, color: Color, antialias: bool = True, position: Position = Position.TOPLEFT) -> None:
        font = getFont(fontName)
        if font is not None:
            self.drawTextByFont(pos, text, font, color, antialias, position)

    @final
    def drawImage(self, image: Image):
        self.__surface.blit(image.getPygameImage(), image.getPos())

    @final
    def drawRect(self, color: Color, pos: Pos, size: Pos, thickness: int = 0, radius: int = -1, top_left_radius: int = -1, top_right_radius: int = -1, bottom_left_radius: int = -1, bottom_right_radius: int = -1) -> None:
        '''
        if thickness is 0, it will draw filled rectangle.\n
        if top_left_radius, top_right_radius, bottom_left_radius, bottom_right_radius < 0, it will use radius value.\n
        if radius < 1, it will draw rectangle without rounded corners.
        '''
        pygame.draw.rect(self.__surface, color.rgba, ((pos[0], pos[1]), (size[0], size[1])), thickness)

    @final
    def drawCircle(self, color: Color, pos: Pos, radius: int, thickness: int = 0, draw_top_right: Optional[bool] = None, draw_top_left: Optional[bool] = None, draw_bottom_left: Optional[bool] = None, draw_bottom_right: Optional[bool] = None) -> None:
        '''
        if thickness is 0, it will draw filled circle.\n
        nothing will be drawn if the radius is less than 1
        '''
        pygame.draw.circle(self.__surface, color.rgba, pos, radius, thickness, draw_top_right, draw_top_left, draw_bottom_right, draw_bottom_left)
    
    @final
    def drawEllipse(self, color: Color, pos: Pos, size: Pos, thickness: int = 0) -> None:
        '''
        if thickness is 0, it will draw filled ellipse.
        '''
        pygame.draw.ellipse(self.__surface, color.rgba, ((pos[0], pos[1]), (size[0], size[1])), thickness)

    @final
    def drawLine(self, color: Color, start_pos: Pos, end_pos: Pos, thickness: int = 1) -> None:
        '''
        if thickness < 1, nothing will be drawn.
        '''
        pygame.draw.line(self.__surface, color.rgba, start_pos, end_pos, thickness)

    @final
    def drawLines(self, color: Color, points: List[Pos], closed: bool = False, thickness: int = 1) -> None:
        '''
        if thickness < 1, nothing will be drawn.\n
        if closed is True, an additional line segment is drawn between the first and last points in the points sequence.
        '''
        pygame.draw.lines(self.__surface, color.rgba, closed, points, thickness)

    @final
    def drawAntialiasedLine(self, color: Color, start_pos: Pos, end_pos: Pos, blend: int = 1) -> None:
        pygame.draw.aaline(self.__surface, color.rgba, start_pos, end_pos, blend)

    @final
    def drawAntialiasedLines(self, color: Color, points: List[Pos], closed: bool = False, blend: int = 1) -> None:
        '''
        if closed is True, an additional line segment is drawn between the first and last points in the points sequence.
        '''
        pygame.draw.aalines(self.__surface, color.rgba, closed, points, blend)

    @final
    def drawSurface(self, surface: Surface, pos: Pos):
        self.__surface.blit(surface.getPygameSurface(), pos)
        self.__tickObjects.append(surface)
        self.__eventObjects.append(surface)

    '''@final
    def drawDynamicObject(self, obj: DynamicObject):
        surface = obj.getPygameSurface()
        self.__surface.blit(surface, obj.getPos())
        self.__tickObjects.append(obj)'''

    @final
    def drawTextBox(self, textBox: TextBox):
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
    def drawButton(self, button: Button):
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
    def drawTextInput(self, textInput: TextInput):
        self.drawTextBox(textInput)

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