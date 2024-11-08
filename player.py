import math
import os
import pygame

import colors
import config
import sound


class Player:
    def __init__(self, pos):
        self.max_speed = config.player_speed
        self.speed = 0
        self.angle = config.player_angle
        self.health = config.player_health

        self.real_x = pos[0]
        self.real_y = pos[1]

        self.color = colors.BLUE
        self.sprite = pygame.Surface([config.tile_size / 12, config.tile_size / 12])
        self.sprite.fill(self.color)
        self.rect = self.sprite.get_rect()
        self.rect.x = self.real_x
        self.rect.y = self.real_y
        config.player_rect = self.rect
        self.last_pos_tile = None

        self.mouse = pygame.mouse
        self.sensitivity = config.sensitivity
        self.gun = 0
        self.gunsprites_aim = []
        self.gunsprites_shoot = []

        config.player = self
        self.collide_list = config.all_solid_tiles + config.npc_list
        self.update_collide_list = False
        self.solid = True
        self.dead = False
        self.last_call = 0
        self.type = 'player'
        self.hurt_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'damage.ogg'))
        self.change_level = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'next_level.ogg'))

        self.current_level = config.current_level

        self.mouse2 = 0
        self.inventory = 0
        self.esc_pressed = False
        self.dont_open_menu = False

    def direction(self, offset, distance):
        if distance == 0:
            direction = [math.cos(math.radians(self.angle + offset)), -math.sin(math.radians(self.angle + offset))]
        else:
            direction = [(math.cos(math.radians(self.angle + offset))) * distance,
                         (-math.sin(math.radians(self.angle + offset))) * distance]
        return direction

    def control(self, canvas):
        if len(self.collide_list) != len(config.all_solid_tiles + config.npc_list):
            self.collide_list = config.all_solid_tiles + config.npc_list
        elif self.current_level != config.current_level:
            self.collide_list = config.all_solid_tiles + config.npc_list
            self.current_level = config.current_level
        elif self.update_collide_list:
            self.collide_list = config.all_solid_tiles + config.npc_list
            self.update_collide_list = False

        if self.health != config.player_health and config.player_states['heal']:
            self.health = config.player_health

        key = pygame.key.get_pressed()

        if not config.player_states['dead']:
            if not config.player_states['invopen']:

                if config.aiming:
                    self.sensitivity = config.sensitivity / 3
                    self.max_speed = config.player_speed / 3
                    if self.speed > self.max_speed:
                        self.speed = self.max_speed
                else:
                    self.sensitivity = config.sensitivity
                    self.max_speed = config.player_speed

                if key[pygame.K_a] or key[pygame.K_d] or key[pygame.K_w] or key[pygame.K_s]:
                    if self.speed < self.max_speed:
                        self.speed += 50
                        if self.speed > self.max_speed:
                            self.speed = self.max_speed
                else:
                    if self.speed > 0:
                        if self.last_call == 0:
                            self.move(self.direction(90, self.speed * 0.8))
                        elif self.last_call == 1:
                            self.move(self.direction(-90, self.speed * 0.8))
                        elif self.last_call == 2:
                            self.move(self.direction(0, self.speed))
                        elif self.last_call == 3:
                            self.move(self.direction(0, -self.speed * 0.5))

                        self.speed -= 80

                        if self.speed < 1:
                            self.speed = 0

                if key[pygame.K_a]:
                    self.move(self.direction(90, self.speed * 0.8))
                    self.last_call = 0
                if key[pygame.K_d]:
                    self.move(self.direction(-90, self.speed * 0.8))
                    self.last_call = 1
                if key[pygame.K_w]:
                    self.move(self.direction(0, self.speed))
                    self.last_call = 2
                if key[pygame.K_s]:
                    self.move(self.direction(0, -self.speed * 0.5))
                    self.last_call = 3

                config.player_states['cspeed'] = self.speed

                if pygame.mouse.get_pressed()[2] and self.mouse2 < 1:
                    config.mouse2_btn_active = True
                    self.mouse2 += 1
                elif self.mouse2 >= 1:
                    config.mouse2_btn_active = False
                if not pygame.mouse.get_pressed()[2]:
                    self.mouse2 = 0

                if pygame.mouse.get_pressed()[0] and not config.player_states['dead']:
                    config.mouse_btn_active = True
                else:
                    config.mouse_btn_active = False

                if key[pygame.K_r]:
                    config.reload_key_active = True
                else:
                    config.reload_key_active = False

                if key[pygame.K_1] and config.inventory['primary']:
                    config.next_gun = config.inventory['primary']
                elif key[pygame.K_2] and config.inventory['secondary']:
                    config.next_gun = config.inventory['secondary']
                elif key[pygame.K_3] and config.inventory['melee']:
                    config.next_gun = config.inventory['melee']

                if self.angle >= 360:
                    self.angle = 0
                elif self.angle < 0:
                    self.angle = 359

                if key[pygame.K_e]:
                    if config.middle_slice:
                        if config.middle_slice_len <= config.tile_size * 1.5 and (
                                config.middle_slice.type == 'vdoor' or config.middle_slice.type == 'hdoor'):
                            config.middle_slice.sesam_luk_dig_op()
                        elif config.middle_slice_len <= config.tile_size and config.middle_slice.type == 'end' and not config.player_states['fade']:
                            config.player_states['fade'] = True
                            config.level_transition = True
                            sound.play_sound(self.change_level, 0)

                madd = self.mouse.get_rel()[0] * self.sensitivity
                if madd > 38:
                    madd = 38
                elif madd < -38:
                    madd = -38
                self.angle -= madd
                config.player_angle = self.angle

            if key[pygame.K_TAB] and self.inventory < 1:
                if config.player_states['invopen']:
                    config.player_states['invopen'] = False
                    config.inv_strings_updated = False
                else:
                    config.player_states['invopen'] = True

                self.inventory += 1
            elif not key[pygame.K_TAB]:
                self.inventory = 0

            if key[pygame.K_ESCAPE] and config.player_states['invopen']:
                config.player_states['invopen'] = False
                config.inv_strings_updated = False
                self.dont_open_menu = True
            elif not key[pygame.K_ESCAPE] and not config.player_states['invopen']:
                self.dont_open_menu = False

            if key[pygame.K_ESCAPE] and not self.dont_open_menu:
                self.esc_pressed = True
            elif self.esc_pressed and not self.dont_open_menu:
                config.in_game = False
                self.esc_pressed = False

        if self.health > config.player_health:
            config.statistics['last dtaken'] += (self.health - config.player_health)
            self.health = config.player_health
            config.player_states['hurt'] = True
            sound.play_sound(self.hurt_sound, 0)
        if config.player_health <= 0:
            self.dead = True
            config.player_states['dead'] = True
        if config.player_health < 0:
            config.player_health = 0

        if not config.in_game or config.player_states['invopen']:
            pygame.event.set_grab(False)
            self.mouse.set_visible(True)
        else:
            pygame.event.set_grab(True)
            self.mouse.set_visible(False)

    def move(self, pos):
        if config.cfps > 5:
            if pos[0] != 0:
                self.update(pos[0], 0)
            if pos[1] != 0:
                self.update(0, pos[1])

    def update(self, x, y):
        self.real_x += x * config.dt
        self.real_y += y * config.dt
        self.rect.x = self.real_x
        self.rect.y = self.real_y
        config.player_rect = self.rect
        tile_hit_list = pygame.sprite.spritecollide(self, self.collide_list, False)

        for tile in tile_hit_list:
            if tile.solid:
                if x > 0:
                    self.rect.right = tile.rect.left
                    self.real_x = self.rect.x
                if x < 0:
                    self.rect.left = tile.rect.right
                    self.real_x = self.rect.x
                if y > 0:
                    self.rect.bottom = tile.rect.top
                    self.real_y = self.rect.y
                if y < 0:
                    self.rect.top = tile.rect.bottom
                    self.real_y = self.rect.y

        config.player_map_pos = [int(self.rect.centerx / config.tile_size),
                                 int(self.rect.centery / config.tile_size)]

        generator_check_list = [x for x in config.walkable_area if x.map_pos == config.player_map_pos]
        if generator_check_list:
            pos = generator_check_list[0].map_pos
        else:
            pos = []

        check_list = config.walkable_area + config.all_solid_tiles
        out_generator = [x for x in check_list if x.map_pos == config.player_map_pos]
        if out_generator:
            pos2 = out_generator[0].map_pos
        else:
            pos2 = []

        if config.player_map_pos == pos:
            config.last_player_map_pos = config.player_map_pos
            self.last_pos_tile = generator_check_list[0]

        elif config.player_map_pos != pos2 and config.last_player_map_pos:
            if self.last_pos_tile:
                config.player_map_pos = config.last_player_map_pos
                self.rect.center = self.last_pos_tile.rect.center
                config.player_rect = self.rect
                self.real_x = self.rect.x
                self.real_y = self.rect.y

    def draw(self, canvas):
        pointer = self.direction(0, 10)
        p1 = pointer[0] + self.rect.center[0]
        p2 = pointer[1] + self.rect.center[1]
        canvas.blit(self.sprite, (self.rect.x / 4, self.rect.y / 4))
        pygame.draw.line(canvas, self.color, (self.rect.center[0] / 4, self.rect.center[1] / 4), (p1 / 4, p2 / 4))
