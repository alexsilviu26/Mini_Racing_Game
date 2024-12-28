import pygame

def scale(image, scale_factor):
    size = image.get_width() * scale_factor, image.get_height() * scale_factor    
    return pygame.transform.scale(image, size)

def blit_rotate(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)

