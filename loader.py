import copy
import random
import pygame
import pickle
import os

import config
from gun import Gun
from item import Item
from level import Level
from map import Map
from player import Player
from texture import Texture
from npc import PathFinder, Npc


class Loader:
    class NpcLoader:
        @staticmethod
        def __load_npc_types():
            config.npc_types = [
                # soldier idle
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.12,
                    'dmg': 2,
                    'health': random.randint(12, 15),
                    'speed': 40,
                    'mind': 'hostile',
                    'state': 'idle',
                    'atcktype': 'hitscan',
                    'atckrate': 1,
                    'id': 0,
                    'filepath': ('assets', 'textures', 'npc', 'soldier_spritesheet.png'),
                    'name': 'idle soldier',
                    'soundpack': 'soldier',
                },

                # Soldier Patrolling
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.12,
                    'dmg': 2,
                    'health': random.randint(12, 15),
                    'speed': 40,
                    'mind': 'hostile',
                    'state': 'patrolling',
                    'atcktype': 'hitscan',
                    'atckrate': 1,
                    'id': 1,
                    'filepath': ('assets', 'textures', 'npc', 'soldier_spritesheet.png'),
                    'name': 'patroul soldier',
                    'soundpack': 'soldier',
                },

                # Ninja idle
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.10,
                    'dmg': 3,
                    'health': 11,
                    'speed': 60,
                    'mind': 'hostile',
                    'state': 'idle',
                    'atcktype': 'melee',
                    'atckrate': 0.8,
                    'id': 2,
                    'filepath': ('assets', 'textures', 'npc', 'ninja_spritesheet.png'),
                    'name': 'idle ninja',
                    'soundpack': 'ninja',
                },

                # Ninja patrolling
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.10,
                    'dmg': 3,
                    'health': 12,
                    'speed': 60,
                    'mind': 'hostile',
                    'state': 'patrolling',
                    'atcktype': 'melee',
                    'atckrate': 0.8,
                    'id': 3,
                    'filepath': ('assets', 'textures', 'npc', 'ninja_spritesheet.png'),
                    'name': 'patroul ninja',
                    'soundpack': 'ninja',
                },

                # Zombie patroling hostile (no dmg?)
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.12,
                    'dmg': 3.1415,  # lol this is used to randomize dmg.
                    'health': 6,
                    'speed': 70,
                    'mind': 'hostile',
                    'state': 'patrolling',
                    'atcktype': 'melee',
                    'atckrate': 0.6,
                    'id': 4,
                    'filepath': ('assets', 'textures', 'npc', 'zombie_spritesheet.png'),
                    'name': 'hostile zombie',
                    'soundpack': 'zombie hostile',
                },

                # Zombie idle shy
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.12,
                    'dmg': 0,
                    'health': 6,
                    'speed': 50,
                    'mind': 'shy',
                    'state': 'idle',
                    'atcktype': 'melee',
                    'atckrate': 0.6,
                    'id': 5,
                    'filepath': ('assets', 'textures', 'npc', 'zombie_spritesheet.png'),
                    'name': 'shy zombie',
                    'soundpack': 'zombie shy',
                },

                # random NPC
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0,
                    'dmg': 0,
                    'health': 0,
                    'speed': 0,
                    'mind': None,
                    'state': None,
                    'atcktype': None,
                    'atckrate': 0,
                    'id': 6,
                    'filepath': ('assets', 'textures', 'npc', 'random_spritesheet.png'),
                    'name': 'random',
                    'soundpack': None,
                },

                # SPECIAL NPCS --------
                # Boss idle
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.10,
                    'dmg': 5,
                    'health': 40,
                    'speed': 20,
                    'mind': 'hostile',
                    'state': 'idle',
                    'atcktype': 'hitscan',
                    'atckrate': 3,
                    'id': 7,
                    'filepath': ('assets', 'textures', 'npc', 'red_soldier_spritesheet.png'),
                    'name': 'idle red',
                    'soundpack': 'red soldier',
                },

                # black soldier idle
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.12,
                    'dmg': 2,
                    'health': random.randint(15, 20),
                    'speed': 30,
                    'mind': 'hostile',
                    'state': 'idle',
                    'atcktype': 'hitscan',
                    'atckrate': 0.5,
                    'id': 8,
                    'filepath': ('assets', 'textures', 'npc', 'black_soldier_spritesheet.png'),
                    'name': 'black idle',
                    'soundpack': 'soldier',
                },

                # black soldier patroul
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.12,
                    'dmg': 2,
                    'health': random.randint(15, 20),
                    'speed': 30,
                    'mind': 'hostile',
                    'state': 'patrolling',
                    'atcktype': 'hitscan',
                    'atckrate': 1.5,
                    'id': 9,
                    'filepath': ('assets', 'textures', 'npc', 'black_soldier_spritesheet.png'),
                    'name': 'black patroul',
                    'soundpack': 'soldier',
                },

                # green ninja idle
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.12,
                    'dmg': 3,
                    'health': random.randint(8, 11),
                    'speed': 100,
                    'mind': 'hostile',
                    'state': 'idle',
                    'atcktype': 'melee',
                    'atckrate': 0.5,
                    'id': 10,
                    'filepath': ('assets', 'textures', 'npc', 'green_ninja_spritesheet.png'),
                    'name': 'idle green',
                    'soundpack': 'ninja',
                },

                # green ninja patrolling
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.12,
                    'dmg': 2,
                    'health': random.randint(8, 11),
                    'speed': 100,
                    'mind': 'hostile',
                    'state': 'patrolling',
                    'atcktype': 'melee',
                    'atckrate': 0.5,
                    'id': 11,
                    'filepath': ('assets', 'textures', 'npc', 'green_ninja_spritesheet.png'),
                    'name': 'idle green',
                    'soundpack': 'ninja',
                },

                # blue ninja idle
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.1,
                    'dmg': 4,
                    'health': 14,
                    'speed': 35,
                    'mind': 'hostile',
                    'state': 'patrolling',
                    'atcktype': 'melee',
                    'atckrate': 1.1,
                    'id': 12,
                    'filepath': ('assets', 'textures', 'npc', 'blue_ninja_spritesheet.png'),
                    'name': 'idle blue',
                    'soundpack': 'ninja',
                },

                # Zombie yellow patrolling
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.18,
                    'dmg': 5,
                    'health': 20,
                    'speed': 20,
                    'mind': 'hostile',
                    'state': 'patrolling',
                    'atcktype': 'melee',
                    'atckrate': 1,
                    'id': 13,
                    'filepath': ('assets', 'textures', 'npc', 'sick_zombie_spritesheet.png'),
                    'name': 'patroul sick',
                    'soundpack': 'zombie hostile',
                },

                # zombie yellow idle
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.18,
                    'dmg': 6,
                    'health': 20,
                    'speed': 20,
                    'mind': 'hostile',
                    'state': 'idle',
                    'atcktype': 'melee',
                    'atckrate': 0.8,
                    'id': 14,
                    'filepath': ('assets', 'textures', 'npc', 'sick_zombie_spritesheet.png'),
                    'name': 'idle sick',
                    'soundpack': 'zombie hostile',
                },

                # zombie yellow idle shy
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.18,
                    'dmg': 10,
                    'health': 35,
                    'speed': 20,
                    'mind': 'hostile',
                    'state': 'idle',
                    'atcktype': 'melee',
                    'atckrate': 1.2,
                    'id': 15,
                    'filepath': ('assets', 'textures', 'npc', 'sick_zombie_spritesheet.png'),
                    'name': 'shy sick',
                    'soundpack': 'zombie hostile',
                },

                # blurry zombie hostile
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.18,
                    'dmg': 8,
                    'health': 5,
                    'speed': 45,
                    'mind': 'hostile',
                    'state': 'patrolling',
                    'atcktype': 'melee',
                    'atckrate': 0.4,
                    'id': 16,
                    'filepath': ('assets', 'textures', 'npc', 'blurry_zombie_spritesheet.png'),
                    'name': 'hostile blurry',
                    'soundpack': 'blurry zombie',
                },

                # blurry zombie hostile hitscan??
                {
                    'pos': [0, 0],
                    'face': 0,
                    'spf': 0.18,
                    'dmg': 1,
                    'health': 15,
                    'speed': 45,
                    'mind': 'hostile',
                    'state': 'patrolling',
                    'atcktype': 'hitscan',
                    'atckrate': 0.4,
                    'id': 17,
                    'filepath': ('assets', 'textures', 'npc', 'blurry_zombie_spritesheet.png'),
                    'name': 'hostile blurry',
                    'soundpack': 'blurry zombie',
                },
            ]

        @staticmethod
        def __load_npc_sounds():
            config.npc_sounds = [
                # Soldier soundpack
                {
                    'name': 'soldier',
                    'attack': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_shoot.ogg')),
                    'spot': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_spot.ogg')),
                    'damage': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_hurt1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_hurt2.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_hurt3.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_hurt4.ogg'))],
                    'die': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_die.ogg')), ],
                },

                # boss soldier soundpack
                {
                    'name': 'red soldier',
                    'attack': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_shoot_heavy.ogg')),
                    'spot': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_spot.ogg')),
                    'damage': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_hurt1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_hurt2.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_hurt3.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_hurt4.ogg'))],
                    'die': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'soldier_die.ogg')), ],
                },

                # Ninja Soundpack
                {
                    'name': 'ninja',
                    'attack': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'ninja_attack.ogg')),
                    'spot': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg')),
                    'damage': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'ninja_hurt1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'ninja_hurt2.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'ninja_hurt3.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'ninja_hurt4.ogg'))],
                    'die': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'ninja_die1.ogg')),
                            pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'ninja_die2.ogg'))],
                },

                # Zombie shy soundpack
                {
                    'name': 'zombie shy',
                    'attack': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg')),
                    'spot': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'zombie_spot2.ogg')),
                    'damage': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'zombie_hurt1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'zombie_hurt2.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'zombie_hurt3.ogg'))],
                    'die': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'zombie_die1.ogg')),
                            pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'zombie_die2.ogg'))],
                },

                # Zombie hostile soundpack
                {
                    'name': 'zombie hostile',
                    'attack': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'zombie_attack.ogg')),
                    'spot': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'zombie_spot1.ogg')),
                    'damage': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'zombie_hurt1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'zombie_hurt2.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'zombie_hurt3.ogg'))],
                    'die': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'zombie_die1.ogg')),
                            pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'zombie_die2.ogg'))],
                },

                # Zombie blurry soundpack
                {
                    'name': 'blurry zombie',
                    'attack': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'blurry_zombie_attack.ogg')),
                    'spot': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'blurry_zombie_spot.ogg')),
                    'damage': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'blurry_zombie_hurt1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'blurry_zombie_hurt2.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'blurry_zombie_hurt3.ogg'))],
                    'die': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'blurry_zombie_die1.ogg')),
                            pygame.mixer.Sound(os.path.join('assets', 'sounds', 'npcs', 'blurry_zombie_die2.ogg'))],
                },
            ]

        @staticmethod
        def __spawn_npcs():
            seed = config.current_level + config.seed
            for npc in config.levels_list[config.current_level].npcs:
                if [x for x in config.npc_types if x['id'] == npc[2]][0]['name'] == 'random':
                    random.seed(seed)
                    seed += 0.001
                    stats = copy.deepcopy(random.choice([x for x in config.npc_types if x['name'] != 'random']))
                    print(stats['name'])
                else:
                    stats = copy.deepcopy([x for x in config.npc_types if x['id'] == npc[2]][0])

                try:
                    sounds = ([x for x in config.npc_sounds if x['name'] == stats['soundpack']][0])
                except:
                    print("Error loading NPC! No soundpack with name ", stats['soundpack'])
                stats['pos'] = npc[0]
                stats['face'] = npc[1]
                config.npc_list.append(Npc(stats, sounds, os.path.join(*stats['filepath'])))

        def load(self):
            self.__load_npc_types()
            self.__load_npc_sounds()

        def spawn(self):
            self.__spawn_npcs()

    class GunLoader:
        @staticmethod
        def __load_guns():
            # AK 47 - 0
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'ak_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'akitem.png')
                 }, {
                    'dmg': 3,
                    'spread': 50,
                    'hitchance': 80,
                    'firerate': 0.08,
                    'range': 10,
                    'magsize': 30,
                    'rlspeed': 1,
                    'zoom': 6,
                    'ammotype': 'bullet',
                    'guntype': 'primary',
                    'name': 'AK-47'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot3.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot4.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot5.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click2.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin2.ogg'))]
                }, (35, 7)))

            # Double Barrel Shotgun - 1
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'shotgun_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'shotgun.png')
                 }, {
                    'dmg': 10,
                    'spread': 200,
                    'hitchance': 65,
                    'firerate': 0.3,
                    'range': 7,
                    'magsize': 2,
                    'rlspeed': 1.4,
                    'zoom': 8,
                    'ammotype': 'shell',
                    'guntype': 'primary',
                    'name': 'Espingarda DB'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_shot3.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_shot4.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'universal_click.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (34, 10)))

            # Hand gun - 2
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'pistol_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'gun.png')
                 }, {
                    'dmg': 2,
                    'spread': 40,
                    'hitchance': 90,
                    'firerate': 0.25,
                    'range': 8,
                    'magsize': 10,
                    'rlspeed': 0.8,
                    'zoom': 2,
                    'ammotype': 'bullet',
                    'guntype': 'secondary',
                    'name': 'Pistola'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_shot3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'universal_click.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_magin2.ogg'))]
                }, (37, 6)))

            # Knife - 3
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'knife_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'knifeitem.png')
                 }, {
                    'dmg': 2,
                    'spread': 40,
                    'hitchance': 100,
                    'firerate': 0.3,
                    'range': 1.5,
                    'magsize': 0,
                    'rlspeed': 0,
                    'zoom': 0,
                    'ammotype': None,
                    'guntype': 'melee',
                    'name': 'Faca'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))]
                }, (37, 10)))

            # Brass Knuckles - 4
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'brass_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'brassitem.png')
                 }, {
                    'dmg': 1,
                    'spread': 30,
                    'hitchance': 100,
                    'firerate': 0.2,
                    'range': 1.5,
                    'magsize': 0,
                    'rlspeed': 0,
                    'zoom': 0,
                    'ammotype': None,
                    'guntype': 'melee',
                    'name': 'Soqueira'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))]
                }, (37, 10)))

            # Gauss - 5
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'gauss_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'gaussitem.png')
                 }, {
                    'dmg': 6,
                    'spread': 10,
                    'hitchance': 85,
                    'firerate': 0.5,
                    'range': 15,
                    'magsize': 8,
                    'rlspeed': 1,
                    'zoom': 8,
                    'ammotype': 'ferromag',
                    'guntype': 'primary',
                    'name': 'Rifle Gauss'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'gauss_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'gauss_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'gauss_shot3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click2.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin2.ogg'))]
                }, (35, 7)))

            # Shotgun pistol - 6
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'sgp_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'shotpistol.png')
                 }, {
                    'dmg': 6,
                    'spread': 100,
                    'hitchance': 60,
                    'firerate': 0.2,
                    'range': 6,
                    'magsize': 1,
                    'rlspeed': 0.5,
                    'zoom': 1,
                    'ammotype': 'shell',
                    'guntype': 'secondary',
                    'name': 'Pistola SG'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'sgp_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'sgp_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'sgp_shot3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'universal_click.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (37, 6)))

            # ------ SPECIAL WEAPONS ----------
            # Fast Brass Knuckles - 7
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'brass_brass_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'brassbrassitem.png')
                 }, {
                    'dmg': 1,
                    'spread': 30,
                    'hitchance': 100,
                    'firerate': 0,
                    'range': 2,
                    'magsize': 0,
                    'rlspeed': 0,
                    'zoom': 0,
                    'ammotype': None,
                    'guntype': 'melee',
                    'name': 'Soqueira Leve'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))]
                }, (37, 10)))

            # Bloody Brass Knuckles - 8
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'blood_brass_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'bloodbrassitem.png')
                 }, {
                    'dmg': 20,
                    'spread': 60,
                    'hitchance': 100,
                    'firerate': 2,
                    'range': 1,
                    'magsize': 0,
                    'rlspeed': 0,
                    'zoom': 0,
                    'ammotype': None,
                    'guntype': 'melee',
                    'name': 'Soqueira de fúria'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))]
                }, (37, 10)))

            # Sharp Knife - 9
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'shiny_knife_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'shinyknifeitem.png')
                 }, {
                    'dmg': 3,
                    'spread': 40,
                    'hitchance': 100,
                    'firerate': 0.3,
                    'range': 1.5,
                    'magsize': 0,
                    'rlspeed': 0,
                    'zoom': 0,
                    'ammotype': None,
                    'guntype': 'melee',
                    'name': 'Faca Afiada'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))]
                }, (37, 10)))

            # Fast Knife - 10
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'desert_knife_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'desertknifeitem.png')
                 }, {
                    'dmg': 2,
                    'spread': 30,
                    'hitchance': 100,
                    'firerate': 0.1,
                    'range': 1.8,
                    'magsize': 0,
                    'rlspeed': 0,
                    'zoom': 0,
                    'ammotype': None,
                    'guntype': 'melee',
                    'name': 'Faca Leve'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'knife_swing3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'other', 'none.ogg'))]
                }, (37, 10)))

            # Modded Double Barrel Shotgun - 11
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'modded_shotgun_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'moddedshotgun.png')
                 }, {
                    'dmg': 15,
                    'spread': 220,
                    'hitchance': 65,
                    'firerate': 0.3,
                    'range': 6,
                    'magsize': 3.1415,  # lol bad code.
                    'rlspeed': 1.4,
                    'zoom': 8,
                    'ammotype': 'shell',
                    'guntype': 'primary',
                    'name': 'Espingarda Modificada'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_shot3.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_shot4.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'universal_click.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (34, 10)))

            # Impossible Double Barrel Shotgun - 12
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'shotgun_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'weirdshotgun.png')
                 }, {
                    'dmg': 8,
                    'spread': 200,
                    'hitchance': 65,
                    'firerate': 0.5,
                    'range': 8,
                    'magsize': 3,
                    'rlspeed': 1.4,
                    'zoom': 8,
                    'ammotype': 'shell',
                    'guntype': 'primary',
                    'name': 'Espingarda TB'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_shot3.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_shot4.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'universal_click.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (34, 10)))

            # AK 74 - 13
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'ak74_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'ak74item.png')
                 }, {
                    'dmg': 4,
                    'spread': 30,
                    'hitchance': 80,
                    'firerate': 0.08,
                    'range': 10,
                    'magsize': 30,
                    'rlspeed': 1,
                    'zoom': 8,
                    'ammotype': 'bullet',
                    'guntype': 'primary',
                    'name': 'AK-74'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot3.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot4.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot5.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click2.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin2.ogg'))]
                }, (35, 7)))

            # Extended mag AK - 14
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'akext_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'akextitem.png')
                 }, {
                    'dmg': 3,
                    'spread': 50,
                    'hitchance': 80,
                    'firerate': 0.08,
                    'range': 10,
                    'magsize': 40,
                    'rlspeed': 1.2,
                    'zoom': 6,
                    'ammotype': 'bullet',
                    'guntype': 'primary',
                    'name': 'AK-47 Pente Alongado'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot3.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot4.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot5.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click2.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin2.ogg'))]
                }, (35, 7)))

            # Camo AK-47 - 15
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'camo_ak_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'camoakitem.png')
                 }, {
                    'dmg': 3,
                    'spread': 50,
                    'hitchance': 90,
                    'firerate': 0.04,
                    'range': 10,
                    'magsize': 30,
                    'rlspeed': 0.8,
                    'zoom': 6,
                    'ammotype': 'bullet',
                    'guntype': 'primary',
                    'name': 'AK-47 Camo'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot3.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot4.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot5.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click2.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin2.ogg'))]
                }, (35, 7)))

            # Light AK-47 - 16
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'ak_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'lightakitem.png')
                 }, {
                    'dmg': 3,
                    'spread': 60,
                    'hitchance': 80,
                    'firerate': 0.08,
                    'range': 10,
                    'magsize': 20,
                    'rlspeed': 0.1,
                    'zoom': 4,
                    'ammotype': 'bullet',
                    'guntype': 'primary',
                    'name': 'AK-47 Leve'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot3.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot4.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_shot5.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click2.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin2.ogg'))]
                }, (35, 7)))

            # Gauss Hand gun - 17
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'gauss_pistol_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'gaussgun.png')
                 }, {
                    'dmg': 9,
                    'spread': 30,
                    'hitchance': 98,
                    'firerate': 0.25,
                    'range': 12,
                    'magsize': 10,
                    'rlspeed': 0.8,
                    'zoom': 8,
                    'ammotype': 'ferromag',
                    'guntype': 'secondary',
                    'name': 'Pistola Anomalia'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'gauss_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'gauss_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'gauss_shot3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click2.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin2.ogg'))]
                }, (37, 6)))

            # High power Hand gun - 18
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'pistol_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'hpgun.png')
                 }, {
                    'dmg': 3,
                    'spread': 40,
                    'hitchance': 85,
                    'firerate': 0.25,
                    'range': 8,
                    'magsize': 10,
                    'rlspeed': 0.8,
                    'zoom': 2,
                    'ammotype': 'bullet',
                    'guntype': 'secondary',
                    'name': 'Pistola HP'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'hpp_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'hpp_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'hpp_shot3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'universal_click.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_magin2.ogg'))]
                }, (37, 6)))

            # Modded Gauss - 19
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'modded_gauss_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'moddedgaussitem.png')
                 }, {
                    'dmg': 9,
                    'spread': 10,
                    'hitchance': 85,
                    'firerate': 0.5,
                    'range': 15,
                    'magsize': 12,
                    'rlspeed': 1,
                    'zoom': 9,
                    'ammotype': 'ferromag',
                    'guntype': 'primary',
                    'name': 'Rifle Gauss Modificado'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'gauss_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'gauss_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'gauss_shot3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click2.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin2.ogg'))]
                }, (35, 7)))

            # bump Gauss - 20
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'bump_gauss_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'bumpgaussitem.png')
                 }, {
                    'dmg': 6,
                    'spread': 20,
                    'hitchance': 70,
                    'firerate': 0.15,
                    'range': 15,
                    'magsize': 8,
                    'rlspeed': 1,
                    'zoom': 7,
                    'ammotype': 'ferromag',
                    'guntype': 'primary',
                    'name': 'Rifle Gauss Bump'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'gauss_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'gauss_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'gauss_shot3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_click2.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'AK_magin2.ogg'))]
                }, (35, 7)))

            # Black Shotgun pistol - 21
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'black_sgp_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'blackshotpistol.png')
                 }, {
                    'dmg': 8,
                    'spread': 100,
                    'hitchance': 60,
                    'firerate': 0.2,
                    'range': 6,
                    'magsize': 1,
                    'rlspeed': 0.4,
                    'zoom': 1,
                    'ammotype': 'shell',
                    'guntype': 'secondary',
                    'name': 'SGP Modificada'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'sgp_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'sgp_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'sgp_shot3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'universal_click.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (37, 6)))

            # TWO Shotgun pistol - 22
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'wtf_sgp_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'wtfshotpistol.png')
                 }, {
                    'dmg': 12,
                    'spread': 150,
                    'hitchance': 60,
                    'firerate': 0.2,
                    'range': 6,
                    'magsize': 2,
                    'rlspeed': 0.8,
                    'zoom': 1,
                    'ammotype': 'shell',
                    'guntype': 'secondary',
                    'name': 'SGP Ultra'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'sgp_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'sgp_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'sgp_shot3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'universal_click.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (37, 6)))

            # Auto Hand gun - 23
            config.gun_list.append(Gun(
                {'spritesheet': os.path.join('assets', 'textures', 'weapon', 'auto_pistol_spritesheet.png'),
                 'item': os.path.join('assets', 'textures', 'items', 'autogun.png')
                 }, {
                    'dmg': 2,
                    'spread': 40,
                    'hitchance': 90,
                    'firerate': 0.05,
                    'range': 8,
                    'magsize': 12,
                    'rlspeed': 0.9,
                    'zoom': 2,
                    'ammotype': 'bullet',
                    'guntype': 'secondary',
                    'name': 'Pistola Automática'
                }, {
                    'shot': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_shot1.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_shot2.ogg')),
                             pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_shot3.ogg'))],
                    'click': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'universal_click.ogg'))],
                    'magout': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_magout1.ogg')),
                               pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_magout2.ogg'))],
                    'magin': [pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_magin1.ogg')),
                              pygame.mixer.Sound(os.path.join('assets', 'sounds', 'weapons', 'pistol_magin2.ogg'))]
                }, (37, 6)))

        def load(self):
            self.__load_guns()

    class ItemLoader:
        @staticmethod
        def __load_item_types():
            config.item_types = [
                #Health
                {
                    'filepath': ('assets', 'textures', 'items', 'firstaid.png'),
                    'type': 'health',
                    'effect': 10,
                    'id': 0,
                },
                #Armor
                {
                    'filepath': ('assets', 'textures', 'items', 'kevlar.png'),
                    'type': 'armor',
                    'effect': 15,
                    'id': 1,
                },
                #Bullet
                {
                    'filepath': ('assets', 'textures', 'items', 'bullet.png'),
                    'type': 'bullet',
                    'effect': 10,
                    'id': 2
                },
                #Shell
                {
                    'filepath': ('assets', 'textures', 'items', 'shell.png'),
                    'type': 'shell',
                    'effect': 4,
                    'id': 3
                },
                #Knife
                {
                    'filepath': tuple(config.gun_list[3].itemtexture.split('\\')),
                    'type': config.gun_list[3].guntype,
                    'effect': config.gun_list[3],
                    'id': 4
                },
                #Pistol
                {
                    'filepath': tuple(config.gun_list[2].itemtexture.split('\\')),
                    'type': config.gun_list[2].guntype,
                    'effect': config.gun_list[2],
                    'id': 5
                },
                #AK-47
                {
                    'filepath': tuple(config.gun_list[0].itemtexture.split('\\')),
                    'type': config.gun_list[0].guntype,
                    'effect': config.gun_list[0],
                    'id': 6
                },
                #DB Shotgun
                {
                    'filepath': tuple(config.gun_list[1].itemtexture.split('\\')),
                    'type': config.gun_list[1].guntype,
                    'effect': config.gun_list[1],
                    'id': 7
                },
                #Brass Knuckles
                {
                    'filepath': tuple(config.gun_list[4].itemtexture.split('\\')),
                    'type': config.gun_list[4].guntype,
                    'effect': config.gun_list[4],
                    'id': 8
                },
                #Gauss rifle
                {
                    'filepath': tuple(config.gun_list[5].itemtexture.split('\\')),
                    'type': config.gun_list[5].guntype,
                    'effect': config.gun_list[5],
                    'id': 9,
                },
                #ferromag ammo
                {
                    'filepath': ('assets', 'textures', 'items', 'ferromag.png'),
                    'type': 'ferromag',
                    'effect': 6,
                    'id': 10,
                },
                #Shotgun pistol
                {
                    'filepath': tuple(config.gun_list[6].itemtexture.split('\\')),
                    'type': config.gun_list[6].guntype,
                    'effect': config.gun_list[6],
                    'id': 11,
                },

                #Random any item
                {
                    'filepath': ('assets', 'textures', 'items', 'random.png'),
                    'type': 'random',
                    'effect': ['health', 'armor', 'bullet', 'shell', 'ferromag',
                               'health', 'armor', 'bullet', 'shell', 'ferromag',
                               'melee', 'secondary', 'primary'],
                    'id': 12,
                },

                #Random weapon
                {
                    'filepath': ('assets', 'textures', 'items', 'randomgun.png'),
                    'type': 'random',
                    'effect': ['melee', 'secondary', 'primary'],
                    'id': 13,
                },

                #Random item
                {
                    'filepath': ('assets', 'textures', 'items', 'randomitem.png'),
                    'type': 'random',
                    'effect': ['health', 'armor', 'bullet', 'shell', 'ferromag'],
                    'id': 14,
                },

                #Light Brass Knuckles
                {
                    'filepath': tuple(config.gun_list[7].itemtexture.split('\\')),
                    'type': config.gun_list[7].guntype,
                    'effect': config.gun_list[7],
                    'id': 15
                },

                #Bloody Brass Knuckles
                {
                    'filepath': tuple(config.gun_list[8].itemtexture.split('\\')),
                    'type': config.gun_list[8].guntype,
                    'effect': config.gun_list[8],
                    'id': 16
                },

                #shiny knife
                {
                    'filepath': tuple(config.gun_list[9].itemtexture.split('\\')),
                    'type': config.gun_list[9].guntype,
                    'effect': config.gun_list[9],
                    'id': 17
                },

                #desert knife
                {
                    'filepath': tuple(config.gun_list[10].itemtexture.split('\\')),
                    'type': config.gun_list[10].guntype,
                    'effect': config.gun_list[10],
                    'id': 18
                },

                #modded shotgun
                {
                    'filepath': tuple(config.gun_list[11].itemtexture.split('\\')),
                    'type': config.gun_list[11].guntype,
                    'effect': config.gun_list[11],
                    'id': 19
                },

                #Impossible Shotgun
                {
                    'filepath': tuple(config.gun_list[12].itemtexture.split('\\')),
                    'type': config.gun_list[12].guntype,
                    'effect': config.gun_list[12],
                    'id': 20
                },

                #AK 74
                {
                    'filepath': tuple(config.gun_list[13].itemtexture.split('\\')),
                    'type': config.gun_list[13].guntype,
                    'effect': config.gun_list[13],
                    'id': 21
                },

                #AK 47 extended magazine
                {
                    'filepath': tuple(config.gun_list[14].itemtexture.split('\\')),
                    'type': config.gun_list[14].guntype,
                    'effect': config.gun_list[14],
                    'id': 22
                },

                #Camo AK-47
                {
                    'filepath': tuple(config.gun_list[15].itemtexture.split('\\')),
                    'type': config.gun_list[15].guntype,
                    'effect': config.gun_list[15],
                    'id': 23
                },

                #Light AK-47
                {
                    'filepath': tuple(config.gun_list[16].itemtexture.split('\\')),
                    'type': config.gun_list[16].guntype,
                    'effect': config.gun_list[16],
                    'id': 24
                },

                #Gauss pistol
                {
                    'filepath': tuple(config.gun_list[17].itemtexture.split('\\')),
                    'type': config.gun_list[17].guntype,
                    'effect': config.gun_list[17],
                    'id': 25
                },

                #HP Pistol
                {
                    'filepath': tuple(config.gun_list[18].itemtexture.split('\\')),
                    'type': config.gun_list[18].guntype,
                    'effect': config.gun_list[18],
                    'id': 26
                },

                #Modded Gauss
                {
                    'filepath': tuple(config.gun_list[19].itemtexture.split('\\')),
                    'type': config.gun_list[19].guntype,
                    'effect': config.gun_list[19],
                    'id': 27
                },

                #Bump Gauss
                {
                    'filepath': tuple(config.gun_list[20].itemtexture.split('\\')),
                    'type': config.gun_list[20].guntype,
                    'effect': config.gun_list[20],
                    'id': 28
                },

                #Black Shotgun Pistol
                {
                    'filepath': tuple(config.gun_list[21].itemtexture.split('\\')),
                    'type': config.gun_list[21].guntype,
                    'effect': config.gun_list[21],
                    'id': 29
                },

                #wtf shotgun pistol
                {
                    'filepath': tuple(config.gun_list[22].itemtexture.split('\\')),
                    'type': config.gun_list[22].guntype,
                    'effect': config.gun_list[22],
                    'id': 30
                },

                #auto pistol
                {
                    'filepath': tuple(config.gun_list[23].itemtexture.split('\\')),
                    'type': config.gun_list[23].guntype,
                    'effect': config.gun_list[23],
                    'id': 31
                },
            ]

        @staticmethod
        def __spawn_items():
            seed = config.current_level + config.seed
            for item in config.levels_list[config.current_level].items:
                stats = [x for x in config.item_types if x['id'] == item[1]][0]
                if stats['type'] == 'random':
                    random.seed(seed)
                    possible_items = [x for x in config.item_types if x['type'] in stats['effect']]
                    stats = random.choice(possible_items)
                    seed += 0.001

                elif stats['type'] not in ('primary', 'secondary', 'melee'):
                    stats = copy.deepcopy([x for x in config.item_types if x['id'] == item[1]][0])

                config.items.append(
                    Item(item[0], os.path.join(*stats['filepath']), stats['type'], stats['effect']))

        def load(self):
            self.__load_item_types()

        def spawn(self):
            self.__spawn_items()

    def __init__(self):
        self.npc_loader = self.NpcLoader()
        self.gun_loader = self.GunLoader()
        self.item_loader = self.ItemLoader()
        Texture.load_textures()

    @staticmethod
    def get_canvas_size():
        config.map_width = len(config.levels_list[config.current_level].array[0]) * config.tile_size
        config.map_height = len(config.levels_list[config.current_level].array) * config.tile_size
        config.actual_width = int(config.width / config.res) * config.res
        config.player_map_pos = config.levels_list[config.current_level].player_pos
        config.player_pos[0] = int(
            (config.levels_list[config.current_level].player_pos[0] * config.tile_size) + config.tile_size / 2)
        config.player_pos[1] = int(
            (config.levels_list[config.current_level].player_pos[1] * config.tile_size) + config.tile_size / 2)
        if len(config.gun_list) != 0:
            for gun in config.gun_list:
                gun.re_init()

    def load_resources(self):
        id = 0
        curr_texture = 0
        self.timer = 0

        Texture.load_textures()

        for texture in Texture.all_textures:
            if config.texture_type[id] == 'sprite':
                config.texture_list.append(pygame.image.load(texture))
            else:
                config.texture_list.append(Texture(texture, id))
            id += 1

        for texture in config.texture_list:
            config.tile_texture.update({curr_texture: texture})
            curr_texture += 1

        pygame.mixer.init()

        with open(os.path.join('data', 'settings.dat'), 'rb') as settings_file:
            settings = pickle.load(settings_file)

        config.fov = settings['fov']
        config.sensitivity = settings['sensitivity']
        config.volume = settings['volume']
        print(settings['volume'])

        with open(os.path.join('data', 'statistics.dat'), 'rb') as stats_file:
            stats = pickle.load(stats_file)

        config.statistics = stats

    def load_entities(self):
        self.npc_loader.load()
        self.gun_loader.load()
        self.item_loader.load()

    @staticmethod
    def load_custom_levels():
        if not os.stat(os.path.join('data', 'customLevels.dat')).st_size == 0:
            with open(os.path.join('data', 'customLevels.dat'), 'rb') as file:
                custom_levels = pickle.load(file)

            for level in custom_levels:
                config.clevels_list.append(Level(level))

        with open(os.path.join('data', 'tutorialLevels.dat'), 'rb') as file:
            tutorial_levels = pickle.load(file)

        for level in tutorial_levels:
            config.tlevels_list.append(Level(level))

    def load_new_level(self, map: Map, player: Player):
        config.npc_list = []
        config.all_items = []
        config.walkable_area = []
        config.all_tiles = []
        config.all_doors = []
        config.all_solid_tiles = []
        config.all_sprites = []

        self.get_canvas_size()
        map.__init__(config.levels_list[config.current_level].array)
        config.player_rect.center = (config.levels_list[config.current_level].player_pos[0] * config.tile_size,
                                     config.levels_list[config.current_level].player_pos[1] * config.tile_size)
        config.player_rect.centerx += config.tile_size / 2
        config.player_rect.centery += config.tile_size / 2
        player.real_x = config.player_rect.centerx
        player.real_y = config.player_rect.centery

        if config.shade and config.levels_list[config.current_level].shade:
            config.shade_rgba = config.levels_list[config.current_level].shade_rgba
            config.shade_visibility = config.levels_list[config.current_level].shade_visibility

        if config.current_level > 0:
            config.level_transition = False
            config.player_states['fade'] = True
        else:
            config.player_states['fade'] = True
            config.player_states['black'] = True

        config.player_states['title'] = True

        config.walkable_area = list(PathFinder().pathfind(config.player_map_pos, config.all_tiles[-1].map_pos))
        map.move_inaccessible_entities()
        self.npc_loader.spawn()
        self.item_loader.spawn()
