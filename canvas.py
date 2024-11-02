import pygame

import colors
import config


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.res_width = 0
        self.light_positions = [(200, 200), (400, 300)]
        if config.mode == 1:
            self.width = int(config.width / config.res) * config.res
            self.height = config.height
            self.res_width = config.actual_width

        self.window = pygame.display.set_mode(
            (self.width, int(self.height + (self.height * 0.15))),
            vsync=1)
        self.canvas = pygame.Surface((self.width, self.height))

        pygame.display.set_caption(f"{config.title.upper()} - V{config.version}")

        self.shade = [pygame.Surface((self.width, self.height)).convert_alpha(),
                      pygame.Surface((self.width, self.height / 1.2)).convert_alpha(),
                      pygame.Surface((self.width, self.height / 2)).convert_alpha(),
                      pygame.Surface((self.width, self.height / 4)).convert_alpha(),
                      pygame.Surface((self.width, self.height / 8)).convert_alpha(),
                      pygame.Surface((self.width, self.height / 18)).convert_alpha()]
        self.rgba = [config.shade_rgba[0], config.shade_rgba[1], config.shade_rgba[2],
                     int(min(255, config.shade_rgba[3] * (50 / config.shade_visibility)))]

    def change_mode(self):
        if config.mode == 1:  # 1 - 3D / 0 - 2D
            config.mode = 0
            self.__init__(config.actual_width, config.height)
        else:
            config.mode = 1
            self.__init__(self.res_width, config.height)
        config.switch_mode = False

    def draw(self):
        if config.mode == 1:
            self.canvas.fill(config.levels_list[config.current_level].sky_color)
            self.window.fill(colors.BLACK)
            pygame.draw.rect(self.canvas, config.levels_list[config.current_level].ground_color,
                             (0, self.height / 2, self.width, self.height / 2))

            pygame.draw.rect(self.canvas, (255, 0, 0), (200, 200, 20, 20))

            if config.shade:
                for i in range(len(self.shade)):
                    if i != 5:
                        self.shade[i].fill((self.rgba[0], self.rgba[1], self.rgba[2], self.rgba[3]))
                    else:
                        self.shade[i].fill((self.rgba[0], self.rgba[1], self.rgba[2], config.shade_rgba[3]))
                    self.canvas.blit(self.shade[i], (0, self.height / 2 - self.shade[i].get_height() / 2))
        else:
            self.window.fill(colors.WHITE)

            if config.ground_weapon:
                groundslot = pygame.Surface((272, 80)).convert_alpha()
                groundslot_rect = groundslot.get_rect()

                pygame.draw.rect(
                    surface=config.ground_weapon.subitemtexture,
                    color=colors.WHITE,
                    rect=(groundslot_rect.x, groundslot_rect.y + 5)
                )
