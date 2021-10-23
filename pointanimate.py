import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = 4,3
from matplotlib.animation import FuncAnimation

# r = 1 # radius of circle
def circle(phi,r):
    return np.array([r*np.cos(phi), r*np.sin(phi)])

# create a figure with an axes
fig, ax = plt.subplots()
# set the axes limits
ax.axis([-1.5,1.5,-1.5,1.5])
# set equal aspect such that the circle is not shown as ellipse
ax.set_aspect("equal")
# create a point in the axes
point, = ax.plot(0,1, marker="o", markersize=10, color="red")

# Updating function, to be repeatedly called by the animation
r=1
def update(phi):
    # obtain point coordinates 
    x,y = circle(phi,r)
    # set point's coordinates
    point.set_data([x],[y])
    return point,

# create animation with 10ms interval, which is repeated,
# provide the full circle (0,2pi) as parameters
ani = FuncAnimation(fig, update, interval=10, blit=True, repeat=True,
                    frames=np.linspace(0,2*np.pi,360, endpoint=False))

plt.show()