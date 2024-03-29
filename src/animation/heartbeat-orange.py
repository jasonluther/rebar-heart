import time
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

pixel_rgb_red = 255
pixel_rgb_green = 85
pixel_rgb_blue = 0

def normal_index(i):
    return i % num_pixels


start_pixel = random.randrange(num_pixels)
start_width_m = 0.1
end_width_m = 2
variance = 0.5
in_beat_time = 0.3  # seconds
out_beat_time = 1.2  # seconds

start_time = time.clock_gettime(time.CLOCK_BOOTTIME)

breathe_in = True


def exit_handler():
    pixels.fill(0)
    pixels.show()


atexit.register(exit_handler)


def sigterm_handler(signum, frame):
    exit_handler()
    os._exit(0)


signal.signal(signal.SIGTERM, sigterm_handler)

while True:
    if breathe_in:
        current_time_delta = time.clock_gettime(
            time.CLOCK_BOOTTIME) - start_time
        pct_time = current_time_delta / in_beat_time
        width_m = start_width_m + abs(pct_time * (end_width_m - start_width_m))

        width_p = width_m * pixels_per_meter
        half_range = round(width_p / 2)
        pixels.fill(0)
        for p in range(half_range):
            brightness = 1 - (p / width_p)
            index_up = normal_index(start_pixel + p)
            index_down = normal_index(start_pixel - p)
            pixels[index_up] = (round(pixel_rgb_red * brightness), round(pixel_rgb_green * brightness), round(pixel_rgb_blue * brightness))
            pixels[index_down] = (round(pixel_rgb_red * brightness), round(pixel_rgb_green * brightness), round(pixel_rgb_blue * brightness))

        if (current_time_delta > in_beat_time):
            start_time = time.clock_gettime(time.CLOCK_BOOTTIME)
            breathe_in = False
    else:
        current_time_delta = time.clock_gettime(
            time.CLOCK_BOOTTIME) - start_time
        pct_time = current_time_delta / out_beat_time
        width_m = start_width_m + \
            abs((1-pct_time) * (end_width_m - start_width_m))

        width_p = width_m * pixels_per_meter
        half_range = round(width_p / 2)
        pixels.fill(0)
        for p in range(half_range):
            brightness = 1 - (p / width_p)
            brightness = abs(brightness * (1-pct_time))
            index_up = normal_index(start_pixel + p)
            index_down = normal_index(start_pixel - p)
            pixels[index_up] = (round(pixel_rgb_red * brightness), round(pixel_rgb_green * brightness), round(pixel_rgb_blue * brightness))
            pixels[index_down] = (round(pixel_rgb_red * brightness), round(pixel_rgb_green * brightness), round(pixel_rgb_blue * brightness))

        if (current_time_delta > out_beat_time):
            start_time = time.clock_gettime(time.CLOCK_BOOTTIME)
            start_pixel = normal_index(random.randrange(
                num_pixels) + round(num_pixels / 3))
            end_width_m = random.randrange(round(
                1000 * (end_width_m-variance)), round(1000 * (end_width_m+variance))) / 1000
            if (end_width_m > 2.5):
                end_width_m = end_width_m / 2

            breathe_in = True

    pixels.show()
    time.sleep(0.001)
