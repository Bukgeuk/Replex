from __future__ import annotations
from typing import Optional
import pygame

from .Base import DisplayObject, Pos, Color
from ..utils.font import getFont

class TextBlock(DisplayObject):
    def __init__(self, pos: Pos, size: Pos, text: str = '', fontName: str = '', font: Optional[pygame.font.Font] = None, textColor: Color = (0, 0, 0), backgroundColor: Color = (255, 255, 255), borderColor: Color = (0, 0, 0), borderThickness: int = 1) -> None:
        super().__init__(pos, size)
        self.__text = text
        self.__textColor = textColor
        self.__backgroundColor = backgroundColor
        self.__borderColor = borderColor
        self.__borderThickness = borderThickness

        if not font is None:
            self.__font = font
        else:
            self.__font = getFont(fontName)

    def setText(self, text: str) -> TextBlock:
        self.__text = text
        return self

    def getText(self) -> str:
        return self.__text

    def setTextColor(self, color: Color) -> TextBlock:
        self.__textColor = color
        return self

    def getTextColor(self) -> Color:
        return self.__textColor

    def getBackgroundColor(self) -> Color:
        return self.__backgroundColor

    def setBackgroundColor(self, color: Color) -> TextBlock:
        self.__backgroundColor = color
        return self

    def setBorderColor(self, color: Color) -> TextBlock:
        self.__borderColor = color
        return self

    def getBorderColor(self) -> Color:
        return self.__borderColor

    def setBorderThickness(self, value: int) -> TextBlock:
        self.__borderThickness = value
        return self

    def getBorderThickness(self) -> int:
        return self.__borderThickness

    def getFont(self) -> Optional[pygame.font.Font]:
        return self.__font

    def setFont(self, font: pygame.font.Font) -> TextBlock:
        self.__font = font
        return self

    def setFontByName(self, fontName: str) -> TextBlock:
        self.__font = getFont(fontName)
        return self

    def tick(self) -> None:
        pass