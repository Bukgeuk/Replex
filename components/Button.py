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
    
    def setTextHoverColor(self, color: Optional[Color]) -> Button:
        self.__textHoverColor = color
        return self
    
    def getTextHoverColor(self) -> Optional[Color]:
        return self.__textHoverColor

    def getTextRenderColor(self) -> Color:
        '''
        Return:
            The actual rendering text color based on hover state
        '''
        if self.isMouseEntered() and self.__textHoverColor != None:
            return self.__textHoverColor
        else:
            return self.getTextColor()

    def getBackgroundRenderColor(self) -> Color:
        '''
        Return:
            The actual rendering background color based on hover state
        '''
        if self.isMouseEntered() and self.__backgroundHoverColor != None:
            return self.__backgroundHoverColor
        else:
            return self.getBackgroundColor()
    
    def getBackgroundHoverColor(self) -> Optional[Color]:
        return self.__backgroundHoverColor
    
    def setBackgroundHoverColor(self, color: Optional[Color]) -> Button:
        self.__backgroundHoverColor = color
        return self
    