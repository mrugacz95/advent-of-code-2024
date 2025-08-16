import unittest

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=24)

def parse(input_data):
    initial = {}
    graph = {}

    initial, gates = input_data.split("\n\n")

    for line in initial.splitlines():
        variable, value = line.split(": ")
        graph[variable] = int(value)

    for line in gates.splitlines():
        gate = line.split(" ")
        lhs = gate[0]
        operator = gate[1]
        rhs = gate[2]
        result = gate[4]
        graph[result] = (lhs, operator, rhs)

    return graph


def calc_value(graph, node):
    current = graph[node]
    if type(current) == int:
        return current

    lhs, operator, rhs = current
    lhs_value = calc_value(graph, lhs)
    rhs_value = calc_value(graph, rhs)

    if operator == "AND":
        return lhs_value & rhs_value
    elif operator == "OR":
        return lhs_value | rhs_value
    elif operator == "XOR":
        return lhs_value ^ rhs_value

    raise RuntimeError(f"Unknown operator: {operator}")



def part1(input_data):
    graph = parse(input_data)

    bits = sorted(filter(lambda x: x[0] == 'z' , graph.keys()), reverse=True)

    value = 0
    for bit in bits:
        value <<= 1
        value |= calc_value(graph, bit)
        print(bit, value)

    return value


def part2(input_data):
    data = parse(input_data)
    return -1


class Day24(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(4, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual(0, part2(puzzle.examples[0].input_data))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day24)
    unittest.TextTestRunner().run(suite)