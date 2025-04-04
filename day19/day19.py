import unittest
from functools import cache

from aocd.models import Puzzle
from tqdm import tqdm

puzzle = Puzzle(year=2024, day=19)

def parse(input_data):
    patterns, designs =  input_data.split('\n\n')
    patterns = tuple(patterns.split(', '))
    designs = designs.split('\n')
    return patterns, designs

def is_possible(patterns, design):
    if design == '':
        return True
    for pattern in patterns:
        if design.startswith(pattern):
            finished = is_possible(patterns, design[len(pattern):])
            if finished:
                return True
    return False

def part1(input_data):
    patterns, designs = parse(input_data)
    counter = 0
    for design in designs:
        possible = is_possible(patterns, design)
        if possible:
            counter += 1
    return counter

@cache
def count_possible(patterns, design):
    if design == '':
        return 1
    counter = 0
    for pattern in patterns:
        if design.startswith(pattern):
            possible_ways = count_possible(patterns, design[len(pattern):])
            counter += possible_ways
    return counter

def part2(input_data):
    patterns, designs = parse(input_data)
    counter = 0
    for design in tqdm(designs):
        possible_ways = count_possible(patterns, design)
        counter += possible_ways
    return counter


class Day19(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(6, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual(16, part2(puzzle.examples[0].input_data))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day19)
    unittest.TextTestRunner().run(suite)
