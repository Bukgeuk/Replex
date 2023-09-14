from __future__ import annotations
from typing import Optional

from Replex.utils.color import Color, COLORS
from Replex.utils.font import Font
from .Base import float2d, int2d, InteractiveComponent
from .TextBox import TextBox, TextBoxStyle
from Replex.utils.style import ComponentStyle
from Replex.utils.event import EventType

__all__ = ['Button', 'ButtonStyle', 'Slider', 'SliderStyle']

class ButtonStyle(TextBoxStyle):
    backgroundHoverColor: Optional[Color] = None
    textHoverColor: Optional[Color] = None

    def __init__(self, font: Font | str, textColor: Color = COLORS.BLACK, backgroundColor: Optional[Color] = COLORS.WHITE, borderColor: Optional[Color] = COLORS.BLACK, borderThickness: int = 1, backgroundHoverColor: Optional[Color] = None, textHoverColor: Optional[Color] = None, radius: int = -1) -> None:
        super().__init__(font, textColor, backgroundColor, borderColor, borderThickness, radius)
        self.backgroundHoverColor = backgroundHoverColor
        self.textHoverColor = textHoverColor

class Button(TextBox):
    def __init__(self, pos: float2d, size: int2d, style: ButtonStyle, text: str = '') -> None:
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
    def backgroundRenderColor(self) -> Optional[Color]:
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
    
class SliderStyle(ComponentStyle):
    sliderColor: Color
    sliderFilledColor: Color
    handleColor: Color
    handleHoverColor: Color
    sliderRadius: int
    handleRadius: int
    handleSize: int2d

    def __init__(self, sliderColor: Color = COLORS.GRAY, sliderFilledColor: Color = COLORS.SKYBLUE, handleColor: Color = COLORS.BLUE, handleHoverColor: Optional[Color] = None, sliderRadius: int = -1, handleRadius: int = -1, handleSize: int2d = (10, 50)) -> None:
        self.sliderColor = sliderColor
        self.handleColor = handleColor
        self.sliderRadius = sliderRadius
        self.handleRadius = handleRadius
        self.handleSize = handleSize
        self.handleHoverColor = handleHoverColor
        self.sliderFilledColor = sliderFilledColor

class Slider(InteractiveComponent):
    def __init__(self, pos: float2d, size: int2d, style: SliderStyle, value: float = 0) -> None:
        super().__init__(pos, size)
        self.__sliderColor = style.sliderColor
        self.__handleColor = style.handleColor
        self.__sliderRadius = style.sliderRadius
        self.__handleRadius = style.handleRadius
        self.__handleSize = style.handleSize
        self.__handleHoverColor = style.handleHoverColor
        self.__sliderFilledColor = style.sliderFilledColor

        self.__value: float = 1 if value > 1 else 0 if value < 0 else value

        self.__handle: Button = Button(pos, self.__handleSize, ButtonStyle(None, backgroundColor=self.__handleColor, backgroundHoverColor=self.__handleHoverColor, radius=self.__handleRadius))
        self.__handle.addEventListener(EventType.onMouseDown, self.onHandlerMouseDown)
        self.renewHandlePos()

        self.__dragging: bool = False

    def renewHandlePos(self) -> None:
        p = (self.pos[0] + self.size[0] * self.value - (self.handleSize[0] / 2), self.pos[1] + (self.size[1] / 2) - (self.handleSize[1] / 2))
        self.__handle.pos = p

    @property
    def value(self) -> float:
        return self.__value
    
    @value.setter
    def value(self, value: float) -> None:
        self.__value = 1 if value > 1 else 0 if value < 0 else value
        self.renewHandlePos()

    @property
    def sliderColor(self) -> Color:
        return self.__sliderColor
    
    @property
    def sliderFilledColor(self) -> Color:
        return self.__sliderFilledColor
    
    @property
    def sliderRadius(self) -> int:
        return self.__sliderRadius
    
    @property
    def handleSize(self) -> int2d:
        return self.__handleSize
    
    def getHandle(self) -> Button:
        return self.__handle
    
    def onMouseDown(self, event) -> None:
        self.value = (event.pos[0] - self.pos[0]) / self.size[0]
        return super().onClick(event)
    
    def onHandlerMouseDown(self, event) -> None:
        if event.button == 1:
            self.__dragging = True

    def onHandlerMouseUp(self, event) -> None:
        if event.button == 1:
            self.__dragging = False

    def onHandlerMouseMove(self, event) -> None:
        if self.__dragging:
            self.value = (event.pos[0] - self.pos[0]) / self.size[0]