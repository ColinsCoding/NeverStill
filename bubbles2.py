import pygame
import sys
from math import sqrt

# define some constants
WIDTH, HEIGHT = 800, 600
BUBBLE_RADIUS = 50
FPS = 60
EXPANSION_SPEED = 1  # speed of bubble expansion

# define a bubble class
class Bubble:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BUBBLE_RADIUS
        self.expanding = False

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.radius, 1)

    def expand(self):
        if self.expanding:
            self.radius += EXPANSION_SPEED


def get_intersection_points(b1, b2):
    d = sqrt((b2.x - b1.x) ** 2 + (b2.y - b1.y) ** 2)
    
    if d > b1.radius + b2.radius:  # circles are separate
        return []
    if d < abs(b1.radius - b2.radius):  # one circle is contained within the other
        return []
    if d == 0 and b1.radius == b2.radius:  # circles coincide
        return []
    
    a = (b1.radius ** 2 - b2.radius ** 2 + d ** 2) / (2 * d)
    h = sqrt(b1.radius ** 2 - a ** 2)
    x2 = b1.x + a * (b2.x - b1.x) / d
    y2 = b1.y + a * (b2.y - b1.y) / d
    rx = -(b2.y - b1.y) * (h / d)
    ry = -(b2.x - b1.x) * (h / d)
    
    return [(x2 + rx, y2 - ry), (x2 - rx, y2 + ry)]


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
            # check if click on any bubble
            for bubble in bubbles:
                if (bubble.x - x)**2 + (bubble.y - y)**2 <= bubble.radius**2:
                    bubble.expanding = True
                    break
            else:
                bubbles.append(Bubble(x, y))
        elif event.type == pygame.MOUSEBUTTONUP:
            # stop expansion on mouse release
            for bubble in bubbles:
                bubble.expanding = False

        # drawing
    screen.fill((0, 0, 0))
    for bubble in bubbles:
        bubble.expand()
        bubble.draw(screen)
    
    # check for intersections
    for i in range(len(bubbles)):
        for j in range(i+1, len(bubbles)):
            points = get_intersection_points(bubbles[i], bubbles[j])
            if len(points) == 2:
                pygame.draw.line(screen, (255, 255, 255), points[0], points[1], 1)

    # flip the display
    pygame.display.flip()

    # cap the frame rate
    clock.tick(FPS)
