import re
import unittest

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=3)


def parse(input_data):
    matches = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', input_data)
    return [(int(l), int(r)) for (l, r) in matches]


def part1(input_data):
    data = parse(input_data)
    return sum(map(lambda x: x[0] * x[1], data))


def part2(input_data):
    matches = re.findall(r'(mul\(\d{1,3},\d{1,3}\))|(do\(\))|(don\'t\(\))', input_data)
    numbers = []
    enabled = True
    for match in matches:
        if match[0] != "" and enabled:
            mul = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', match[0])
            (l, r) = mul[0]
            numbers.append((int(l), int(r)))
        elif match[1] != "":
            enabled = True
        elif match[2] != "":
            enabled = False

    return sum(map(lambda x: x[0] * x[1], numbers))


class Day3(unittest.TestCase):
    def test_part1_example(self):
        self.assertEqual(161, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        example = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
        self.assertEqual(48, part2(example))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)



if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day3)
    unittest.TextTestRunner().run(suite)
