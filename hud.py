import pygame
import os

import colors
import config
from text import Text


class HUD:
    def __init__(self):
        self.health = config.player_health
        self.armor = config.player_armor
        self.ammo = 0

        self.sprite = pygame.image.load(os.path.join('assets', 'textures', 'hud.png')).convert()
        self.sprite = pygame.transform.scale(self.sprite, (config.actual_width, config.window_height - config.height))
        self.rect = self.sprite.get_rect()
        self.rect.topleft = (0, config.height)

        self.text = [
            Text(int(self.rect.width / 35), self.rect.y + int(self.rect.height / 2.5),
                 'ARMADURA',
                 colors.DARKGRAY, 35),
            Text(int(self.rect.width / 3.4), self.rect.y + int(self.rect.height / 2.5),
                 'VIDA',
                 colors.DARKGRAY, 35),
            Text(int(self.rect.width / 1.8), self.rect.y + int(self.rect.height / 2.5),
                 'MUNIÇÃO',
                 colors.DARKGRAY, 35)
        ]

        self.arrow_spritesheet = pygame.image.load(os.path.join('assets', 'textures', 'arrows.png')).convert_alpha()

        self.arrow = self.arrow_spritesheet.subsurface(0, 0, 17, 17).convert_alpha()
        self.arrow = pygame.transform.scale(self.arrow, (50, 50))
        self.original_arrow = self.arrow
        self.arrow_rect = self.arrow.get_rect()
        self.arrow_rect.center = (self.rect.topright[0] - 46, self.rect.topright[1] + 66)
        self.arrow_center = (self.arrow_rect.centerx - self.arrow_rect.width / 2,
                             self.arrow_rect.centery - self.arrow_rect.height / 2)

        self.arrow2 = self.arrow_spritesheet.subsurface(0, 17, 17, 17).convert_alpha()
        self.arrow2 = pygame.transform.scale(self.arrow2, (50, 50))
        self.original_arrow2 = self.arrow2
        self.arrow3 = self.arrow_spritesheet.subsurface(0, 34, 17, 17).convert_alpha()
        self.arrow3 = pygame.transform.scale(self.arrow3, (50, 50))
        self.original_arrow3 = self.arrow3

    def render(self, canvas):
        canvas.blit(self.sprite, self.rect)
        self.text[0].update_string('%s / 100' % config.player_armor)
        self.text[1].update_string('%s / 100' % config.player_health)
        if config.current_gun and config.current_gun.ammo_type:
            self.text[2].update_string(
                '%s / %s' % (config.current_gun.current_mag, config.held_ammo[config.current_gun.ammo_type]))
        else:
            self.text[2].update_string('-- / --')
        for string in self.text:
            string.draw(canvas)

        self.arrow = pygame.transform.rotate(self.original_arrow, config.end_angle)
        self.arrow_rect.topleft = (self.arrow_center[0] - self.arrow.get_rect().width / 2,
                                   self.arrow_center[1] - self.arrow.get_rect().height / 2)
        canvas.blit(self.arrow, self.arrow_rect)

        self.arrow2 = pygame.transform.rotate(self.original_arrow2, config.end_angle)
        self.arrow3 = pygame.transform.rotate(self.original_arrow3, config.end_angle)

        canvas.blit(self.arrow2, (self.arrow_rect[0], self.arrow_rect[1] - 4))
        canvas.blit(self.arrow3, (self.arrow_rect[0], self.arrow_rect[1] - 8))

        if config.ground_weapon:
            self.ammoslot1 = pygame.Surface((191, 79)).convert_alpha()
            self.ammoslot1_rect = self.ammoslot1.get_rect()
            self.ammoslot1_rect.topleft = (self.rect.x + 320, self.rect.y + 33)
            self.ammoslot1.fill((100, 100, 100, 100))
            self.ammoslot1_text = Text(
                posx=100,
                posy=100,
                string=str(config.ground_weapon),
                color=colors.WHITE,
                size=15
            )
