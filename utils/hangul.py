import ctypes

hanguldll = ctypes.windll.LoadLibrary("../dll/Hangul.dll")
func = hanguldll['run']
func.argtypes = (ctypes.c_wchar_p,)
func.restype = ctypes.c_wchar_p

def combineHangul(text: str) -> str:
    return str(func(text))