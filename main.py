import operator
from functools import reduce
from itertools import permutations
from collections import Counter, defaultdict
from math import floor

from advent.machine import Machine

# 1
def day_1_a():
  with open('input1.txt') as f:
    data = f.read().split('\n')
    data = [floor(float(d)/3) - 2 for d in data]

  print(reduce(lambda x, y: x+y, data))

def day_1_b():
  with open('input1.txt') as f:
    data = f.read().split('\n')
    data = [float(d) for d in data]
  
  def recursive_fuel(mass):
    sum_of_mas = 0
    mass = floor(mass / 3) - 2 
    while(mass > 0):
      sum_of_mas += mass
      mass = floor(mass / 3) - 2 
    return sum_of_mas

  sum_of_all = 0
  for d in data:
    sum_of_all += recursive_fuel(d)

  print(sum_of_all)

# 2

def day_2_a(nun=12, verb=2):
  with open('input2.txt') as f:
    data = f.read().split(',')
    data = [int(d) for d in data]

  op_code_mapping = {
    1: operator.add,
    2: operator.mul,
  }

  data[1] = nun
  data[2] = verb

  it = 0
  while True:
    op_code = data[it]
    if op_code == 99:
      return data[0]
      
    a, b = data[data[it+1]], data[data[it+2]]
    z = data[it+3]

    it += 4
    if op_code == 99:
      print(data[0])
      return data[0]

    result = op_code_mapping[op_code](a, b)
    data[z] = result
  
def day_2_b():
  for x in range(100):
    for y in range(100):
      print(x, y)
      if day_2_a(x, y) == 19690720:
        return x, y


def day_3_a():
  with open('input3.txt') as f:
    l1, l2 = f.read().split('\n')
    l1, l2 = l1.split(','), l2.split(',')

  def calculate_new_point(point, direction, value):
    vector = {
      'R': (value, 0),
      'L': (-value, 0),
      'U': (0, value),
      'D': (0, -value)
    }[direction]

    return (point[0] + vector[0], point[1] + vector[1])

  def calculate_sections(instructions):
    last_point = (0, 0)
    sections = []

    for inst in instructions:
      direction, value = inst[0], int(inst[1:])
      new_point = calculate_new_point(last_point, direction, value)
      sections.append((last_point, new_point))
      last_point = new_point

    return sections

  def get_intersection(line1, line2):
    def is_horizontal(a, b):
      return a[0] == b[0]

    def is_vertical(a, b):
      return a[1] == b[1]

    if is_horizontal(*line1) and is_horizontal(*line2):
      return None

    if is_vertical(*line1) and is_vertical(*line2):
      return None 
    
    if is_horizontal(*line1):
      tmp = line1
      line1 = line2
      line2 = tmp
    

    
    if min(line1[0][0], line1[1][0]) < line2[0][0] < max(line1[0][0], line1[1][0]):
      if min(line2[0][1], line2[1][1]) < line1[0][1] < max(line2[0][1], line2[1][1]):
        return (line2[0][0], line1[0][1])
  
  l1_sections = calculate_sections(l1)
  l2_secitons = calculate_sections(l2)
  min_result = 10000000000
  for l1 in l1_sections:
    for l2 in l2_secitons:
      result = get_intersection(l1, l2)
      if result:
        print(result)
      if result and min_result > abs(result[0]) + abs(result[1]):
        min_result = abs(result[0]) + abs(result[1])

  return min_result

