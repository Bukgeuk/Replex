from ..utils.position import float2d, int2d
from ..utils.language import Language, LanguageState, Hangul
from .TextBox import TextBox, TextBoxStyle
import pygame
import threading

'''
TODO: buffer가 아니라 LanguageChangePoint를 이용해 한글 입력을 구현해야 함.
buffer를 사용하면 한글 입력 상태에서 buffer에 담긴 내용 이전까지 지우려 할 때 문제가 발생함
어디에서 한영전환이 일어났는지 기록한 후 모드를 바꿔가며 구현해야 함.
'''

__all__ = ['TextInput', 'TextInputStyle']

TextInputStyle = TextBoxStyle

mapping = {'1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_', '=': '+', '`': '~', '\'': '"', ';': ':', ',': '<', '.': '>', '/': '?', '\\':'|'}
class TextInput(TextBox):
    def __init__(self, pos: float2d, size: int2d, style: TextInputStyle, text: str = '') -> None:
        super().__init__(pos, size, style, text)
        self.__completedText = ""
        self.__buffer = ""
        self.__isDeleting: bool = False
        self.__timer = None
        Language.addEventListener(self.__languageChangeHandler)

    def __startDeleting(self):
        self.__isDeleting = True
        self.__runDeleting()

    def __languageChangeHandler(self, language: LanguageState):
        if language == LanguageState.KOREAN:
            self.__completedText = self.text
            self.__buffer = ""

    def __applyBuffer(self):
        self.text = self.__completedText + Hangul.combineIntoHangul(self.__buffer)

    def __runDeleting(self):
        if Language.getLanguageState() == LanguageState.ENGLISH:
            self.text = self.text[0:-1]
        else:
            if (len(self.__buffer) == 0):
                #self.__
                pass
            count = Hangul.getLengthOfLastChar(self.__buffer)
            self.__buffer = self.__buffer[0:-count]
            self.__applyBuffer()

        if self.__isDeleting:
            threading.Timer(0.01, self.__runDeleting).start()
            
    def onKeyDown(self, event) -> None:
        super().onKeyDown(event)
        key = event.key
        ls = Language.getLanguageState()

        if key == pygame.K_BACKSPACE:
            if len(self.text) == 0:
                return
            self.__timer = threading.Timer(0.3, self.__startDeleting)
            self.__timer.start()
            if ls == LanguageState.ENGLISH:
                self.text = self.text[0:-1]
            else:
                self.__buffer = self.__buffer[0:-1]
                self.__applyBuffer()
            return
        elif not 32 <= event.key <= 126:
            return
        
        if mapping.get(chr(key)) != None and (event.mod & pygame.KMOD_SHIFT):
            key = ord(mapping[chr(key)])
        
        if (97 <= key <= 122):
            if (event.mod & pygame.KMOD_CAPS) and (not (event.mod & pygame.KMOD_SHIFT)):
                key -= 32
            elif (not (event.mod & pygame.KMOD_CAPS)) and (event.mod & pygame.KMOD_SHIFT):
                key -= 32
        
        if ls == LanguageState.ENGLISH:
            self.text = self.text + chr(key)
        else:
            self.__buffer += chr(key)
            self.__applyBuffer()

    def onKeyUp(self, event) -> None:
        super().onKeyUp(event)

        if event.key == pygame.K_BACKSPACE:
            if self.__isDeleting:
                self.__isDeleting = False
            elif self.__timer is not None:
                self.__timer.cancel()
                


