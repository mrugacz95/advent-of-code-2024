import unittest

from aocd.models import Puzzle
from tqdm import tqdm

puzzle = Puzzle(year=2024, day=17)

A = 0
B = 1
C = 2


def parse(input_data):
    reg, prog = input_data.split("\n\n")
    reg = reg.split("\n")
    prog = prog.split(": ")[1]
    registers = [int(r.split(": ")[1]) for r in reg]
    program = list(map(int, prog.split(",")))
    return registers, program


def part1(input_data):
    reg, prog = parse(input_data)
    output, reg = simulate(reg, prog)
    return ','.join(map(str, output))


def simulate(reg, prog):
    pointer = 0
    output = []

    def get_combo_value(operand):
        if 4 <= operand <= 6:
            return reg[operand - 4]
        elif operand == 7:
            raise ValueError("Invalid operand")
        return operand

    while pointer < len(prog):
        opcode = prog[pointer]
        operand = prog[pointer + 1]
        if opcode == 0:  # adv
            numerator = reg[A]
            denominator = pow(2, get_combo_value(operand))
            reg[A] = numerator // denominator
        elif opcode == 1:  # bxl
            b = reg[B]
            reg[B] = b ^ operand
        elif opcode == 2:  # bst
            combo = get_combo_value(operand)
            modulo = combo & 0b111
            reg[B] = modulo
        elif opcode == 3:  # jnz
            cond = reg[A]
            if cond != 0:
                pointer = operand
                continue
        elif opcode == 4:  # bxc
            b = reg[B]
            c = reg[C]
            reg[B] = b ^ c
        elif opcode == 5:  # out
            value = get_combo_value(operand) % 8
            output.append(value)
        elif opcode == 6:  # bdv
            numerator = reg[A]
            denominator = pow(2, get_combo_value(operand))
            reg[B] = numerator // denominator
        elif opcode == 7:  # cdv
            numerator = reg[A]
            denominator = pow(2, get_combo_value(operand))
            reg[C] = numerator // denominator
        pointer += 2
        # print(f'simulation after {opcode, operand}', reg)
    return output, reg


def part2_slow(input_data):
    reg, prog = parse(input_data)
    for a in range(500000):
        output, reg = simulate([a, 0, 0], prog)
        if output == prog:
            return a
    raise ValueError("Not found")


def part2(input_data):
    reg, prog = parse(input_data)
    expected = [2, 4, 1, 1, 7, 5, 1, 5, 0, 3, 4, 3, 5, 5, 3, 0]
    for a in tqdm(range(50_000, 100_000_000)):
        reg = [a, 0, 0]
        # prog = '2,4, 1,1, 7,5, 1,5, 0,3, 4,3, 5,5, 3,0'
        out = []
        # source
        while True:
            reg[B] = reg[A] & 0b111  # 2,4
            reg[B] = reg[B] ^ 1  # 1,1
            reg[C] = reg[A] // pow(2, reg[B])  # 7,5
            reg[B] = reg[B] ^ 5  # 1,5
            reg[A] = reg[A] // pow(2, 3)  # 0,3
            reg[B] = reg[B] ^ reg[C]  # 4,3,
            out.append(reg[B] % 8)  # 5,5
            if expected[:len(out)] != out:
                break
            if reg[A] == 0:  # 3,0,
                break
        if out == [2, 4, 1, 1, 7, 5, 1, 5, 0, 3, 4, 3, 5, 5, 3, 0]:
            return a
    raise ValueError("Not found")


def just_source(init_a):
    a = init_a
    out = []
    while True:
        b = ((a & 0b111) ^ 1)
        c = a // pow(2, b)
        a = a // 8
        b = (b ^ 5) ^ c
        out.append(b % 8)
        if a == 0:
            break
    return out

def dfs(prog):
    # during the search we find new numbers that has the same tail as expected
    # ..., 1225958, 153244, 19155, 2394, 299, 37, 4
    # prog, ..., [3,4,3,5,5,3,0], [4,3,5,5,3,0], [3,5,5,3,0], [5,5,3,0], [5,3,0], [3,0], [0]
    expected = prog
    queue = list(range(8))
    while len(queue) > 0:
        num = queue.pop(0)
        print(num)
        out = just_source(num)
        if expected[-len(out):] == out: # one numer closer
            for p in range(8):
                queue.append(num * 8 + p)
        else:
            continue
        if len(out) == len(expected):
            return num
    raise ValueError("Not found")


def part2_fast(input):
    reg, prog = parse(input)
    return dfs(prog)


class Day17(unittest.TestCase):

    def test_1(self):
        reg = [0, 0, 9]
        prog = [2, 6]
        output, out_reg = simulate(reg, prog)
        self.assertEqual(out_reg[B], 1)

    def test_2(self):
        reg = [10, 0, 0]
        prog = [5, 0, 5, 1, 5, 4]
        output, out_reg = simulate(reg, prog)
        self.assertEqual(output, [0, 1, 2])

    def test_3(self):
        reg = [2024, 0, 0]
        prog = [0, 1, 5, 4, 3, 0]
        output, out_reg = simulate(reg, prog)
        self.assertEqual(output, [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0])
        self.assertEqual(out_reg[A], 0)

    def test_4(self):
        reg = [0, 29, 0]
        prog = [1, 7]
        output, out_reg = simulate(reg, prog)
        self.assertEqual(out_reg[B], 26)

    def test_5(self):
        reg = [0, 2024, 43690]
        prog = [4, 0]
        output, out_reg = simulate(reg, prog)
        self.assertEqual(out_reg[B], 44354)

    def test_part1_example(self):
        self.assertEqual('4,6,3,5,6,3,5,2,1,0', part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        example = ("Register A: 2024\n"
                   "Register B: 0\n"
                   "Register C: 0\n"
                   "\n"
                   "Program: 0,3,5,4,3,0")
        self.assertEqual(117440, part2_slow(example))

    def test_part2(self):
        puzzle.answer_b = part2_fast(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day17)
    unittest.TextTestRunner().run(suite)
