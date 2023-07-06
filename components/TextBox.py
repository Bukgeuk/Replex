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

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text
    
    @property
    def textColor(self) -> Color:
        return self.__textColor
    
    @textColor.setter
    def textColor(self, color: Color):
        self.__textColor = color
    
    @property
    def backgroundColor(self) -> Color:
        return self.__backgroundColor
    
    @backgroundColor.setter
    def setBackgroundColor(self, color: Color):
        self.__backgroundColor = color

    @property
    def borderColor(self) -> Color:
        return self.__borderColor

    @borderColor.setter
    def borderColor(self, color: Color):
        self.__borderColor = color

    @property
    def borderThickness(self) -> int:
        return self.__borderThickness

    @borderThickness.setter
    def borderThickness(self, value: int):
        self.__borderThickness = value

    @property
    def font(self) -> Optional[Font]:
        return self.__font

    @font.setter
    def font(self, font: Font | str):
        if type(font) is str:
            self.__font = getFont(font)
        else:
            self.__font = font

    def tick(self) -> None:
        pass