import unittest
from os.path import split

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=25)


def rot(arr):
    """Rotate a 2D array clockwise."""
    return [''.join(row) for row in zip(*arr[::-1])]


def encode(arr):
    return [len(list(filter(lambda x: x == '#', column))) - 1 for column in rot(arr)]


def parse(input_data):
    objects = input_data.split("\n\n")
    locks = []
    keys = []
    for obj in objects:
        current = obj.split("\n")
        encoded = encode(current)
        if '.' in current[0] and '.' not in current[-1]:  # key
            keys.append(encoded)
        elif '.' not in current[0] and '.' in current[-1]:  # lock
            locks.append(encoded)
        else:
            raise ValueError(f"Invalid object format: {obj}")

    return locks, keys


def part1(input_data):
    fits = 0
    locks, keys = parse(input_data)
    for lock in locks:
        for key in keys:
            def match():
                for l,k in zip(lock, key):
                    if l + k >= 6:
                        return False
                return True
            if match():
                fits += 1
    return fits


def part2(input_data):
    data = parse(input_data)
    return -1


class Day25(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(3, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual(0, part2(puzzle.examples[0].input_data))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day25)
    unittest.TextTestRunner().run(suite)
