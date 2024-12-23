import unittest
from collections import Counter

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=1)


def parse(input_data):
    return tuple(zip(*map(lambda line: map(int, line.split("   ")), input_data.split("\n"))))


def part1(input_data):
    l, r = parse(input_data)
    return sum(map(lambda l: abs(l[0] - l[1]), zip(sorted(l), sorted(r))))


def part2(input_data):
    l, r = parse(input_data)
    counter = Counter(r)
    return sum(map(lambda key: key * counter[key], l))


class Day1(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(11, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual(31, part2(puzzle.examples[0].input_data))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day1)
    unittest.TextTestRunner().run(suite)
