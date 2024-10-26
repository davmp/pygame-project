from pygame import mixer
import config


def play_sound(sound, distance):
    if distance <= config.tile_size * config.render:
        if distance >= config.tile_size * (config.render*0.8):
            mixer.Sound.set_volume(sound, 0.2 * config.volume)
        elif distance >= config.tile_size * (config.render*0.4):
            mixer.Sound.set_volume(sound, 0.5 * config.volume)

        else:
            mixer.Sound.set_volume(sound, config.volume)
        mixer.Sound.play(sound)
