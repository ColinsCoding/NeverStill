import matplotlib.pyplot as plt
from shapely.geometry import Point
from descartes import PolygonPatch

# Create two circles
circle1 = Point(1.0, 1.0).buffer(1.5)
circle2 = Point(2.0, 1.0).buffer(1.5)

# Calculate intersection
intersection = circle1.intersection(circle2)

# Create figure and axes
fig, ax = plt.subplots()

# Add circles to plot
ax.add_patch(PolygonPatch(circle1.difference(intersection), fc='blue', alpha=0.5))
ax.add_patch(PolygonPatch(circle2.difference(intersection), fc='red', alpha=0.5))

# Set limits and aspect ratio
ax.set_xlim(0, 3)
ax.set_ylim(0, 2.5)
ax.set_aspect('equal')

plt.show()
