from typing import List, Optional, Tuple, Union, final

import pygame

import api.font
from components.Base import InteractiveDisplayObject, Positioning
from components.Image import Image

ColorType = Union[Tuple[int, int, int], Tuple[int, int, int, int]]

class Surface(InteractiveDisplayObject):
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int]) -> None:
        super().__init__(pos, size)
        self.__surface = pygame.Surface(size)

    @final
    def getPygameSurface(self):
        return self.__surface

    @final
    def fill(self, color: ColorType) -> None:
        self.__surface.fill(color)

    @final
    def drawTextByFont(self, pos: Tuple[int, int], text: str, font: pygame.font.Font, color: ColorType, antialias: bool = True, positioning: Positioning = Positioning.TOPLEFT) -> None:
        image = font.render(text, antialias, color)
        rect = image.get_rect()

        if positioning == Positioning.CENTER:
            rect.center = pos
        elif positioning == Positioning.TOPLEFT:
            rect.topleft = pos
        elif positioning == Positioning.TOPRIGHT:
            rect.topright = pos
        elif positioning == Positioning.BOTTOMLEFT:
            rect.bottomleft = pos
        elif positioning == Positioning.BOTTOMRIGHT:
            rect.bottomright = pos

        self.__surface.blit(image, rect)

    @final
    def drawTextByFontName(self, pos: Tuple[int, int], text: str, fontName: str, color: ColorType, antialias: bool = True, positioning: Positioning = Positioning.TOPLEFT) -> None:
        font = api.font.getFont(fontName)
        if font is not None:
            self.drawTextByFont(pos, text, font, color, antialias, positioning)

    @final
    def drawImage(self, image: Image):
        self.__surface.blit(image.getPygameImage(), image.getPos())

    @final
    def drawRect(self, color: ColorType, pos: Tuple[int, int], size: Tuple[int, int], thickness: int = 0, radius: int = -1, top_left_radius: int = -1, top_right_radius: int = -1, bottom_left_radius: int = -1, bottom_right_radius: int = -1) -> None:
        '''
        if thickness is 0, it will draw filled rectangle.\n
        if top_left_radius, top_right_radius, bottom_left_radius, bottom_right_radius < 0, it will use radius value.\n
        if radius < 1, it will draw rectangle without rounded corners.
        '''
        pygame.draw.rect(self.__surface, color, (pos[0], pos[1], size[0], size[1]), thickness)

    @final
    def drawCircle(self, color: ColorType, pos: Tuple[int, int], radius: int, thickness: int = 0, draw_top_right: Optional[bool] = None, draw_top_left: Optional[bool] = None, draw_bottom_left: Optional[bool] = None, draw_bottom_right: Optional[bool] = None) -> None:
        '''
        if thickness is 0, it will draw filled circle.\n
        nothing will be drawn if the radius is less than 1
        '''
        pygame.draw.circle(self.__surface, color, pos, radius, thickness, draw_top_right, draw_top_left, draw_bottom_right, draw_bottom_left)
    
    @final
    def drawEllipse(self, color: ColorType, pos: Tuple[int, int], size: Tuple[int, int], thickness: int = 0) -> None:
        '''
        if thickness is 0, it will draw filled ellipse.
        '''
        pygame.draw.ellipse(self.__surface, color, (pos[0], pos[1], size[0], size[1]), thickness)

    @final
    def drawLine(self, color: ColorType, start_pos: Tuple[int, int], end_pos: Tuple[int, int], thickness: int = 1) -> None:
        '''
        if thickness < 1, nothing will be drawn.
        '''
        pygame.draw.line(self.__surface, color, start_pos, end_pos, thickness)

    @final
    def drawLines(self, color: ColorType, points: List[Tuple[int, int]], closed: bool = False, thickness: int = 1) -> None:
        '''
        if thickness < 1, nothing will be drawn.\n
        if closed is True, an additional line segment is drawn between the first and last points in the points sequence.
        '''
        pygame.draw.lines(self.__surface, color, closed, points, thickness)

    @final
    def drawAntialiasedLine(self, color: ColorType, start_pos: Tuple[int, int], end_pos: Tuple[int, int], blend: int = 1) -> None:
        pygame.draw.aaline(self.__surface, color, start_pos, end_pos, blend)

    @final
    def drawAntialiasedLines(self, color: ColorType, points: List[Tuple[int, int]], closed: bool = False, blend: int = 1) -> None:
        '''
        if closed is True, an additional line segment is drawn between the first and last points in the points sequence.
        '''
        pygame.draw.aalines(self.__surface, color, closed, points, blend)