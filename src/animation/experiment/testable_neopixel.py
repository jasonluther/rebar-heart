try:
    from typing import Optional, Tuple, Union, Sequence

    ColorUnion = Union[int, Tuple[int, int, int], Tuple[int, int, int, int]]
except ImportError:
    pass

# Pixel color order constants from https://github.com/adafruit/Adafruit_CircuitPython_Pixelbuf/blob/5f64550ac0a019bb033fa832cf0acd0a201c02c6/adafruit_pixelbuf.py#L195

RGB = "RGB"
"""Red Green Blue"""
GRB = "GRB"
"""Green Red Blue"""
RGBW = "RGBW"
"""Red Green Blue White"""
GRBW = "GRBW"
"""Green Red Blue White"""

class NeoPixel(list):
    def __init__(self, pin, size, **kwargs):
        try:
            import board
            import neopixel
            return neopixel.NeoPixel(pin, size, kwargs)
        except:
            super(NeoPixel, self).__init__([0] * size)

    def show(self):
        print(*self)

    def fill(self, val):
        for i in range(len(self)):
            self[i] = val