import time
import math
import board
import neopixel
import random
import adafruit_fancyled.adafruit_fancyled as fancy
import atexit
import signal
import os

# Heart strip configuration
num_pixels = 177
pixels_per_meter = 60
pixel_mid_bot = 59
pixel_mid_top = 148
brightness = 1

pixel_pin = board.D18
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER
)
pixels.fill(0)
pixels.show()


def normal_index(i):
    return i % num_pixels


max_hue = 1.0
max_sat = 1.0
max_val = 1.0
px_hue = []
px_sat = []
px_val = []
px_life = []


def rand_hsv():
    return random.uniform(0, 1)


def init_px_arrays():
    for i in range(num_pixels):
        px_hue.append(rand_hsv())
        px_sat.append(1.0)
        px_val.append(1.0)
        px_life.append(1)


def random_update(r):
    for i in range(num_pixels):
        if random.randrange(r) == 1:
            px_hue[i] = rand_hsv()
            px_sat[i] = rand_hsv()
            px_val[i] = rand_hsv()
            px_life[i] = random.randrange(20, 100)


def darken():
    cumulative_value = 0
    for i in range(num_pixels):
        if px_val[i] > 0:
            px_val[i] = px_val[i] * (px_life[i] / 100)
        cumulative_value += px_val[i]
        px_life[i] = px_life[i] - 1
    return cumulative_value


def write_hsv_to_pixels():
    for i in range(num_pixels):
        color = fancy.CHSV(px_hue[i], px_sat[i], px_val[i])
        pixels[i] = color.pack()
    pixels.show()


init_px_arrays()

period = 60
amplitude = num_pixels / 5


def exit_handler():
    pixels.fill(0)
    pixels.show()


atexit.register(exit_handler)


def sigterm_handler(signum, frame):
    exit_handler()
    os._exit(0)


signal.signal(signal.SIGTERM, sigterm_handler)

while True:
    secs = time.clock_gettime(time.CLOCK_MONOTONIC)
    val = math.sin(2*math.pi * secs/period) * amplitude + num_pixels
    random_update(round(val))
    darken()
    write_hsv_to_pixels()
    time.sleep(0.00001)
