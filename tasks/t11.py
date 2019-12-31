from advent.machine import Machine
from collections import defaultdict

face_mapping = {
  (0, 1): 'v',
  (1, 0): '>',
  (0, -1): '^',
  (-1, 0): '<'
}

class PaintingRobot:
  def __init__(self):
    self.color_wrote = 0
    self.panel = defaultdict(lambda: 0)
    self.position = (0, 0)
    self.face = (0, 1)
    self.program = Machine('inputs/input11.txt', 'robot')
    self.used = set()

  def turn_n_move(self, parameter):
    if parameter == 1:
      self.turn_right()
    else:
      self.turn_left()
    self.move()
  
  def turn_left(self):
    self.face = (-self.face[1], self.face[0])

  def turn_right(self):
    self.face = (self.face[1], -self.face[0])

  def move(self):
    self.position = (
      self.position[0] + self.face[0], 
      self.position[1] + self.face[1]
    )

  def run(self, default_input=None):
    if default_input is not None:
      self.program.set_input(default_input)
    else:
      self.program.set_input(self.panel[self.position])
    color, turn = self.program.run(), self.program.run()
    self.panel[self.position] = color
    self.turn_n_move(turn)

    self.used.add(self.position)

  def print_panel(self):
    s = 25

    for y in range(10, -10, -1):
      row = ''
      for x in range(-10, 50):
        if self.panel[(x, y)] == 1:
          row = row + '█'
        elif (x, y) == self.position:
          row = row + face_mapping[self.face]
        else:
          row = row + ' '
      print(row)
    print('')

def day_11_a():
  r = PaintingRobot()
  r.run(1)
  try:
    while True:
      r.run()
  except:
    print(len(r.used))
    print(len(r.panel))
    r.print_panel()
