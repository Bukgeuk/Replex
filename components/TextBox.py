from __future__ import annotations
from typing import Optional
from .Base import InteractiveComponent
from ..utils.position import Pos
from ..utils.font import Font, getFont
from ..utils.color import Color, COLORS
from ..utils.style import ComponentStyle

__all__ = ['TextBox', 'TextBoxStyle']

class TextBoxStyle(ComponentStyle):
    font: Font | str
    textColor: Color
    backgroundColor: Color
    borderColor: Color
    borderThickness: int

    def __init__(self, font: Font | str, textColor: Color = COLORS.BLACK, backgroundColor: Color = COLORS.WHITE, borderColor: Color = COLORS.BLACK, borderThickness: int = 1) -> None:
        super().__init__()
        self.font = font
        self.textColor = textColor
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.borderThickness = borderThickness

class TextBox(InteractiveComponent):
    def __init__(self, pos: Pos, size: Pos, style: TextBoxStyle, text: str = '') -> None:
        super().__init__(pos, size)
        self.__text = text
        self.__textColor = style.textColor
        self.__backgroundColor = style.backgroundColor
        self.__borderColor = style.borderColor
        self.__borderThickness = style.borderThickness
        self.__font: Font | None

        if type(style.font) is str:
            self.__font = getFont(style.font)
        elif type(style.font) is Font:
            self.__font = style.font

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
        elif type(font) is Font:
            self.__font = font

    def tick(self) -> None:
        pass