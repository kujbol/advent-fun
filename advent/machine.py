class Machine:
  def __init__(self, code_file_name, name):
    self.inputs = []
    self.name = name
    self.it = 0
    with open(code_file_name) as f:
      data = f.read().split(',')
      data = [int(d) for d in data]
      self.data = data

  def set_input(self, value):
    self.inputs.append(value)

  def run(self):
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
      # print(parameter)
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

    it = self.it
    while True:
      op_code = self.data[it]
      op_code, parameter_types = decode_op_code(op_code)
      if op_code == 99:
        raise StopIteration(self.data[0])
      # print(parameter_types, self.data[it + 1: it + op_code_length[op_code] + 1])
      
      parameters = [
        value if typ == 1 else self.data[value]
        for typ, value in zip(parameter_types, self.data[it + 1: it + op_code_length[op_code]+1])
      ]
      extra_parameters = {}
      # print(f'Running {self.name}: {op_code}, with: {parameters}')
      it, result = op_code_mapping[op_code](it, *parameters, **extra_parameters)

      self.it = it
      if result:
        return result
