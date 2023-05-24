import pygame
import pymunk
import pymunk.pygame_util

def create_chain(space, start_pos, end_pos, n_segments=30):
    """Create a chain of segments in the given pymunk.Space."""
    # Calculate properties of the chain
    segment_length = ((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)**0.5 / n_segments
    segment_mass = 1
    segment_radius = segment_length / 2
    segment_moment = pymunk.moment_for_circle(segment_mass, 0, segment_radius)

    # Create the segments
    segments = []
    for i in range(n_segments):
        x = start_pos[0] + i * (end_pos[0] - start_pos[0]) / n_segments
        y = start_pos[1] + i * (end_pos[1] - start_pos[1]) / n_segments

        segment_body = pymunk.Body(segment_mass, segment_moment)
        segment_body.position = (x, y)
        segment_shape = pymunk.Circle(segment_body, segment_radius)
        segments.append((segment_body, segment_shape))
        space.add(segment_body, segment_shape)

    # Connect the segments with pivot joints
    for i in range(n_segments - 1):
        joint = pymunk.PivotJoint(segments[i][0], segments[i + 1][0], segments[i][0].local_to_world((0,0)), segments[i+1][0].local_to_world((0,0)))
        space.add(joint)

    # Connect the first and last segment to static anchors
    anchor1 = pymunk.Body(body_type=pymunk.Body.STATIC)
    anchor1.position = start_pos
    anchor2 = pymunk.Body(body_type=pymunk.Body.STATIC)
    anchor2.position = end_pos
    joint1 = pymunk.PivotJoint(anchor1, segments[0][0], anchor1.local_to_world((0,0)), segments[0][0].local_to_world((0,0)))
    joint2 = pymunk.PivotJoint(anchor2, segments[-1][0], anchor2.local_to_world((0,0)), segments[-1][0].local_to_world((0,0)))
    space.add(joint1, joint2)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Initialize Pymunk and create a space for the simulation
space = pymunk.Space()
space.gravity = (0, -900)

# Run the simulation
running = True
start_pos = None
end_pos = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            end_pos = pygame.mouse.get_pos()
            create_chain(space, start_pos, end_pos)

    screen.fill((255, 255, 255))

    # Draw everything
    options = pymunk.pygame_util.DrawOptions(screen)
    space.debug_draw(options)

    # Update the physics
    dt = 1/60.0
    space.step(dt)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
