import time
import pygame

import colors
from game import Game
from events import Events
from sprites import Button

from pygame import mixer
import debug

pygame.init()


game = Game()
events_tracker = Events(game)
game.refresh(events_tracker)


butts_font_path = "Fonts/Plaguard-ZVnjx.otf"
glue_gun_font_path = "Fonts/GlueGun-GW8Z.ttf"

start_screen_font = pygame.font.Font("Fonts/Plaguard-ZVnjx.otf", 50)
cubic_pixel_font = pygame.font.Font("Fonts/CubicPixel-lgEmy.otf", 70)

start_screen_background = pygame.transform.scale(
    pygame.image.load("Images/Scenes/start_bg.jpg").convert(), (880, 620)
)
paused_screen_background = pygame.image.load("Images/Scenes/pause_bg.jpg").convert()

# Some buttons
start_button = Button(400, 280, "start", 50, butts_font_path, colors.GREEN)
resume_button = Button(400, 335, "Resume", 55, glue_gun_font_path, colors.WHITE)
retry_button = Button(290, 330, "Retry", 55, "Fonts/GlueGun-GW8Z.ttf", colors.WHITE)
menu_button = Button(520, 330, "Menu", 55, "Fonts/GlueGun-GW8Z.ttf", colors.WHITE)

quit_button_when_not_stated = Button(
    400, 370, "Quit", 40, butts_font_path, colors.WHITE
)
quit_button_when_paused = Button(400, 420, "Quit", 55, glue_gun_font_path, colors.WHITE)

# Plays the background music
# mixer.init()
# mixer.music.load("./Sound/karlson_vibe.mp3")
# mixer.music.set_volume(0.2)
# mixer.music.play()

