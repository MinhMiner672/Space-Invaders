import pygame


def show_info(info: str, y_pos=10, x_pos=10) -> None:
    """
    Shows a piece of information onto the display surface
    This helps you to track the change of variables
    """
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)
    info_text_surf = font.render(str(info), True, (255, 255, 255))
    screen.blit(info_text_surf, (x_pos, y_pos)) 


def show_cursor() -> None:
    """Show the current position of the mouse cursor in real time"""
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)
    pos_list = [pos for pos in pygame.mouse.get_pos()]
    cursor_pos_surf = font.render(f'x: {pos_list[0]} y: {pos_list[1]}', True, (255, 255, 255))
    screen.blit(cursor_pos_surf, (10, 50))
    
