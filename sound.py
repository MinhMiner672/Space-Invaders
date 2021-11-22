from pygame import mixer

class SoundPlayer:
    def __init__(self):
        self.shoot = mixer.Sound('./Sound/shoot.wav')
        self.activate = mixer.Sound('./Sound/activation.wav')
        self.heal = mixer.Sound('./Sound/heal.wav')
        self.player_touches_an_enemy = mixer.Sound('./Sound/lost_1_health.mp3')
        self.an_enemy_dies = mixer.Sound('./Sound/kill_an_enemy.mp3')
        self.game_over = mixer.Sound('./Sound/game_over.mp3')

        self.shoot.set_volume(0.1)
        self.activate.set_volume(1)
        self.an_enemy_dies.set_volume(0.2)
        self.player_touches_an_enemy.set_volume(0.5)
        self.heal.set_volume(0.5)
        self.game_over.set_volume(1)

    

    

