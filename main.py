import time

import _debug
import pygame

import _global
import colors
from sprites import Rect
from game import Game
from events import Events

collide_shield = False

pygame.init()

game = Game()
game.refresh()

events_tracker = Events(game)

start_screen_font = pygame.font.Font('Fonts/Plaguard-ZVnjx.otf', 50)

start_screen_img = pygame.transform.scale(pygame.image.load('Images/start_bg.jpg').convert_alpha(), (880, 620))
start_screen_text_surf = start_screen_font.render('Start', True, colors.GREEN)
start_screen_text_rect = start_screen_text_surf.get_rect(topleft=(330, 300))
topleft_pos = 205

game.screen.blit(start_screen_text_surf, start_screen_text_rect)

# Retry button
retry_font = pygame.font.Font('Fonts/GlueGun-GW8Z.ttf', 55)
retry_text_surf = retry_font.render('Retry', False, (255, 255, 255))
retry_text_rect = retry_text_surf.get_rect(midtop=(290, 330))

# Menu button
menu_font = pygame.font.Font('Fonts/GlueGun-GW8Z.ttf', 55)
menu_text_surf = menu_font.render('Menu', False, (255, 255, 255))
menu_text_rect = menu_text_surf.get_rect(midtop=(520, 330))

shield_rect_on_player = None

# Timer for gradually fast enemy spawning
spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, 3500)

# Timer for enemy addition
seconds_per_timer = 1700
enemy_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_timer, seconds_per_timer)

# Health Item Timer
health_timer = pygame.USEREVENT + 1
pygame.time.set_timer(health_timer, 10000)

# Energy Bar Rectangles
mana_rect_x_pos = 497

