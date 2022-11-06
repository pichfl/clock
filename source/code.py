from board import GP8, GP9
from time import sleep, localtime
from ylk_display import Display
from ylk_render import renderTime
from ylk_time import set_rtc
from ylk_led import led

display = Display(GP9, GP8, [0x30, 0x33])
_ = 0

display.draw([
  [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
  [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
  [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
  [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
  [_,_,_,_,_,_,_,_,_,1,1,_,1,1,_,1,1,_,_,_,_,_,_,_,_,_],
  [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
  [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
  [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
  [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
])

def render():
  matrix = renderTime()
  display.draw(matrix)

set_rtc()
render()

is_running = False

def main():
  global is_running
  
  if is_running:
    return

  is_running = True

  while True:
    now = localtime()

    led.value = not led.value
    render()

    if now.tm_yday % 2 and now.tm_hour == 3 and now.tm_min == 0 and now.tm_sec == 0:
      set_rtc()

    sleep(0.5)

main()