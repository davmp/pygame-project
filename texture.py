import os
import pygame


class Texture:
    all_textures = []

    def __init__(self, file_path, _id):
        self.slices = []
        self.texture = pygame.image.load(file_path).convert()
        self.rect = self.texture.get_rect()
        self.id = _id

        self.create_slices()

    def create_slices(self):
        for row in range(0, self.rect.width):
            self.slices.append(row)
            row += 1

    @staticmethod
    def load_textures():
        Texture.all_textures = [
                os.path.join('assets', 'textures', 'tiles', 'null.png'),  # 0

                # -- Wood theme --
                # Walls
                os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_wall.png'),  # 1
                os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_painting.png'),  # 2
                os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_fireplace.png'),  # 3
                os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_books.png'),  # 4
                os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_end.png'),  # 5
                # Doors
                os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_door.png'),  # 6
                os.path.join('assets', 'textures', 'tiles', 'walls', 'wood_door.png'),  # 7
                # Sprites
                os.path.join('assets', 'textures', 'tiles', 'sprites', 'pillar.png'),  # 8
                os.path.join('assets', 'textures', 'tiles', 'sprites', 'table.png'),  # 9
                os.path.join('assets', 'textures', 'tiles', 'sprites', 'lysekrone.png'),  # 10

                # -- Stone theme --
                # Walls
                os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_wall.png'),  # 11
                os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_vent.png'),  # 12
                os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_wall_crack.png'),  # 13
                os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_vase.png'),  # 14
                os.path.join('assets', 'textures', 'tiles', 'walls', 'stone_end.png'),  # 15
                # Sprites
                os.path.join('assets', 'textures', 'tiles', 'sprites', 'lysestage.png'),  # 16
                os.path.join('assets', 'textures', 'tiles', 'sprites', 'barrel.png'),  # 17
                os.path.join('assets', 'textures', 'tiles', 'sprites', 'stone_pillar.png'),  # 18

                # -- Baroque theme --
                # Walls
                os.path.join('assets', 'textures', 'tiles', 'walls', 'baroque.png'),  # 19
                os.path.join('assets', 'textures', 'tiles', 'walls', 'baroque_lamps.png'),  # 20
                os.path.join('assets', 'textures', 'tiles', 'walls', 'baroque_worn.png'),  # 21
                os.path.join('assets', 'textures', 'tiles', 'walls', 'baroque_end.png'),  # 22
                # Doors
                os.path.join('assets', 'textures', 'tiles', 'walls', 'baroque_door.png'),  # 23
                os.path.join('assets', 'textures', 'tiles', 'walls', 'baroque_door.png'),  # 24
                # Sprites
                os.path.join('assets', 'textures', 'tiles', 'sprites', 'fern.png'),  # 25
            ]
