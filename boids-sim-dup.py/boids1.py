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

    def limit_velocity(self, max_speed):
        magnitude = np.linalg.norm(self.velocity)
        if magnitude > max_speed:
            self.velocity = (self.velocity / magnitude) * max_speed

    def rule1(self, boids, mouse_pos):
        perceived_center = np.array([0.0, 0.0])
        for boid in boids:
            if boid is not self:
                perceived_center += boid.position
        perceived_center += np.array(mouse_pos)
        perceived_center /= len(boids)

        return 0.02 * (perceived_center - self.position)

    def rule2(self, boids):
        c = np.array([0.0, 0.0])
        for b in boids:
            if b != self:
                if np.linalg.norm(b.position - self.position) < 10:
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
        v1 = self.rule1(boids, pygame.mouse.get_pos())
        v2 = self.rule2(boids)
        v3 = self.rule3(boids)
        self.velocity += v1 + v2 + v3
        
        # Limiting the velocity to a maximum speed
        self.limit_velocity(max_speed=0.5)
        
        self.position += self.velocity

        # Bouncing off boundaries with dampening effect
        dampening = 0.8  # The velocity is reduced to 80% of its original value after a bounce
        if self.position[0] < 0 or self.position[0] > WIDTH:
            self.velocity[0] = -self.velocity[0] * dampening
        if self.position[1] < 0 or self.position[1] > HEIGHT:
            self.velocity[1] = -self.velocity[1] * dampening

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
