import os

class Memory(dict):
  def __getitem__(self, key):
      if isinstance( key, slice ):
        #Get the start, stop, and step from the slice
        return [self[ii] for ii in range(*key.indices(len(self)))]
      try:
        return super().__getitem__(key)
      except KeyError:
        return 0

class Machine:
  def __init__(self, code_or_path, name, debug=False):
    self.inputs = []
    self.name = name
    self.it = 0
    self.relative_base = 0
    self.debug = debug

    if os.path.exists(code_or_path):
      with open(code_or_path) as f:
        data = f.read().split(',')
    else:
      data = code_or_path.split(',')

    data = {it: int(d) for it, d in enumerate(data)}
    self.data = Memory(data)

  def set_input(self, value):
    self.inputs.append(value)

  def run(self, print_results=False):
    def calculate_parameters(op_code, parameter_types):

      parameters = []
      original_parameters = self.data[it + 1: it + op_code_length[op_code] + 1]
      for typ, value in zip(parameter_types, original_parameters):
        if typ == 1:
          parameters.append(value)
        elif typ == 2:
          # relative mode
          parameters.append(self.data[value + self.relative_base])
        else:
          # position mode
          parameters.append(self.data[value])

      if op_code in [1, 2, 3, 7, 8]:
        if parameter_types[-1] == 0:
          parameters[-1] = original_parameters[-1]
        elif parameter_types[-1] == 2:
          parameters[-1] = original_parameters[-1] + self.relative_base

      return parameters
    
    def decode_op_code(op_code):
      decoded_op_code = []
      for i in range(5):
        decoded_op_code.append(op_code % 10)
        op_code = op_code // 10
      
      # print(f'Decoded opcode: {op_code}, {self.it}, {self.data}')
      op_code = decoded_op_code[0]+10*decoded_op_code[1]
      length = op_code_length[op_code]

      return op_code, decoded_op_code[2:2 + length]

    def opcode_1(it, a, b, z,  *not_used_params):
      self.data[z] = a + b
      return it + 4, None

    def opcode_2(it, a, b, z, *not_used_params):
      self.data[z] = a * b
      return it + 4, None

    def opcode_3(it, parameter, *not_used_params):
      if self.inputs:
        user_input = self.inputs.pop(0)
      else:
        print('zjebane', self.data, it)
        raise StopIteration(1)
        user_input = int(input())
      
      self.data[parameter] = user_input
      return it + 2, None

    def opcode_4(it, parameter, *not_used_params):
      return it + 2, parameter

    def opcode_5(it, condition, parameter, *not_used_params):
      if condition != 0:
        return parameter, None
      return it + 3, None

    def opcode_6(it, condition, parameter, *not_used_params):
      if condition == 0:
        return parameter, None
      return it + 3, None

    def opcode_7(it, first, second, parameter):
      if first < second:
        self.data[parameter] = 1
      else:
        self.data[parameter] = 0
      return it + 4, None

    def opcode_8(it, first, second, parameter):
      if first == second:
        self.data[parameter] = 1
      else:
        self.data[parameter] = 0

      return it + 4, None

    def opcode_9(it, parameter):
      self.relative_base += parameter
      return it + 2, None

    op_code_mapping = {
      1: opcode_1,
      2: opcode_2,
      3: opcode_3,
      4: opcode_4,
      5: opcode_5,
      6: opcode_6,
      7: opcode_7,
      8: opcode_8,
      9: opcode_9,
    }

    op_code_to_name = {
      1: "add",
      2: "mul",
      3: "input",
      4: "return",
      5: "if != 0",
      6: "if == 0",
      7: "if a<b",
      8: "if a==b",
      9: "change relateive",
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
      9: 1,
      99: 0
    }

    it = self.it
    while True:
      op_code = self.data[it]
      op_code, parameter_types = decode_op_code(op_code)
      if op_code == 99:
        raise StopIteration(self.data[0])

      parameters = calculate_parameters(op_code, parameter_types)
      if self.debug:
        print(f'Running {self.name}: {op_code_to_name.get(op_code)}: {op_code}, with: {parameters}, of type: {parameter_types}, it: {self.it}, original_data: {self.data[it + 1: it + op_code_length[op_code] + 1]}')
      it, result = op_code_mapping[op_code](it, *parameters)

      self.it = it
      if result is not None:
        if print_results:
          print(result)
        else:
          return result
