import pygame
import math

import config

pygame.init()


class Slice:
    def __init__(self, location, surface, width, vh):
        self.slice = surface.subsurface(pygame.Rect(location, (1, width))).convert()
        self.rect = self.slice.get_rect(center=(0, config.height / 2))
        self.distance = None
        self.type = 'slice'
        self.vh = vh
        self.xpos = 0

        if config.shade:
            self.shade_slice = pygame.Surface(self.slice.get_size()).convert_alpha()
            sv = config.shade_visibility / 10
            self.shade_intensity = [sv * 1, sv * 2, sv * 3, sv * 4, sv * 5, sv * 6, sv * 7, sv * 8, sv * 9, sv * 10]

    def update_rect(self, new_slice):
        self.tempslice = new_slice
        self.rect = new_slice.get_rect(center=(self.xpos, int(config.height / 2)))

        if self.vh == 'v':
            self.darkslice = pygame.Surface(self.tempslice.get_size()).convert_alpha()
            self.darkslice.fill((0, 0, 0, config.texture_darken))

        if config.shade:
            if self.distance < self.shade_intensity[0]:
                intensity = 0
            elif self.distance < self.shade_intensity[1]:
                intensity = 0.1
            elif self.distance < self.shade_intensity[2]:
                intensity = 0.2
            elif self.distance < self.shade_intensity[3]:
                intensity = 0.3
            elif self.distance < self.shade_intensity[4]:
                intensity = 0.4
            elif self.distance < self.shade_intensity[5]:
                intensity = 0.5
            elif self.distance < self.shade_intensity[6]:
                intensity = 0.6
            elif self.distance < self.shade_intensity[7]:
                intensity = 0.7
            elif self.distance < self.shade_intensity[8]:
                intensity = 0.8
            elif self.distance < self.shade_intensity[9]:
                intensity = 0.9
            else:
                intensity = 1

            self.shade_slice = pygame.Surface(self.tempslice.get_size()).convert_alpha()
            self.shade_slice.fill((config.shade_rgba[0] * intensity, config.shade_rgba[1] * intensity,
                                   config.shade_rgba[2] * intensity, config.shade_rgba[3] * intensity))


