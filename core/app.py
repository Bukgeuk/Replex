from __future__ import annotations

import sys
from typing import Callable, Dict, List, Optional

import pygame
from ..components.Scene import Scene
from ..utils.event import EventType
from ..utils.app import renewFramerate, DisplayMode, renewWindowSize
from ..utils.language import Language

__all__ = ['App']

class App:
    def __init__(self) -> None:
        pygame.init()

        self.__terminate = False
        self.__clock = pygame.time.Clock()
        self.__framerate: int = 0
        self.__eventListeners: Dict[EventType, List[Callable[[App], None]]] = {}
        self.__scene: Optional[Scene]
        self.__pygameSurface: Optional[pygame.surface.Surface] = None

    def __occurEvent(self, event: EventType) -> None:
        if event in self.__eventListeners:
            for callback in self.__eventListeners[event]:
                callback(self)
    
    def run(self, initialScene: Scene) -> None:
        self.__scene = initialScene

        self.__occurEvent(EventType.RUN)
        self.__scene.onEnterScene()

        while not self.__terminate:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__scene.onEscapeScene()
                    self.__occurEvent(EventType.QUIT)
                    self.terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not (event.button == 4 or event.button == 5):
                        self.__scene.onMouseDown(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if not (event.button == 4 or event.button == 5):
                        self.__scene.onMouseUp(event)
                elif event.type == pygame.MOUSEWHEEL:
                    self.__scene.onMouseWheel(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.__scene.onMouseMove(event)
                elif event.type == pygame.KEYDOWN:
                    self.__scene.onKeyDown(event)
                    if event.key == pygame.K_RALT:
                        Language.changeLanguage()
                elif event.type == pygame.KEYUP:
                    self.__scene.onKeyUp(event)

            # Drawing
            self.__scene.tick()
            self.__scene.draw()
            self.__scene.render()

            assert self.__pygameSurface is not None, 'Use setWindowMode before running'

            self.__pygameSurface.blit(self.__scene.getPygameSurface(), (0, 0))
            pygame.display.update()         
            
            # Framerate
            if not self.__framerate == 0:
                self.__clock.tick(self.__framerate)
                
        pygame.quit()
        sys.exit()

    @property
    def title(self) -> str:
        return pygame.display.get_caption()[0]

    @title.setter
    def title(self, title: str) -> None:
        pygame.display.set_caption(title)

    def setWindowMode(self, width: int, height: int, displayMode: DisplayMode = DisplayMode.WINDOWED, resizable: bool = False, vsync: bool = False) -> None:
        flags = 0
        vs = 0

        if displayMode == DisplayMode.FULLSCREEN:
            flags |= pygame.FULLSCREEN
        elif displayMode == DisplayMode.NOFRAME:
            flags |= pygame.NOFRAME
        elif displayMode == DisplayMode.HIDDEN:
            flags |= pygame.HIDDEN

        if resizable:
            flags |= pygame.RESIZABLE

        if vsync:
            vs = 1

        self.__pygameSurface = pygame.display.set_mode((width, height), flags, vsync=vs)
        renewWindowSize((width, height))

    def toggleFullscreen(self) -> None:
        pygame.display.toggle_fullscreen()

    @property
    def framerate(self) -> int:
        return self.__framerate

    @framerate.setter
    def framerate(self, framerate: int) -> None:
        renewFramerate(framerate)
        self.__framerate = framerate

    @property
    def scene(self) -> Scene | None:
        return self.__scene
    
    @scene.setter
    def scene(self, scene: Scene) -> None:
        if self.__scene is not None:
            self.__scene.onEscapeScene()
        self.__scene = scene
        self.__scene.onEnterScene()

    
    def terminate(self) -> None:
        self.__terminate = True

    def addEventListener(self, event: EventType, callback: Callable[[App], None]) -> None:
        if not event in self.__eventListeners:
            self.__eventListeners[event] = []
        self.__eventListeners[event].append(callback)

    def removeEventListener(self, event: EventType, callback: Callable[[App], None]) -> None:
        if event in self.__eventListeners:
            self.__eventListeners[event].remove(callback)

    def clearEventListeners(self, event: EventType) -> None:
        if event in self.__eventListeners:
            self.__eventListeners[event].clear()