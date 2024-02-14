import pygame as pg
import os
from settings import UI
from path import path

class Sounds():
    music_volume = 0.9

    def __init__(self, musics: list) -> None:
        self.path_music = path('Sounds/musics')
        self.musics = [os.path.join(self.path_music, music) for music in musics]
        self.index = -1

        self.reset()
        
    def set_music_volume(music_volume):
        Sounds.music_volume = music_volume/100
        pg.mixer.music.set_volume(Sounds.music_volume)

    def play(self, transition):
        if transition:
            pg.mixer.music.fadeout(1000)
        elif not pg.mixer.music.get_busy():
            pg.mixer.music.set_volume(Sounds.music_volume)
            self.index += 1
            if self.index >= len(self.musics): self.index = 0
            pg.mixer.music.load(self.musics[self.index])
            pg.mixer.music.play(fade_ms=1500)

    def stop(self, fadeout: int):
        pg.mixer.music.fadeout(fadeout)

    def skip(self):
        pg.mixer.music.stop()

    def pause(self):
        pg.mixer.music.pause()

    def unpause(self):
        pg.mixer.music.unpause()

    def low_volume(self):
        self.decrease -= 0.9/(max(UI.clock.get_fps(), 1)*2)
        if self.decrease <= 0.1: self.decrease = 0.1
        pg.mixer.music.set_volume(self.decrease*Sounds.music_volume)

    def high_volume(self):
        self.increase += 0.9/(max(UI.clock.get_fps(), 1)*2.5)
        if self.increase >= 1: self.increase = 1
        pg.mixer.music.set_volume(self.increase*Sounds.music_volume)

    def reset(self):
        self.increase = 0.1
        self.decrease = 1