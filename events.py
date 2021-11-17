from random import choice

import pygame
import sys
import _global
from sprites import Bullet, Enemy, Health_Item, Rect
import time


class Events:
    """This class is used to track some events during the game"""

    # __init__ takes the game class arg to manipulate with Game()
    def __init__(self, game_class):
        self.game = game_class

        # Timers
        self.health_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.health_timer, 10000)

        self.spawn_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_timer, 3500)

        self.seconds_per_timer = 1700
        self.enemy_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.enemy_timer, self.seconds_per_timer)

        # Power Sprites
        self.triple_bullets_surf = pygame.transform.scale(pygame.image.load('Images/Bullets/triple_bullets.jpg').convert_alpha(), (30, 30))
        self.triple_bullets_rect = self.triple_bullets_surf.get_rect(topleft=(205, 18))

        self.big_bullets_surf = pygame.transform.scale(pygame.image.load('Images/Bullets/bullet.png').convert_alpha(), (30, 30))
        self.big_bullets_rect = self.big_bullets_surf.get_rect(topleft=(205 + 100, 18))

        self.shield_surf = pygame.transform.scale(pygame.image.load('Images/blue_shield.png').convert_alpha(), (30, 30))
        self.shield_rect = self.shield_surf.get_rect(topleft=(205 + 200, 18))

        self.die_img_surf = pygame.transform.scale(pygame.image.load('Images/die.png').convert_alpha(), (30, 30))
        self.die_rect = self.die_img_surf.get_rect(topleft=(205 + 300, 18))

        self.cross_surf = pygame.transform.scale(pygame.image.load('Images/cross_mark.png').convert_alpha(), (50, 50))
        self.cross_rect = self.cross_surf.get_rect(topleft=(495, 6))

        # Events variables (boolean)
        self.wait_for_user_activation = False
        self.ability_to_kill_all = False
        self.shield_activation = False
        self.max_mana_reach = False
        self.mana_rect_x_pos = 497

        self.if_an_enemy_touches_a_bullet = False
        self.lost_1_health = False
        self.player_heals = False

        self.killed_an_enemy = False
        self.bullet_type = 0

        self.start_cooldown = 0
        self.timer_in_progress = True

        self.mana_color_index = 0

    def key_board_inputs(self):
        """If a specific key is pressed, this function will be executed"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if the game is started
            if self.game.started:
                # checks if a key is pressed
                if event.type == pygame.KEYDOWN:
                    # if the 'space' key is pressed (shoots)
                    if event.key == pygame.K_SPACE:
                        # if user reaches the maximum amount of energy
                        if len(self.game.mana_grp) == 10:
                            self.wait_for_user_activation = True

                        # if user has activated the first power-up (triple bullets)
                        if self.bullet_type == 1:
                            x_pos_for_each_bullet = (self.game.player_grp.sprite.rect.x + 29) - 50
                            for i in range(3):
                                self.game.bullet_grp.add(Bullet('normal', x_pos_for_each_bullet))
                                x_pos_for_each_bullet += 50

                        # if user has activated the first power-up (giant bullets)
                        elif self.bullet_type == 2:
                            self.game.bullet_grp.add(Bullet('bigger', self.game.player_grp.sprite.rect.x + 30))

                        # normal power-up (bullets)
                        else:
                            self.game.bullet_grp.add(Bullet('normal', self.game.player_grp.sprite.rect.x + 29))

                # the game will wait for user power-up activation
                if self.wait_for_user_activation:
                    if event.type == pygame.KEYDOWN:
                        # user chooses the first power-up (triple bullets)
                        if event.key == pygame.K_1:
                            self.game.mana_grp.empty()
                            for sprite in self.game.list_of_power_ups.sprites():
                                if self.game.list_of_power_ups.sprites().index(sprite) == 0:
                                    continue
                                self.game.list_of_power_ups.remove(sprite)

                            x_pos_for_each_bullet = (self.game.player_grp.sprite.rect.x + 29) - 50
                            for i in range(3):
                                self.game.bullet_grp.add(Bullet('normal', x_pos_for_each_bullet))
                                x_pos_for_each_bullet += 50

                            self.game.x_pos_for_each_power_up_in_list = 200

                            _global.max_mana_reach = False
                            _global.killed_an_enemy = False
                            _global.bullet_type = 1

                            _global.start_cooldown = int(str(time.time()).split('.')[0])
                            _global.activated_power = True
                            _global.wait_for_user_activation = False

                        # user chooses the first power-up (giant bullets)
                        elif event.key == pygame.K_2:
                            _global.bullet_type = 2
                            self.game.mana_grp.empty()
                            selected_power_sprite = self.game.list_of_power_ups.sprites()[1]
                            for sprite in self.game.list_of_power_ups.sprites():
                                if sprite != selected_power_sprite:
                                    self.game.list_of_power_ups.remove(sprite)

                            self.game.x_pos_for_each_power_up_in_list = 200

                            self.game.bullet_grp.empty()
                            _global.killed_an_enemy = False
                            _global.max_mana_reach = False
                            _global.start_cooldown = int(str(time.time()).split('.')[0])
                            _global.activated_power = True
                            _global.wait_for_user_activation = False

                        # user chooses the first power-up (shield)
                        elif event.key == pygame.K_3:
                            selected_power_sprite = self.game.list_of_power_ups.sprites()[2]

                            for sprite in self.game.list_of_power_ups.sprites():
                                if sprite != selected_power_sprite:
                                    self.game.list_of_power_ups.remove(sprite)

                            self.game.x_pos_for_each_power_up_in_list = 200

                            _global.shield_activation = True
                            _global.killed_an_enemy = False
                            _global.max_mana_reach = False
                            _global.activated_power = True
                            _global.wait_for_user_activation = False

                            _global.start_cooldown = int(str(time.time()).split('.')[0])
                            self.game.mana_grp.empty()

                        # user chooses the first power-up (kill all enemies, this depends on user's ability)
                        elif event.key == pygame.K_4:
                            if self.ability_to_kill_all:
                                selected_power_sprite = self.game.list_of_power_ups.sprites()[3]
                                for sprite in self.game.list_of_power_ups.sprites():
                                    if sprite != selected_power_sprite:
                                        self.game.list_of_power_ups.remove(sprite)

                                self.game.x_pos_for_each_power_up_in_list = 200

                                _global.killed_an_enemy = False
                                _global.max_mana_reach = False
                                _global.activated_power = True
                                _global.wait_for_user_activation = False

                                self.game.enemy_grp.empty()
                                self.game.list_of_power_ups.empty()
                                self.game.mana_grp.empty()

                if event.type == self.enemy_timer:
                    self.game.enemy_grp.add(Enemy(choice(
                        ['normal', 'normal', 'normal', 'normal', 'big', 'mega', 'normal', 'normal', 'big', 'normal',
                         'normal']), self.game, self))

                if event.type == self.health_timer:
                    if len(self.game.health_cells_grp) < 5:
                        self.game.health_items.add(Health_Item())

                if event.type == self.spawn_timer:
                    self.seconds_per_timer -= 50
                    self.enemy_timer = pygame.USEREVENT + 2
                    pygame.time.set_timer(self.enemy_timer, self.seconds_per_timer)

    def collision(self, shield_rect):
        """
        This functions checks for 4 collision events:
        - If an enemy touches a bullet
        - If an enemy touches the player
        - If an enemy touches player's shield
        - If the player gets a health item
        """

        for ene_sprite in self.game.enemy_grp.sprites():
            if len(self.game.activated_power_up.sprites()) != 0:
                if ene_sprite.rect.colliderect(shield_rect):
                    ene_sprite.kill()

            # If the player touches an enemy
            if ene_sprite.rect.colliderect(self.game.player_grp.sprite.rect) or ene_sprite.rect.y > 605:
                self.lost_1_health = True

                # remove the enemy sprite
                ene_sprite.kill()

                # remove one health cell (loses 1 health cell)
                self.game.health_cells_grp.sprites()[-1].kill()
                try:
                    self.game.health_top_left_x_pos = self.game.health_cells_grp.sprites()[-1].rect.x + 60
                except IndexError:
                    # index error with health_cells_grp (this is due to empty list)
                    return

        # if the enemy touches a bullet
        for bullet_sprite in self.game.bullet_grp.sprites():
            for ene_sprite in self.game.enemy_grp.sprites():
                if bullet_sprite.rect.colliderect(ene_sprite.rect) or ene_sprite.rect.top > 595:
                    bullet_sprite.kill()
                    self.if_an_enemy_touches_a_bullet = True

        # if the player gets the health item
        for health_item in self.game.health_items.sprites():
            if health_item.rect.colliderect(self.game.player_grp.sprite.rect):
                self.game.health_cells_grp.add(Rect(self.game.health_top_left_x_pos, 580, 'health_cell', self, 60, 15))
                _global.player_heals = True
                health_item.kill()

    def player_events(self):
        """
        Tracks the player's events (reaching full energy, losing 1 health cell, power-up activation...).
        This function doesn't include collision events
        """
        # If the player hits an enemy and loses 1 health cell
        if self.lost_1_health:
            # if the player dies
            if len(self.game.health_cells_grp) == 0:
                self.game.over, self.game.started = True, False
                self.game.refresh()
            self.lost_1_health = False

        # If the player gets a health item
        if self.player_heals:
            self.game.health_top_left_x_pos += 60
            self.player_heals = False

        # If the player's energy bar is full
        if self.max_mana_reach:
            # if the player has not obtained the last power-up
            if not self.ability_to_kill_all:
                self.game.screen.blit(self.cross_surf, self.cross_rect)

            if len(self.game.list_of_power_ups.sprites()) < 4:
                for i in range(4):
                    self.game.list_of_power_ups.add(Rect(self.game.x_pos_for_each_power_up_in_list, 13, 'powers', self, 40, 40))
                    # powers_grp.add(Rect(x_pos_for_power_rects, 13, 'powers', 40, 40))
                    self.game.x_pos_for_each_power_up_in_list += 100

        # If an enemy is killed by the player, then add 1 energy cell for the player
        if self.killed_an_enemy:
            # if the energy bar is not full yet
            if len(self.game.mana_grp) < 10:
                mana_surf = Rect(self.mana_rect_x_pos + (len(self.game.mana_grp) * 30), 560, 'energy', self, 30, 15)
                self.game.mana_grp.add(mana_surf)
                self.mana_color_index = len(self.game.mana_grp) - 1
                self.killed_an_enemy = False
            else:
                self.max_mana_reach = True

        # check if the player is able to use "kill all" power
        if self.game.game_score % 30 in [0, 1] and self.game.game_score != 0 and self.game.game_score >= 20:
            self.ability_to_kill_all = True

    def __repr__(self):
        return 'Events Class'
