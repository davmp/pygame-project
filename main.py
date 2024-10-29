import logging
import math
import sys
import pygame
import colors
import config
import os
import pickle

from generation import Generator
from hud import HUD
from inventory import Inventory
from loader import Loader
from map import Map
from music import Music
from player import Player
from raycast import Raycast
from text import Text
from canvas import Canvas
import menu as Menu
import tutorial as Tutorial


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_mode((1, 1))

        self.loader = Loader()
        self.music = Music()

        self.generator = None
        self.text = None
        self.map = None
        self.canvas = None
        self.player = None
        self.raycast = None
        self.inventory = None
        self.hud = None
        self.tutorial = None
        self.menu = None

    @staticmethod
    def calculate_statistics():
        config.statistics['all enemies'] += config.statistics['last enemies']
        config.statistics['all ddealt'] += config.statistics['last ddealt']
        config.statistics['all dtaken'] += config.statistics['last dtaken']
        config.statistics['all shots'] += config.statistics['last shots']
        config.statistics['all levels'] += config.statistics['last levels']

        if config.statistics['best enemies'] < config.statistics['last enemies']:
            config.statistics['best enemies'] = config.statistics['last enemies']
        if config.statistics['best ddealt'] < config.statistics['last ddealt']:
            config.statistics['best ddealt'] = config.statistics['last ddealt']
        if config.statistics['best dtaken'] < config.statistics['last dtaken']:
            config.statistics['best dtaken'] = config.statistics['last dtaken']
        if config.statistics['best shots'] < config.statistics['last shots']:
            config.statistics['best shots'] = config.statistics['last shots']
        if config.statistics['best levels'] < config.statistics['last levels']:
            config.statistics['best levels'] = config.statistics['last levels']

        with open(os.path.join('data', 'statistics.dat'), 'wb') as saved_stats:
            pickle.dump(config.statistics, saved_stats)

    def render_screen(self):
        config.rendered_tiles = []

        for sprite in config.all_sprites:
            sprite.get_pos(self.canvas)

        def sort_distance(x):
            if x is None:
                return 0
            else:
                return x.distance

        def sort_atan(x):
            if config.middle_ray_pos:
                pos = config.middle_ray_pos
            else:
                pos = config.player_rect.center

            xpos = max(x.rect.left, min(pos[0], x.rect.right)) - config.player_rect.centerx
            ypos = config.player_rect.centery - max(x.rect.top, min(pos[1], x.rect.bottom))
            theta = math.atan2(ypos, xpos)
            theta = math.degrees(theta)
            theta -= config.player_angle

            if theta < 0:
                theta += 360
            if theta > 180:
                theta -= 360

            if x.type == 'end':
                config.end_angle = theta

            theta = abs(theta)

            return theta

        config.zbuffer = sorted(config.zbuffer, key=sort_distance, reverse=True)
        config.all_solid_tiles = sorted(config.all_solid_tiles, key=lambda x: (x.type, sort_atan(x), x.distance))

        for tile in config.all_solid_tiles:
            if tile.distance and config.tile_visible[tile.ID]:
                if sort_atan(tile) <= config.fov:
                    if tile.distance < config.render * config.tile_size:
                        config.rendered_tiles.append(tile)

                elif tile.distance <= config.tile_size * 1.5:
                    config.rendered_tiles.append(tile)

        for item in config.zbuffer:
            if item is None:
                pass
            elif item.type == 'slice':
                self.canvas.canvas.blit(item.tempslice, (item.xpos, item.rect.y))
                if item.vh == 'v':
                    self.canvas.canvas.blit(item.darkslice, (item.xpos, item.rect.y))
                if config.shade:
                    self.canvas.canvas.blit(item.shade_slice, (item.xpos, item.rect.y))

            else:
                if (item.new_rect.right > 0 and
                        item.new_rect.x < config.actual_width and
                        item.distance < (config.render * config.tile_size)):
                    item.draw(self.canvas.canvas)

        if config.current_gun:
            config.current_gun.draw(self.canvas.canvas)
        elif config.next_gun:
            config.next_gun.draw(self.canvas.canvas)

        # Draw Inventory and effects
        if config.player_states['invopen']:
            self.inventory.draw(self.canvas.canvas)
        # EFFECTS.render(self.canvas.canvas)

        config.zbuffer = []

        # Draw HUD and canvas
        self.canvas.window.blit(self.canvas.canvas, config.axes)
        self.hud.render(self.canvas.window)

        # Draw tutorial strings
        if config.levels_list == config.tlevels_list:
            self.tutorial.control(self.canvas.window)

    def update(self):
        if config.npc_list:
            for npc in config.npc_list:
                if not npc.dead:
                    npc.think()

        config.ground_weapon = None
        for item in config.items:
            item.update()

        if (config.level_transition and config.player_states['black']) or config.player_states['dead']:
            if config.current_level < len(config.levels_list) - 1 and config.level_transition:
                config.current_level += 1
                config.statistics['last levels'] += 1
                self.loader.load_new_level(self.map, self.player)
            elif (config.current_level == len(config.levels_list) - 1 or
                  config.player_states['dead']) and self.loader.timer < 4 and not config.player_states['fade']:
                if not config.player_states['dead'] and config.current_level == len(
                        config.levels_list) - 1 and self.text.string != 'YOU  WON':
                    self.text.update_string('YOU  WON')
                elif config.player_states['dead'] and self.text.string != 'GAME  OVER':
                    self.text.update_string('GAME  OVER')
                self.text.draw(self.canvas.window)
                if not config.won:
                    self.loader.timer = 0
                config.game_won = True
                self.loader.timer += config.dt
            elif config.won and self.loader.timer >= 4:
                self.loader.timer = 0
                config.game_won = False
                self.menu.current_type = 'main'
                self.menu.current_menu = 'score'
                self.calculate_statistics()
                config.menu_showing = True
                config.current_level = 0

    def play(self):
        self.loader.load_resources()
        self.loader.load_entities()
        self.loader.load_custom_levels()

        self.generator = Generator()
        self.generator.generate_levels(1, 2)
        config.levels_list = config.glevels_list

        self.loader.get_canvas_size()

        self.text = Text(
            posx=0,
            posy=0,
            string="VOCÊ FUGIU DA CASA!",
            color=colors.WHITE,
            size=48
        )
        beta = Text(
            posx=5,
            posy=5,
            string=f"{config.title.upper()} V{config.version}",
            color=colors.WHITE,
            size=48
        )

        self.text.update_pos(config.actual_width / 2 - self.text.layout.get_width() / 2,
                             config.height / 2 - self.text.layout.get_height() / 2)

        self.map = Map(config.levels_list[config.current_level].array)
        self.canvas = Canvas(config.map_width, config.map_height)
        self.player = Player(config.player_pos)
        self.raycast = Raycast(self.canvas.canvas, self.canvas.window)
        self.inventory = Inventory({'bullet': 150, 'shell': 25, 'ferromag': 50})
        self.hud = HUD()

        self.loader.load_new_level(self.map, self.player)

        self.tutorial = Tutorial.Controller()
        self.menu = Menu.Controller(self.canvas.window)

        n_curr = pygame.transform.scale(
            pygame.image.load('assets/sprites/cursor/normal.png'),
            (32, 32))
        c_curr = pygame.transform.scale(
            pygame.image.load('assets/sprites/cursor/click.png'),
            (32, 32)
        )

        running = True
        clock = pygame.time.Clock()
        logging.basicConfig(filename=os.path.join('data', 'CrashReport.log'), level=logging.WARNING)

        while running:
            config.zbuffer = []
            if config.played_seconds >= 60:
                config.statistics['playtime'] += 1
                config.played_seconds = 0
            else:
                config.played_seconds += config.dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            try:
                self.music.control_music()

                if not config.in_game and self.menu.current_type == "main":
                    self.canvas.window.fill((14, 14, 14))
                    self.menu.control()

                    if len(Menu.Button.hovered) > 0:
                        pygame.mouse.set_cursor(pygame.cursors.Cursor((4, 0), c_curr))
                    else:
                        pygame.mouse.set_cursor(pygame.cursors.Cursor((4, 0), n_curr))

                    if config.playing_customs:
                        config.levels_list = config.clevels_list
                        self.loader.get_canvas_size()
                        self.loader.load_new_level(self.map, self.player)
                    elif config.playing_new:
                        self.generator.__init__()
                        self.generator.generate_levels(config.levels_amnt, config.levels_size)
                        config.levels_list = config.glevels_list
                        self.loader.get_canvas_size()
                        self.loader.load_new_level(self.map, self.player)
                    elif config.playing_tutorial:
                        config.levels_list = config.tlevels_list
                        self.loader.get_canvas_size()
                        self.loader.load_new_level(self.map, self.player)
                elif not config.in_game and self.menu.current_type == "game":
                    self.menu.control()
                else:
                    self.player.control(self.canvas)
                    config.fov = max(10, min(config.fov, 100))

                    if config.switch_mode:
                        self.canvas.change_mode()

                    self.raycast.calculate()
                    self.canvas.draw()

                    if config.mode == 1:
                        self.render_screen()
                    elif config.mode == 0:
                        self.map.draw(self.canvas.window)
                        self.player.draw(self.canvas.window)

                        for x in config.raylines:
                            pygame.draw.line(self.canvas.window, colors.RED, (x[0][0] / 4, x[0][1] / 4),
                                             (x[1][0] / 4, x[1][1] / 4))
                        config.raylines = []

                        for i in config.npc_list:
                            if i.rect and i.dist <= config.render * config.tile_size * 1.2:
                                pygame.draw.rect(
                                    surface=self.canvas.window,
                                    color=colors.RED,
                                    rect=(i.rect[0] / 4, i.rect[1] / 4, i.rect[2] / 4, i.rect[3] / 4))
                            elif i.rect:
                                pygame.draw.rect(
                                    surface=self.canvas.window,
                                    color=colors.DARKGREEN,
                                    rect=(i.rect[0] / 4, i.rect[1] / 4, i.rect[2] / 4, i.rect[3] / 4))
                    self.update()
            except Exception as e:
                running = False
                logging.warning(f"{config.title} crashou.")
                logging.exception("Mensagem de erro: ")

            pygame.display.update()
            dt = clock.tick(config.fps)
            config.dt = dt / 1000.0
            config.cfps = int(clock.get_fps())

        self.menu.save_settings()
        self.calculate_statistics()
        pygame.quit()
        sys.exit(0)


if __name__ == '__main__':
    game = Game()
    game.play()
