import pygame

def show_info(info, y_pos = 10, x_pos = 10):
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)
    info_text_surf = font.render(str(info), True, 'White')
    screen.blit(info_text_surf, (x_pos, y_pos)) 


def show_cursor():
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)
    pos_list = [pos for pos in pygame.mouse.get_pos()]
    info_text_surf = font.render(f'x: {pos_list[0]} y: {pos_list[1]}', True, 'White')
    screen.blit(info_text_surf, (10, 50))
    