# GAME LOOP
running = True
while running:
    # Track all events
    events_tracker.key_board_inputs()

    if game.started:
        game.show_background()
        game.display_score()
        game.style_health_bar()

        events_tracker.player_events()

        # Draw, update the player
        game.player_grp.draw(game.screen)
        game.player_grp.update()

        # Draw, update the bullet
        game.bullet_grp.draw(game.screen)
        game.bullet_grp.update()

        # Draw, update the falling health item
        game.health_items.draw(game.screen)
        game.health_items.update()

        # Show the shield
        if events_tracker.shield_activation:
            shield_surf_on_player = pygame.transform.scale(pygame.image.load('Images/blue_shield.png').convert_alpha(), (130, 130))
            shield_surf_on_player.set_alpha(70)
            shield_rect_on_player = shield_surf_on_player.get_rect(center=game.player_grp.sprite.rect.center)
            game.screen.blit(shield_surf_on_player, shield_rect_on_player)

        # Declare 2 variables, one indicates the seconds of the start cooldown time
        if events_tracker.bullet_type != 0 or events_tracker.shield_activation:
            cooldown_start = events_tracker.start_cooldown
            current_time = int(str(time.time()).split('.')[0])

            # If the interval between 'current_time' and 'cooldown_start' is equal to 5 seconds (the mega bullet
            # cooldown expires)
            delta = current_time - cooldown_start
            if delta == 7:
                if events_tracker.bullet_type != 0:
                    events_tracker.bullet_type = 0

                if events_tracker.shield_activation:
                    events_tracker.shield_activation = False

                events_tracker.activated_power = False
                events_tracker.ability_to_kill_all = False if events_tracker.ability_to_kill_all else True
                events_tracker.start_cooldown = 0
                # bullet_grp.empty()
                game.list_of_power_ups.empty()

        # Draw 2 bars (health and energy)
        pygame.draw.rect(game.screen, colors.SILVER, (494, 577, 303, 20), 4)
        pygame.draw.rect(game.screen, colors.SILVER, (494, 557, 303, 20), 4)

        # Draw and update (bounce, check if there's collision) the enemy surfaces, rects
        game.enemy_grp.draw(game.screen)
        game.enemy_grp.update()

        events_tracker.collision(events_tracker.shield_rect)

        # Draw, update the health bar
        game.health_cells_grp.draw(game.screen)
        game.health_cells_grp.update()

        # Draw, update the power-up group
        game.list_of_power_ups.draw(game.screen)
        game.list_of_power_ups.update()

        _debug.show_info(str(len(game.mana_grp)))

        # If the energy bar is full (10 kills / 1 max energy)
        if events_tracker.max_mana_reach:
            events_tracker.game.screen.blit(events_tracker.triple_bullets_surf, events_tracker.triple_bullets_rect)
            events_tracker.game.screen.blit(events_tracker.big_bullets_surf, events_tracker.big_bullets_rect)
            events_tracker.game.screen.blit(events_tracker.shield_surf, events_tracker.shield_rect)
            events_tracker.game.screen.blit(events_tracker.die_img_surf, events_tracker.die_rect)
            if not events_tracker.ability_to_kill_all:
                events_tracker.game.screen.blit(events_tracker.cross_surf, events_tracker.cross_rect)

        # if the bullet_type is not the original one
        if events_tracker.bullet_type != 0:
            # if the player uses the first power-up (multiple bullets)
            if events_tracker.bullet_type == 1:
                game.screen.blit(events_tracker.triple_bullets_surf, events_tracker.triple_bullets_rect)
            # the second power-up (big bullets)
            elif events_tracker.bullet_type == 2:
                game.screen.blit(events_tracker.big_bullets_surf, events_tracker.big_bullets_rect)

        # if the player uses shield power-up
        if events_tracker.shield_activation:
            game.screen.blit(events_tracker.shield_surf, events_tracker.shield_rect)

        # draw, update energy sprites
        game.mana_grp.draw(game.screen)
        game.mana_grp.update()

    else:
        if not game.over:
            game.screen.blit(start_screen_img, (0, 0))

            # game.screen.blit(start_screen_text_surf, start_screen_text_rect)

            if start_screen_text_rect.collidepoint(pygame.mouse.get_pos()):
                start_screen_font = pygame.font.Font('Fonts/Plaguard-ZVnjx.otf', 60)
                start_screen_text_surf = start_screen_font.render('Start', True, colors.GREEN)
                start_screen_text_rect = start_screen_text_surf.get_rect(topleft=(315, 295))
                if pygame.mouse.get_pressed(num_buttons=3)[0] and start_screen_text_rect.collidepoint(pygame.mouse.get_pos()):
                    game.started = True

            else:
                start_screen_font = pygame.font.Font('Fonts/Plaguard-ZVnjx.otf', 50)

                start_screen_img = pygame.transform.scale(pygame.image.load('Images/start_bg.jpg').convert_alpha(),
                                                          (880, 620))
                start_screen_text_surf = start_screen_font.render('Start', True, colors.GREEN)
                start_screen_text_rect = start_screen_text_surf.get_rect(topleft=(330, 300))

            game.screen.blit(start_screen_text_surf, start_screen_text_rect)

        # if player loses the game
        else:
            # screen.fill(colors.BLACK)
            game.screen.blit(pygame.transform.rotozoom(pygame.image.load('Images/over_bg.jpg').convert(), 0, 4.0), (0, 0))

            # Game Over Text
            game_over_font = pygame.font.Font('Fonts/DebugFreeTrial-MVdYB.otf', 120)
            game_over_text_surf = game_over_font.render('Game Over', False, colors.RED)
            game_over_text_rect = game_over_text_surf.get_rect(midtop=(400, 160))
            game.screen.blit(game_over_text_surf, game_over_text_rect)

            # Retry button (text)
            game.screen.blit(retry_text_surf, retry_text_rect)
            if retry_text_rect.collidepoint(pygame.mouse.get_pos()):
                retry_font = pygame.font.Font('Fonts/GlueGun-GW8Z.ttf', 65)
                retry_text_surf = retry_font.render('Retry', False, (255, 255, 255))
                retry_text_rect = retry_text_surf.get_rect(midtop=(290, 325))
                # If the user clicks the RETRY button
                if pygame.mouse.get_pressed(num_buttons=3)[0] and retry_text_rect.collidepoint(pygame.mouse.get_pos()):
                    game.refresh()
                    game.over, game.started = False, True

            else:
                retry_font = pygame.font.Font('Fonts/GlueGun-GW8Z.ttf', 55)
                retry_text_surf = retry_font.render('Retry', False, (255, 255, 255))
                retry_text_rect = retry_text_surf.get_rect(midtop=(290, 330))

            # Menu button (text)
            game.screen.blit(menu_text_surf, menu_text_rect)
            if menu_text_rect.collidepoint(pygame.mouse.get_pos()):
                menu_font = pygame.font.Font('Fonts/GlueGun-GW8Z.ttf', 65)
                menu_text_surf = menu_font.render('Menu', False, (255, 255, 255))
                menu_text_rect = menu_text_surf.get_rect(midtop=(520, 325))
                # If the user clicks the MENu button
                if pygame.mouse.get_pressed(num_buttons=3)[0] and menu_text_rect.collidepoint(pygame.mouse.get_pos()):
                    game.over = False

            else:
                menu_font = pygame.font.Font('Fonts/GlueGun-GW8Z.ttf', 55)
                menu_text_surf = menu_font.render('Menu', False, (255, 255, 255))
                menu_text_rect = menu_text_surf.get_rect(midtop=(520, 330))

    # Always update a portion of the screen, and control the FPS
    game.control_fps()

pygame.quit()
