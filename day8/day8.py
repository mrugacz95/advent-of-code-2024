import unittest
from collections import defaultdict
from itertools import combinations

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=8)


def parse(input_data):
    grid = input_data.splitlines()
    pos = defaultdict(list)
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c != '.':
                pos[c].append((y, x))
    return pos, len(grid) - 1, len(grid[0]) - 1


def print_grid(positions, antinodes):
    inv_pos = {}
    for c, l in positions.items():
        for p in l:
            inv_pos[p] = c
    for y in range(12):
        for x in range(12):
            if (y, x) in antinodes:
                print('#', end='')
            elif (y, x) in inv_pos:
                print(inv_pos[(y, x)], end='')
            else:
                print('.', end='')
        print()


def part1(input_data):
    positions, y_max, x_max = parse(input_data)
    antinodes = set()
    for antenna, locations in positions.items():
        for (y1, x1), (y2, x2) in combinations(locations, 2):
            dy = y1 - y2
            dx = x1 - x2
            a1 = (y1 + dy, x1 + dx)
            a2 = (y2 - dy, x2 - dx)
            if 0 <= a1[0] <= y_max and 0 <= a1[1] <= x_max:
                antinodes.add(a1)
            if 0 <= a2[0] <= y_max and 0 <= a2[1] <= x_max:
                antinodes.add(a2)
    print_grid(positions, antinodes)
    return len(antinodes)


def part2(input_data):
    positions, y_max, x_max = parse(input_data)
    antinodes = set()
    all_positions = set()
    for antenna, locations in positions.items():
        all_positions.update(locations)
    for antenna, locations in positions.items():
        for (y1, x1), (y2, x2) in combinations(locations, 2):
            dy = y1 - y2
            dx = x1 - x2

            def harmonics(y, x, d):
                mul = 1
                while True:
                    if 0 <= y + d * dy * mul <= y_max and 0 <= x + d * dx * mul <= x_max:
                        yield y + d * dy * mul, x + d * dx * mul
                        mul += 1
                    else:
                        break

            for a1 in harmonics(y1, x1, 1):
                antinodes.add(a1)
            for a1 in harmonics(y2, x2, -1):
                antinodes.add(a1)
    antinodes.update(all_positions)
    print_grid(positions, antinodes)
    return len(antinodes)


class Day8(unittest.TestCase):

    def test_simple(self):
        example = """..........
..........
..........
....a.....
..........
.....a....
..........
..........
..........
.........."""
        self.assertEqual(2, part1(example))

    def test_harder(self):
        example = """..........
..........
..........
....a.....
........a.
.....a....
..........
......A...
..........
.........."""
        self.assertEqual(5, part1(example))

    def test_part1_example(self):
        self.assertEqual(14, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_simple(self):
        example = """T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
.........."""
        self.assertEqual(9, part2(example))

    def test_part2_example(self):
        self.assertEqual(34, part2(puzzle.examples[0].input_data))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day8)
    unittest.TextTestRunner().run(suite)
