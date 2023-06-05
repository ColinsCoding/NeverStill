import pygame
import sys
import math

# define some constants
WIDTH, HEIGHT = 800, 600
BUBBLE_RADIUS = 50
FPS = 60
POINT_COUNT = 100

# define a bubble class
class Bubble:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BUBBLE_RADIUS
        self.points = [(math.cos(2*math.pi/POINT_COUNT*i)*self.radius+self.x, math.sin(2*math.pi/POINT_COUNT*i)*self.radius+self.y) for i in range(POINT_COUNT)]

    def draw(self, surface, bubbles):
        points_outside_other_bubbles = [p for p in self.points if not any((p[0]-b.x)**2 + (p[1]-b.y)**2 < b.radius**2 for b in bubbles if b != self)]
        if len(points_outside_other_bubbles) > 2:
            pygame.draw.polygon(surface, (0, 0, 0), points_outside_other_bubbles)
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
    screen.fill((255, 255, 255))
    for bubble in bubbles:
        bubble.draw(screen, bubbles)

    # flip the display
    pygame.display.flip()

    # cap the frame rate
    clock.tick(FPS)
