import pygame
import pygame_gui
import math

# Initialize pygame and create a window
pygame.init()
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Wire Simulation")

# Define the colors to use in the simulation
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the two endpoints of the wire (initialized to None)
point1 = None
point2 = None

# Define the mass and acceleration of the wire (initialized to zero)
mass = 0
acceleration = 0

# Define the constants for the simulation
GRAVITY = 9.8    # gravitational acceleration
TIME_STEP = 0.1  # time step for the simulation

# Define the function to calculate the force between the two endpoints of the wire
def calculate_force():
    global mass, acceleration
    if point1 and point2:
        # Calculate the distance between the two endpoints
        distance = math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
        
        # Calculate the tension force in the wire
        tension = distance * mass * GRAVITY
        
        # Calculate the acceleration of the wire
        acceleration = tension / mass
        
        # Calculate the x and y components of the force
        force_x = tension * (point2[0]-point1[0]) / distance
        force_y = tension * (point2[1]-point1[1]) / distance
        
        # Return the force vector as a tuple
        return (force_x, force_y)
    else:
        return (0, 0)

# Define the function to update the position of the endpoints of the wire
def update_positions():
    global point1, point2, acceleration
    if point1 and point2:
        # Calculate the force vector
        force = calculate_force()
        
        # Calculate the new positions of the endpoints based on the acceleration
        point1 = (point1[0] + acceleration*force[0]*TIME_STEP**2, point1[1] + acceleration*force[1]*TIME_STEP**2)
        point2 = (point2[0] + acceleration*force[0]*TIME_STEP**2, point2[1] + acceleration*force[1]*TIME_STEP**2)

# Define the function to draw the wire on the screen
def draw_wire():
    global point1, point2
    if point1 and point2:
        pygame.draw.line(screen, WHITE, point1, point2, 5)

# Set up the GUI manager
gui_manager = pygame_gui.UIManager(WINDOW_SIZE)

# Set up the text input boxes for the user to enter the coordinates of the endpoints
text_input_box1 = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((50, 50), (100, 30)),
    manager=gui_manager)
text_input_box2 = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((50, 100), (100, 30)),
    manager=gui_manager)

# Set up the button for the user to submit the coordinates
submit_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 150), (100, 30)),
    text="Submit",
    manager=gui_manager)

# Start the game loop
is_running = True
while is_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == submit_button:
                    # Get the coordinates entered by the user and convert to integers
                    x1, y1 = int(text_input_box1.text), int(text_input_box2.text)
                    x2, y2 = int(text_input_box2.text), int(text_input_box2.text)
                    
                    # Set the endpoints of the wire and the mass
                    point1 = (x1, y1)
                    point2 = (x2, y2)
                    mass = math.sqrt((x2-x1)**2 + (y2-y1)**2) * 0.1  # set mass proportional to length
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == text_input_box1 or event.ui_element == text_input_box2:
                    # Update the text entry with the new value
                    event.ui_element.set_text(str(int(event.ui_element.text)))
                    
        # Handle GUI events
        gui_manager.process_events(event)
        
    # Update the positions of the endpoints of the wire
    update_positions()
    
    # Draw the wire on the screen
    screen.fill(BLACK)
    draw_wire()
    
    # Update the GUI
    gui_manager.update(TIME_STEP)
    gui_manager.draw_ui(screen)
    
    # Update the screen
    pygame.display.update()

# Quit pygame and exit
pygame.quit()
exit() 
