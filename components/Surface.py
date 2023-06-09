from __future__ import annotations
from typing import List, Optional, final

import pygame

from ..utils.font import getFont
from .Base import InteractiveDisplayObject, Positioning, DynamicObject, Pos, Color
from .Image import Image
from .Button import Button


class Surface(InteractiveDisplayObject):
    def __init__(self, pos: Pos, size: Pos) -> None:
        super().__init__(pos, size)
        self.__surface = pygame.Surface(size)
        self.__tickObjects: List[Surface | DynamicObject] = []
        self.__eventObjects: List[InteractiveDisplayObject] = []

    @final
    def getPygameSurface(self):
        return self.__surface

    @final
    def fill(self, color: Color) -> None:
        self.__surface.fill(color)

    @final
    def drawTextByFont(self, pos: Pos, text: str, font: pygame.font.Font, color: Color, antialias: bool = True, positioning: Positioning = Positioning.TOPLEFT) -> None:
        image = font.render(text, antialias, color)
        rect = image.get_rect()
        v = (round(pos[0]), round(pos[1]))

        if positioning == Positioning.CENTER:
            rect.center = v
        elif positioning == Positioning.TOPLEFT:
            rect.topleft = v
        elif positioning == Positioning.TOPRIGHT:
            rect.topright = v
        elif positioning == Positioning.BOTTOMLEFT:
            rect.bottomleft = v
        elif positioning == Positioning.BOTTOMRIGHT:
            rect.bottomright = v

        self.__surface.blit(image, rect)

    @final
    def drawTextByFontName(self, pos: Pos, text: str, fontName: str, color: Color, antialias: bool = True, positioning: Positioning = Positioning.TOPLEFT) -> None:
        font = getFont(fontName)
        if font is not None:
            self.drawTextByFont(pos, text, font, color, antialias, positioning)

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
        pygame.draw.rect(self.__surface, color, ((pos[0], pos[1]), (size[0], size[1])), thickness)

    @final
    def drawCircle(self, color: Color, pos: Pos, radius: int, thickness: int = 0, draw_top_right: Optional[bool] = None, draw_top_left: Optional[bool] = None, draw_bottom_left: Optional[bool] = None, draw_bottom_right: Optional[bool] = None) -> None:
        '''
        if thickness is 0, it will draw filled circle.\n
        nothing will be drawn if the radius is less than 1
        '''
        pygame.draw.circle(self.__surface, color, pos, radius, thickness, draw_top_right, draw_top_left, draw_bottom_right, draw_bottom_left)
    
    @final
    def drawEllipse(self, color: Color, pos: Pos, size: Pos, thickness: int = 0) -> None:
        '''
        if thickness is 0, it will draw filled ellipse.
        '''
        pygame.draw.ellipse(self.__surface, color, ((pos[0], pos[1]), (size[0], size[1])), thickness)

    @final
    def drawLine(self, color: Color, start_pos: Pos, end_pos: Pos, thickness: int = 1) -> None:
        '''
        if thickness < 1, nothing will be drawn.
        '''
        pygame.draw.line(self.__surface, color, start_pos, end_pos, thickness)

    @final
    def drawLines(self, color: Color, points: List[Pos], closed: bool = False, thickness: int = 1) -> None:
        '''
        if thickness < 1, nothing will be drawn.\n
        if closed is True, an additional line segment is drawn between the first and last points in the points sequence.
        '''
        pygame.draw.lines(self.__surface, color, closed, points, thickness)

    @final
    def drawAntialiasedLine(self, color: Color, start_pos: Pos, end_pos: Pos, blend: int = 1) -> None:
        pygame.draw.aaline(self.__surface, color, start_pos, end_pos, blend)

    @final
    def drawAntialiasedLines(self, color: Color, points: List[Pos], closed: bool = False, blend: int = 1) -> None:
        '''
        if closed is True, an additional line segment is drawn between the first and last points in the points sequence.
        '''
        pygame.draw.aalines(self.__surface, color, closed, points, blend)

    @final
    def drawSurface(self, surface: Surface, pos: Pos):
        self.__surface.blit(surface.getPygameSurface(), pos)
        self.__tickObjects.append(surface)
        self.__eventObjects.append(surface)

    @final
    def drawDynamicObject(self, obj: DynamicObject):
        surface = obj.getPygameSurface()
        self.__surface.blit(surface, obj.getPos())
        self.__tickObjects.append(obj)

    @final
    def drawButton(self, btn: Button):
        size = btn.getSize()
        b = btn.getBorderThickness()
        pos = btn.getPos()
        font = btn.getFont()
        self.drawRect(btn.getBorderColor(), pos, (size[0] + (b * 2), size[1] + (b * 2)))
        self.drawRect(btn.getBackgroundRenderColor(), (pos[0] + b, pos[1] + b), size)
        if not font is None:
            self.drawTextByFont((pos[0] + (size[0] / 2), pos[1] + (size[1] / 2)), btn.getText(), font, btn.getTextRenderColor(), positioning=Positioning.CENTER)

        self.__eventObjects.append(btn)

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
                if not obj.isMouseEntered():
                    obj.onMouseEnter(event)
            elif obj.isMouseEntered():
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