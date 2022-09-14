
from queue import Queue
from operator import add, mul, floordiv, mod, eq

class ALU:
    def __init__(self, code):
        self.regs = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0,
        }

        self.ip = 0
        self.code = code
        self.input = Queue()

    @property
    def value(self):
        if self.code[self.ip][2] in self.regs:
            return self.regs[self.code[self.ip][2]]
        else:
            return int(self.code[self.ip][2])
        
    def run(self):
        while True:
            if self.ip == len(self.code):
                return

            op = self.code[self.ip][0]
            reg = self.code[self.ip][1]

            if op == 'inp':
                self.regs[reg] = self.input.get()
            elif op == 'add':
                self.regs[reg] += self.value
            elif op == 'mul':
                self.regs[reg] *= self.value
            elif op == 'div':
                self.regs[reg] //= self.value
            elif op == 'mod':
                self.regs[reg] %= self.value
            elif op == 'eql':
                self.regs[reg] = 1 if self.regs[reg] == self.value else 0

            print(f'{self.code[self.ip]} --> {self.regs}')
            self.ip += 1


class Instruction:
    operations = {'add': add, 'mul': mul, 'div': floordiv, 'mod': mod, 'eql': eq}
    oprepr = {'add': '+', 'mul': '*', 'div': '//', 'mod': '%', 'eql': '=='}

    def __init__(self, instr, op1=None, op2=None, index=None):
        self.instr = instr
        self.index = index
        #self._op = self.operations[instr]
        self.op1 = op1
        self.op2 = op2

    def __repr__(self):
        #return f'<Instruction({self.instr}, {self.op1}, {self.op2})>'
        if self.instr == 'inp':
            return f'inp[{self.index}]'
        else:
            return f'({self.op1} {self.oprepr[self.instr]} {self.op2})'

    def simplify(self):
        if self.op1 is None or self.op2 is None:
            return self

        op1 = self.op1#.simplify() if not isinstance(self.op1, int) else self.op1
        op2 = self.op2#.simplify() if not isinstance(self.op2, int) else self.op2
        
        op1_const = isinstance(op1, int)
        op2_const = isinstance(op2, int)


        if op1_const and op2_const:
            return self.operations[self.instr](op1, op2)
        elif op1_const and self.instr in ('add', 'mul', 'eql'):
            return Instruction(self.instr, op2, op1).simplify()


        if self.instr == 'add':
            if op2 == 0:
                return op1
            elif not op1_const and op1.instr == 'add':
                return Instruction('add', op1.op1, op1.op2 + op2)
            else:
                return self
        elif self.instr == 'mul':
            if op2 == 0:
                return 0
            elif op2 == 1:
                return op1
            # elif not op1_const and op1.instr == 'mul':
            #     return Instruction('mul', op1.op1, op1.op2 * op2)
            else:
                return self
        elif self.instr == 'div':
            if op2 == 1:
                return op1
            # elif not op1_const and op1.instr == 'div':
            #     return Instruction('div', op1.op1, op1.op2 * op2)
            else:
                return self
        # elif self.instr == 'mod':
        #     return op1 if op1.op1.instr == 'inp' else op1.op2
        elif self.instr == 'eql':
            offset = op1.op2
            if op2_const or offset > 9:
                return 0
            else:
                print(offset)
                return 1
        else:
            return self
            # return Instruction(self.instr, self.op1.simplify(), self.op2.simplify())




example = '''inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2'''

with open('inputs/day-24-input.txt') as input_file:
    data = input_file.read()


def parse(line):
    parts = line.split()
    if len(parts) == 2:
        operand = None
    elif parts[2].isdigit() or parts[2].startswith('-'):
        operand = int(parts[2])
    else:
        operand = parts[2]
    return parts[0], parts[1], operand

regs = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
index = 0
for instr, reg, op in [parse(line) for line in data.split('\n')]:
    if instr == 'inp':
        regs[reg] = Instruction(instr, index=index)
        index += 1
    else:
        if not isinstance(op, int):
            op = regs[op]

        regs[reg] = Instruction(instr, regs[reg], op).simplify()

print(regs['z'])


sn = '13579246899999'

code = [l.split() for l in example.split('\n')]
# print(code)

# alu = ALU(code)
# for c in sn:
#     alu.input.put(int(c))
# alu.input.put(5)
# alu.run()
# print(alu.regs)

# inp w
# mul x 0   ; (x = 0)
# add x z   ; x = z
# mod x 26  ; x = x % 26 
# div z 1   ; do nothing
# add x 11  ; x = (z % 26) + 11
# eql x w   ; x == w ? w == ()
# eql x 0   ; x != 0
# mul y 0   ; y = 0
# add y 25  ; y = 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 5
# mul y x
# add z y


# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 13
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 5
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 12
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 1
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 15
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 15
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 10
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 2
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -1
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 2
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 14
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 5
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -8
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 8
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -7
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 14
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -8
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 12
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 11
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 7
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -2
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 14
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -2
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 13
# mul y x
# add z y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -13
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 6
# mul y x
# add z y