class Raycast:
    def __init__(self, canvas, canvas2):
        self.res = config.res
        self.fov = config.fov
        self.render = config.render
        self.tile_size = config.tile_size
        self.door_size = self.tile_size / 2
        self.wall_width = int(config.width / self.res)
        self.canvas = canvas
        self.canvas2 = canvas2

        self.current_vtile = None
        self.current_htile = None

    def calculate(self):
        self.res = config.res
        self.fov = config.fov
        angle = config.player_angle

        step = self.fov / self.res
        fov = int(self.fov / 2)
        ray = -fov
        ray_number = 0

        for tile in config.all_solid_tiles:
            tile.distance = tile.get_dist(config.player_rect.center)

        while ray < fov:
            degree = angle - ray
            if degree <= 0:
                degree += 360
            elif degree > 360:
                degree -= 360

            self.beta = abs(degree - angle)

            self.cast(config.player_rect, degree, ray_number)

            ray_number += 1
            ray += step

    def find_offset(self, position, ray_number, angle, tile, hv):
        if hv == 'v':
            if tile.type == 'vdoor':
                offset = abs(int(position - tile.rect.y)) - tile.open
            else:
                offset = abs(int(position - tile.rect.y))

        else:
            if tile.type == 'hdoor':
                offset = abs(int(position - tile.rect.x)) - tile.open
            else:
                offset = abs(int(position - tile.rect.x))

        if offset >= config.tile_size:
            offset = config.tile_size - 1
        return offset

    @staticmethod
    def check_hit(V_hit, H_hit, H_distance, V_distance, full_check):
        if H_hit and V_hit:
            return True

        elif full_check:
            if H_hit:
                if H_distance < V_distance:
                    return True

            elif V_hit:
                if V_distance < H_distance:
                    return True

    def cast(self, player_rect, angle, ray_number):
        h_hit = False
        v_hit = False
        h_offset = v_offset = 0
        end_pos = (0, 0)
        angle -= 0.001

        # Horizontal
        if angle < 180:
            h_y = int(player_rect.center[1] / self.tile_size) * self.tile_size
        else:
            h_y = int(player_rect.center[1] / self.tile_size) * self.tile_size + self.tile_size

        h_x = player_rect.center[0] + (player_rect.center[1] - h_y) / math.tan(math.radians(angle))

        # Vertical
        if angle > 270 or angle < 90:
            v_x = int(player_rect.center[0] / self.tile_size) * self.tile_size + self.tile_size
        else:
            v_x = int(player_rect.center[0] / self.tile_size) * self.tile_size

        v_y = player_rect.center[1] + (player_rect.center[0] - v_x) * math.tan(math.radians(angle))

        for x in range(0, config.render):
            h_distance = abs((player_rect.center[0] - h_x) / math.cos(math.radians(angle)))
            v_distance = abs((player_rect.center[0] - v_x) / math.cos(math.radians(angle)))

            if self.check_hit(v_hit, h_hit, h_distance, v_distance, True):
                break

            for tile in config.rendered_tiles:

                if self.check_hit(v_hit, h_hit, h_distance, v_distance, False):
                    break

                if not h_hit:
                    if ((h_y == tile.rect.bottom and
                         tile.rect.bottomleft[0] <= h_x <= tile.rect.bottomright[0]) and
                            player_rect.centery > tile.rect.bottom):
                        h_hit = True
                        h_texture = config.tile_texture[tile.ID]
                        self.current_htile = tile
                        if tile.type == 'hdoor':
                            h_y -= self.door_size
                            h_x += self.door_size / math.tan(math.radians(angle))
                            h_offset = offset = self.find_offset(h_x, ray_number, angle, tile, 'h')
                            if h_offset < 0:
                                h_hit = False
                                h_y += self.door_size
                                h_x -= self.door_size / math.tan(math.radians(angle))
                        else:
                            h_offset = offset = self.find_offset(h_x, ray_number, angle, tile, 'h')

                    elif ((h_y == tile.rect.top and
                           tile.rect.topleft[0] <= h_x <= tile.rect.topright[0]) and
                          player_rect.centery < tile.rect.top):
                        h_hit = True
                        h_texture = config.tile_texture[tile.ID]
                        self.current_htile = tile
                        if tile.type == 'hdoor':
                            h_y += self.door_size
                            h_x -= self.door_size / math.tan(math.radians(angle))
                            h_offset = offset = self.find_offset(h_x, ray_number, angle, tile, 'h')
                            if h_offset < 0:
                                h_hit = False
                                h_y -= self.door_size
                                h_x += self.door_size / math.tan(math.radians(angle))
                        else:
                            h_offset = self.find_offset(h_x, ray_number, angle, tile, 'h')

                if self.check_hit(v_hit, h_hit, h_distance, v_distance, False):
                    break

                if not v_hit:
                    if ((v_x == tile.rect.left and
                        tile.rect.topleft[1] <= v_y <= tile.rect.bottomleft[1]) and
                            player_rect.centerx < tile.rect.left):
                        v_hit = True
                        v_texture = config.tile_texture[tile.ID]
                        self.current_vtile = tile
                        if tile.type == 'vdoor':
                            v_x += self.door_size
                            v_y -= self.door_size * math.tan(math.radians(angle))
                            v_offset = self.find_offset(v_y, ray_number, angle, tile, 'v')
                            if v_offset < 0:
                                v_hit = False
                                v_x -= self.door_size
                                v_y += self.door_size * math.tan(math.radians(angle))
                        else:
                            v_offset = self.find_offset(v_y, ray_number, angle, tile, 'v')
                    elif ((v_x == tile.rect.right and
                           tile.rect.topright[1] <= v_y <= tile.rect.bottomright[1]) and
                          player_rect.centerx > tile.rect.right):
                        v_hit = True
                        v_texture = config.tile_texture[tile.ID]
                        self.current_vtile = tile
                        if tile.type == 'vdoor':
                            v_x -= self.door_size
                            v_y += self.door_size * math.tan(math.radians(angle))
                            v_offset = self.find_offset(v_y, ray_number, angle, tile, 'v')
                            if v_offset < 0:
                                v_hit = False
                                v_x += self.door_size
                                v_y -= self.door_size * math.tan(math.radians(angle))
                        else:
                            v_offset = self.find_offset(v_y, ray_number, angle, tile, 'v')

            # Extend actual ray
            if not h_hit:
                if angle < 180:
                    h_y -= self.tile_size
                else:
                    h_y += self.tile_size
                if angle >= 180:
                    h_x -= self.tile_size / math.tan(math.radians(angle))
                else:
                    h_x += self.tile_size / math.tan(math.radians(angle))

            if not v_hit:
                if angle > 270 or angle < 90:  # ->
                    v_x += self.tile_size
                else:
                    v_x -= self.tile_size
                if angle >= 270 or angle < 90:  # <-
                    v_y -= self.tile_size * math.tan(math.radians(angle))
                else:
                    v_y += self.tile_size * math.tan(math.radians(angle))

        if v_hit and h_hit:
            h_hit, v_hit = False, False
            if h_distance < v_distance:
                end_pos = (h_x, h_y)
                texture = h_texture
                tile_len = h_distance
                offset = h_offset
                current_tile = self.current_htile
                h_hit = True
            else:
                end_pos = (v_x, v_y)
                texture = v_texture
                tile_len = v_distance
                offset = v_offset
                current_tile = self.current_vtile
                v_hit = True

        elif h_hit and not v_hit:
            end_pos = (h_x, h_y)
            texture = h_texture
            tile_len = h_distance
            offset = h_offset
            current_tile = self.current_htile

        elif v_hit and not h_hit:
            end_pos = (v_x, v_y)
            texture = v_texture
            tile_len = v_distance
            offset = v_offset
            current_tile = self.current_vtile

        else:
            end_pos = (config.player_rect[0], config.player_rect[1])
            texture = None
            tile_len = None
            offset = 0
            current_tile = None

        if v_hit:
            vh = 'v'
        else:
            vh = 'h'

        self.control(end_pos, ray_number, tile_len, player_rect, texture, offset, current_tile, vh)

    def control(self, end_pos, ray_number, tile_len, player_rect, texture, offset, current_tile, vh):
        if config.mode == 1:
            if tile_len:
                wall_dist = tile_len * math.cos(math.radians(self.beta))
            else:
                wall_dist = None
            self.render_screen(ray_number, wall_dist, texture, int(offset), current_tile, vh, end_pos)

        else:
            self.draw_line(player_rect, end_pos)

    def render_screen(self, ray_number, wall_dist, texture, offset, current_tile, vh, end_pos):
        if wall_dist:
            wall_height = int((self.tile_size / wall_dist) * (360 / math.tan(math.radians(config.fov * 0.8))))
            config.zbuffer.append(Slice((texture.slices[offset], 0), texture.texture, texture.rect.width, vh))
            config.zbuffer[ray_number].distance = wall_dist
            rendered_slice = pygame.transform.scale(config.zbuffer[ray_number].slice, (self.wall_width, wall_height))
            config.zbuffer[ray_number].update_rect(rendered_slice)
            config.zbuffer[ray_number].xpos = (ray_number * self.wall_width)

        else:
            config.zbuffer.append(None)

        # Middle ray info
        if ray_number == int(self.res / 2):
            config.middle_slice_len = wall_dist
            config.middle_slice = current_tile
            config.middle_ray_pos = end_pos

    @staticmethod
    def draw_line(player_rect, end_pos):
        config.raylines.append((player_rect.center, end_pos))
