import pygame
import os

import config
import sound

from sprite import Sprite


class Item:
    def __init__(self, pos, sprite, item_type, effect):
        self.pos = (pos[0] * config.tile_size, pos[1] * config.tile_size)
        self.map_pos = pos
        self.item_type = item_type
        self.rect = pygame.Rect(self.pos[0], self.pos[1], int(config.tile_size), int(config.tile_size))
        self.rect.center = (self.pos[0] + config.tile_size / 2, self.pos[1] + config.tile_size / 2)
        self.sprite = Sprite(pygame.image.load(sprite), hash(item_type), self.rect.center, 'sprite')
        self.effect = effect
        self.sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'pickup.wav'))

    def update(self):
        remove = False
        if self.rect:
            if config.player_rect.colliderect(self.rect):
                if self.item_type == 'health':
                    if config.player_health < 100:
                        config.player_health += self.effect
                        if config.player_health > 100:
                            config.player_health = 100
                        config.player_states['heal'] = True
                        remove = True
                elif self.item_type == 'armor':
                    if config.player_armor < 100:
                        config.player_armor += self.effect
                        if config.player_armor > 100:
                            config.player_armor = 100
                        config.player_states['armor'] = True
                        remove = True
                elif self.item_type == 'bullet' or self.item_type == 'shell' or self.item_type == 'ferromag':
                    if config.held_ammo[self.item_type] < config.max_ammo[self.item_type]:
                        config.held_ammo[self.item_type] += self.effect
                        if config.held_ammo[self.item_type] > config.max_ammo[self.item_type]:
                            config.held_ammo[self.item_type] = config.max_ammo[self.item_type]
                        config.player_states['armor'] = True
                        remove = True
                elif self.item_type == 'primary':
                    if not config.inventory['primary']:
                        config.inventory['primary'] = self.effect
                        config.next_gun = self.effect
                        config.player_states['armor'] = True
                        remove = True
                    else:
                        config.ground_weapon = self.effect
                elif self.item_type == 'secondary':
                    if not config.inventory['secondary']:
                        config.inventory['secondary'] = self.effect
                        config.next_gun = self.effect
                        config.player_states['armor'] = True
                        remove = True
                    else:
                        config.ground_weapon = self.effect
                elif self.item_type == 'melee':
                    if not config.inventory['melee']:
                        config.inventory['melee'] = self.effect
                        config.next_gun = self.effect
                        config.player_states['armor'] = True
                        remove = True
                    else:
                        config.ground_weapon = self.effect

                if self.sprite in config.all_sprites and remove:
                    sound.play_sound(self.sound, 0)
                    config.all_sprites.remove(self.sprite)
                    self.rect = None
