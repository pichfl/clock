from ylk_digits import DIGITS, DIVIDER, SPACE
from time import localtime

blink = 0

def renderTime():
  global blink
  blink = not blink

  now = localtime()
  hours = now.tm_hour
  minutes = now.tm_min
  width = 26
  height = 9

  hours = [int(x) for x in "%02d" % hours]
  minutes = [int(x) for x in "%02d" % minutes]

  time_characters = [
    DIGITS[hours[0]], SPACE, DIGITS[hours[1]], 
    SPACE, DIVIDER if blink else SPACE, SPACE,
    DIGITS[minutes[0]], SPACE, DIGITS[minutes[1]],
  ]

  pad_y = [0 for _ in range(width)]
  
  matrix = [
    pad_y,
  ]

  for y in range(len(time_characters[0])):
    row = []

    for character in range(len(time_characters)):
      row.extend(time_characters[character][y])

    if (len(row) < width):
      row.extend([0 for _ in range(width - len(row))])
    elif (len(row) > width):
      row = row[:width]

    matrix.append(row)

  if (len(matrix) < height):
    for _ in range(height - len(matrix)):
      matrix.append(pad_y)

  return matrix

def printTime(matrix):
  for row in matrix:
    for cell in row:
        print(" ⬤" if (cell == 1) else "  ", end="")
    print("")