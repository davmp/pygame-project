import random

import pygame
import os

import config


class Music:
    def __init__(self):
        self.menu_track = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'music', 'menu.wav'))
        self.base_track = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'music',
                                                          random.choice([
                                                              'tension.wav',
                                                              'tension1.mp3'])))
        self.hard_track = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'music', 'hard_tension.wav'))

        self.volume = config.music_volume * config.volume * 0.2

        pygame.mixer.Sound.set_volume(self.menu_track, self.volume)
        pygame.mixer.Sound.set_volume(self.base_track, 0)
        pygame.mixer.Sound.set_volume(self.hard_track, 0)

        if config.music_volume > 0:
            pygame.mixer.Sound.play(self.menu_track, loops=-1)
            pygame.mixer.Sound.play(self.base_track, loops=-1)
            pygame.mixer.Sound.play(self.hard_track, loops=-1)

    def control_music(self):
        if [x for x in config.npc_list if x.state == 'attacking' and not x.dead] and config.in_game or \
                config.player_states['dead']:
            self.menu_track.set_volume(0)
            self.base_track.set_volume(0)
            self.hard_track.set_volume(self.volume)#max(0, (self.hard_volume - self.menu_volume) * config.music_volume))
        else:
            self.menu_track.set_volume(0)
            self.base_track.set_volume(self.volume)#max(0, (self.hard_volume - self.menu_volume) * config.music_volume))
            self.hard_track.set_volume(0)

        if not config.in_game:
            self.menu_track.set_volume(self.volume)#max(0, (self.settings_volume - self.menu_volume) * config.music_volume))
            self.base_track.set_volume(0)
            self.hard_track.set_volume(0)
        else:
            self.menu_track.set_volume(0)
            self.base_track.set_volume(self.volume)#max(0, (self.hard_volume - self.menu_volume) * config.music_volume))
            self.hard_track.set_volume(0)
