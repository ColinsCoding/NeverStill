import pygame
import sys

# define some constants
WIDTH, HEIGHT = 800, 600
BUBBLE_RADIUS = 50
FPS = 60

# define a bubble class
class Bubble:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BUBBLE_RADIUS

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.radius, 1)

# initialize pygame
pygame.init()

# set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set up the clock
clock = pygame.time.Clock()

# set up the bubbles
bubbles = []

# main loop
while True:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            bubbles.append(Bubble(x, y))

    # drawing
    screen.fill((0, 0, 0))
    for bubble in bubbles:
        bubble.draw(screen)

    # flip the display
    pygame.display.flip()

    # cap the frame rate
    clock.tick(FPS)
