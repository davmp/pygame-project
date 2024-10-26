import pygame
import pickle
import os
import copy
import random

import colors
import config
import sound
from text import Text

config.paused = True


class Controller:
    def __init__(self, canvas):
        self.current_menu = 'main'
        self.current_type = 'main'
        self.canvas = canvas
        self.shut_up = False

        self.load_settings()
        self.esc_pressed = False
        self.new_pressed = False

        self.mainMenu = MainMenu()
        self.newMenu = NewMenu(self.current_settings)
        self.optionsMenu = OptionsMenu(self.current_settings)
        self.creditsMenu = CreditsMenu()
        self.gMainMenu = PauseMenu()
        self.supportSplash = SupportSplash()
        self.scoreMenu = ScoreMenu()

    def load_settings(self):
        with open(os.path.join('data', 'settings.dat'), 'rb') as file1:
            settings = pickle.load(file1)

        self.current_settings = settings
        self.shut_up = self.current_settings['shut up']

    def save_settings(self):
        current_settings = self.optionsMenu.current_settings
        current_settings['shut up'] = self.shut_up

        with open(os.path.join('data', 'settings.dat'), 'wb') as file2:
            pickle.dump(current_settings, file2)

    @staticmethod
    def check_mouse():
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)

    def control(self):
        self.check_mouse()
        if self.current_type == 'main':
            if self.current_menu == 'main':
                self.mainMenu.draw(self.canvas)
                if self.mainMenu.new_button.get_clicked():
                    self.current_menu = 'new'
                elif self.mainMenu.options_button.get_clicked():
                    self.current_menu = 'options'
                elif self.mainMenu.score_button.get_clicked():
                    self.current_menu = 'score'
                elif self.mainMenu.credits_button.get_clicked():
                    self.current_menu = 'credits'
                if config.statistics['playtime'] >= 120 and not self.shut_up:
                    self.supportSplash.draw(self.canvas)
                    if self.supportSplash.button.get_clicked():
                        self.shut_up = True
                        self.save_settings()
            elif self.current_menu == 'new':
                self.newMenu.draw(self.canvas)
                if self.newMenu.back_button.get_clicked():
                    self.current_menu = 'main'
                elif self.newMenu.new_button.get_clicked():
                    self.newMenu.reset_inventory()
                    self.newMenu.loading.draw(self.canvas)
                    self.new_pressed = True
                elif self.new_pressed:
                    config.playing_new = True
                    self.new_pressed = False
                elif config.playing_new:
                    self.current_type = 'game'
                    self.current_menu = 'main'
                    config.current_level = 0
                    config.menu_showing = False
                    config.playing_new = False
                elif self.newMenu.custom_button.get_clicked():
                    if config.clevels_list:
                        self.newMenu.reset_inventory()
                        config.playing_customs = True
                    else:
                        self.newMenu.no_levels_on = True
                elif config.playing_customs:
                    self.current_type = 'game'
                    self.current_menu = 'main'
                    config.current_level = 0
                    config.menu_showing = False
                    config.playing_customs = False
                elif self.newMenu.tutorial_button.get_clicked():
                    self.newMenu.reset_inventory()
                    config.playing_tutorial = True
                elif config.playing_tutorial:
                    self.current_type = 'game'
                    self.current_menu = 'main'
                    config.current_level = 0
                    config.menu_showing = False
                    config.playing_tutorial = False
            elif self.current_menu == 'options':
                self.optionsMenu.draw(self.canvas)
                if self.optionsMenu.back_button.get_clicked():
                    self.current_menu = 'main'
                if self.optionsMenu.save:
                    self.save_settings()
                    self.optionsMenu.save = False
            elif self.current_menu == 'score':
                self.scoreMenu.draw(self.canvas)
                if self.scoreMenu.back_button.get_clicked():
                    self.current_menu = 'main'
            elif self.current_menu == 'credits':
                self.creditsMenu.draw(self.canvas, self.shut_up)
                if self.creditsMenu.back_button.get_clicked():
                    self.current_menu = 'main'
        elif self.current_type == 'game':
            key = pygame.key.get_pressed()
            if self.current_menu == 'main':
                self.gMainMenu.draw(self.canvas)
                if self.gMainMenu.resume_button.get_clicked() or (self.esc_pressed and not key[pygame.K_ESCAPE]):
                    config.paused = False
                    self.esc_pressed = False
                elif self.gMainMenu.exit_button.get_clicked():
                    self.current_type = 'main'
            if key[pygame.K_ESCAPE]:
                self.esc_pressed = True


