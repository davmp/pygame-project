import pickle
import os

import config


class Segment:
    def __init__(self, stats):
        self.stats = stats
        self.ID = stats['id']
        self.array = stats['array']
        self.width = len(self.array[0])
        self.height = len(self.array)
        self.doors = stats['doors']
        self.items = stats['items']
        self.npcs = stats['npcs']
        self.type = stats['type']
        self.level_pos = None
        if 'player_pos' in stats:
            self.player_pos = stats['player_pos']
        else:
            self.player_pos = None


def load_customs():
    segments = []
    with open(os.path.join('data', 'standardSegments.dat'), 'rb') as file:
        segments = pickle.load(file)

    for seg in segments:
        config.segments_list.append(Segment(seg))

    if os.stat(os.path.join('data', 'customSegments.dat')).st_size != 0:
        with open(os.path.join('data', 'customSegments.dat'), 'rb') as file1:
            custom_segs = pickle.load(file1)

        for seg in custom_segs:
            config.segments_list.append(Segment(seg))


load_customs()