def day_3_b():
  with open('input3.txt') as f:
    l1, l2 = f.read().split('\n')
    l1, l2 = l1.split(','), l2.split(',')

  def calculate_new_point(point, direction, value):
    vector = {
      'R': (value, 0),
      'L': (-value, 0),
      'U': (0, value),
      'D': (0, -value)
    }[direction]

    return (point[0] + vector[0], point[1] + vector[1])

  def calculate_sections(instructions):
    last_point = (0, 0)
    prev_value = 0
    sections = []
    distances = []

    for inst in instructions:
      direction, value = inst[0], int(inst[1:])
      new_point = calculate_new_point(last_point, direction, value)
      sections.append((last_point, new_point))
      distances.append(prev_value)
      prev_value += value
      last_point = new_point

    return sections, distances

  def get_intersection(line1, line2):
    def is_horizontal(a, b):
      return a[0] == b[0]

    def is_vertical(a, b):
      return a[1] == b[1]

    if is_horizontal(*line1) and is_horizontal(*line2):
      return None

    if is_vertical(*line1) and is_vertical(*line2):
      return None 
    
    if is_horizontal(*line1):
      tmp = line1
      line1 = line2
      line2 = tmp
    
    if min(line1[0][0], line1[1][0]) < line2[0][0] < max(line1[0][0], line1[1][0]):
      if min(line2[0][1], line2[1][1]) < line1[0][1] < max(line2[0][1], line2[1][1]):
        distance = abs(line1[0][0] - line2[0][0]) + abs(line2[0][1] - line1[0][1]) 
        return (line2[0][0], line1[0][1], distance)
  
  l1_sections, l1_distances = calculate_sections(l1)
  l2_sections, l2_distances = calculate_sections(l2)
  min_result = 10000000000
  for l1, dist1 in zip(l1_sections, l1_distances):
    for l2, dist2 in zip(l2_sections, l2_distances):
      result = get_intersection(l1, l2)
      if result:
        print(result, dist1, dist2)
      if result and min_result > dist1 + dist2 + result[2]:
        min_result = dist1 + dist2 + result[2]

  return min_result

def day_4_a_and_b(): 
  counter = 0
  for i in range(193651, 649729 + 1):
    number = str(i)
    same = False
    problem = False
    for prev_digit, digit in zip(number[:-1], number[1:]):
      if prev_digit > digit:
        problem = True
        continue
    
    is_any_2 = [k for k, v in Counter(number).items() if v == 2]
    if problem == False and any(is_any_2):
      counter += 1
  
  return counter


def day_5_a_b(
  file_name='input5.txt', 
  inputs=None, 
  results=False, 
  yield_mode=False
):
  if results:
    results = []
  def decode_op_code(op_code):
    decoded_op_code = []
    for i in range(5):
      decoded_op_code.append(op_code % 10)
      op_code = op_code // 10
    
    op_code = decoded_op_code[0]+10*decoded_op_code[1]
    length = op_code_length[op_code]


    strange = [4, 5, 6]
    z_parameter = [1] if op_code not in strange else [decoded_op_code[3]]
    return op_code, decoded_op_code[2:2 + length - 1] + z_parameter  

  def opcode_1(it, data, a, b, z,  *not_used_params) -> int:
    data[z] = a + b
    return it + 4, None

  def opcode_2(it, data, a, b, z, *not_used_params) -> int:
    data[z] = a * b
    return it + 4, None

  def opcode_3(it, data, parameter, *not_used_params, yield_input=None):
    if yield_input:
      user_input = yield_input
    elif inputs:
      user_input = inputs.pop(0)
    else:
      user_input = int(input())
    data[parameter] = user_input
    return it + 2, None

  def opcode_4(it, data, parameter, *not_used_params) -> int:
    if type(results) == list:
      results.append(parameter)
    else:
      print(parameter)
    return it + 2, parameter

  def opcode_5(it, data, condition, parameter, *not_used_params):
    if condition != 0:
      return parameter, None
    return it + 3, None

  def opcode_6(it, data, condition, parameter, *not_used_params):
    if condition == 0:
      return parameter, None
    return it + 3, None

  def opcode_7(it, data, first, second, parameter):
    if first < second:
      data[parameter] = 1
    else:
      data[parameter] = 0
    return it + 4, None

  def opcode_8(it, data, first, second, parameter):
    if first == second:
      data[parameter] = 1
    else:
      data[parameter] = 0
    return it + 4, None


  with open(file_name) as f:
    data = f.read().split(',')
    data = [int(d) for d in data]

  op_code_mapping = {
    1: opcode_1,
    2: opcode_2,
    3: opcode_3,
    4: opcode_4,
    5: opcode_5,
    6: opcode_6,
    7: opcode_7,
    8: opcode_8,
  }

  op_code_length = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    99: 0
  }

  it = 0
  while True:
    op_code = data[it]
    # print(f'iteration: {it}, opcode: {op_code}')
    op_code, parameter_types = decode_op_code(op_code)
    if op_code == 99:
      if results:
        return results
      return data[0]
    # print(parameter_types, data[it + 1: it + op_code_length[op_code] + 1])
    
    parameters = [
      value if typ == 1 else data[value]
      for typ, value in zip(parameter_types, data[it + 1: it + op_code_length[op_code]+1])
    ]
    extra_parameters = {}

    if yield_mode and op_code == 3:
      yield_input = yield
      print(yield_input)
      extra_parameters['yield_input'] = yield_input

    # print(f'Running: {op_code}, with: {parameters}')
    it, result = op_code_mapping[op_code](it, data, *parameters, **extra_parameters)

    if yield_mode and result != None:
      yield result
    

