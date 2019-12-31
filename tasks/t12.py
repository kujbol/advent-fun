from dataclasses import dataclass
from itertools import combinations

positions = 'z'


@dataclass
class Vector3:
  x: int
  y: int
  z: int

  def add(self, vector):
    for pos in positions:
      setattr(self, pos, getattr(self, pos ) + getattr(vector, pos))
  
  def get_energy(self):
    energy = 0
    for pos in positions:
      energy += abs(getattr(self, pos))
    
    return energy


@dataclass
class Moon:
  position: Vector3
  velocity: Vector3

  def update(self):
    self.position.add(self.velocity)
  
  def get_energy(self):
    kin = self.velocity.get_energy()
    pot = self.position.get_energy()

    return kin * pot

class Simulation():
  def __init__(self, moons):
    self.moons = moons

  def step(self):
    # update velocity
    for moon1, moon2 in combinations(self.moons, 2):
      for pos in positions:
        p1 = getattr(moon1.position, pos)
        p2 = getattr(moon2.position, pos)
        v1 = getattr(moon1.velocity, pos)
        v2 = getattr(moon2.velocity, pos)

        if p1 > p2:
          setattr(moon1.velocity, pos, v1 -1)
          setattr(moon2.velocity, pos, v2 +1)

        if p1 < p2:
          setattr(moon1.velocity, pos, v1 +1)
          setattr(moon2.velocity, pos, v2 -1)

    # set positions
    for moon in self.moons:
      moon.update()

  def print_state(self):
    for m in self.moons:
      print(m)
    print()

  def get_energy(self):
    energy = 0
    for moon in self.moons:
      energy += moon.get_energy()
    return energy

  def __eq__(self, other):
    return all(
      (moon.position == original.position and 
      moon.velocity == original.velocity)
      for moon, original in zip(self.moons, other.moons)
    )


def read_input():
  moons = []
  with open('inputs/input12.txt') as f:
    data = f.read()
    for moon in data.split('\n'):
      cleaned_mooon = moon\
        .replace('<', '')\
        .replace('>', '')\
        .replace(' ', '')\
        .replace('=', '')\
        .replace('x', '')\
        .replace('y', '')\
        .replace('z', '')

      moon_position = Vector3(*map(int, cleaned_mooon.split(',')))
      moon_velocity = Vector3(0, 0, 0)
      moons.append(Moon(moon_position, moon_velocity))
  return moons
    

def day_12_a():
  s = Simulation(read_input())
  s.print_state()
  for i in range(1000):
    s.step()

  s.print_state()
  print(s.get_energy())

def day_12_b():
  initial = Simulation(read_input())
  s = Simulation(read_input())

  for i in range(1000000):
    s.step()
    if s == initial:
      print(i + 1)
      break
