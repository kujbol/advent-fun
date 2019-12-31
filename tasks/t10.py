from collections import defaultdict
from math import sqrt, atan2, pi

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


with open('input10.txt') as f:
  data = f.read().split('\n')
  
def vector_length(v):
  return sqrt(v[0]*v[0] + v[1]*v[1])

def distance(p1, p2):
  return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) 

def isBetween(p1, p2, p3):
  return (
    min(p1[0], p3[0]) <= p2[0] <= max(p1[0], p3[0]) and 
    min(p1[1], p3[1]) <= p2[1] <= max(p1[1], p3[1])
  )

def iterateAsteroids(data, filter_out=None):
  if not filter_out:
    filter_out = set()
  for y, row in enumerate(data):
    for x, value in enumerate(row):
      if value == '#' and (x, -y) not in filter_out:
        yield int(x), int(-y)

def generate_rays(asteroids, start_asteroid):
  rays = defaultdict(list)

  for asteroid in asteroids: 
    product = atan2(asteroid[0] - start_asteroid[0], asteroid[1]  - start_asteroid[1])
    product-= pi
    if product < -pi:
      product += 2*pi
    rays[product].append(asteroid)

  
  for ray_value in rays.values():
    ray_value.sort(
      key=cmp_to_key(lambda x, y: distance(y, start_asteroid) - distance(x, start_asteroid))
    )
  return rays
  return {
    letter: item[1]
    for letter, item in zip(
      'abcdefghijklmnoprstuwvyz', 
      sorted(rays.items(), key=lambda item: item[0])
    )
  }
  
def day_10_a():
  asteroids = list(iterateAsteroids(data))
  max_rays = 0
  for y in range(len(data)):
    for x in range(len(data[y])):
      start_asteroid = (x, -y)
      start_asteroids = [asteroid for asteroid in asteroids if asteroid != start_asteroid ]
      rays = generate_rays(start_asteroids, start_asteroid)
      if len(rays) > max_rays:
        max_rays = len(rays)
        print(start_asteroid)
  

def day_10_b():
  start_asteroid = (20, -18)
  # start_asteroid = (11, -13)
  asteroids = list(iterateAsteroids(data))
  asteroids = [asteroid for asteroid in asteroids if asteroid != start_asteroid ]

  rays = generate_rays(asteroids, start_asteroid)

  it = 0

  # debug print
  # for y in range(len(data)):
  #   row = ''
  #   for x in range(len(data[y])):
  #     found = False
  #     for asteroid in asteroids:
  #       if asteroid == (x, -y):
  #         for ray, ray_value in rays.items():
  #           if asteroid in ray_value:
  #             row = row + str(ray)
  #             found = True
  #     if start_asteroid == (x, -y):
  #       row = row + 's'
  #       found = True
  #     if not found:
  #       row = row + '.'
  #   print(row)

  while True:
    changed = False
    for ray_value, ray in sorted(rays.items(), key=lambda item: item[0]):
      if ray:
        it+= 1
        print(f'{it}: {ray.pop()}')
        changed = True
    
    if changed == False:
      return
