import pygame

# checkers board parameters
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
WHITE = (255, 255, 255)
YELLOW = (179, 135, 0)
BROWN = (63, 42, 20)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))