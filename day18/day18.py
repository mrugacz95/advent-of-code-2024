import unittest

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=18)

def parse(input_data):
    return input_data


def part1(input_data):
    data = parse(input_data)
    return -1


def part2(input_data):
    data = parse(input_data)
    return -1


class Day18(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(0, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual(0, part2(puzzle.examples[0].input_data))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day18)
    unittest.TextTestRunner().run(suite)
