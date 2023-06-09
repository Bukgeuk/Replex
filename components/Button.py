from __future__ import annotations
from typing import Optional
import pygame
from .Base import InteractiveDisplayObject, Pos, Color
from ..utils.font import getFont

class Button(InteractiveDisplayObject):
    def __init__(self, pos: Pos, size: Pos, text: str = '', fontName: str = '', font: Optional[pygame.font.Font] = None, textColor: Color = (0, 0, 0), backgroundColor: Color = (255, 255, 255), borderColor: Color = (0, 0, 0), borderThickness: int = 1, backgroundHoverColor: Optional[Color] = None, textHoverColor: Optional[Color] = None) -> None:
        super().__init__(pos, size)
        self.__text = text
        self.__textColor = textColor
        self.__backgroundColor = backgroundColor
        self.__borderColor = borderColor
        self.__borderThickness = borderThickness
        self.__backgroundHoverColor = backgroundHoverColor
        self.__textHoverColor = textHoverColor

        if not font is None:
            self.__font = font
        else:
            self.__font = getFont(fontName)

    def setText(self, text: str) -> Button:
        self.__text = text
        return self

    def getText(self) -> str:
        return self.__text

    def setTextColor(self, color: Color) -> Button:
        self.__textColor = color
        return self
    
    def getTextColor(self) -> Color:
        return self.__textColor
    
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
            return self.__textColor

    def getBackgroundRenderColor(self) -> Color:
        '''
        Return:
            The actual rendering background color based on hover state
        '''
        if self.isMouseEntered() and self.__backgroundHoverColor != None:
            return self.__backgroundHoverColor
        else:
            return self.__backgroundColor

    def setBackgroundColor(self, color: Color) -> Button:
        self.__backgroundColor = color
        return self
    
    def getBackgroundColor(self) -> Color:
        return self.__backgroundColor
    
    def getBackgroundHoverColor(self) -> Optional[Color]:
        return self.__backgroundHoverColor
    
    def setBackgroundHoverColor(self, color: Optional[Color]) -> Button:
        self.__backgroundHoverColor = color
        return self

    def setBorderColor(self, color: Color) -> Button:
        self.__borderColor = color
        return self

    def getBorderColor(self) -> Color:
        return self.__borderColor

    def setBorderThickness(self, value: int) -> Button:
        self.__borderThickness = value
        return self

    def getBorderThickness(self) -> int:
        return self.__borderThickness

    def getFont(self) -> Optional[pygame.font.Font]:
        return self.__font

    def setFont(self, font: pygame.font.Font) -> Button:
        self.__font = font
        return self

    def setFontByName(self, fontName: str) -> Button:
        self.__font = getFont(fontName)
        return self

    def onMouseMove(self, event) -> None:
        super().onMouseMove(event)

    def tick(self) -> None:
        pass


    