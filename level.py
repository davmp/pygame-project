class Level:
    def __init__(self, stats):
        self.stats = stats

        self.lvl_number = stats['lvl_number']
        self.sky_color = stats['sky_color']
        self.ground_color = stats['ground_color']
        self.npcs = stats['npcs']
        self.items = stats['items']
        self.player_pos = stats['player_pos']
        self.array = stats['array']
        self.shade = stats['shade'][0]
        self.shade_rgba = stats['shade'][1]
        self.shade_visibility = stats['shade'][2]
        if 'name' in stats:
            self.name = stats['name']
