from random import choice

import pygame
import sys
from sprites import Bullet, Enemy, Health_Item, Rect
import time
import colors
from pygame import mixer
from sound import SoundPlayer


class Events:
    """This class is used to track some events during the game"""

    # __init__ takes the game class arg to manipulate with Game()
    def __init__(self, game_class):
        self.sound_player = SoundPlayer()

        self.game = game_class

        # Timers
        self.health_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.health_timer, 15000)

        self.spawn_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_timer, 3500)

        self.seconds_per_timer = 1700
        self.enemy_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.enemy_timer, self.seconds_per_timer)

        # Power Sprites
        self.triple_bullets_surf = pygame.transform.scale(
            pygame.image.load("Images/Bullets/triple_bullets.jpg").convert_alpha(),
            (30, 30),
        )
        self.triple_bullets_rect = self.triple_bullets_surf.get_rect(topleft=(205, 18))

        self.big_bullets_surf = pygame.transform.scale(
            pygame.image.load("Images/Bullets/bullet.png").convert_alpha(), (30, 30)
        )
        self.big_bullets_rect = self.big_bullets_surf.get_rect(topleft=(205 + 100, 18))

        self.shield_surf = pygame.transform.scale(
            pygame.image.load("Images/Power-ups/blue_shield_icon.png").convert_alpha(),
            (30, 30),
        )
        self.shield_rect = self.shield_surf.get_rect(topleft=(205 + 200, 18))

        self.die_img_surf = pygame.transform.scale(
            pygame.image.load("Images/Power-ups/die_icon.png").convert_alpha(), (30, 30)
        )
        self.die_rect = self.die_img_surf.get_rect(topleft=(205 + 300, 18))

        self.cross_surf = pygame.transform.scale(
            pygame.image.load("Images/Power-ups/cross_mark_icon.png").convert_alpha(),
            (50, 50),
        )
        self.cross_rect = self.cross_surf.get_rect(topleft=(495, 6))

        self.shield_surf_on_player = None
        self.shield_rect_on_player = None

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

        self.activated_power = False
        self.start_cooldown = 0
        self.timer_in_progress = True

        self.mana_color_index = 0
        self.rect_health_color = colors.GREEN
        self.rect_mama_color = colors.CYAN

    def keyboard_inputs(self) -> None:
        """If a specific key is pressed, this function will be executed"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if the game is started
            if self.game.started and not self.game.paused:
                # checks if a key is pressed
                if event.type == pygame.KEYDOWN:
                    # if user presses ESCAPE key (pauses the game)
                    if event.key == pygame.K_ESCAPE:
                        self.game.paused = True

                    # if the 'space' key is pressed (shoots)
                    if event.key == pygame.K_SPACE:
                        self.sound_player.shoot.play()
                        # if user reaches the maximum amount of energy
                        if len(self.game.mana_grp) == 10:
                            self.wait_for_user_activation = True

                        # if user has activated the first power-up (triple bullets)
                        if self.bullet_type == 1:
                            x_pos_for_each_bullet = (
                                self.game.player_grp.sprite.rect.x + 29
                            ) - 50
                            for i in range(3):
                                self.game.bullet_grp.add(
                                    Bullet("normal", x_pos_for_each_bullet)
                                )
                                x_pos_for_each_bullet += 50

                        # if user has activated the first power-up (giant bullets)
                        elif self.bullet_type == 2:
                            self.game.bullet_grp.add(
                                Bullet(
                                    "bigger", self.game.player_grp.sprite.rect.x + 30
                                )
                            )

                        # normal power-up (bullets)
                        else:
                            self.game.bullet_grp.add(
                                Bullet(
                                    "normal", self.game.player_grp.sprite.rect.x + 29
                                )
                            )

                # the game will wait for user power-up activation
                if self.wait_for_user_activation:
                    if event.type == pygame.KEYDOWN:
                        # user chooses the first power-up (triple bullets)
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                            if event.key == pygame.K_1:
                                self.game.mana_grp.empty()
                                for sprite in self.game.list_of_power_ups.sprites():
                                    if (
                                        self.game.list_of_power_ups.sprites().index(sprite)
                                        == 0
                                    ):
                                        continue
                                    self.game.list_of_power_ups.remove(sprite)

                                x_pos_for_each_bullet = (
                                    self.game.player_grp.sprite.rect.x + 29
                                ) - 50
                                for i in range(3):
                                    self.game.bullet_grp.add(
                                        Bullet("normal", x_pos_for_each_bullet)
                                    )
                                    x_pos_for_each_bullet += 50

                                self.bullet_type = 1
                                self.start_cooldown = int(str(time.time()).split(".")[0])

                            # user chooses the first power-up (giant bullets)
                            elif event.key == pygame.K_2:
                                # _global.bullet_type = 2
                                self.game.mana_grp.empty()
                                selected_power_sprite = (
                                    self.game.list_of_power_ups.sprites()[1]
                                )
                                for sprite in self.game.list_of_power_ups.sprites():
                                    if sprite != selected_power_sprite:
                                        self.game.list_of_power_ups.remove(sprite)

                                self.bullet_type = 2
                                self.start_cooldown = int(str(time.time()).split(".")[0])
                                

                            # user chooses the first power-up (shield)
                            elif event.key == pygame.K_3:
                                selected_power_sprite = (
                                    self.game.list_of_power_ups.sprites()[2]
                                )
                                for sprite in self.game.list_of_power_ups.sprites():
                                    if sprite != selected_power_sprite:
                                        self.game.list_of_power_ups.remove(sprite)

                                self.shield_activation = True
                                self.start_cooldown = int(str(time.time()).split(".")[0])
                            

                            # user chooses the first power-up (kill all enemies, this depends on user's ability)
                            elif event.key == pygame.K_4:
                                if self.ability_to_kill_all:
                                    selected_power_sprite = (
                                        self.game.list_of_power_ups.sprites()[3]
                                    )
                                    for sprite in self.game.list_of_power_ups.sprites():
                                        if sprite != selected_power_sprite:
                                            self.game.list_of_power_ups.remove(sprite)

                                    self.game.enemy_grp.empty()
                                    self.game.list_of_power_ups.empty()
                                    self.seconds_per_timer = 1700


                            self.sound_player.activate.play()
                            self.game.x_pos_for_each_power_up_in_list = 200
                            self.killed_an_enemy = False
                            self.max_mana_reach = False
                            self.activated_power = True
                            self.wait_for_user_activation = False
                            self.game.mana_grp.empty()
                        

                if event.type == self.enemy_timer:
                    self.game.enemy_grp.add(
                        Enemy(
                            choice(
                                [
                                    "normal",
                                    "normal",
                                    "normal",
                                    "normal",
                                    "big",
                                    "mega",
                                    "normal",
                                    "normal",
                                    "big",
                                    "normal",
                                    "normal",
                                ]
                            ),
                            self.game,
                            self,
                        )
                    )

                if event.type == self.health_timer:
                    if len(self.game.health_cells_grp) < 5:
                        self.game.health_items.add(Health_Item())

                if event.type == self.spawn_timer:
                    self.seconds_per_timer -= 50
                    self.enemy_timer = pygame.USEREVENT + 2
                    pygame.time.set_timer(self.enemy_timer, self.seconds_per_timer)

    def collision(self) -> None:
        """
        This functions checks for 4 collision events:
        - If an enemy touches a bullet
        - If an enemy touches the player
        - If an enemy touches player's shield
        - If the player gets a health item
        """
        for ene_sprite in self.game.enemy_grp.sprites():
            # If an enemy touches player's shield
            try:
                if ene_sprite.rect.colliderect(self.shield_rect_on_player):
                    ene_sprite.kill()
            except TypeError:
                pass

            # If the player touches an enemy
            if (
                ene_sprite.rect.colliderect(self.game.player_grp.sprite.rect)
                or ene_sprite.rect.y > 605
            ):
                self.lost_1_health = True

                # remove the enemy sprite
                ene_sprite.kill()

                # remove one health cell (loses 1 health cell)
                self.game.health_cells_grp.sprites()[-1].kill()
                try:
                    self.game.health_top_left_x_pos = (
                        self.game.health_cells_grp.sprites()[-1].rect.x + 60
                    )
                except IndexError:
                    # index error with health_cells_grp (this is due to empty list)
                    return

        # if the enemy touches a bullet
        for bullet_sprite in self.game.bullet_grp.sprites():
            for ene_sprite in self.game.enemy_grp.sprites():
                if (
                    bullet_sprite.rect.colliderect(ene_sprite.rect)
                    or ene_sprite.rect.top > 595
                ):
                    bullet_sprite.kill()
                    self.if_an_enemy_touches_a_bullet = True

        # if the player gets the health item
        for health_item in self.game.health_items.sprites():
            if health_item.rect.colliderect(self.game.player_grp.sprite.rect):
                if len(self.game.health_cells_grp) == 5:
                    return

                SoundPlayer().heal.play()
                self.game.health_cells_grp.add(
                    Rect(
                        self.game.health_top_left_x_pos,
                        580,
                        "health_cell",
                        self,
                        60,
                        15,
                    )
                )
                self.player_heals = True
                health_item.kill()

    def player_events(self) -> None:
        """
        Tracks the player's events (reaching full energy, losing 1 health cell, power-up activation...).
        This function doesn't include collision events
        """
        # If the player hits an enemy and loses 1 health cell
        if self.lost_1_health:
            # if the player dies
            if len(self.game.health_cells_grp) == 0:
                self.game.over, self.game.started = True, False
                self.game.refresh(self)
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
                    self.game.list_of_power_ups.add(
                        Rect(
                            self.game.x_pos_for_each_power_up_in_list,
                            13,
                            "powers",
                            self,
                            40,
                            40,
                        )
                    )
                    # powers_grp.add(Rect(x_pos_for_power_rects, 13, 'powers', 40, 40))
                    self.game.x_pos_for_each_power_up_in_list += 100

        # if user reaches the maximum amount of energy
        if len(self.game.mana_grp) == 10:
            self.wait_for_user_activation = True

        # If an enemy is killed by the player, then add 1 energy cell for the player
        if self.killed_an_enemy:
            # if the energy bar is not full yet
            if len(self.game.mana_grp) < 10:
                mana_surf = Rect(
                    self.mana_rect_x_pos + (len(self.game.mana_grp) * 30),
                    560,
                    "energy",
                    self,
                    30,
                    15,
                )
                self.game.mana_grp.add(mana_surf)
                self.mana_color_index = len(self.game.mana_grp) - 1
                self.killed_an_enemy = False
            else:
                self.max_mana_reach = True

        # check if the player is able to use "kill all" power
        if (
            self.game.game_score % 30 in [0, 1]
            and self.game.game_score != 0
            and self.game.game_score >= 20
        ):
            self.ability_to_kill_all = True

        # if the player uses shield power-up
        if self.shield_activation:
            # Shows the selected power-up
            self.game.screen.blit(self.shield_surf, self.shield_rect)

            # Displays the shield on the player
            self.shield_surf_on_player = pygame.transform.scale(
                pygame.image.load(
                    "Images/Power-ups/blue_shield_icon.png"
                ).convert_alpha(),
                (130, 130),
            )
            self.shield_surf_on_player.set_alpha(70)
            self.shield_rect_on_player = self.shield_surf_on_player.get_rect(
                center=self.game.player_grp.sprite.rect.center
            )
            self.game.screen.blit(
                self.shield_surf_on_player, self.shield_rect_on_player
            )

    def bullet_events(self) -> None:
        # if the bullet_type is not the original one
        if self.bullet_type != 0:
            # if the player uses the first power-up (multiple bullets)
            if self.bullet_type == 1:
                self.game.screen.blit(
                    self.triple_bullets_surf, self.triple_bullets_rect
                )
            # the second power-up (big bullets)
            elif self.bullet_type == 2:
                self.game.screen.blit(self.big_bullets_surf, self.big_bullets_rect)

    def __repr__(self) -> str:
        return "Event Object"
