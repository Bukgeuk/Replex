from __future__ import annotations
from typing import Optional
from .Base import Pos
from .TextBox import TextBox
from ..utils.color import Color, BLACK, WHITE
from ..utils.font import Font

__all__ = ['Button']

class Button(TextBox):
    def __init__(self, pos: Pos, size: Pos, text: str = '', fontName: str = '', font: Optional[Font] = None, textColor: Color = BLACK, backgroundColor: Color = WHITE, borderColor: Color = BLACK, borderThickness: int = 1, backgroundHoverColor: Optional[Color] = None, textHoverColor: Optional[Color] = None) -> None:
        super().__init__(pos, size, text, fontName, font, textColor, backgroundColor, borderColor, borderThickness)
        self.__backgroundHoverColor = backgroundHoverColor
        self.__textHoverColor = textHoverColor
    
    @property
    def textHoverColor(self) -> Optional[Color]:
        return self.__textHoverColor

    @textHoverColor.setter
    def textHoverColor(self, color: Optional[Color]):
        self.__textHoverColor = color

    @property
    def textRenderColor(self) -> Color:
        '''
        Return:
            The actual rendering text color based on hover state
        '''
        if self.isMouseEntered and self.__textHoverColor != None:
            return self.__textHoverColor
        else:
            return self.textColor

    @property
    def backgroundRenderColor(self) -> Color:
        '''
        Return:
            The actual rendering background color based on hover state
        '''
        if self.isMouseEntered and self.__backgroundHoverColor != None:
            return self.__backgroundHoverColor
        else:
            return self.backgroundColor
    
    @property
    def backgroundHoverColor(self) -> Optional[Color]:
        return self.__backgroundHoverColor
    
    @backgroundHoverColor.setter
    def backgroundHoverColor(self, color: Optional[Color]):
        self.__backgroundHoverColor = color
    