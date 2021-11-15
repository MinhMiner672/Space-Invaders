import time
from random import choice
from sys import exit

import _debug
import pygame

import _global
import colors
from sprites import SpaceShip, Bullet, Enemy, Rect, Health_Item

collide_shield = False


def collision_check():
    for bullet_sprite in bullet_grp.sprites():
        for ene_sprite in enemy_grp.sprites():
            if bullet_sprite.rect.colliderect(ene_sprite.rect) or ene_sprite.rect.top > 595:
                bullet_sprite.kill()
                _global.collision = True

    for health_item in health_grp.sprites():
        if health_item.rect.colliderect(player_grp.sprites()[0].rect):
            health_rects.add(Rect(health_rect_x_pos, 580, 60, 15, 'health'))
            _global.player_heals = True
            health_item.kill()

    if shield_rect_on_player is None:
        return
    else:
        for ene_sprite in enemy_grp.sprites():
            if ene_sprite.rect.colliderect(shield_rect_on_player):
                ene_sprite.kill()


def check_if_lose_health(x_pos_of_the_last_health_cell):
    for ene_sprite in enemy_grp.sprites():
        if ene_sprite.rect.colliderect(player_grp.sprite.rect):
            _global.lost_1_health = True
            ene_sprite.kill()
            health_rects.sprites()[-1].kill()
            return health_rects.sprites()[-1].rect.x + 60

    return x_pos_of_the_last_health_cell


def display_score():
    text_score_surf = space_font.render(f'Score: {_global.glb_score}', False, (194, 255, 212))
    score_text_rect = text_score_surf.get_rect(topleft=(20, 540))
    screen.blit(text_score_surf, score_text_rect)


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()
background = pygame.image.load('Images/bg.jpg').convert()
space_font = pygame.font.Font('big_space.ttf', 40)
start_screen_font = pygame.font.Font('Plaguard-ZVnjx.otf', 50)

start_screen_img = pygame.transform.scale(pygame.image.load('Images/start_bg.jpg').convert_alpha(), (880, 620))
start_screen_text_surf = start_screen_font.render('Start', True, colors.GREEN)
start_screen_text_rect = start_screen_text_surf.get_rect(topleft=(330, 300))
topleft_pos = 205
# Import power images
triple_bullets_surf = pygame.transform.scale(pygame.image.load('Images/Bullets/triple_bullets.jpg').convert_alpha(),
                                             (30, 30))
triple_bullets_rect = triple_bullets_surf.get_rect(topleft=(topleft_pos * 1, 18))

big_bullets_surf = pygame.transform.scale(pygame.image.load('Images/Bullets/bullet.png').convert_alpha(), (30, 30))
big_bullets_rect = big_bullets_surf.get_rect(topleft=(topleft_pos + 100, 18))

shield_surf = pygame.transform.scale(pygame.image.load('Images/blue_shield.png').convert_alpha(), (30, 30))
shield_rect = shield_surf.get_rect(topleft=(topleft_pos + 200, 18))

die_img = pygame.transform.scale(pygame.image.load('Images/die.png').convert_alpha(), (30, 30))
die_rect = die_img.get_rect(topleft=(topleft_pos + 300, 18))

cross_surf = pygame.transform.scale(pygame.image.load('Images/cross_mark.png').convert_alpha(), (50, 50))
cross_rect = cross_surf.get_rect(topleft=(495, 6))

shield_rect_on_player = None

# Creating bullet
bullet_grp = pygame.sprite.Group()
bullet_y_pos = 508

# Create player sprite group
player_grp = pygame.sprite.GroupSingle(SpaceShip())

# Enemies
enemy_grp = pygame.sprite.Group()

# Timer for gradually fast enemy spawning
spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, 5000)

# Timer for enemy addition
seconds_per_timer = 1700
enemy_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_timer, seconds_per_timer)

# Health Item Timer
health_grp = pygame.sprite.Group()
health_timer = pygame.USEREVENT + 1
pygame.time.set_timer(health_timer, 10000)

# Health Bar Rectangles
health_rects = pygame.sprite.Group()
health_rect_x_pos = 497

for i in range(5):
    # size:
    health_rects.add(Rect(health_rect_x_pos, 580, 60, 15, 'health'))
    health_rect_x_pos += 60

health_rect_x_pos -= 60
# health_rect_x_pos = health_rect_x_pos - 60
# Energy Bar Rectangles
mana_rect_x_pos = 497
mana_grp = pygame.sprite.Group()

# Powers Rects Group
powers_grp = pygame.sprite.Group()

# GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if _global.game_start:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if _global.glb_score % 10 == 0 and _global.glb_score != 0:
                        _global.wait_for_user_activation = True

                    if _global.bullet_type == 1:
                        x_pos_for_each_bullet = (player_grp.sprite.rect.x + 29) - 50
                        for i in range(3):
                            bullet_grp.add(Bullet('normal', x_pos_for_each_bullet))
                            x_pos_for_each_bullet += 50

                    elif _global.bullet_type == 2:
                        bullet_grp.add(Bullet('bigger', player_grp.sprite.rect.x + 30))

                    else:
                        bullet_grp.add(Bullet('normal', player_grp.sprite.rect.x + 29))

            if _global.wait_for_user_activation:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        if _global.bullet_type == 0:
                            mana_grp.empty()
                            for sprite in powers_grp.sprites():
                                if powers_grp.sprites().index(sprite) == 0:
                                    continue
                                powers_grp.remove(sprite)

                            x_pos_for_each_bullet = (player_grp.sprite.rect.x + 29) - 50
                            for i in range(3):
                                bullet_grp.add(Bullet('normal', x_pos_for_each_bullet))
                                x_pos_for_each_bullet += 50

                            _global.max_mana_reach = False
                            _global.bullet_type = 1
                            _global.killed_an_enemy = False

                            _global.start_cooldown = int(str(time.time()).split('.')[0])
                            _global.activated_power = True

                    elif event.key == pygame.K_2:
                        if _global.bullet_type == 0:
                            _global.bullet_type = 2
                            mana_grp.empty()
                            selected_power_sprite = powers_grp.sprites()[1]
                            for sprite in powers_grp.sprites():
                                if sprite != selected_power_sprite:
                                    powers_grp.remove(sprite)

                            bullet_grp.empty()
                            _global.killed_an_enemy = False
                            _global.max_mana_reach = False
                            _global.start_cooldown = int(str(time.time()).split('.')[0])
                            _global.activated_power = True

                    elif event.key == pygame.K_3:
                        selected_power_sprite = powers_grp.sprites()[2]

                        for sprite in powers_grp.sprites():
                            if sprite != selected_power_sprite:
                                powers_grp.remove(sprite)

                        _global.shield_activation = True
                        _global.killed_an_enemy = False
                        _global.max_mana_reach = False
                        _global.activated_power = True
                        _global.start_cooldown = int(str(time.time()).split('.')[0])
                        mana_grp.empty()

                    elif event.key == pygame.K_4:
                        if _global.able_to_kill_all:
                            selected_power_sprite = powers_grp.sprites()[3]
                            for sprite in powers_grp.sprites():
                                if sprite != selected_power_sprite:
                                    powers_grp.remove(sprite)

                            _global.killed_an_enemy = False
                            _global.max_mana_reach = False
                            _global.activated_power = True

                            enemy_grp.empty()
                            powers_grp.empty()
                            mana_grp.empty()

            if event.type == enemy_timer:
                enemy_grp.add(Enemy(choice(
                    ['normal', 'normal', 'normal', 'normal', 'big', 'mega', 'normal', 'normal', 'big', 'normal',
                     'normal'])))

            if event.type == health_timer:
                if len(health_rects) < 5:
                    health_grp.add(Health_Item())

            if event.type == spawn_timer:
                seconds_per_timer -= 50
                enemy_timer = pygame.USEREVENT + 2
                pygame.time.set_timer(enemy_timer, seconds_per_timer)

    if _global.game_start:
        screen.blit(background, (0, 0))

        if _global.lost_1_health:
            if len(health_rects) == 0:
                pygame.quit()
                exit()
            _global.lost_1_health = False
            # health_rects.sprites()[-1].kill()
            # _global.lost_1_health = False

        if 1 < len(health_rects) < 4:
            _global.rect_health_color = colors.YELLOW
        elif len(health_rects) == 1:
            _global.rect_health_color = colors.RED
        elif len(health_rects) >= 4:
            _global.rect_health_color = colors.GREEN

        display_score()

        # Draw the player
        player_grp.draw(screen)
        player_grp.update()

        # Draw the bullet
        bullet_grp.draw(screen)
        bullet_grp.update()

        # Show the shield
        if _global.shield_activation:
            shield_surf_on_player = pygame.transform.scale(pygame.image.load('Images/blue_shield.png').convert_alpha(),
                                                           (130, 130))
            shield_surf_on_player.set_alpha(70)
            shield_rect_on_player = shield_surf_on_player.get_rect(center=player_grp.sprite.rect.center)
            screen.blit(shield_surf_on_player, shield_rect_on_player)

        # shield_rect_on_player = 'var'
        collision_check()
        if _global.player_heals:
            health_rect_x_pos += 60
            _global.player_heals = False
        health_rect_x_pos = check_if_lose_health(health_rect_x_pos)

        # Declare 2 variables, one indicates the seconds of the start cooldown time
        if _global.bullet_type != 0 or _global.shield_activation:

            cooldown_start = _global.start_cooldown

            current_time = int(str(time.time()).split('.')[0])

            # If the interval between 'current_time' and 'cooldown_start' is equal to 5 seconds (the mega bullet
            # cooldown expires)
            delta = current_time - cooldown_start
            if delta == 7:
                if _global.bullet_type != 0:
                    _global.bullet_type = 0

                if _global.shield_activation:
                    _global.shield_activation = False

                _global.activated_power = False
                _global.able_to_kill_all = False if _global.able_to_kill_all else True
                _global.start_cooldown = 0
                bullet_grp.empty()
                powers_grp.empty()

        # Draw 2 bars (health and energy)
        pygame.draw.rect(screen, colors.SILVER, (494, 577, 303, 20), 4)
        pygame.draw.rect(screen, colors.SILVER, (494, 557, 303, 20), 4)

        # Draw and update (bounce, check if there's collision) the enemy surfaces, rects
        enemy_grp.draw(screen)
        enemy_grp.update()

        health_grp.draw(screen)
        health_grp.update()

        # Draw, update the health bar
        health_rects.draw(screen)
        health_rects.update()

        # If the energy bar is full (10 kills / 1 max energy)
        if _global.max_mana_reach:
            if len(powers_grp) < 4:
                x_pos_for_power_rects = 200
                for i in range(4):
                    powers_grp.add(Rect(x_pos_for_power_rects, 13, 40, 40, 'powers'))
                    x_pos_for_power_rects += 100

        # If an enemy is killed by the player, then add 1 energy cell for the player
        if _global.killed_an_enemy:
            if len(mana_grp) < 10:
                mana_surf = Rect(mana_rect_x_pos + (len(mana_grp) * 30), 560, 30, 15, 'energy')
                mana_grp.add(mana_surf)
                _global.mana_color_index = len(mana_grp) - 1
                _global.killed_an_enemy = False
            else:
                _global.max_mana_reach = True

        if _global.glb_score % 30 in [0, 1] and _global.glb_score != 0 and _global.glb_score >= 20:
            _global.able_to_kill_all = True

        powers_grp.draw(screen)
        powers_grp.update()

        if _global.max_mana_reach:
            screen.blit(triple_bullets_surf, triple_bullets_rect)
            screen.blit(big_bullets_surf, big_bullets_rect)
            screen.blit(shield_surf, shield_rect)
            screen.blit(die_img, die_rect)

            if not _global.able_to_kill_all:
                screen.blit(cross_surf, cross_rect)

        if _global.bullet_type != 0:
            if _global.bullet_type == 1:
                screen.blit(triple_bullets_surf, triple_bullets_rect)
            elif _global.bullet_type == 2:
                screen.blit(big_bullets_surf, big_bullets_rect)

        if _global.shield_activation:
            screen.blit(shield_surf, shield_rect)

        mana_grp.draw(screen)
        mana_grp.update()

    else:
        screen.blit(start_screen_img, (0, 0))
        if start_screen_text_rect.collidepoint(pygame.mouse.get_pos()):
            start_screen_font = pygame.font.Font('Plaguard-ZVnjx.otf', 60)
            start_screen_text_surf = start_screen_font.render('Start', True, colors.GREEN)
            start_screen_text_rect = start_screen_text_surf.get_rect(topleft=(315, 295))
            if pygame.mouse.get_pressed()[0] and start_screen_text_rect.collidepoint(pygame.mouse.get_pos()):
                _global.game_start = True

        else:
            start_screen_font = pygame.font.Font('Plaguard-ZVnjx.otf', 50)

            start_screen_img = pygame.transform.scale(pygame.image.load('Images/start_bg.jpg').convert_alpha(),
                                                      (880, 620))
            start_screen_text_surf = start_screen_font.render('Start', True, colors.GREEN)
            start_screen_text_rect = start_screen_text_surf.get_rect(topleft=(330, 300))

        screen.blit(start_screen_text_surf, start_screen_text_rect)

    # Always update a portion of the screen, and control the FPS
    pygame.display.update()
    clock.tick(60)
