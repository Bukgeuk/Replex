from abc import ABCMeta, abstractmethod

class Screen(metaclass=ABCMeta):
    def onEnterScreen(self) -> None:
        pass

    def onEscapeScreen(self) -> None:
        pass

    def onMouseDown(self, event) -> None:
        pass

    def onMouseUp(self, event) -> None:
        pass

    def onMouseWheel(self, event) -> None:
        pass

    def onMouseMove(self, event) -> None:
        pass

    def onKeyDown(self, event) -> None:
        pass

    def onKeyUp(self, event) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass
