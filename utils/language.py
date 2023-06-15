import ctypes
from typing import Callable, List
from enum import Enum
import os.path

__all__ = ['Hangul', 'LanguageState', 'Language']

__dllpath = os.path.sep.join([os.path.split(__file__)[0], '..', 'dll', 'Hangul.dll'])
__hanguldll = ctypes.windll.LoadLibrary(__dllpath)
__run = __hanguldll['run']
__run.argtypes = (ctypes.c_wchar_p,)
__run.restype = ctypes.c_wchar_p
__getLength = __hanguldll['getLengthOfLastChar']
__getLength.argtypes = (ctypes.c_wchar_p,)
__getLength.restype = ctypes.c_int

class Hangul:
    @staticmethod
    def combineIntoHangul(text: str) -> str:
        s = str(__run(text))
        return s
    
    @staticmethod
    def getLengthOfLastChar(text: str) -> int:
        return __getLength(text)

class LanguageState(Enum):
    ENGLISH = 1
    KOREAN = 2


class Language:
    __languageState: LanguageState = LanguageState.ENGLISH
    __eventListeners: List[Callable[[LanguageState], None]] = []

    @staticmethod
    def changeLanguage():
        global __languageState
        if __languageState == LanguageState.ENGLISH:
            __languageState = LanguageState.KOREAN
        else:
            __languageState = LanguageState.ENGLISH
        
        for listener in Language.__eventListeners:
            listener(__languageState)

    @staticmethod
    def getLanguageState() -> LanguageState:
        return Language.__languageState

    @staticmethod
    def addEventListener(callback: Callable[[LanguageState], None]):
        '''
        add listener to language change event
        '''
        Language.__eventListeners.append(callback)

    @staticmethod
    def removeEventListener(callback: Callable[[LanguageState], None]):
        Language.__eventListeners.remove(callback)

    @staticmethod
    def clearEventListeners():
        Language.__eventListeners.clear()