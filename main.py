import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
# my stuff
from functions import update_coords, load_plot, save_plot, zoomable, wait_for_movement, switch_animal


"""
live_scatter() - shows live data
detect_move() - uses keylogger to track movement
"""

# pack is the map ID
x, y, coords, pack = load_plot()
STARTING_RES = 30
LIGHT_GREY = '#969696'
DARK_GREY = '#CCCCCC'


# global values
plt.xlim((coords[0] - STARTING_RES, coords[0] + STARTING_RES))
plt.ylim((coords[1] - STARTING_RES, coords[1] + STARTING_RES))


def live_scatter(na):
    global x
    global y
    global coords
    xlim = plt.gca().get_xlim()
    ylim = plt.gca().get_ylim()
    plt.cla()
    # marker size in units of area - 30000 was found arbitrarily
    s = 30000 / round(xlim[1] - xlim[0]) ** 2
    plt.scatter(x, y, s=s)
    plt.xlim(xlim)
    # need to invert the y axis to match the map coords system
    plt.ylim((max(ylim[1],ylim[0]), min(ylim[0],ylim[1])))
    # display coords as title
    ax = plt.gca()
    ax.set_title(str(coords))
    # gridlines every 5 units
    ax.set_xticks(np.arange(int(xlim[0]) - int(xlim[0]) % 5, int(xlim[1]), 5), minor=True)
    ax.set_yticks(np.arange(int(ylim[1]) - int(ylim[1]) % 5, int(ylim[0]), 5), minor=True)
    plt.gca().grid(color=DARK_GREY)
    plt.gca().grid(which="minor", color=LIGHT_GREY)


def detect_move():
    while True:
        global coords
        global x
        global y
        move = wait_for_movement()
        # esc pauses the detection
        if move == "esc":
            print("Ending detection, please close graph window... ")
            plt.close()
            return
        # numlock allows you to switch animals within the same map
        if move == "numlock":
            coords = switch_animal()
        # any else is movement
        else:
            print(move)
            coords = update_coords(coords, move)
            x.append(coords[0])
            y.append(coords[1])


# constantly detect movement
movements = threading.Thread(target=detect_move)
movements.start()

# allow zooming on the plot
zoomable(plt.gca())

# show the plot as an animation - allows live updates
ani = FuncAnimation(plt.gcf(), live_scatter, interval=500)
plt.show()

print("Saving map data. Program closing... ")

save_plot(x, y, coords, pack)

