from dataclasses import dataclass
from collections import defaultdict
from typing import List
import math
import copy

from bisect import bisect_left

@dataclass
class Element:
  name: str
  quantity: int

@dataclass
class GraphNode:
  product: Element
  substracts: List[Element]

def extract_element(raw_data):
  quantity, name = raw_data.strip().split(' ')
  return Element(name, int(quantity))

def load_data():
  graph = {}

  with open('inputs/input14.txt') as f:
    data = f.read()
    for row in data.split('\n'):
      raw_substracts, raw_product = row.split('=>')
      product = extract_element(raw_product)
      substracts = []
      for raw_substract in raw_substracts.split(','):
        substracts.append(extract_element(raw_substract))

      graph[product.name] = GraphNode(product, substracts)

  return graph


class ChemicalReactor:
  def __init__(self, graph, start_value=1):
    self.graph = graph
    self.needs = [Element('FUEL', start_value)]
    self.leftovers = defaultdict(lambda: 0)
    self.ore = 0

  def calculate_ore_need(self):
    while self.needs:
      need = self.needs.pop(0)
      # print(f'Before leftovers {need}, {self.leftovers}')
      if need.name == 'ORE':
        self.ore += need.quantity
        continue 
      
      need = self.fill_need_from_leftovers(need)
      # print(f'After leftovers {need}, {self.leftovers}')
      product = copy.deepcopy(self.graph[need.name].product)
      substracts = copy.deepcopy(self.graph[need.name].substracts)

      recip_multiplier = math.ceil(need.quantity / product.quantity)
      if recip_multiplier == 0:
        continue

      product.quantity *= recip_multiplier
      for substract in substracts:
        substract.quantity *= recip_multiplier
        substract = self.fill_need_from_leftovers(substract)
        self.add_need(substract)

      self.leftovers[product.name] += (product.quantity - need.quantity)
    return self.ore

  def fill_need_from_leftovers(self, need: Element):
    if self.leftovers.get(need.name):
      used = min(need.quantity, self.leftovers[need.name])
      self.leftovers[need.name] -= used
      need.quantity -= used

    return need

  def add_need(self, need: Element):
    for saved_need in self.needs:
      if need.name == saved_need.name:
        saved_need.quantity += need.quantity
        return

    self.needs.append(need)


def day_14_a():
  graph = load_data()
  r = ChemicalReactor(graph, start + i)
  dupa = r.calculate_ore_need()
      
def day_14_b():
  graph = load_data()

  start = 5613130
  end = 56131300

  class BiSectWrapper:
    def __getitem__(self, val):
      r = ChemicalReactor(graph, val)
      result = r.calculate_ore_need()
      print(result)
      return result

  result = bisect_left(BiSectWrapper(), 1000000000000, start, end)
  print(result - 1)
  
day_14_b()