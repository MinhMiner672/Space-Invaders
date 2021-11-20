import pygame
from random import randint
import colors


class Rect(pygame.sprite.Sprite):
    """This class is a base class for rectangular surfaces"""

    def __init__(
        self,
        x: int,
        y: int,
        surf_type: str,
        event_class=None,
        width: int = None,
        height: int = None,
    ):
        super().__init__()
        if event_class is not None:
            self.events_tracker = event_class

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.x = x
        self.y = y
        self.rect_type = surf_type
        self.color_index = 0
        self.flashing_power_index = 0
        self.direction = ""

    def update(self):
        if self.rect_type == "health_cell":
            try:
                self.image.fill(self.events_tracker.rect_health_color)
            except AttributeError:
                pass

        elif self.rect_type == "energy":
            if self.events_tracker.max_mana_reach:
                if self.color_index >= len(colors.MANA_COLORS):
                    self.color_index = 0
                self.image.fill(colors.MANA_COLORS[int(self.color_index)])
                self.color_index += 0.2

            else:
                self.image.fill(
                    colors.MANA_COLORS[self.events_tracker.mana_color_index]
                )

        elif self.rect_type == "powers":
            if self.events_tracker.activated_power:
                if self.flashing_power_index >= len(colors.POWERS_COLORS):
                    self.flashing_power_index = 0
                self.image.fill(colors.POWERS_COLORS[int(self.flashing_power_index)])
                self.flashing_power_index += 0.3

            else:
                self.image.fill(colors.YELLOW)


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Images/Player/spaceship.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(400, 570))
        self.attr = "lmao"

    def key_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.left -= 6
            if self.rect.left == 0:
                self.rect.left = 0
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.right += 6
            if self.rect.left == 800:
                self.rect.left = 800

    def update(self):
        self.key_input()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_type, x_pos):
        super().__init__()
        if bullet_type == "normal":
            self.image = pygame.transform.scale(
                pygame.image.load("Images/Bullets/bullet.png").convert_alpha(), (25, 25)
            )

        elif bullet_type == "bigger":
            self.image = pygame.transform.scale(
                pygame.image.load("Images/Bullets/bullet.png").convert_alpha(), (45, 45)
            )

        self.rect = self.image.get_rect(midbottom=(x_pos, 508))

    def destroy(self):
        if self.rect.y < -10:
            self.kill()

    def update(self):
        self.rect.y -= 8
        self.destroy()


class Power_Ups(pygame.sprite.Sprite):
    def __init__(self, power_type, x_pos: int, y_pos: int):
        super().__init__()

        if power_type == "big_bullets":
            self.image = pygame.transform.scale(
                pygame.image.load("Images/Bullets/bullet.png").convert_alpha(), (45, 45)
            )

        self.rect = self.image.get_rect(midbotton=(x_pos, y_pos))

        if power_type == "shield":
            self.image = pygame.transform.scale(
                pygame.image.load("Images/blue_shield.png").convert_alpha(), (30, 30)
            )
            self.rect = self.image.get_rect(center=(x_pos, y_pos))

        if power_type == "kill_all":
            self.image = pygame.transform.scale(
                pygame.image.load("Images/die.png").convert_alpha(), (30, 30)
            )


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, game_class, event_class) -> None:
        super().__init__()

        self.game = game_class
        self.events_tracker = event_class

        self.enemy_type = enemy_type
        if self.enemy_type == "normal":
            self.image = pygame.image.load("Images/Enemy/alien1.png").convert_alpha()
            self.health = 5
        elif self.enemy_type == "big":
            self.image = pygame.image.load(
                "Images/Enemy/alien_bigger.png"
            ).convert_alpha()
            self.health = 10
        elif self.enemy_type == "mega":
            self.image = pygame.transform.scale(
                pygame.image.load("Images/Enemy/alien_large.png").convert_alpha(),
                (70, 70),
            )
            self.health = 17

        self.rect = self.image.get_rect(midtop=(randint(10, 700), 5))
        self.direction = ""

    def bounce(self):
        if self.direction == "":
            if self.rect.x < 400:
                self.direction = "left"
            else:
                self.direction = "right"

        if self.direction == "left":
            self.rect.left -= 3
            self.rect.y += 1
            if self.rect.left <= 0:
                self.rect.left = 0
                self.direction = "right"

        else:
            self.rect.right += 3
            self.rect.y += 1
            if self.rect.right >= 800:
                self.rect.right = 800
                self.direction = "left"

    def if_the_enemy_touches_a_bullet(self):
        if self.events_tracker.if_an_enemy_touches_a_bullet:
            if (
                self.events_tracker.bullet_type == 0
                or self.events_tracker.bullet_type == 1
            ):
                self.health -= 1
            elif self.events_tracker.bullet_type == 2:
                self.health -= 3

            self.events_tracker.if_an_enemy_touches_a_bullet = False

    def if_enemy_is_health_low(self):
        if self.health <= 0:
            self.kill()
            increase_score = 2 if self.enemy_type == "mega" else 1
            self.game.game_score += increase_score
            self.events_tracker.killed_an_enemy = True

    def update(self):
        self.if_enemy_is_health_low()
        self.bounce()
        self.if_the_enemy_touches_a_bullet()


class Health_Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(
            pygame.image.load("Images/Power-ups/heal_icon.png").convert_alpha(),
            (50, 50),
        )
        self.rect = self.image.get_rect(midtop=(randint(10, 700), 5))
        self.direction = ""

    def bounce(self):
        if self.direction == "":
            if self.rect.x < 400:
                self.direction = "left"
            else:
                self.direction = "right"

        if self.direction == "left":
            self.rect.left -= 5
            self.rect.y += 2
            if self.rect.left <= 0:
                self.rect.left = 0
                self.direction = "right"

        else:
            self.rect.right += 5
            self.rect.y += 2
            if self.rect.right >= 800:
                self.rect.right = 800
                self.direction = "left"

    def update(self):
        if self.rect.y > 695:
            self.kill()
        self.bounce()


class Button(pygame.sprite.Sprite):
    def __init__(
        self, x_pos: int, y_pos: int, text: str, size: int, font_path: str, color: tuple
    ):
        super(Button, self).__init__()
        self.text = text

        self.x = x_pos
        self.y = y_pos

        self.font_path = font_path
        self.font_size = size
        self.text = text
        self.color = color

        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.image = self.font.render(text, False, color)
        self.rect = self.image.get_rect(midtop=(self.x, self.y))

    def on_hover(self) -> bool:
        """If the user hovers the mouse on the button"""
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

        return False

    def on_click(self):
        """If the user clicks on the button"""
        if self.on_hover() and pygame.mouse.get_pressed(num_buttons=3)[0]:
            return True

        return False

    def __repr__(self):
        return "Button Object"
