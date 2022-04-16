import matplotlib.pyplot as plt
from datetime import datetime
import csv
from pynput import keyboard

"""
zoomable(): allows zooming / moving on the grid

wait_for_movement(): detects important keys and returns them
    - uses on_press() and on_release()

"""


def update_coords(coords, direction):
    # for plotting (up = positive)
    if direction=="up":
        return (coords[0], coords[1]-1)
    if direction=="down":
        return (coords[0], coords[1]+1)
    if direction=="left":
        return (coords[0]-1, coords[1])
    if direction=="right":
        return (coords[0]+1, coords[1])


def switch_animal():
    print("Switching animal...")
    x = int(input("Enter your X coordinate: "))
    y = int(input("Enter your Y coordinate: "))
    return (x, y)


def load_plot():
    pack = input("Enter the map ID: ")
    x_start = int(input("Enter your X coordinate: "))
    y_start = int(input("Enter your Y coordinate: "))
    try:
        dir = 'map' + str(pack) + '.csv'
        with open(dir, 'r') as f:
            reader = f.readlines()
            coords = [x_start, y_start]
            x = [int(val.strip('\n')) for val in reader[1].split(',')]
            y = [int(val.strip('\n')) for val in reader[2].split(',')]
    except FileNotFoundError:
        print("Using new data... ")
        coords = (x_start, y_start)
        x = [x_start]
        y = [y_start] 

    return x, y, coords, pack


def save_plot(x, y, coords, pack):
    # eg map1.csv
    dir = 'map' + str(pack) + '.csv'
    with open(dir, 'w', newline='') as f:
        write = csv.writer(f) 
        write.writerow([str(value) for value in coords])
        write.writerow([str(value) for value in x])
        write.writerow([str(value) for value in y])

    # store a backup copy
    date = str(datetime.now().replace(microsecond=0)).replace(':', '-')
    with open(f'backup\saved data at {date} for pack {pack}.csv', 'w', newline='') as backup:
        write = csv.writer(backup) 
        write.writerow([str(value) for value in coords])
        write.writerow([str(value) for value in x])
        write.writerow([str(value) for value in y])


def zoomable(ax, base_scale = 2.):
    # this isn't my code
    def zoom_fun(event):
        # get the current x and y limits
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print(event.button)
        # set new limits
        ax.set_xlim([xdata - cur_xrange*scale_factor,
                     xdata + cur_xrange*scale_factor])
        ax.set_ylim([ydata - cur_yrange*scale_factor,
                     ydata + cur_yrange*scale_factor])
        plt.draw() # force re-draw

    fig = ax.get_figure() # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event',zoom_fun)

    return zoom_fun


def on_press(key):
    global last
    try:
        last = key.char
    except AttributeError:
        last = key

def on_release(key):
    if key in [keyboard.Key.esc, keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right, keyboard.Key.num_lock]:
        return False

def wait_for_movement():
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    global last

    if last == keyboard.Key.esc:
        return "esc"
    elif last == keyboard.Key.num_lock:
        return "numlock"

    # convert to string
    last = str(last).split('.')[len(str(last).split('.'))-1]
    return last
