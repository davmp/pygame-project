# Configurações
title = "A Casa"
version = "0.0.1"

"""
-> Configurações de Jogo
"""
current_level = 0
fps = 31
mode = 1
volume = 1
music_volume = 1
paused = False

current_level_size = None
level_transition = False
won = False
dt = 0
cfps = 0
statistics = {}
played_seconds = 0

"""
-> Configurações do Mapa
"""
levels_size = 4
levels_amnt = 100

levels_list = []
segments_list = []
clevels_list = []
glevels_list = []
tlevels_list = []
seed = None
playing_customs = False
playing_new = False
playing_tutorial = False

"""
-> Configurações da Tela
"""
width, height = 700, 550
actual_width = 0
map_width = None
map_height = None
window_height = int(height + (height * 0.15))
axes = (0, 0)
scn_shake = 0
font = "assets/fonts/VCR_MONO.ttf"
switch_mode = False

"""
-> Configurações do Raycast (Interações)
"""
res = 140
fov = 60
render = 16
shade = False
shade_rgba = (0, 0, 0, 255)
shade_visibility = 1000

zbuffer = []
middle_slice_len = None
middle_slice = None
middle_ray_pos = None
raylines = []

"""
-> Configurações dos Blocos
"""
tile_size = 64

all_tiles = []
trigger_tiles = []
all_solid_tiles = []
rendered_tiles = []
walkable_area = []
all_doors = []
end_angle = 0
tile_texture = {}
tile_solid = {
    0: False,
    1: True,
    2: True,
    3: True,
    4: True,
    5: True,
    6: True,
    7: True,
    8: True,
    9: True,
    10: False,

    11: True,
    12: True,
    13: True,
    14: True,
    15: True,
    16: True,
    17: True,
    18: True,

    19: True,
    20: True,
    21: True,
    22: True,
    23: True,
    24: True,
    25: True,
}
tile_visible = {
    0: False,
    1: True,
    2: True,
    3: True,
    4: True,
    5: True,
    6: True,
    7: True,
    8: False,
    9: False,
    10: False,

    11: True,
    12: True,
    13: True,
    14: True,
    15: True,
    16: False,
    17: False,
    18: False,

    19: True,
    20: True,
    21: True,
    22: True,
    23: True,
    24: True,
    25: False,
}
texture_type = {
    0: 'air',
    1: 'wall',
    2: 'wall',
    3: 'wall',
    4: 'wall',
    5: 'end',
    6: 'vdoor',
    7: 'hdoor',
    8: 'sprite',
    9: 'sprite',
    10: 'sprite',

    11: 'wall',
    12: 'wall',
    13: 'wall',
    14: 'wall',
    15: 'end',
    16: 'sprite',
    17: 'sprite',
    18: 'sprite',

    19: 'wall',
    20: 'wall',
    21: 'wall',
    22: 'end',
    23: 'vdoor',
    24: 'hdoor',
    25: 'sprite',
}

all_sprites = []

"""
-> Configurações do Jogador
"""
player_speed = 256
sensitivity = 0.25
player_angle = 270
og_player_health = 25
og_player_armor = 5

player_health = og_player_health
player_armor = og_player_armor
player_pos = [0, 0]
player_map_pos = []
player_rect = None
mouse_btn_active = False
mouse2_btn_active = False
reload_key_active = False
aiming = False
player_states = {
    'dead': False,
    'hurt': False,
    'heal': False,
    'armor': False,
    'invopen': False,
    'fade': False,
    'black': False,
    'title': False,
    'cspeed': 0
}
player = None
last_player_map_pos = None

items = []

"""
-> Configurações de Textura
"""
texture_darken = 100
texture_list = []


"""
--> Configurações das Armas
"""
unlimited_ammo = False

current_gun = None
next_gun = None
prev_gun = None
gun_list = []
ground_weapon = None


"""
--> Configurações dos NPCs
"""
ignore_player = False

npc_list = []
npc_types = []
npc_sounds = []


"""
--> Configurações do Inventário
"""
held_ammo = {}
max_ammo = {}
inventory = {
    'primary': None,
    'secondary': None,
    'melee': None
}
item_types = []
inv_strings_updated = False

temp = []
