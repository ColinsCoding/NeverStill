import pygame
import numpy as np

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Scalar resource field dimensions
FIELD_WIDTH = 80
FIELD_HEIGHT = 60

# Time system
SECONDS_PER_TICK = 60
TICKS_PER_HOUR = 60
HOURS_PER_DAY = 24

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tree Growth Simulation")

# Tree class
class Tree:
    def __init__(self, position):
        self.position = position
        self.branches = []
        self.energy = 0

    def grow(self, energy_field):
        self.energy += energy_field[int(self.position[1]) // 10, int(self.position[0]) // 10]

        if not self.branches and self.energy > 5:
            self.branches.append(Tree(self.position + np.array([0, -10])))
            self.energy -= 5
        for branch in self.branches:
            branch.grow(energy_field)

    def draw(self, screen):
        if self.branches:
            for branch in self.branches:
                pygame.draw.line(screen, (0, 0, 0), self.position, branch.position)
                branch.draw(screen)

# List of trees
trees = []

# Energy field
energy_field = np.zeros((HEIGHT // 10, WIDTH // 10))

# Timer
timer = 0

# Main game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            trees.append(Tree(np.array(event.pos)))

    # Update the simulation (tree agents and resource field)
    if timer % (TICKS_PER_HOUR * 6) == 0:  # Every 6 hours
        sun_position = timer // (TICKS_PER_HOUR * 6) % 4
        if sun_position == 0:
            energy_field[:, :] = 1
        elif sun_position == 1:
            energy_field[:, :] = np.linspace(0, 1, WIDTH // 10)
        elif sun_position == 2:
            energy_field[:, :] = 0
        else:
            energy_field[:, :] = np.linspace(1, 0, WIDTH // 10)
        
        for tree in trees:
            tree.grow(energy_field)

    # Render the scene
    screen.fill((255, 255, 255))  # Clear the screen with a white background

    # Render the trees
    for tree in trees:
        tree.draw(screen)

    pygame.display.flip()  # Update the display

    # Increment timer
    timer += 1
    if timer >= TICKS_PER_HOUR * HOURS_PER_DAY:
        timer = 0

pygame.quit()
