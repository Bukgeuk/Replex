from __future__ import annotations
from typing import Optional

from Replex.utils.color import Color, COLORS
from Replex.utils.font import Font
from .Base import Pos
from .TextBox import TextBox, TextBoxStyle

__all__ = ['Button', 'ButtonStyle']

class ButtonStyle(TextBoxStyle):
    backgroundHoverColor: Optional[Color] = None
    textHoverColor: Optional[Color] = None

    def __init__(self, font: Font | str, textColor: Color = COLORS.BLACK, backgroundColor: Color = COLORS.WHITE, borderColor: Color = COLORS.BLACK, borderThickness: int = 1, backgroundHoverColor: Optional[Color] = None, textHoverColor: Optional[Color] = None) -> None:
        super().__init__(font, textColor, backgroundColor, borderColor, borderThickness)
        self.backgroundHoverColor = backgroundHoverColor
        self.textHoverColor = textHoverColor

class Button(TextBox):
    def __init__(self, pos: Pos, size: Pos, style: ButtonStyle, text: str = '') -> None:
        super().__init__(pos, size, style, text)
        self.__backgroundHoverColor = style.backgroundHoverColor
        self.__textHoverColor = style.textHoverColor
    
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
    