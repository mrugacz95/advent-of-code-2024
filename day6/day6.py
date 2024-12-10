import unittest
from copy import deepcopy

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=6)


def parse(input_data):
    grid = list(map(lambda x: list(x), input_data.splitlines()))

    def find_pos():
        for y, line in enumerate(grid):
            for x, c in enumerate(line):
                if c == '^':
                    return y, x
        raise RuntimeError()

    return grid, find_pos()


def rotate(dir):
    return {
        'v': '<',
        '^': '>',
        '<': '^',
        '>': 'v'
    }.get(dir)


def dir_to_delta(dir):
    return {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1),
    }.get(dir)


def part1(input_data):
    grid, (y, x) = parse(input_data)
    visited = set()
    while True:
        visited.add((y, x))
        dir = grid[y][x]
        (dy, dx) = dir_to_delta(dir)
        if (0 > y + dy or y + dy >= len(grid)) or (0 > x + dx or x + dx >= len(grid[0])):
            break
        if grid[y + dy][x + dx] == '#':
            grid[y][x] = rotate(dir)
            continue
        grid[y + dy][x + dx] = dir
        grid[y][x] = 'X'
        y, x = y + dy, x + dx
        # for line in grid:
        #     print(''.join(line))
        # print()
    return len(visited)


def simulate(grid, y, x, dir, oy, ox):
    visited = set()
    while True:
        if (y, x, dir) in visited:
            return True, visited
        visited.add((y, x, dir))
        (dy, dx) = dir_to_delta(dir)
        if (0 > y + dy or y + dy >= len(grid)) or (0 > x + dx or x + dx >= len(grid[0])):
            return False, visited
        if grid[y + dy][x + dx] == '#' or (y + dy == oy and x + dx == ox):
            dir = rotate(dir)
            continue
        y, x = y + dy, x + dx
    raise RuntimeError()


def part2(input_data):
    grid, (y, x) = parse(input_data)
    dir = grid[y][x]
    count = 0
    _, visited = simulate(grid, y, x, dir,-1,-1)
    to_consider = set()
    for oy, ox, _ in visited:
        to_consider.add((oy, ox))
    for idx, (oy, ox) in enumerate(to_consider):
        if (oy, ox) == (y, x):  # skip start pos
            continue
        if grid[oy][ox] == '#':  # skip already taken
            continue
        looped, _ = simulate(grid, y, x, dir, oy, ox)
        if looped:
            count += 1
    return count


class Day6(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(41, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_loop_detection(self):
        result, _ = simulate([
            [".", ".", ".", "."],
            [".", ".", ".", "#"],
            ["#", ".", ".", "."],
            [".", ".", "#", "."]
        ],
            1,
            1, '^', 0, 1)
        self.assertEqual(True, result)

    def test_loop_detection2(self):
        result, _ = simulate([
            [".", ".", ".", "."],
            [".", "^", ".", "#"],
            [".", ".", ".", "."],
            [".", ".", "#", "."]
        ],
            1,
            1, '^', 0, 1)
        self.assertEqual(False, result)

    def test_part2_example(self):
        self.assertEqual(6, part2(puzzle.examples[0].input_data))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)

    if __name__ == '__main__':
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day6)
        unittest.TextTestRunner().run(suite)
