import pygame
import math

import config


class Sprite:
    def __init__(self, texture, _id, pos, texture_type, parent=None):
        self.texture = texture
        self.texture = (pygame.transform
                        .scale(self.texture,
                               (config.tile_size * 2, config.tile_size * 4))
                        .convert_alpha())
        self.texture_type = texture_type
        self.type = texture_type
        self.ID = _id

        self.rect = self.texture.get_rect()
        self.rect_size = (self.rect.width, self.rect.height)
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

        self.new_rect = None
        self.distance = None

        self.theta = None

        if self.texture_type == 'npc':
            self.parent = parent
        else:
            self.parent = None

        config.all_sprites.append(self)

    def get_pos(self, canvas):
        angle = config.player_angle
        fov = config.fov

        xpos = self.rect.centerx - config.player_rect[0]
        ypos = config.player_rect[1] - self.rect.centery

        dist = math.sqrt(xpos * xpos + ypos * ypos)
        if dist == 0:
            dist += 0.0001
        self.distance = dist

        thetaTemp = math.atan2(ypos, xpos)
        thetaTemp = math.degrees(thetaTemp)
        if thetaTemp < 0:
            thetaTemp += 360

        self.theta = thetaTemp

        yTmp = angle + (fov / 2) - thetaTemp
        if thetaTemp > 270 and angle < 90:
            yTmp = angle + (fov / 2) - thetaTemp + 360
        if angle > 270 and thetaTemp < 90:
            yTmp = angle + (fov / 2) - thetaTemp - 360

        xTmp = yTmp * config.width / fov

        sprite_height = int((self.rect.height / dist) * (100 / math.tan(math.radians(fov * 0.8))))
        if sprite_height > 2500:
            sprite_height = 2500

        sprite_width = int(self.rect.width / self.rect.height * sprite_height)

        if (0 - sprite_width) < xTmp < (config.actual_width + sprite_width):
            config.zbuffer.append(self)

            if self.parent:
                self.parent.in_canvas = True
        else:
            if self.parent:
                self.parent.in_canvas = False

        self.new_size = pygame.transform.scale(self.texture, (sprite_width, sprite_height))
        self.new_rect = self.new_size.get_rect()
        self.new_rect.center = (xTmp, config.width / 2)
        if self.parent:
            self.parent.hit_rect = self.new_rect

    def draw(self, canvas):
        canvas.blit(self.new_size, self.new_rect)

    def update_pos(self, pos):
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
