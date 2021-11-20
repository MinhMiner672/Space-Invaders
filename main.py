import time
import debug
import pygame

import colors
from game import Game
from events import Events
from sprites import Button

collide_shield = False

pygame.init()

game = Game()
events_tracker = Events(game)
game.refresh(events_tracker)

start_screen_font = pygame.font.Font('Fonts/Plaguard-ZVnjx.otf', 50)

cubic_pixel_font = pygame.font.Font('Fonts/CubicPixel-lgEmy.otf', 70)
paused_title_surf = cubic_pixel_font.render('Game Paused', False, colors.CYAN)
paused_title_rect = paused_title_surf.get_rect(midtop=(400, 190))

start_screen_background = pygame.transform.scale(pygame.image.load('Images/Scenes/start_bg.jpg').convert(), (880, 620))
paused_screen_background = pygame.image.load('Images/Scenes/pause_bg.jpg').convert()

butts_font_path = 'Fonts/Plaguard-ZVnjx.otf'
glue_gun_font_path = 'Fonts/GlueGun-GW8Z.ttf'
start_button = Button(400, 280, 'start', 50, butts_font_path, colors.GREEN)
quit_button_when_not_stated = Button(400, 370, 'Quit', 40, butts_font_path, colors.WHITE)

resume_button = Button(400, 335, 'Resume', 55, glue_gun_font_path, colors.WHITE)
quit_button_when_paused = Button(400, 420, 'Quit', 55, glue_gun_font_path, colors.WHITE)
# Retry button
retry_font = pygame.font.Font('Fonts/GlueGun-GW8Z.ttf', 55)
retry_text_surf = retry_font.render('Retry', False, (255, 255, 255))
retry_text_rect = retry_text_surf.get_rect(midtop=(290, 330))

# Menu button
menu_font = pygame.font.Font('Fonts/GlueGun-GW8Z.ttf', 55)
menu_text_surf = menu_font.render('Menu', False, (255, 255, 255))
menu_text_rect = menu_text_surf.get_rect(midtop=(520, 330))

# Energy Bar Rectangles
mana_rect_x_pos = 497

# GAME LOOP
running = True
while running:
    # Track all events
    events_tracker.keyboard_inputs()

    # If the game has started
    if game.started and not game.paused:
        game.show_background()
        game.display_score()
        game.style_health_bar(events_tracker)

        # Draw, update the player
        game.player_grp.draw(game.screen)
        game.player_grp.update()

        # Draw, update the bullet
        game.bullet_grp.draw(game.screen)
        game.bullet_grp.update()

        # Draw, update the falling health item
        game.health_items.draw(game.screen)
        game.health_items.update()

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

                game.list_of_power_ups.empty()

        # Draw 2 bars (health and energy)
        pygame.draw.rect(game.screen, colors.SILVER, (494, 577, 303, 20), 4)
        pygame.draw.rect(game.screen, colors.SILVER, (494, 557, 303, 20), 4)

        # Draw and update (bounce, check if there's collision) the enemy surfaces, rects
        game.enemy_grp.draw(game.screen)
        game.enemy_grp.update()

        events_tracker.collision()

        # Draw, update the health bar
        game.health_cells_grp.draw(game.screen)
        game.health_cells_grp.update()

        # Draw, update the power-up group
        game.list_of_power_ups.draw(game.screen)
        game.list_of_power_ups.update()

        events_tracker.player_events()

        # If the energy bar is full (10 kills / 1 max energy)
        if events_tracker.max_mana_reach:
            events_tracker.game.screen.blit(events_tracker.triple_bullets_surf, events_tracker.triple_bullets_rect)
            events_tracker.game.screen.blit(events_tracker.big_bullets_surf, events_tracker.big_bullets_rect)
            events_tracker.game.screen.blit(events_tracker.shield_surf, events_tracker.shield_rect)
            events_tracker.game.screen.blit(events_tracker.die_img_surf, events_tracker.die_rect)
            if not events_tracker.ability_to_kill_all:
                events_tracker.game.screen.blit(events_tracker.cross_surf, events_tracker.cross_rect)

        events_tracker.bullet_events()

        # Draw, update energy sprites
        game.mana_grp.draw(game.screen)
        game.mana_grp.update()

    # if the game is paused
    elif game.started and game.paused:
        game.screen.blit(paused_screen_background, (0, 0))

        game.screen.blit(paused_title_surf, paused_title_rect)
        game.screen.blit(resume_button.image, resume_button.rect)
        if resume_button.on_hover():
            resume_button.font = pygame.font.Font(resume_button.font_path, resume_button.font_size + 10)
            resume_button.image = resume_button.font.render(resume_button.text, False, resume_button.color)
            resume_button.rect = resume_button.image.get_rect(midtop=(resume_button.x, resume_button.y - 5))
            if resume_button.on_click():
                game.paused = False
        else:
            resume_button = Button(400, 335, 'Resume', 55, glue_gun_font_path, colors.WHITE)

        game.screen.blit(quit_button_when_paused.image, quit_button_when_paused.rect)
        if quit_button_when_paused.on_hover():
            quit_button_when_paused.font = pygame.font.Font(quit_button_when_paused.font_path, quit_button_when_paused.font_size + 10)
            quit_button_when_paused.image = quit_button_when_paused.font.render(quit_button_when_paused.text, False, quit_button_when_paused.color)
            quit_button_when_paused.rect = quit_button_when_paused.image.get_rect(midtop=(quit_button_when_paused.x, quit_button_when_paused.y - 5))
            if quit_button_when_paused.on_click():
                running = False
        else:
            quit_button_when_paused = Button(400, 420, 'Quit', 55, glue_gun_font_path, colors.WHITE)

    # Else if the game has not started
    elif not game.started and not game.paused:
        # If the game is not over
        if not game.over:
            game.screen.blit(start_screen_background, (0, 0))

            # Shows the 'start' button
            game.screen.blit(start_button.image, start_button.rect)
            if start_button.on_hover():
                start_button.font = pygame.font.Font(start_button.font_path, start_button.font_size + 10)
                start_button.image = start_button.font.render(start_button.text, False, start_button.color)
                start_button.rect = start_button.image.get_rect(midtop=(start_button.x, start_button.y - 5))
                if start_button.on_click():
                    game.started = True
            else:
                start_button = Button(400, 280, 'start', 50, butts_font_path, colors.GREEN)

            # Shows the 'quit' button
            game.screen.blit(quit_button_when_not_stated.image, quit_button_when_not_stated.rect)
            if quit_button_when_not_stated.on_hover():
                quit_button_when_not_stated.font = pygame.font.Font(quit_button_when_not_stated.font_path, quit_button_when_not_stated.font_size + 10)
                quit_button_when_not_stated.image = quit_button_when_not_stated.font.render(quit_button_when_not_stated.text, False, quit_button_when_not_stated.color)
                quit_button_when_not_stated.rect = quit_button_when_not_stated.image.get_rect(midtop=(quit_button_when_not_stated.x, quit_button_when_not_stated.y - 5))
                if quit_button_when_not_stated.on_click():
                    running = False
            else:
                quit_button_when_not_stated = Button(400, 370, 'Quit', 40, 'Fonts/Plaguard-ZVnjx.otf', (255, 255, 255))

        # if player loses the game
        else:
            # screen.fill(colors.BLACK)
            game.screen.blit(
                pygame.transform.rotozoom(pygame.image.load('Images/Scenes/over_bg.jpg').convert(), 0, 4.0), (0, 0))

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