def day_6_a():
  graph = defaultdict(list)

  with open('input6.txt') as f:
    orbits = f.read().split('\n')
    for orbit in orbits:
      a, b = orbit.split(')')
      graph[a].append(b)

  queue = ['COM']
  orbiting = {'COM': 0}
  def bfs():
    while queue:
      node = queue.pop(0)
      for neighbour in graph[node]:
        orbiting[neighbour] = orbiting[node] + 1
        queue.append(neighbour)
  
  bfs()
  return sum(orbiting.values())

def day_6_b():
  graph = defaultdict(list)

  with open('input6.txt') as f:
    orbits = f.read().split('\n')
    for orbit in orbits:
      a, b = orbit.split(')')
      graph[a].append(b)
      graph[b].append(a)

  queue = ['YOU']
  orbiting = {'YOU': 0}
  def bfs():
    while queue:
      node = queue.pop(0)
      for neighbour in graph[node]:
        if neighbour not in orbiting:
          orbiting[neighbour] = orbiting[node] + 1
          queue.append(neighbour)
  
  bfs()
  return orbiting['SAN']


def day_7_a():
  max_result = 0
  for permutation in list(permutations(range(5, 10), 5)):
    actual_value = 0
    for value in permutation:
      results = day_5_a_b(
        'input7.txt', inputs=[value, actual_value], results=True
      )
      actual_value = results[0]

    print(permutation, results[0])
    if results[0] > max_result:
      max_result = results[0]
      max_permutation = permutation
  
  print(max_result)


def day_7_a_with_machine():
  max_result = 0
  for permutation in list(permutations(range(5), 5)):
    actual_value = 0
    for value in permutation:
      m = Machine('input7.txt')
      m.set_input(value)
      m.set_input(actual_value)
      try:
        actual_value = m.run()
      except StopIteration as e:
        actual_value = e.args[0]
    
    print(permutation, actual_value)
    if actual_value > max_result:
      max_result = actual_value
  
  print(max_result)

def day_7_b():
  max_result = 0
  check_permutations = list(permutations(range(5, 10), 5))
  # check_permutations = [[9,7,8,5,6], ]
  for permutation in check_permutations:
    machines = []
    actual_value = 0
    is_working = True
    for value, name in zip(permutation, 'abcde'):
      m = Machine('input7.txt', name)
      m.set_input(value)
      m.set_input(actual_value)
      try:
        actual_value = m.run()
      except StopIteration as exc:
        pass
      machines.append(m)

    last_thruster = actual_value
    while is_working:
      for m in machines:
        m.set_input(actual_value)
        try:
          actual_value = m.run()
        except StopIteration as exc:
          if (max_result < last_thruster):
            max_result = last_thruster
          is_working = False
      last_thruster = actual_value
    
    print(permutation, last_thruster)

  print(max_result)

day_7_b()