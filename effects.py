import pygame
import config
import colors
from text import Text
import random


class Effects:
    def __init__(self):
        self.title = Text(0, 0, "None :-)", colors.BLACK, 60)

        self.hurt_intensity = 128
        self.dead_intensity = 0
        self.heal_intensity = 85
        self.armor_intensity = 85
        self.fade_value = 0
        self.title_timer = 0

        self.int_to_string = {
            0: 'PRIMEIRO',
            1: 'SEGUNDO',
            2: 'TERCEIRO',
            3: 'QUARTO',
            4: 'QUINTO',
            5: 'SEXTO',
            6: 'SÉTIMO',
            7: 'OITAVO',
            8: 'NONO',
            9: 'DÉCIMO',
            10: 'DÉCIMO PRIMEIRO',
            11: 'DÉCIMO SEGUNDO',
            12: 'DÉCIMO TERCEIRO',
            13: 'DÉCIMO QUARTO',
            14: 'DÉCIMO QUINTO',
            15: 'DÉCIMO SEXTO',
            16: 'DÉCIMO SÉTIMO',
            17: 'DÉCIMO OITAVO',
            18: 'DÉCIMO NONO',
            19: 'VIGÉSIMO',
        }

    def render(self, canvas):
        if config.screen_shake > 0:
            self.screen_shake()
        if config.player_states['hurt'] or config.player_states['dead']:
            self.player_hurt(canvas)
        if config.player_states['heal']:
            self.player_heal(canvas)
        if config.player_states['armor']:
            self.player_armor(canvas)
        if config.player_states['fade'] or config.player_states['black']:
            self.fade_black(canvas)
        if config.player_states['title']:
            self.show_title(canvas)

    @staticmethod
    def screen_shake():
        if config.screen_shake > 0:
            config.axes = (random.randint(-config.screen_shake, config.screen_shake),
                           random.randint(-config.screen_shake, config.screen_shake))
            config.screen_shake /= 2
            config.screen_shake = int(config.screen_shake)
            if config.screen_shake == 0:
                config.screen_shake = 0
                config.axes = (0, 0)

    def player_hurt(self, canvas):
        blood = pygame.Surface((config.actual_width, config.height)).convert_alpha()

        if config.player_states['hurt']:
            blood.fill((255, 0, 0, max(min(self.hurt_intensity, 255), 0)))
            self.hurt_intensity = int(self.hurt_intensity / (2 - config.dt))
            if self.hurt_intensity == 0:
                config.player_states['hurt'] = False
                self.hurt_intensity = 128

        elif config.player_states['dead']:
            blood.fill((255, 0, 0, self.dead_intensity))
            if self.dead_intensity <= 120:
                self.dead_intensity += 10
        canvas.blit(blood, (0, 0))

    def player_heal(self, canvas):
        heal = pygame.Surface((config.actual_width, config.height)).convert_alpha()

        heal.fill((0, 255, 0, self.heal_intensity))
        self.heal_intensity = int(self.heal_intensity / (2 - config.dt))

        if self.heal_intensity == 0:
            config.player_states['heal'] = False
            self.heal_intensity = 85
        canvas.blit(heal, (0, 0))

    def player_armor(self, canvas):
        armor = pygame.Surface((config.actual_width, config.height)).convert_alpha()

        armor.fill((0, 0, 225, self.armor_intensity))
        self.armor_intensity = int(self.armor_intensity / (2 - config.dt))

        if self.armor_intensity == 0:
            config.player_states['armor'] = False
            self.armor_intensity = 85
        canvas.blit(armor, (0, 0))

    def fade_black(self, canvas):
        black = pygame.Surface((config.actual_width, config.height)).convert_alpha()
        black.fill((0, 0, 0, max(0, min(self.fade_value, 255))))
        if config.player_states['fade'] and not config.player_states['black']:
            if self.fade_value < 400:
                self.fade_value += 15
            else:
                config.player_states['black'] = True
                config.player_states['fade'] = False

        elif config.player_states['fade'] and config.player_states['black']:
            if self.fade_value > 0:
                self.fade_value -= 20
            elif self.fade_value <= 0:
                self.fade_value = 0
                config.player_states['black'] = False
                config.player_states['fade'] = False

        canvas.blit(black, (0, 0))

    def show_title(self, canvas):
        if config.levels_list == config.clevels_list or config.levels_list == config.tlevels_list:
            self.title.update_string(config.levels_list[config.current_level].name)
            self.title.update_pos((config.actual_width / 2) - (self.title.layout.get_width() / 2) + 8, 200)

            white_box = (pygame.Surface((self.title.layout.get_width() + 5, self.title.layout.get_height() + 5))
                         .convert_alpha())
            white_box.fill((255, 255, 255, 180))

        elif config.levels_list == config.glevels_list:
            self.title.update_pos((config.actual_width / 2) - (self.title.layout.get_width() / 2) + 8, 200)
            if config.current_level in self.int_to_string:
                self.title.update_string("%s  NÍVEL" % self.int_to_string[config.current_level])
            else:
                self.title.update_string("NÍVEL %s" % (config.current_level + 1))
            white_box = pygame.Surface((self.title.layout.get_width() + 5, self.title.layout.get_height() + 5)).convert_alpha()
            white_box.fill((255, 255, 255, 180))

        if self.title_timer <= 3:
            canvas.blit(white_box, (self.title.posx - 7, self.title.posy - 8))
            self.title.draw(canvas)
            self.title_timer += config.dt
        else:
            config.player_states['title'] = False
            self.title_timer = 0
