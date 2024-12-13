import unittest
from itertools import combinations_with_replacement, product

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=7)


def parse(input_data):
    calibrations = []
    for line in input_data.splitlines():
        result, numbers = line.split(": ")
        numbers = list(map(int, numbers.split(" ")))
        result = int(result)
        calibrations.append((result, numbers))
    return calibrations


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def concat(a, b):
    return int(str(a) + str(b))


def bin_to_signs(bin, places):
    signs = []
    for _ in range(places):
        s = {
            0: '+',
            1: '*'
        }.get(bin & 1, '-')
        bin >>= 1
        signs.append(s)
    return signs


def is_possible(result, numbers):
    possibilities = 0
    places = len(numbers) - 1
    options = (1 << places) - 1
    for op in range(options + 1):
        sign = bin_to_signs(op, places)
        actual = numbers[0]
        for s, n in zip(sign, numbers[1:]):
            func = {
                '*': mul,
                '+': add
            }.get(s)
            actual = func(actual, n)
            if actual > result:
                break
        if actual == result:
            possibilities += 1
    return possibilities > 0


def part1(input_data):
    calib = parse(input_data)
    total = 0
    for result, numbers in calib:
        if is_possible(result, numbers):
            total += result
    return total


def is_possible2(result, numbers, with_concat=False):
    places = len(numbers) - 1
    available = '+*'
    if with_concat:
        available += '|'
    signs = list(product(available, repeat=places))
    for sign in signs:
        actual = numbers[0]
        for s, n in zip(sign, numbers[1:]):
            func = {
                '*': mul,
                '+': add,
                '|': concat
            }.get(s)
            actual = func(actual, n)
            if actual > result:
                break
        if actual == result:
            return True
    return False


def part2(input_data):
    calib = parse(input_data)
    total = 0
    for result, numbers in calib:
        if is_possible2(result, numbers, True):
            total += result
    return total


class Day7(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(3749, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual(11387, part2(puzzle.examples[0].input_data))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day7)
    unittest.TextTestRunner().run(suite)
