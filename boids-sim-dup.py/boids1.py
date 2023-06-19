import pygame
import random
import math
import numpy as np

# Parameters
WIDTH, HEIGHT = 800, 600
N = 50
SPEED = 3

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids Simulation")
clock = pygame.time.Clock()

# Boid class
class Boid:
    def __init__(self):
        self.position = np.array([random.uniform(0, WIDTH), random.uniform(0, HEIGHT)])
        self.velocity = np.array([random.uniform(-1, 1), random.uniform(-1, 1)]) * SPEED

    def rule1(self, boids):
        pcJ = np.array([0.0, 0.0])
        for b in boids:
            if b != self:
                pcJ += b.position
        pcJ /= (N-1)
        return (pcJ - self.position) / 100

    def rule2(self, boids):
        c = np.array([0.0, 0.0])
        for b in boids:
            if b != self:
                if np.linalg.norm(b.position - self.position) < 100:
                    c -= (b.position - self.position)
        return c

    def rule3(self, boids):
        pvJ = np.array([0.0, 0.0])
        for b in boids:
            if b != self:
                pvJ += b.velocity
        pvJ /= (N-1)
        return (pvJ - self.velocity) / 8

    def move(self, boids):
        v1 = self.rule1(boids)
        v2 = self.rule2(boids)
        v3 = self.rule3(boids)
        self.velocity += v1 + v2 + v3
        self.position += self.velocity

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position[0]), int(self.position[1])), 5)

# Initialize boids
boids = [Boid() for _ in range(N)]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Move boids
    for boid in boids:
        boid.move(boids)
        boid.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
