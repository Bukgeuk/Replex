from __future__ import annotations
from typing import Optional
from .Base import InteractiveComponent
from ..utils.position import Pos
from ..utils.font import Font, getFont
from ..utils.color import Color, BLACK, WHITE

__all__ = ['TextBox']

class TextBox(InteractiveComponent):
    def __init__(self, pos: Pos, size: Pos, text: str = '', fontName: str = '', font: Optional[Font] = None, textColor: Color = BLACK, backgroundColor: Color = WHITE, borderColor: Color = BLACK, borderThickness: int = 1) -> None:
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

    def setText(self, text: str) -> TextBox:
        self.__text = text
        return self

    def getText(self) -> str:
        return self.__text

    def setTextColor(self, color: Color) -> TextBox:
        self.__textColor = color
        return self
    
    def getTextColor(self) -> Color:
        return self.__textColor
    
    def setBackgroundColor(self, color: Color) -> TextBox:
        self.__backgroundColor = color
        return self
    
    def getBackgroundColor(self) -> Color:
        return self.__backgroundColor
    
    def setBorderColor(self, color: Color) -> TextBox:
        self.__borderColor = color
        return self

    def getBorderColor(self) -> Color:
        return self.__borderColor

    def setBorderThickness(self, value: int) -> TextBox:
        self.__borderThickness = value
        return self

    def getBorderThickness(self) -> int:
        return self.__borderThickness

    def getFont(self) -> Optional[Font]:
        return self.__font

    def setFont(self, font: Font) -> TextBox:
        self.__font = font
        return self

    def setFontByName(self, fontName: str) -> TextBox:
        self.__font = getFont(fontName)
        return self

    def tick(self) -> None:
        pass