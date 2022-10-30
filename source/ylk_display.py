
import adafruit_bh1750
import adafruit_is31fl3741
import busio
import adafruit_fancyled.adafruit_fancyled as fancy

from adafruit_is31fl3741.adafruit_rgbmatrixqt import Adafruit_RGBMatrixQT

class Display():
  def __init__(self, scl, sda, addresses, global_current = 255, led_scaling = 255):
    self.displayWidth = 13
    self.display_height = 9
    self.displays = []
    self.max_lux = 200
    self.lux_values = []
    self.brightness_window = 7

    i2c = busio.I2C(scl=scl, sda=sda)
  
    for address in addresses:
      display = Adafruit_RGBMatrixQT(i2c, address, allocate=adafruit_is31fl3741.PREFER_BUFFER)
      display.set_led_scaling(led_scaling)
      display.global_current = global_current
      display.enable = True
      self.displays.append(display)

    self.sensor = adafruit_bh1750.BH1750(i2c)

  @property
  def brightness(self):
    self.lux_values.append(self.sensor.lux)

    if len(self.lux_values) > self.brightness_window:
      del self.lux_values[0]

    lux = sum(self.lux_values) / len(self.lux_values)

    return max(0.01, min(lux, self.max_lux) / self.max_lux)

  @property
  def totalWidth(self):
    return self.displayWidth * len(self.displays)
  
  @property
  def global_current(self):
    return self.displays[0].global_current
  
  @global_current.setter
  def global_current(self, value):
    for display in self.displays:
      display.global_current = value

  @property
  def led_scaling(self):
    return self.displays[0].led_scaling

  @led_scaling.setter
  def led_scaling(self, value):
    for display in self.displays:
      display.set_led_scaling(value)

  def draw(self, matrix):
    if (len(matrix) != self.display_height):
      raise ValueError("Matrix height must be %d" % self.display_height)
    if (len(matrix[0]) != self.totalWidth):
      raise ValueError("Matrix width must be %d" % self.totalWidth)

    self.global_current = int(self.brightness * 0xFF)
  
    hue = -0.35 * self.brightness
    saturation = 1.0
    value = 1.0

    on_color = fancy.gamma_adjust(
      fancy.CHSV(
        hue, saturation, value), 
      gamma_value=2.2
    ).pack()

    for display in self.displays:
      for displayX in range(self.displayWidth):
        for y in range(self.display_height):
          x = displayX + (self.displayWidth * self.displays.index(display))
  
          display.pixel(displayX, y, on_color if matrix[y][x] == 1 else 0x000000)
      display.show()