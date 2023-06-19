import pygame
import random
import numpy as np

# Parameters
WIDTH, HEIGHT = 800, 600
N = 50
SPEED = .025

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids Simulation")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74) # Font size 74

# Boid class
class Boid:
    def __init__(self):
        self.position = np.array([random.uniform(0, WIDTH), random.uniform(0, HEIGHT)])
        self.velocity = np.array([random.uniform(-1, 1), random.uniform(-1, 1)]) * SPEED

    # rule1: Boids try to fly towards the centre of mass of neighbouring boids.
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
                if np.linalg.norm(b.position - self.position) < 10:
                    c -= (b.position - self.position)
        return c

    # rule3 is the same as rule1, but with velocity instead of position
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

        # Bouncing off boundaries
        if self.position[0] < 0 or self.position[0] > WIDTH:
            self.velocity[0] = -self.velocity[0]
        if self.position[1] < 0 or self.position[1] > HEIGHT:
            self.velocity[1] = -self.velocity[1]

    def draw(self):
        angle = np.arctan2(self.velocity[1], self.velocity[0])
        points = [
            (
                self.position[0] + 10 * np.cos(angle),
                self.position[1] + 10 * np.sin(angle)
            ),
            (
                self.position[0] + 10 * np.cos(angle + 2.5),
                self.position[1] + 10 * np.sin(angle + 2.5)
            ),
            (
                self.position[0] + 10 * np.cos(angle - 2.5),
                self.position[1] + 10 * np.sin(angle - 2.5)
            ),
        ]
        pygame.draw.polygon(screen, (255, 255, 255), points)

# Initialize boids
boids = [Boid() for _ in range(N)]

# Initialize boids
boids = [Boid() for _ in range(N)]

# Main loop
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused # Toggle paused state
    
    screen.fill((0, 0, 0))

    # Always draw boids, regardless of paused state
    for boid in boids:
        boid.draw()

    # Only move boids if not paused
    if not paused:
        for boid in boids:
            boid.move(boids)
    else:
        # Draw red overlay with "STOPPED" text if paused
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((255, 0, 0))
        overlay.set_alpha(128) # Setting opacity to 128 (range 0 to 255)
        screen.blit(overlay, (0, 0))
        text = font.render("STOPPED", 1, (255, 255, 255))
        text_pos = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text, text_pos)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
