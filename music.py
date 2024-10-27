import pygame
import os

import config


class Music:
    def __init__(self):
        self.settings_volume = config.volume * 0.8
        self.menu_track = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'music', 'menu.mp3'))
        self.base_track = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'music', 'tension.wav'))
        # self.hard_track = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'music', 'hard_layer.ogg'))

        self.hard_volume = 0
        self.menu_volume = self.settings_volume * 0.8

        pygame.mixer.Sound.set_volume(self.menu_track,
                                      max(0, (self.settings_volume - self.menu_volume) * config.music_volume))
        pygame.mixer.Sound.set_volume(self.base_track, 0)
        # pygame.mixer.Sound.set_volume(self.hard_track,
        #                               max(0, (self.hard_volume - self.menu_volume) * config.music_volume))

        if config.music_volume > 0:
            pygame.mixer.Sound.play(self.menu_track, loops=-1)
            pygame.mixer.Sound.play(self.base_track, loops=-1)

    def control_music(self):
        if config.music_volume > 0:
            if [x for x in config.npc_list if x.state == 'attacking' and not x.dead] and config.in_game or \
                    config.player_states['dead']:
                if self.hard_volume < self.settings_volume:
                    self.hard_volume += 0.05
                    pygame.mixer.Sound.set_volume(self.hard_track,
                                                  max(0, (self.hard_volume - self.menu_volume) * config.music_volume))
            else:
                if self.hard_volume > 0:
                    self.hard_volume -= 0.005
                    pygame.mixer.Sound.set_volume(self.base_track,
                                                  max(0, (self.hard_volume - self.menu_volume) * config.music_volume))
            if not config.in_game:
                if self.menu_volume < self.settings_volume * 0.2:
                    self.menu_volume += 0.05
                    pygame.mixer.Sound.set_volume(self.base_track,
                                                  max(0, (self.settings_volume - self.menu_volume) * config.music_volume))
                    pygame.mixer.Sound.set_volume(self.menu_track, 0)
            else:
                if self.menu_volume > 0:
                    self.menu_volume -= 0.05
                    pygame.mixer.Sound.set_volume(self.base_track, 0)
                    pygame.mixer.Sound.set_volume(self.menu_track,
                                                  max(0, (self.hard_volume - self.menu_volume) * config.music_volume))
