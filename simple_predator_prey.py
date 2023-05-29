import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Constants
PREY_GROWTH = 10
PREDATOR_GROWTH = 10
PREDATOR_LOSS = 2
PREY_LOSS = 2

# Initial populations
prey_population = 100
predator_population = 20

# Lists to hold the population data
prey_populations = [prey_population]
predator_populations = [predator_population]

fig, ax = plt.subplots()

# The line objects for the populations
prey_line, = ax.plot(prey_populations, label='Prey')
predator_line, = ax.plot(predator_populations, label='Predator')
plt.legend()

def update(frame):
    global prey_population, predator_population

    # Calculate the changes in population
    delta_prey = (PREY_GROWTH * prey_population ) -  (PREDATOR_GROWTH * predator_population * prey_population )
    delta_predator = (PREY_LOSS * predator_population * prey_population ) - ( PREDATOR_LOSS * predator_population)

    # Update the populations
    prey_population += delta_prey
    predator_population += delta_predator

    # Add the new populations to the lists
    prey_populations.append(prey_population)
    predator_populations.append(predator_population)

    # Update the data of the line objects
    prey_line.set_ydata(prey_populations)
    prey_line.set_xdata(range(len(prey_populations)))
    predator_line.set_ydata(predator_populations)
    predator_line.set_xdata(range(len(predator_populations)))

    # Make sure the plot shows enough x-axis for the new data
    ax.relim()
    ax.autoscale_view()

# Create the animation
animation = FuncAnimation(fig, update, frames=range(1000000), repeat=False)

# Show the plot
plt.show()
