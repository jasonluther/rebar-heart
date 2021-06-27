# Animation Programs

These Python scripts follow a simple pattern, mostly based on example code:

1. Configure the details of the NeoPixel strip. 

```
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER
)
pixels.fill(0)
pixels.show()
```
2. Set up an exit handler to turn the strip off when the program exits.

```
def exit_handler():
    pixels.fill(0)
    pixels.show()


atexit.register(exit_handler)


def sigterm_handler(signum, frame):
    exit_handler()
    os._exit(0)


signal.signal(signal.SIGTERM, sigterm_handler)
```

3. Set `pixels` values, sleep, repeat.

```
while True:
    # Do the animation stuff...
    pixels.show()
    time.sleep(0.01)
```

## Choosing a random animation

`random-animation.py` assumes that any `.py` files in the same directory are animations, and it picks one at random to run. 

## Running as `root`

Because the programs manipulate the hardware, they must be run as the `root` superuser. 

Make sure you trust any code that you incorporate into a program like this, as it has full control of the Pi. 
