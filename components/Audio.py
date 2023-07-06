from __future__ import annotations

import pygame

__all__ = ['Audio']

class Audio:
    def __init__(self, path: str) -> None:
        self.__audio = pygame.mixer.Sound(path)

    def play(self, loops: int = 1, maxtime: int = 0, fade: int = 0) -> Audio:
        '''
        if loops is -1, the audio will loop infinitely.\n
        The maxtime can be used to stop playback after a given number of milliseconds.\n
        The fade_ms will make the sound start playing at 0 volume and fade up to full volume over the time given.
        '''
        self.__audio.play(loops, maxtime, fade)
        return self

    def stop(self) -> Audio:
        self.__audio.stop()
        return self
    
    @property
    def volume(self) -> float:
        return self.__audio.get_volume()

    @volume.setter
    def volume(self, value: float):
        '''
        volume in the range of 0.0 to 1.0\n
        If value < 0.0, the volume will not be changed\n
        If value > 1.0, the volume will be set to 1.0
        '''
        self.__audio.set_volume(value)

    @property
    def length(self) -> float:
        return self.__audio.get_length()

    @property
    def numOfChannels(self) -> int:
        return self.__audio.get_num_channels()

    @property
    def rawAudio(self) -> bytes:
        return self.__audio.get_raw()
