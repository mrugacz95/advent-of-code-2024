import heapq
import unittest

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=18)


def parse(input_data):
    return [tuple(map(int, line.split(','))) for line in input_data.split("\n")]

directions = ((-1, 0), (0, -1), (1, 0), (0, 1))

def find_path(memory, memory_size):
    queue = [(0, 0, 0)]  # cost, y, x
    visited = set()
    while len(queue) > 0:
        cost, y, x = heapq.heappop(queue)
        if (y, x) in visited:
            continue
        # print('visiting', y, x)
        visited.add((y, x))
        if y == memory_size and x == memory_size:
            return cost
        for dy, dx in directions:
            ny = y + dy
            nx = x + dx
            if 0 <= ny <= memory_size and 0 <= nx <= memory_size:
                if (ny, nx) not in memory:
                    heapq.heappush(queue, (cost + 1, ny, nx))
    return None

def part1(input_data, memory_size = 70,  corrupted = 1024):
    data = parse(input_data)
    memory = {}
    for x,y in data[:corrupted]:
        memory[y,x] = True
    return find_path(memory, memory_size)


def part2(input_data, memory_size = 70):
    data = parse(input_data)
    memory = {}
    for x, y in data:
        memory[y, x] = True
        path_length = find_path(memory, memory_size)
        if path_length is None:
            return f"{x},{y}"


class Day18(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(22, part1(puzzle.examples[0].input_data, memory_size = 6, corrupted= 12))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual("6,1", part2(puzzle.examples[0].input_data, memory_size = 6))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day18)
    unittest.TextTestRunner().run(suite)