# GAME LOOP
running = True
while running:
    # Track all events
    events_tracker.keyboard_inputs()

    # If the game has started
    if game.started and not game.paused:

        # theme_sound.play(loops=-1)
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
            current_time = int(str(time.time()).split(".")[0])

            # If the interval between 'current_time' and 'cooldown_start' is equal to 5 seconds (the mega bullet
            # cooldown expires)
            delta = current_time - cooldown_start
            if delta == 7:
                if events_tracker.bullet_type != 0:
                    events_tracker.bullet_type = 0

                if events_tracker.shield_activation:
                    events_tracker.shield_activation = False

                events_tracker.activated_power = False
                events_tracker.ability_to_kill_all = (
                    False if events_tracker.ability_to_kill_all else True
                )
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
            events_tracker.game.screen.blit(
                events_tracker.triple_bullets_surf, events_tracker.triple_bullets_rect
            )
            events_tracker.game.screen.blit(
                events_tracker.big_bullets_surf, events_tracker.big_bullets_rect
            )
            events_tracker.game.screen.blit(
                events_tracker.shield_surf, events_tracker.shield_rect
            )
            events_tracker.game.screen.blit(
                events_tracker.die_img_surf, events_tracker.die_rect
            )
            if not events_tracker.ability_to_kill_all:
                events_tracker.game.screen.blit(
                    events_tracker.cross_surf, events_tracker.cross_rect
                )

        events_tracker.bullet_events()

        # Draw, update energy sprites
        game.mana_grp.draw(game.screen)
        game.mana_grp.update()

    # if the game is paused
    elif game.started and game.paused:
        mixer.music.pause()
        paused_title_surf = cubic_pixel_font.render("Game Paused", False, colors.CYAN)
        paused_title_rect = paused_title_surf.get_rect(midtop=(400, 190))

        game.screen.blit(paused_screen_background, (0, 0))

        game.screen.blit(paused_title_surf, paused_title_rect)
        game.screen.blit(resume_button.image, resume_button.rect)
        if resume_button.on_hover():
            resume_button.font = pygame.font.Font(
                resume_button.font_path, resume_button.font_size + 10
            )
            resume_button.image = resume_button.font.render(
                resume_button.text, False, resume_button.color
            )
            resume_button.rect = resume_button.image.get_rect(
                midtop=(resume_button.x, resume_button.y - 5)
            )
            if resume_button.on_click():
                mixer.music.unpause()
                game.paused = False
        else:
            resume_button = Button(
                400, 335, "Resume", 55, glue_gun_font_path, colors.WHITE
            )

        game.screen.blit(quit_button_when_paused.image, quit_button_when_paused.rect)
        if quit_button_when_paused.on_hover():
            quit_button_when_paused.font = pygame.font.Font(
                quit_button_when_paused.font_path,
                quit_button_when_paused.font_size + 10,
            )
            quit_button_when_paused.image = quit_button_when_paused.font.render(
                quit_button_when_paused.text, False, quit_button_when_paused.color
            )
            quit_button_when_paused.rect = quit_button_when_paused.image.get_rect(
                midtop=(quit_button_when_paused.x, quit_button_when_paused.y - 5)
            )
            if quit_button_when_paused.on_click():
                running = False
        else:
            quit_button_when_paused = Button(
                400, 420, "Quit", 55, glue_gun_font_path, colors.WHITE
            )

    # Else if the game has not started
    elif not game.started and not game.paused:
        # If the game is not over
        if not game.over:
            game.screen.blit(start_screen_background, (0, 0))

            # Shows the 'start' button
            game.screen.blit(start_button.image, start_button.rect)
            if start_button.on_hover():
                start_button.font = pygame.font.Font(
                    start_button.font_path, start_button.font_size + 10
                )
                start_button.image = start_button.font.render(
                    start_button.text, False, start_button.color
                )
                start_button.rect = start_button.image.get_rect(
                    midtop=(start_button.x, start_button.y - 5)
                )
                if start_button.on_click():
                    game.started = True
            else:
                start_button = Button(
                    400, 280, "start", 50, butts_font_path, colors.GREEN
                )

            # Shows the 'quit' button
            game.screen.blit(
                quit_button_when_not_stated.image, quit_button_when_not_stated.rect
            )
            if quit_button_when_not_stated.on_hover():
                quit_button_when_not_stated.font = pygame.font.Font(
                    quit_button_when_not_stated.font_path,
                    quit_button_when_not_stated.font_size + 10,
                )
                quit_button_when_not_stated.image = (
                    quit_button_when_not_stated.font.render(
                        quit_button_when_not_stated.text,
                        False,
                        quit_button_when_not_stated.color,
                    )
                )
                quit_button_when_not_stated.rect = (
                    quit_button_when_not_stated.image.get_rect(
                        midtop=(
                            quit_button_when_not_stated.x,
                            quit_button_when_not_stated.y - 5,
                        )
                    )
                )
                if quit_button_when_not_stated.on_click():
                    running = False
            else:
                quit_button_when_not_stated = Button(
                    400, 370, "Quit", 40, "Fonts/Plaguard-ZVnjx.otf", (255, 255, 255)
                )

        # if player loses the game
        else:
            # Set the seconds_per_timer back to 170, to avoid rapid enemy spawn_timer
            events_tracker.seconds_per_timer = 170

            # Game over background
            game.screen.blit(
                pygame.transform.rotozoom(
                    pygame.image.load("Images/Scenes/over_bg.jpg").convert(), 0, 4.0
                ),
                (0, 0),
            )

            # Game Over Text
            game_over_font = pygame.font.Font("Fonts/DebugFreeTrial-MVdYB.otf", 120)
            game_over_text_surf = game_over_font.render("Game Over", False, colors.RED)
            game_over_text_rect = game_over_text_surf.get_rect(midtop=(400, 160))
            game.screen.blit(game_over_text_surf, game_over_text_rect)

            # Retry button)
            game.screen.blit(retry_button.image, retry_button.rect)
            if retry_button.on_hover():
                retry_button.font = pygame.font.Font(
                    retry_button.font_path, retry_button.font_size + 10
                )
                retry_button.image = retry_button.font.render(
                    retry_button.text, False, retry_button.color
                )
                retry_button.rect = retry_button.image.get_rect(
                    midtop=(retry_button.x, retry_button.y - 5)
                )
                if retry_button.on_click():
                    game.refresh(events_tracker)
                    game.started = True
            else:
                retry_button = Button(
                    290, 330, "Retry", 55, "Fonts/GlueGun-GW8Z.ttf", colors.WHITE
                )

            # Menu button (text)
            game.screen.blit(menu_button.image, menu_button.rect)
            if menu_button.on_hover():
                menu_button.font = pygame.font.Font(
                    menu_button.font_path, menu_button.font_size + 10
                )
                menu_button.image = menu_button.font.render(
                    menu_button.text, False, menu_button.color
                )
                menu_button.rect = menu_button.image.get_rect(
                    midtop=(menu_button.x, menu_button.y - 5)
                )
                if menu_button.on_click():
                    game.refresh(events_tracker)
                    game.over = False
            else:
                menu_button = Button(
                    520, 330, "Menu", 55, "Fonts/GlueGun-GW8Z.ttf", colors.WHITE
                )
    # Always update a portion of the screen, and control the FPS
    game.control_fps()

pygame.quit()
