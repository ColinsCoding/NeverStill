import pygame
import pygame_gui
import numpy as np
from scipy.spatial.distance import cdist
from scipy.ndimage import gaussian_filter


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

# Initialize Pygame GUI manager
gui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))


# Create slider and checkboxes
time_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((50, 10), (300, 20)),
    start_value=1,
    value_range=(1, 10),
    manager=gui_manager,
)

energy_checkbox = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((400, 10), (150, 20)),
    text="Toggle Energy Field",
    manager=gui_manager,
)

growth_rate_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((50, 40), (300, 20)),
    start_value=2,
    value_range=(1, 10),
    manager=gui_manager,
)

# Create Quit button
quit_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((600, 10), (150, 20)),
    text="Quit",
    manager=gui_manager,
)

energy_field_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((400, 40), (150, 20)),
    text="Change Energy Field",
    manager=gui_manager,
)


# 
def generate_energy_field(config, sigma=1.0):
    energy_field = np.zeros((HEIGHT // 10, WIDTH // 10))

    if config == "uniform":
        energy_field[:, :] = 1
    elif config == "gradient_horizontal":
        energy_field[:, :] = np.linspace(0, 1, WIDTH // 10)
    elif config == "gradient_vertical":
        for i in range(HEIGHT // 10):
            energy_field[i, :] = i / (HEIGHT // 10)
    elif config == "random":
        energy_field = np.random.rand(HEIGHT // 10, WIDTH // 10)
        energy_field = gaussian_filter(energy_field, sigma=sigma)

    return energy_field

def generate_distance_field(metric):
    grid = np.array([[x, y] for y in range(HEIGHT // 10) for x in range(WIDTH // 10)])
    center = np.array([[WIDTH // 20, HEIGHT // 20]])
    distances = cdist(center, grid, metric=metric)
    energy_field = distances.reshape(HEIGHT // 10, WIDTH // 10)

    # Normalize the energy field values to be between 0 and 1
    energy_field = (energy_field - energy_field.min()) / (energy_field.max() - energy_field.min())

    return energy_field


class Tree:

    scalefactor = 2

    def __init__(self, position, max_branches=1000, growth_rate=100):
        self.position = position
        self.branches = []
        self.energy = 0
        self.growth_rate = growth_rate
        self.direction = None
        self.length = 0
        self.max_branches = max_branches

    # ... other methods here ...

    def grow(self, energy_field, occupied_space):
        num_branches = len(self.branches)
        # Apply the logistic growth model to adjust the growth rate
        adjusted_growth_rate = self.growth_rate * num_branches * (1 - num_branches / self.max_branches)
        
        self.energy += adjusted_growth_rate * energy_field[int(self.position[1]) // 10, int(self.position[0]) // 10]

        # ... rest of the method here ...




# ... (rest of the Tree class implementation)
# Tree class
class Tree:

    scalefactor = 2

    def __init__(self, position, max_branches=1000, growth_rate=100):
        self.position = position
        self.branches = []
        self.energy = 0
        self.growth_rate = growth_rate
        self.direction = None
        self.length = 0
        self.max_branches = max_branches

    def get_energy_gradient(self, energy_field):
        y, x = int(self.position[1]) // 10, int(self.position[0]) // 10
        dy = energy_field[min(y + 1, energy_field.shape[0] - 1), x] - energy_field[max(y - 1, 0), x]
        dx = energy_field[y, min(x + 1, energy_field.shape[1] - 1)] - energy_field[y, max(x - 1, 0)]
        return np.array([dx, dy])
    
    def update_occupied_space(self, occupied_space):
        if self.direction:
            end_position = self.position + np.array([np.sin(self.direction) * self.length, -np.cos(self.direction) * self.length])
            y, x = int(end_position[1]) // 10, int(end_position[0]) // 10
            if 0 <= y < occupied_space.shape[0] and 0 <= x < occupied_space.shape[1]:
                occupied_space[y, x] = 1

        for branch in self.branches:
            branch.update_occupied_space(occupied_space)


    def grow(self, energy_field, occupied_space):
        self.energy += self.growth_rate * energy_field[int(self.position[1]) // 10, int(self.position[0]) // 10]

        if self.energy > 5:
            if not self.direction:
                energy_gradient = self.get_energy_gradient(energy_field)
                self.direction = np.arctan2(energy_gradient[1], energy_gradient[0]) + np.random.uniform(-np.pi / 4, np.pi / 4)
                self.length = 0

            self.length += 1
            self.energy -= 5

            new_position = self.position + np.array([np.sin(self.direction) * self.length, -np.cos(self.direction) * self.length])
            new_y, new_x = int(new_position[1]) // 10, int(new_position[0]) // 10

            if not (0 <= new_y < occupied_space.shape[0] and 0 <= new_x < occupied_space.shape[1] and occupied_space[new_y, new_x] == 1):
                if self.length >= 10:
                    self.branches.append(Tree(new_position))
                    self.direction = None
                    self.length = 0

        for branch in self.branches:
            branch.grow(energy_field, occupied_space)

    def draw(self, screen):
        if self.direction:
            end_position = self.position + np.array([np.sin(self.direction) * self.length, -np.cos(self.direction) * self.length])
            pygame.draw.line(screen, (0, 0, 0), self.position, end_position)

        for branch in self.branches:
            pygame.draw.line(screen, (0, 0, 0), self.position, branch.position)
            branch.draw(screen)


# List of trees
trees = []

# Energy field intalized to zero 
energy_field = np.zeros((HEIGHT // 10, WIDTH // 10))

# List of distance metrics
distance_metrics = ['euclidean', 'cityblock', 'chebyshev']
distance_metric_index = 0

# Energy field
energy_field = generate_distance_field(distance_metrics[distance_metric_index])

# Occupied space field
occupied_space = np.zeros((HEIGHT // 10, WIDTH // 10))

# Timer
timer = 0

# Flags for showing scalar fields
show_energy_field = False

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60) / 1000.0
        # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            trees.append(Tree(np.array(event.pos)))

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == energy_checkbox:
                    show_energy_field = not show_energy_field
                elif event.ui_element == quit_button:
                    running = False
                elif event.ui_element == energy_field_button:  # Add this condition
                    distance_metric_index = (distance_metric_index + 1) % len(distance_metrics)
     

    # Update UI
    gui_manager.process_events(event)

    # Get growth rate from the slider
    growth_rate = growth_rate_slider.get_current_value()

    # Update the simulation (tree agents and resource field)
    if timer % (TICKS_PER_HOUR * .025) == 0:  # Every 6 hours
        # # ... (rest of the energy field calculation and tree growth logic)
        # sun_position = timer // (TICKS_PER_HOUR * 6) % 4
        # if sun_position == 0:
        #     energy_field[:, :] = 1
        # elif sun_position == 1:
        #     energy_field[:, :] = np.linspace(0, 1, WIDTH // 10)
        # elif sun_position == 2:
        #     energy_field[:, :] = 0
        # else:
        #     energy_field[:, :] = np.linspace(1, 0, WIDTH // 10)
        
        # for tree in trees:

        #Update the energy field based on the selected distance metric
        energy_field = generate_energy_field('random', sigma=1.0)
       #energy_field = generate_distance_field(distance_metrics[distance_metric_index])

    for tree in trees:
        tree.grow(energy_field, occupied_space)
        tree.update_occupied_space(occupied_space)

    # Render the scene
    screen.fill((255, 255, 255))  # Clear the screen with a white background

    

    # Render the scalar fields
    if show_energy_field:
        for y in range(energy_field.shape[0]):
            for x in range(energy_field.shape[1]):
                intensity = int(energy_field[y, x] * 255)
                pygame.draw.rect(screen, (intensity, 0, 0), (x * 10, y * 10, 10, 10))

    # Render the trees
    for tree in trees:
        tree.draw(screen)

    # Render UI elements
    gui_manager.draw_ui(screen)

    pygame.display.flip()  # Update the display

    # Increment timer
    timer += int(time_slider.get_current_value())
    if timer >= TICKS_PER_HOUR * HOURS_PER_DAY:
        timer = 0

    # Update UI
    gui_manager.update(time_delta)

pygame.quit()
