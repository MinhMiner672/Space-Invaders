from time import time
import pygame, _debug
from random import randint
import _global, colors


class Rect(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, type: str):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect_type = type
        self.color_index = 0
        self.flashing_power_index = 0 


    def update(self):
        if self.rect_type == 'health':
            self.image.fill(_global.rect_health_color)
            
        elif self.rect_type == 'energy':
            if _global.max_mana_reach == True:
                if self.color_index >= len(colors.MANA_COLORS):
                    self.color_index = 0
                self.image.fill(colors.MANA_COLORS[int(self.color_index)])
                self.color_index += 0.2
                
            else:
                self.image.fill(colors.MANA_COLORS[_global.mana_color_index])

        elif self.rect_type == 'powers':
            if _global.activated_power == True:
                if self.flashing_power_index >= len(colors.POWERS_COLORS):
                    self.flashing_power_index = 0
                self.image.fill(colors.POWERS_COLORS[int(self.flashing_power_index)])
                self.flashing_power_index += 0.3
            
            else:
                self.image.fill(colors.YELLOW)
            
    

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.image = pygame.image.load('Images/Player/spaceship.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (400, 570))


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
    def __init__(self, type, x_pos):
        super().__init__()
        if type == 'normal':
            self.image = pygame.transform.scale(pygame.image.load('Images/Bullets/bullet.png').convert_alpha(), (25, 25))
            # self.id = 'normal_bullet'
        elif type == 'bigger':
            self.image = pygame.transform.scale(pygame.image.load('Images/Bullets/bullet.png').convert_alpha(), (45, 45))
            # self.id = 'powered'


        self.rect = self.image.get_rect(midbottom = (x_pos, 508))

    def destroy(self):
        if self.rect.y < -10:
            self.kill()

    def update(self):
        self.rect.y -= 8
        self.destroy()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type) -> None:
        super().__init__()
        self.enemy_type = type
        if self.enemy_type == 'normal':
            self.image = pygame.image.load('Images/Enemy/alien1.png').convert_alpha()
            self.health = 5
        elif self.enemy_type == 'big':
            self.image = pygame.image.load('Images/Enemy/alien_bigger.png').convert_alpha()
            self.health = 10
        elif self.enemy_type == 'mega':
            self.image = pygame.transform.scale(pygame.image.load('Images/Enemy/alien_large.png').convert_alpha(), (70, 70))
            self.health = 17

        self.rect = self.image.get_rect(midtop = (randint(10, 700), 5))
        self.direction = ''

    def bounce(self):
        if self.direction == '':
            if self.rect.x < 400:
                self.direction = 'left'
            else:
                self.direction = 'right'

        if self.direction == 'left':
            self.rect.left -= 3
            self.rect.y += 1
            if self.rect.left <= 0:
                self.rect.left = 0
                self.direction = 'right'

        else:
            self.rect.right += 3
            self.rect.y += 1
            if self.rect.right >= 800:
                self.rect.right = 800
                self.direction = 'left'

    def collision_check(self):
        if _global.collision == True:
            if _global.bullet_type == 0 or _global.bullet_type == 1:
                self.health -= 1
            elif _global.bullet_type == 2:
                self.health -= 3
            
            if self.health <= 0:
                increase_score = 2 if self.enemy_type == 'mega' else 1
                _global.glb_score += increase_score
                self.kill()
                _global.killed_an_enemy = True

            _global.collision = False

    def if_the_enemy_is_too_low(self):
        if self.rect.top > 695:
            self.kill()


    def update(self):
        self.bounce()
        self.if_the_enemy_is_too_low()
        self.collision_check()


class Health_Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load('Images/heal.png').convert_alpha(), (50, 50))
        self.rect = self.image.get_rect(midtop=(randint(10, 700), 5))
        self.direction = ''

    def bounce(self):
        if self.direction == '':
            if self.rect.x < 400:
                self.direction = 'left'
            else:
                self.direction = 'right'

        if self.direction == 'left':
            self.rect.left -= 5
            self.rect.y += 2
            if self.rect.left <= 0:
                self.rect.left = 0
                self.direction = 'right'

        else:
            self.rect.right += 5
            self.rect.y += 2
            if self.rect.right >= 800:
                self.rect.right = 800
                self.direction = 'left'
    
    def update(self):
        if self.rect.y > 695:
            self.kill()
        self.bounce()