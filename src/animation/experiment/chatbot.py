import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

# Create a figure and an axis
fig, ax = plt.subplots()

# Set the axis limits
ax.set_xlim(0, 2)
ax.set_ylim(0, 100)

# Initialize a line plot with empty data
line, = ax.plot([], [], lw=2)

# Define the animation function
def animate(i):
    # Calculate the x and y values for the current frame
    x = i / 50
    y = 100 * (1 - math.log(2 - x, 2))

    # Update the line data
    line.set_data([x, x], [0, y])

# Create the animation object
anim = animation.FuncAnimation(fig, animate, frames=100, interval=20, blit=True)

# Show the animation
plt.show()
