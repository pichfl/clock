# Clock

9x26 pixels make an excellent clock. Uses NTP and the internal RTC to keep the time.


## Hardware Requirements

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/) W for Wifi
- 2× [Adafruit IS31FL3741 13x9 PWM RGB LED Matrix Driver](https://www.adafruit.com/product/5201#technical-details)
- [Adafruit BH1750 Light Sensor ](https://www.adafruit.com/product/4681) (or similar)
- [USB-C breakout board](https://www.adafruit.com/product/4090) to relocate the power connector
- a few cables to connect all the things (STEMMA QT / Qwiic sets make this easy)

## Software 

- Flash Pico with [CircuitPython](https://circuitpython.org)
- Copy content of `./source` to the USB volume

### Required libraries

Download the offical and community bundle of the [CircuitPython Libraries](https://circuitpython.org/libraries).

Copy these libraries to the `./lib` folder:

- adafruit_bh1750.mpy
- adafruit_datetime.mpy
- adafruit_fancyled
- adafruit_framebuf.mpy
- adafruit_is31fl3741
- adafruit_led_animation
- adafruit_ntp.mpy
- adafruit_register
- adafruit_requests.mpy
- adafruit_ticks.mpy
- nonblocking_timer

TODO: Check which are actually in use, I played around with different options.

### Configuration

Add your WIFI credentials to `secrets.py`. This projects is currently hardcoded for Europe/Berlin. If you want to use a different timezone, you'll have to change the code in `ylk_time.py`.

## Assembly

I made a case from wood. I'll add the files whenever I finish this project. 
