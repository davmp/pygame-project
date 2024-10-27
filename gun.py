import pygame
import random
import math
import os

import config
import sound


class Gun:
    def __init__(self, textures, stats, sounds, aim_pos):
        self.spritesheet = pygame.image.load(textures['spritesheet'])
        self.itemtexture = textures['item']
        self.subitemtexture = pygame.transform.scale(
            pygame.image.load(self.itemtexture).subsurface(0, 112, 64, 16).convert_alpha(), (256, 64))
        self.rect = self.spritesheet.get_rect()
        self.spritesheet = pygame.transform.scale(self.spritesheet,
                                                  (int(self.rect.width * 6), int(self.rect.height * 6)))
        self.aim = [self.spritesheet.subsurface(0, 0, 420, 360).convert_alpha(),
                    self.spritesheet.subsurface(0, 360, 420, 360).convert_alpha(),
                    self.spritesheet.subsurface(0, 720, 420, 360).convert_alpha()]
        self.hipfire = [self.spritesheet.subsurface(420, 0, 420, 360).convert_alpha(),
                        self.spritesheet.subsurface(420, 360, 420, 360).convert_alpha(),
                        self.spritesheet.subsurface(420, 720, 420, 360).convert_alpha()]
        self.aimdown = [self.spritesheet.subsurface(840, 0, 420, 360).convert_alpha(),
                        self.spritesheet.subsurface(840, 360, 420, 360).convert_alpha(),
                        self.spritesheet.subsurface(840, 720, 420, 360).convert_alpha()]
        self.reload = [self.spritesheet.subsurface(0, 0, 420, 360).convert_alpha(),
                       self.spritesheet.subsurface(1260, 0, 420, 360).convert_alpha(),
                       self.spritesheet.subsurface(1260, 360, 420, 360).convert_alpha(),
                       self.spritesheet.subsurface(1260, 720, 420, 360).convert_alpha(),
                       self.spritesheet.subsurface(1260, 1080, 420, 360).convert_alpha(),
                       self.spritesheet.subsurface(1260, 1440, 420, 360).convert_alpha()]

        self.sounds = sounds
        self.hit_marker = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'hitmarker.ogg'))

        self.dmg = stats['dmg']
        self.accuracy = stats['spread'] * 2
        self.firerate = stats['firerate']

        self.hit_percent = stats['hitchance']
        self.rlspeed = stats['rlspeed']
        self.aim_pos = [config.actual_width / 2 - aim_pos[0] * 6,
                        config.height / 2 - aim_pos[1] * 6]
        self.OG_aim_pos = [config.actual_width / 2 - aim_pos[0] * 6,
                           config.height / 2 - aim_pos[1] * 6]
        self.raw_aim_pos = aim_pos
        self.mag_size = stats['magsize']
        if stats['magsize'] == 3.1415:
            self.mag_size = 2
        self.zoom = stats['zoom']
        self.ammo_type = stats['ammotype']
        self.guntype = stats['guntype']
        self.name = stats['name']
        self.stats = stats

        if self.guntype != 'melee':
            self.range = stats['range'] * config.tile_size
        else:
            self.range = config.tile_size * 0.9

        self.hit_rect = pygame.Rect((config.actual_width / 2) - (self.accuracy / 2), 0,
                                    self.accuracy, 600)

        self.current_img = self.aim[0]
        self.current_mag = 0
        self.timer = 0
        self.firetimer = self.firerate

        self.aim_busy = False
        self.aim_is_up = False
        self.shoot_busy = False
        self.reload_busy = False

        self.go_reload_next_my_gun = False
        self.have_shot = False
        self.sintemp = 0
        self.swing = 10
        self.wobble = 20

        self.ID = hash(self)

        if self.guntype != 'melee':
            self.shoottime = 0.03
        else:
            self.shoottime = 0.1

    def update_rect(self, accuracy_added):
        self.hit_rect.width = self.hit_rect.width * accuracy_added
        self.hit_rect.centerx = config.actual_width / 2

    def aim_animation(self):
        if self.guntype != 'melee':
            if not self.aim_is_up:
                # Raise the gun
                self.aim_busy = True
                if self.current_img != self.aim[-1] and self.timer >= 0.08:
                    x = self.aim.index(self.current_img) + 1
                    self.current_img = self.aim[x]
                    config.fov -= self.zoom
                    self.timer = 0
                elif self.current_img == self.aim[-1]:
                    self.aim_busy = False
                    self.aim_is_up = True
                    self.update_rect(0.5)
                    self.hit_percent += 20
                    config.aiming = True

            elif self.aim_is_up:
                # Lower the gun
                self.aim_busy = True
                if self.current_img != self.aim[0] and self.timer >= 0.10:
                    x = self.aim.index(self.current_img) - 1
                    self.current_img = self.aim[x]
                    config.fov += self.zoom
                    self.timer = 0
                elif self.current_img == self.aim[0]:
                    self.aim_busy = False
                    self.aim_is_up = False
                    self.update_rect(2)
                    self.hit_percent -= 20
                    config.aiming = False
        else:
            config.aiming = False

    def shoot_animation(self):
        if self.current_mag > 0 or self.guntype == 'melee':
            if self.firetimer >= self.firerate:
                if not self.aim_is_up and self.guntype != 'melee':
                    if self.current_img not in self.hipfire:
                        self.current_img = self.hipfire[random.randint(0, 1)]
                        self.shoot_busy = True
                        sound.play_sound(random.choice(self.sounds['shot']), 0)
                        config.screen_shake = self.dmg * 2
                        self.damage()
                        self.timer = 0
                    elif self.hipfire.index(self.current_img) <= 1 and self.timer >= self.shoottime:
                        self.current_img = self.hipfire[-1]
                        self.timer = 0
                    elif self.current_img == self.hipfire[-1] and self.timer >= self.shoottime:
                        self.current_img = self.aim[0]
                        self.shoot_busy = False
                        self.current_mag -= 1
                        config.statistics['last shots'] += 1
                        if self.stats['magsize'] == 3.1415:
                            self.current_mag -= 1
                            config.statistics['last shots'] += 1
                        self.firetimer = 0
                elif self.guntype == 'melee':
                    if self.current_img not in self.hipfire:
                        self.current_img = self.hipfire[0]
                        self.shoot_busy = True
                        sound.play_sound(random.choice(self.sounds['shot']), 0)
                        self.damage()
                        self.timer = 0
                    elif self.hipfire.index(self.current_img) < 2 and self.timer >= self.shoottime:
                        self.current_img = self.hipfire[self.hipfire.index(self.current_img) + 1]
                        self.timer = 0
                    elif self.current_img == self.hipfire[-1] and self.timer >= self.shoottime:
                        self.current_img = self.aim[0]
                        self.shoot_busy = False
                        self.firetimer = 0
                elif self.aim_is_up:
                    if self.current_img not in self.aimdown:
                        self.current_img = self.aimdown[random.randint(0, 1)]
                        self.shoot_busy = True
                        sound.play_sound(random.choice(self.sounds['shot']), 0)
                        config.screen_shake = self.dmg * 2
                        self.damage()
                        self.timer = 0
                    elif self.aimdown.index(self.current_img) <= 1 and self.timer >= self.shoottime:
                        self.current_img = self.aimdown[-1]
                        self.timer = 0
                    elif self.current_img == self.aimdown[-1] and self.timer >= self.shoottime:
                        self.current_img = self.aim[-1]
                        self.shoot_busy = False
                        self.current_mag -= 1
                        config.statistics['last shots'] += 1
                        if self.stats['magsize'] == 3.1415:
                            self.current_mag -= 1
                            config.statistics['last shots'] += 1
                        self.firetimer = 0
        else:
            if self.firetimer >= self.firerate:
                sound.play_sound(random.choice(self.sounds['click']), 0)
                self.firetimer = 0

    def damage(self):
        if config.middle_slice_len:
            target_npcs = [x for x in config.npc_list if
                           x.hit_rect.colliderect(self.hit_rect) and x.dist < config.middle_slice_len]
        else:
            target_npcs = [x for x in config.npc_list if x.hit_rect.colliderect(self.hit_rect)]

        if len(target_npcs) > 3:
            target_npcs = sorted(target_npcs, key=lambda x: x.sprite.theta)[:3]

        for npc in target_npcs:
            if npc.dist <= self.range and not npc.dead:
                if npc.dist <= config.tile_size * 2:
                    cap = 100
                else:
                    cap = (self.hit_percent * 0.96 ** (npc.dist * ((100 - self.hit_percent) / 100)))

                if cap >= random.randint(0, int(npc.dist * (1 / self.range))):
                    sound.play_sound(self.hit_marker, 0)

                    if self.hit_rect.width < 120 or (
                            self.hit_rect.left + self.hit_rect.width / 3 < npc.hit_rect.centerx < self.hit_rect.right - self.hit_rect.width / 3):

                        if (npc.state == 'idle' or npc.state == 'patrouling') and not npc.player_in_view:
                            npc.health -= self.dmg * 2
                            config.statistics['last ddealt'] += self.dmg * 2
                        else:
                            npc.health -= self.dmg
                            config.statistics['last ddealt'] += self.dmg
                    else:
                        if (npc.state == 'idle' or npc.state == 'patrouling') and not npc.player_in_view:
                            npc.health -= self.dmg
                            config.statistics['last ddealt'] += self.dmg * 2
                        else:
                            npc.health -= self.dmg / 2
                            config.statistics['last ddealt'] += self.dmg
                    npc.timer = 0
                    npc.hurting = True
                    if npc.health <= 0:
                        npc.knockback = self.dmg * (config.tile_size / 2)

    def reload_animation(self):
        if config.held_ammo[self.ammo_type] > 0 or config.unlimited_ammo:
            if self.current_img not in self.reload:
                self.current_img = self.reload[0]
                sound.play_sound(random.choice(self.sounds['magout']), 0)

            self.reload_busy = True
            if (self.current_img == self.reload[3] and self.timer > self.rlspeed) or (
                    self.current_img != self.reload[-1] and self.current_img != self.reload[3] and self.timer >= 0.15):
                x = self.reload.index(self.current_img) + 1
                self.current_img = self.reload[x]
                self.timer = 0
            elif self.current_img == self.reload[-1] and self.timer >= 0.15:
                self.current_img = self.aim[0]
                self.reload_busy = False
                self.timer = 0
                sound.play_sound(random.choice(self.sounds['magin']), 0)
                if not config.unlimited_ammo:
                    taken_ammo = self.mag_size - self.current_mag
                    if config.held_ammo[self.ammo_type] >= taken_ammo:
                        self.current_mag = self.mag_size
                        config.held_ammo[self.ammo_type] -= taken_ammo
                    elif config.held_ammo[self.ammo_type] < taken_ammo:
                        self.current_mag = config.held_ammo[self.ammo_type] + self.current_mag
                        config.held_ammo[self.ammo_type] = 0
                else:
                    self.current_mag = self.mag_size

    def draw(self, canvas):
        swing = self.swing
        wobble = self.wobble

        if not config.player_states['dead']:
            self.timer += config.dt
            self.firetimer += config.dt

            if config.reload_key_active and self.aim_is_up and (
                    self.current_mag < self.mag_size or config.unlimited_ammo):
                self.aim_animation()
                self.go_reload_next_my_gun = True
            elif (config.mouse2_btn_active or self.aim_busy) and (
                    not self.shoot_busy and not self.reload_busy):
                self.aim_animation()
            elif (config.mouse_btn_active or self.shoot_busy) and (
                    not self.aim_busy and not self.reload_busy):
                self.shoot_animation()
                swing *= 2
                wobble /= 2
            elif ((config.reload_key_active or self.reload_busy) and (
                    not self.aim_busy and not self.shoot_busy)) or self.go_reload_next_my_gun:
                if not self.aim_is_up and self.current_mag < self.mag_size:
                    self.reload_animation()
                self.go_reload_next_my_gun = False
                swing *= 2
                wobble /= 2

            if self.aim_is_up:
                swing *= 20
                wobble /= 20

            if config.player_states['cspeed'] > 0 and config.next_gun == config.current_gun:
                self.sintemp += math.pi / 14 * (25 * config.dt)
                self.aim_pos[0] = math.sin(self.sintemp) * (config.actual_width / swing) + \
                                  self.OG_aim_pos[0]
                self.aim_pos[1] = math.sin(self.sintemp * 2) * wobble + (self.OG_aim_pos[1] + 10)
            elif config.player_states['cspeed'] == 0:
                if self.aim_pos[0] > self.OG_aim_pos[0]:
                    self.aim_pos[0] -= int((self.aim_pos[0] - self.OG_aim_pos[0]) / 2)
                    if int((self.aim_pos[0] - self.OG_aim_pos[0]) / 2) == 0:
                        self.aim_pos[0] = self.OG_aim_pos[0]
                elif self.aim_pos[0] < self.OG_aim_pos[0]:
                    self.aim_pos[0] += int((self.OG_aim_pos[0] - self.aim_pos[0]) / 2)
                    if int((self.OG_aim_pos[0] - self.aim_pos[0]) / 2) == 0:
                        self.aim_pos[0] = self.OG_aim_pos[0]

                if self.sintemp != 0 or self.sintemp != -math.pi:
                    self.sintemp = random.choice([0, -math.pi])

                if self.aim_pos[1] > self.OG_aim_pos[1] and config.next_gun == config.current_gun:
                    self.aim_pos[1] -= int((self.aim_pos[1] - self.OG_aim_pos[1]) / 2)
                    if int((self.aim_pos[1] - self.OG_aim_pos[1]) / 2) == 0:
                        self.aim_pos[1] = self.OG_aim_pos[1]
        if config.player_states['dead'] and self.aim_pos[1] <= config.height:
            self.aim_pos[1] += 10

        if not config.current_gun:
            config.current_gun = self
            config.prev_gun = self
        elif config.next_gun != config.current_gun:
            if not self.aim_is_up and not self.reload_busy and not self.shoot_busy:
                if self.aim_pos[1] <= config.height:
                    self.aim_pos[1] += 80
                else:
                    config.prev_gun = config.current_gun
                    config.current_gun = config.next_gun
            elif self.aim_is_up:
                self.aim_animation()
        elif config.prev_gun != config.current_gun and self.aim_pos[1] != self.OG_aim_pos[
            1]:
            if self.aim_pos[1] > self.OG_aim_pos[1]:
                self.aim_pos[1] -= 80
                if self.aim_pos[1] < self.OG_aim_pos[1]:
                    self.aim_pos[1] = self.OG_aim_pos[1]
            else:
                config.prev_gun = config.current_gun

        canvas.blit(self.current_img, self.aim_pos)

    def re_init(self):
        self.aim_pos = [config.actual_width / 2 - self.raw_aim_pos[0] * 6,
                        config.height / 2 - self.raw_aim_pos[1] * 6]
        self.OG_aim_pos = [config.actual_width / 2 - self.raw_aim_pos[0] * 6,
                           config.height / 2 - self.raw_aim_pos[1] * 6]
        self.hit_rect = pygame.Rect((config.actual_width / 2) - (self.accuracy / 2), 0,
                                    self.accuracy, 600)
