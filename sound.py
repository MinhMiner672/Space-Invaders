from pygame import mixer

class SoundPlayer:
    def __init__(self):
        self.shoot = mixer.Sound('./Sound/shoot.wav')
        self.activate = mixer.Sound('./Sound/activation.wav')
        self.heal = mixer.Sound('./Sound/heal.wav')
        # self.player_touches_an_enemy = mixer.Sound('')
        self.an_enemy_dies = mixer.Sound('./Sound/roblox_die.mp3')
        # self.game_over = mixer.Sound('')
        # self.touches_an_bullet = mixer.Sound('')
        # self.get_score = mixer.Sound('')

        self.shoot.set_volume(0.1)
        self.activate.set_volume(1)
        self.an_enemy_dies.set_volume(0.2)

    

    

