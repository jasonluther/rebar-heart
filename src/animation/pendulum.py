import time
import math
import board
import neopixel
import random
import collections
import adafruit_fancyled.adafruit_fancyled as fancy
import atexit
import signal
import os

# Heart strip configuration
num_pixels = 177
pixels_per_meter = 60
pixel_mid_bot = 59
pixel_mid_top = 148
brightness = 0.5

left_top = pixel_mid_top
right_top = left_top + 1
left_bot = pixel_mid_bot + 1
right_bot = left_bot - 1

pixel_pin = board.D18
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER
)
pixels.fill(0)
pixels.show()


def normal_index(i):
    return (right_bot + i) % num_pixels


def rand_hsv():
    hsv = fancy.CHSV(random.uniform(0, 1), random.uniform(0, 1), 0.2)
    return hsv


period = 10
period_min = 1
period_max = 10
amplitude = 80
amplitude_min = 70
amplitude_max = round(num_pixels/2 - 1)
change_secs = 120
tail = 10
lastvals = collections.deque([0], tail)
c = rand_hsv().pack()
dir = last_dir = "off"
start_secs = time.clock_gettime(time.CLOCK_MONOTONIC)


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
    val = round(math.cos(2*math.pi * secs/period) * amplitude)
    lastvals.appendleft(val)

    pixels.fill(0)

    last_dir = dir
    if (abs(val) == amplitude):
        dir = "edge"
    elif (val > lastvals[1]):
        if val <= 0:
            dir = "right_down"
        else:
            dir = "left_up"
    elif (val < lastvals[1]):
        if val <= 0:
            dir = "right_up"
        else:
            dir = "left_down"

    if (dir != last_dir):
        # we changed direction
        tail_hue = random.uniform(0, 1)
        if (dir == "edge"):
            if (secs > start_secs + change_secs):
                start_secs = secs
                amplitude = random.randrange(amplitude_min, amplitude_max)
                period = random.uniform(period_min, period_max)
                lastvals.clear()
                lastvals.append(val)

    # same direction
    first_px = val
    last_px = lastvals[-1]

    valdelta = abs(first_px - last_px)
    if (first_px > last_px):
        step = -1
    else:
        step = 1
    tail_val = 1.0
    tail_sat = 1.0
    for v in range(first_px, last_px, step):
        tail_val = 1-((abs(first_px - v))/(valdelta))
        pixels[normal_index(v)] = fancy.CHSV(
            tail_hue, tail_sat, tail_val).pack()
        tail_val = tail_val / 2.0
        tail_sat -= tail_sat * 0.02

    pixels[normal_index(val)] = fancy.CHSV(tail_hue, 1, 1).pack()

    pixels.show()
    time.sleep(0.01)
