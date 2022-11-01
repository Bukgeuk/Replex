from enum import Enum
import pygame
from typing import Tuple, final

from components.Base import InteractiveDisplayObject, Positioning
import api.font

class Surface(InteractiveDisplayObject):
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int]) -> None:
        super().__init__(pos, size)
        self.__surface = pygame.Surface(size)

    @final
    def getPygameSurface(self):
        return self.__surface

    @final
    def fillBackground(self, color: Tuple[int, int, int]) -> None:
        self.__surface.fill(color)

    @final
    def drawTextByFont(self, pos: Tuple[int, int], text: str, font: pygame.font.Font, color: Tuple[int, int, int], antialias: bool = True, positioning: Positioning = Positioning.TOPLEFT) -> None:
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
    def drawTextByFontName(self, pos: Tuple[int, int], text: str, fontName: str, color: Tuple[int, int, int], antialias: bool = True, positioning: Positioning = Positioning.TOPLEFT) -> None:
        font = api.font.getFont(fontName)
        if font is not None:
            self.drawTextByFont(pos, text, font, color, antialias, positioning)