class Menu:
    def __init__(self, title):
        self.title = Text(
            posx=0,
            posy=0,
            string=title,
            color=colors.BLACK,
            font=config.font,
            size=120)
        self.title.update_pos((config.width / 2) - (self.title.layout.get_width() / 2) + 8, 20)

        self.background_image = None


class MainMenu(Menu):
    def __init__(self):
        Menu.__init__(self, '')
        self.new_button = Button((config.width / 2, 320, 200, 60), "JOGAR")
        self.options_button = Button((config.width / 2, 390, 200, 60), "CONFIGURAÇÕES")
        self.score_button = Button((config.width / 2, 460, 200, 60), "ESTATÍSTICAS")
        self.credits_button = Button((config.width / 2, 530, 200, 60), "CRÉDITOS")

        self.logo = pygame.image.load(os.path.join('assets', 'textures', 'logo.png')).convert_alpha()
        self.logo_rect = self.logo.get_rect()

        self.logo_surface = pygame.Surface(self.logo.get_size()).convert()
        self.logo_surface_rect = self.logo_surface.get_rect()
        self.logo_surface_rect.center = (config.width / 2, 120)

        # self.background = pygame.image.load(os.path.join('assets', 'textures', 'background.png')).convert_alpha()
        # self.background_rect = self.background.get_rect()
        #
        # self.background_surface = pygame.Surface(self.background.get_size()).convert()
        # self.background_surface_rect = self.background_surface.get_rect()
        # self.background_surface_rect.center = (config.width / 2, config.window_height / 2)

        self.stone_tiles = [
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_wall.png')).convert(),
             self.logo_surface_rect.left],
            [pygame.image.load(
                os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_wall_crack.png')).convert(),
             self.logo_surface_rect.left + 160],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_wall.png')).convert(),
             self.logo_surface_rect.left + (2 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_wall.png')).convert(),
             self.logo_surface_rect.left + (3 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_vent.png')).convert(),
             self.logo_surface_rect.left + (4 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_wall.png')).convert(),
             self.logo_surface_rect.left + (5 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_vase.png')).convert(),
             self.logo_surface_rect.left + (6 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_wall.png')).convert(),
             self.logo_surface_rect.left + (7 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_wall.png')).convert(),
             self.logo_surface_rect.left + (8 * 160)]
        ]

        self.baroque_tiles = [
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'baroque.png')).convert(),
             self.logo_surface_rect.left],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'baroque.png')).convert(),
             self.logo_surface_rect.left + 160],
            [pygame.image.load(
                os.path.join('assets', 'textures', 'tiles', 'walls', 'baroque_lamps.png')).convert(),
             self.logo_surface_rect.left + (2 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'baroque.png')).convert(),
             self.logo_surface_rect.left + (3 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'baroque.png')).convert(),
             self.logo_surface_rect.left + (4 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'baroque_worn.png')).convert(),
             self.logo_surface_rect.left + (5 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'baroque.png')).convert(),
             self.logo_surface_rect.left + (6 * 160)]
        ]

        self.wood_tiles = [
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_wall.png')).convert(),
             self.logo_surface_rect.left],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_painting.png')).convert(),
             self.logo_surface_rect.left + 160],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_wall.png')).convert(),
             self.logo_surface_rect.left + (2 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_wall.png')).convert(),
             self.logo_surface_rect.left + (3 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_books.png')).convert(),
             self.logo_surface_rect.left + (4 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_fireplace.png')).convert(),
             self.logo_surface_rect.left + (5 * 160)],
            [pygame.image.load(os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_wall.png')).convert(),
             self.logo_surface_rect.left + (6 * 160)]
        ]

        self.tiles = random.choice((self.stone_tiles, self.baroque_tiles, self.wood_tiles))

        for i in range(len(self.tiles)):
            self.tiles[i][0] = pygame.transform.scale(self.tiles[i][0], (160, 160))

    def draw(self, canvas):
        self.logo_animation(canvas)

        self.new_button.draw(canvas)
        self.options_button.draw(canvas)
        self.score_button.draw(canvas)
        self.credits_button.draw(canvas)

    def logo_animation(self, canvas):
        for tile in self.tiles:
            self.logo_surface.blit(tile[0], (tile[1], self.logo_rect.top))
            tile[1] -= 1

            if tile[1] < self.logo_surface_rect.left - 160:
                tile[1] += (160 * len(self.tiles))

        self.logo_surface.blit(self.logo, (0, 0))

        canvas.blit(self.logo_surface, self.logo_surface_rect)


class NewMenu(Menu):
    def __init__(self, settings):
        Menu.__init__(self, 'NEW GAME')
        self.new_button = Button((config.width / 2, 200, 200, 60), "NOVO JOGO")
        self.custom_button = Button((config.width / 2, 270, 200, 60), "MAPAS")
        self.tutorial_button = Button((config.width / 2, 325, 200, 30), "TUTORIAL")
        self.back_button = Button((config.width / 2, 500, 200, 60), "VOLTAR")

        self.loading = Text(0, 0, "CARREGANDO...", colors.BLACK, config.font, 74)
        self.loading.update_pos((config.width / 2) - (self.loading.layout.get_width() / 2) + 8,
                                (config.height / 2) - (self.loading.layout.get_height() / 2))

        self.nolevels = Text(0, 0, "NENHUM MAPA ENCONTRADO", colors.RED, config.font, 50)
        self.nolevels.update_pos((config.width / 2) - (self.nolevels.layout.get_width() / 2) + 8,
                                 (config.height / 2) - (self.nolevels.layout.get_height() / 2))
        self.timer = 0
        self.no_levels_on = False
        self.settings = settings

    def draw(self, canvas):
        self.new_button.draw(canvas)
        self.custom_button.draw(canvas)
        self.tutorial_button.draw(canvas)
        self.back_button.draw(canvas)
        self.title.draw(canvas)

        if self.no_levels_on:
            self.draw_no_levels(canvas)
        else:
            self.timer = 0

    def reset_inventory(self):
        for i in config.inventory:
            config.inventory[i] = None

        for i in config.held_ammo:
            config.held_ammo[i] = 0

        for i in config.gun_list:
            i.current_mag = 0

        config.current_gun = None
        config.next_gun = None
        config.player_health = config.og_player_health
        config.player_armor = config.og_player_armor
        config.current_level = 0

        config.player_states['dead'] = False
        config.player_states['invopen'] = False
        config.player_states['heal'] = False
        config.player_states['armor'] = False
        config.player_states['cspeed'] = 0

        config.statistics['last enemies'] = 0
        config.statistics['last dtaken'] = 0
        config.statistics['last ddealt'] = 0
        config.statistics['last shots'] = 0
        config.statistics['last levels'] = 0

        config.fov = self.settings['fov']
        config.player_states['cspeed'] = config.player_speed
        config.aiming = False
        config.player.update_collide_list = True

    def draw_no_levels(self, canvas):
        if self.timer <= 1.2:
            self.nolevels.draw(canvas)
        else:
            self.no_levels_on = False

        self.timer += config.dt


class OptionsMenu(Menu):
    def __init__(self, settings):
        Menu.__init__(self, 'CONFIGURAÇÕES')
        self.save = False

        self.strings = ['BAIXO', 'MÉDIO', 'ALTO']
        self.music_strings = ['DESLIGADO', 'MÉDIO', 'ALTO']
        self.degrees = ['50', '60', '70']
        self.onoff = ['LIGADO', 'DESLIGADO']

        self.strings_to_data = {
            'graphics': [(100, 10), (140, 12), (175, 14)],
            'fov': [50, 60, 70],
            'sensitivity': [0.15, 0.25, 0.35],
            'volume': [0.1, 0.5, 1],
            'music volume': [0, 0.5, 1],
            'fullscreen': [True, False], }

        self.graphics_index = self.strings_to_data['graphics'].index(settings['graphics'])
        self.fov_index = self.strings_to_data['fov'].index(settings['fov'])
        self.sens_index = self.strings_to_data['sensitivity'].index(settings['sensitivity'])
        self.vol_index = self.strings_to_data['volume'].index(settings['volume'])
        self.music_index = self.strings_to_data['music volume'].index(settings['music volume'])
        self.fs_index = self.strings_to_data['fullscreen'].index(settings['fullscreen'])

        self.update_strings()

    def update_strings(self):
        self.graphics_button = Button((config.width / 2, 150, 300, 30),
                                      "GRÁFICOS: %s" % self.strings[self.graphics_index])
        self.fov_button = Button((config.width / 2, 200, 300, 30),
                                 "FOV: %s" % self.degrees[self.fov_index])
        self.sensitivity_button = Button((config.width / 2, 250, 300, 30),
                                         "SENSIBILIDADE: %s" % self.strings[self.sens_index])
        self.volume_button = Button((config.width / 2, 300, 300, 30),
                                    "VOLUME PRINCIPAL: %s" % self.strings[self.vol_index])
        self.music_button = Button((config.width / 2, 350, 300, 30),
                                   "VOLUME DA MÚSICA: %s" % self.music_strings[self.music_index])
        self.back_button = Button((config.width / 2, 500, 200, 60), "VOLTAR")

        self.restart = Text(0, 0, 'REINICIE O JOGO PARA APLICAR AS MUDANÇAS', colors.LIGHTGRAY, config.font, 20)
        self.restart.update_pos((config.width / 2) - (self.restart.layout.get_width() / 2), 580)

        self.current_settings = {
            'graphics': self.strings_to_data['graphics'][self.graphics_index],
            'fov': self.strings_to_data['fov'][self.fov_index],
            'sensitivity': self.strings_to_data['sensitivity'][self.sens_index],
            'volume': self.strings_to_data['volume'][self.vol_index],
            'music volume': self.strings_to_data['music volume'][self.music_index],
            'fullscreen': self.strings_to_data['fullscreen'][self.fs_index], }

        self.save = True

    def control_options(self):
        if self.graphics_button.get_clicked():
            self.graphics_index += 1
            if self.graphics_index >= len(self.strings):
                self.graphics_index = 0
            self.update_strings()

        elif self.fov_button.get_clicked():
            self.fov_index += 1
            if self.fov_index >= len(self.degrees):
                self.fov_index = 0
            self.update_strings()

        elif self.sensitivity_button.get_clicked():
            self.sens_index += 1
            if self.sens_index >= len(self.strings):
                self.sens_index = 0
            self.update_strings()

        elif self.volume_button.get_clicked():
            self.vol_index += 1
            if self.vol_index >= len(self.strings):
                self.vol_index = 0
            self.update_strings()

        elif self.music_button.get_clicked():
            self.music_index += 1
            if self.music_index >= len(self.music_strings):
                self.music_index = 0
            self.update_strings()

    def draw(self, canvas):
        self.graphics_button.draw(canvas)
        self.fov_button.draw(canvas)
        self.sensitivity_button.draw(canvas)
        self.volume_button.draw(canvas)
        self.music_button.draw(canvas)
        self.back_button.draw(canvas)
        self.title.draw(canvas)
        self.restart.draw(canvas)

        self.control_options()


class ScoreMenu(Menu):
    def __init__(self):
        Menu.__init__(self, 'ESTATÍSTICAS')

        self.area = pygame.Surface((600, 300))
        self.area_rect = self.area.get_rect()
        self.area_rect.center = (config.width / 2, config.height / 2)
        self.area.fill((200, 200, 200))

        self.middle_area = pygame.Surface((200, 300))
        self.middle_area.fill((180, 180, 180))

        self.back_button = Button((config.width / 2, 500, 200, 60), "Voltar")
        self.score_testing = copy.copy(config.statistics)

        self.highlights = []
        for i in range(6):
            if i == 0:
                self.highlights.append(pygame.Surface((600, 35)).convert_alpha())
            else:
                self.highlights.append(pygame.Surface((600, 30)).convert_alpha())
            self.highlights[i].fill((0, 0, 0, 20))

        # High scores
        self.best_scores = ['HIGHEST SCORES',
                            'ENEMIES  KILLED : %s' % config.statistics['best enemies'],
                            'DAMAGE  DEALT : %s' % config.statistics['best ddealt'],
                            'DAMAGE  TAKEN : %s' % config.statistics['best dtaken'],
                            'SHOTS  FIRED : %s' % config.statistics['best shots'],
                            'LEVEL  STREAK : %s' % config.statistics['best levels']]

        self.texts = []
        self.pos = 10

        for i in range(len(self.best_scores)):
            if i == 0:
                self.texts.append(Text(0, 0, self.best_scores[i], colors.DARKGRAY, config.font, 18))
            else:
                self.texts.append(Text(0, 0, self.best_scores[i], colors.WHITE, config.font, 18))
            self.texts[i].update_pos(10, self.pos)
            self.pos += 30

        # Last play scores
        self.last_scores = ['ÚLTIMA JOGADA',
                            'INIMIGOS ABATIDOS : %s' % config.statistics['last enemies'],
                            'DANO CAUSADO : %s' % config.statistics['last ddealt'],
                            'DANO TOMADO : %s' % config.statistics['last dtaken'],
                            'TIROS DISPARADOS : %s' % config.statistics['last shots'],
                            'NÍVEL STREAK : %s' % config.statistics['last levels']]
        self.last_texts = []
        self.pos = 10

        for i in range(len(self.last_scores)):
            if i == 0:
                self.last_texts.append(Text(0, 0, self.last_scores[i], colors.DARKGRAY, config.font, 18))
            else:
                if self.last_scores[i] == self.best_scores[i] and self.last_scores[i].find(' 0') == -1:
                    self.last_texts.append(Text(0, 0, self.last_scores[i], colors.GRAY, config.font, 18))
                else:
                    self.last_texts.append(Text(0, 0, self.last_scores[i], colors.WHITE, config.font, 18))
            self.last_texts[i].update_pos(210, self.pos)
            self.pos += 30

        self.all_scores = ['TODOS OS TEMPOS',
                           'INIMIGOS ABATIDOS : %s' % config.statistics['all enemies'],
                           'DANO CAUSADO : %s' % config.statistics['all ddealt'],
                           'DANO TOMADO : %s' % config.statistics['all dtaken'],
                           'TIROS DISPARADOS : %s' % config.statistics['all shots'],
                           'NÍVEL STREAK : %s' % config.statistics['all levels'],
                           'HORÁRIO DA JOGADA : {:02d}h {:02d}m'.format(*divmod(config.statistics['playtime'], 60))]
        self.all_texts = []
        self.pos = 10

        for i in range(len(self.all_scores)):
            if i == 0:
                self.all_texts.append(Text(0, 0, self.all_scores[i], colors.DARKGRAY, config.font, 18))
            else:
                self.all_texts.append(Text(0, 0, self.all_scores[i], colors.WHITE, config.font, 18))
            self.all_texts[i].update_pos(410, self.pos)
            self.pos += 30

    def draw(self, canvas):
        if self.score_testing != config.statistics:
            self.__init__()

        self.title.draw(canvas)
        self.back_button.draw(canvas)
        self.area.fill((200, 200, 200))
        self.area.blit(self.middle_area, (200, 0))

        pos = 0
        for i in self.highlights:
            self.area.blit(i, (0, pos))
            if pos == 0:
                pos = 5
            pos += 60

        for i in self.texts:
            i.draw(self.area)

        for i in self.last_texts:
            i.draw(self.area)

        for i in self.all_texts:
            i.draw(self.area)

        canvas.blit(self.area, self.area_rect)


class CreditsMenu(Menu):
    def __init__(self):
        Menu.__init__(self, 'CRÉDITOS')
        self.back_button = Button((config.width / 2, 500, 200, 60), "VOLTAR")

        # Created by
        self.createdby = Text(
            posx=0,
            posy=0,
            string='CRIADO POR',
            font=config.font,
            color=colors.LIGHTGRAY,
            size=24)
        self.createdby.update_pos((config.width / 2) - (self.createdby.layout.get_width() / 2) + 8, 130)

        self.maxwellsalmon = Text(
            posx=0,
            posy=0,
            string='DAVI COSTA SCARTEZINI',
            font=config.font,
            color=colors.DARKGRAY,
            size=38)
        self.maxwellsalmon.update_pos(
            (config.width / 2) - (self.maxwellsalmon.layout.get_width() / 2) + 8, 160)

        # Music
        self.musicby = Text(
            posx=0,
            posy=0,
            string='MUSICA POR DAVI COSTA SCARTEZINI',
            color=colors.LIGHTGRAY,
            font=config.font,
            size=20)
        self.musicby.update_pos((config.width / 2) - (self.musicby.layout.get_width() / 2) + 8, 210)

        self.eli = Text(
            posx=0,
            posy=0,
            string='HUD-LUM @ SOUNDCLOUD',
            color=colors.DARKGRAY,
            font=config.font,
            size=30)
        self.eli.update_pos((config.width / 2) - (self.eli.layout.get_width() / 2) + 8, 240)

        # Maps
        self.contributions = Text(
            posx=0,
            posy=0,
            string='THANKS  TO',
            color=colors.LIGHTGRAY,
            font=config.font,
            size=20)
        self.contributions.update_pos(
            (config.width / 2) - (self.contributions.layout.get_width() / 2) + 8, 290)

        self.contributors = Text(
            posx=0,
            posy=0,
            string='POELE,  OLE,  ROCKETTHEMINIFIG,  ANDY BOY,  J4CKINS',
            color=colors.DARKGRAY,
            font=config.font,
            size=20)
        self.contributors.update_pos(
            (config.width / 2) - (self.contributors.layout.get_width() / 2) + 8, 320)
        self.contributors2 = Text(
            posx=0,
            posy=0,
            string='THEFATHOBBITS,  STARLITEPONY',
            color=colors.DARKGRAY,
            font=config.font,
            size=20)
        self.contributors2.update_pos(
            (config.width / 2) - (self.contributors2.layout.get_width() / 2) + 8, 345)

        self.specialthanks = Text(
            posx=0,
            posy=0,
            string='THANKS  TO  THE  PYGAME  COMMUNITY  FOR  HELP  AND  MOTIVATION',
            color=colors.DARKGRAY,
            font=config.font,
            size=15)
        self.specialthanks.update_pos(
            (config.width / 2) - (self.specialthanks.layout.get_width() / 2) + 8, 380)

        self.and_you = Text(
            posx=0,
            posy=0,
            string='THANKS  TO  YOU  FOR  PLAYING!',
            color=colors.GREEN,
            font=config.font,
            size=22)
        self.and_you.update_pos((config.width / 2) - (self.and_you.layout.get_width() / 2) + 8, 410)

    def draw(self, canvas, show):
        self.back_button.draw(canvas)
        self.title.draw(canvas)
        self.createdby.draw(canvas)
        self.musicby.draw(canvas)
        self.eli.draw(canvas)
        self.contributions.draw(canvas)
        self.contributors.draw(canvas)
        self.contributors2.draw(canvas)
        self.specialthanks.draw(canvas)
        self.maxwellsalmon.draw(canvas)

        if show or config.statistics['playtime'] >= 120:
            self.and_you.draw(canvas)


class SupportSplash:
    def __init__(self):
        self.area = pygame.Surface((200, 300)).convert()
        self.rect = self.area.get_rect()
        self.rect.topleft = config.width - 220, config.height - 280
        self.area.fill((200, 200, 200))

        self.title = Text(
            posx=0,
            posy=0,
            string='OBRIGADO POR JOGAR',
            color=colors.DARKGRAY,
            font=config.font,
            size=19)
        self.title.update_pos((self.rect.width / 2) - (self.title.layout.get_width() / 2) + 2, 5)

        self.pleas = ['Você está jogando A Casa', 'por mais de duas horas agora.  Eu',
                      'espero que você tenha gostado']
        self.texts = []

        self.pos = 30
        self.button = Button((config.width - 120, config.height - 15, 192, 40),
                             "ME DEIXE EM PAZ!")

        for i in range(len(self.pleas)):
            self.texts.append(Text(0, 0, self.pleas[i], colors.WHITE, config.font, 15))
            self.texts[i].update_pos((self.rect.width / 2) - (self.texts[i].layout.get_width() / 2) + 2, self.pos)
            self.pos += 17

    def draw(self, canvas):
        self.title.draw(self.area)

        for text in self.texts:
            text.draw(self.area)

        canvas.blit(self.area, self.rect)

        self.button.draw(canvas)


class PauseMenu(Menu):
    def __init__(self):
        Menu.__init__(self, config.title.upper())
        self.resume_button = Button((config.width / 2, 200, 200, 60), "CONTINUAR")
        self.exit_button = Button((config.width / 2, 500, 200, 60), "SAIR")

        self.background = pygame.Surface((config.width, config.height)).convert_alpha()
        self.background.fill((100, 100, 100, 10))

    def draw(self, canvas):
        canvas.blit(self.background, (0, 0))
        self.resume_button.draw(canvas)
        self.exit_button.draw(canvas)
        self.title.draw(canvas)


class Button:
    hovered = []

    def __init__(self, xywh, text):
        self.surface = pygame.Surface((xywh[2], xywh[3]))
        self.rect = self.surface.get_rect()
        self.rect.center = (xywh[0], xywh[1])
        self.clicked = False
        self.hover = False

        self.text = Text(0, 0, text, colors.WHITE, config.font, 24)
        self.text.update_pos(xywh[0] - self.text.layout.get_width() / 2,
                             xywh[1] - (self.text.layout.get_height() / 2) + 2)

        self.filling = colors.LIGHTGRAY
        self.click_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'button.wav'))
        self.hover_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'button_hov.wav'))

    def draw(self, canvas):
        self.surface.fill(self.filling)
        canvas.blit(self.surface, self.rect)
        self.text.draw(canvas)

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.filling = colors.DARKGRAY
        else:
            self.filling = colors.LIGHTGRAY

    def get_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.rect not in Button.hovered:
                Button.hovered.append(self.rect)

            if not self.hover:
                self.hover = True
                sound.play_sound(self.hover_sound, 0)

            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
            if not pygame.mouse.get_pressed()[0] and self.clicked:
                self.clicked = False
                sound.play_sound(self.click_sound, 0)
                return True
            else:
                return False
        self.hover = False
        if self.rect in Button.hovered:
            Button.hovered.remove(self.rect)
        return False
