import pygame
import _global
from sprites import SpaceShip, Rect, Bullet
import colors


class Game:
    """Main Game Class"""
    def __init__(self):
        # Basic stuff for the screen
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load('Images/bg.jpg').convert()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Space Invaders')
        pygame.display.set_icon(pygame.image.load('Images/game_icon.png').convert_alpha())

        # Game states
        self.started = False
        self.over = False
        self.game_score = 0

        # Sprite Groups
        self.player_grp = pygame.sprite.GroupSingle(SpaceShip())
        _global.player = self.player_grp

        self.bullet_grp = pygame.sprite.Group()
        self.power_type = 0

        self.enemy_grp = pygame.sprite.Group()
        self.mana_grp = pygame.sprite.Group()
        self.health_cells_grp = pygame.sprite.Group()
        self.health_items = pygame.sprite.Group()

        self.list_of_power_ups = pygame.sprite.Group()
        self.activated_power_up = pygame.sprite.GroupSingle()

        self.health_top_left_x_pos = 497
        self.x_pos_for_each_power_up_in_list = 200

        # Bool Vars
        self.shield_rect_on_player = False

    def show_background(self):
        """Shows the game background"""
        self.screen.blit(self.background, (0, 0))

    def display_score(self):
        """Displays the game score"""
        space_font = pygame.font.Font('Fonts/big_space.ttf', 40)
        text_score_surf = space_font.render(f'Score: {self.game_score}', False, (194, 255, 212))
        score_text_rect = text_score_surf.get_rect(topleft=(20, 540))
        self.screen.blit(text_score_surf, score_text_rect)

    def refresh(self):
        """Cleans the game"""
        # clear all bullets and enemies
        self.bullet_grp.empty()
        self.enemy_grp.empty()
        self.mana_grp.empty()

        # recover the player (full 5 health cells)
        self.health_top_left_x_pos = 497
        for i in range(5):
            self.health_cells_grp.add(Rect(x=self.health_top_left_x_pos, y=580, surf_type='health_cell', width=60, height=15))
            self.health_top_left_x_pos += 60
        self.health_top_left_x_pos -= 60

    def style_health_bar(self):
        if 1 < len(self.health_cells_grp) < 4:
            _global.rect_health_color = colors.YELLOW
        elif len(self.health_cells_grp) == 1:
            _global.rect_health_color = colors.RED
        elif len(self.health_cells_grp) >= 4:
            _global.rect_health_color = colors.GREEN

    def control_fps(self):
        """Controls the FPS's consistence, make it not fluctuate"""
        pygame.display.update()
        self.clock.tick(60)

    def __repr__(self):
        return f'Space Invaders Main Class'
