import unittest

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=10)


def parse(input_data):
    grid = []
    for line in input_data.splitlines():
        row = []
        for c in line:
            if c.isdigit():
                row.append(int(c))
            else:
                row.append(c)
        grid.append(row)
    return grid


DIR = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def part1(input_data):
    data = parse(input_data)
    visited = set()

    def dfs(sy, sx, node):
        if data[sy][sx] != node:
            return 0
        if node == 9:
            if (sy, sx) not in visited:
                visited.add((sy, sx))
                return 1
        endings = 0
        for dy, dx in DIR:
            y = sy + dy
            x = sx + dx
            if 0 <= y < len(data) and 0 <= x < len(data[0]):
                endings += dfs(y, x, node + 1)
        return endings

    scores = 0
    for y in range(len(data)):
        for x in range(len(data[0])):
            score = dfs(y, x, 0)
            if score > 0:
                print(y, x, score)
            scores += len(visited)
            visited = set()
    return scores


def part2(input_data):
    data = parse(input_data)

    def dfs(sy, sx, node):
        if data[sy][sx] != node:
            return 0
        if node == 9:
            return 1
        endings = 0
        for dy, dx in DIR:
            y = sy + dy
            x = sx + dx
            if 0 <= y < len(data) and 0 <= x < len(data[0]):
                endings += dfs(y, x, node + 1)
        return endings

    scores = 0
    for y in range(len(data)):
        for x in range(len(data[0])):
            score = dfs(y, x, 0)
            if score > 0:
                print(y, x, score)
            scores += score
    return scores


class Day10(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(1, part1(puzzle.examples[0].input_data))

    def test_part1_second_example(self):
        example = ("...0...\n"
                   "...1...\n"
                   "...2...\n"
                   "6543456\n"
                   "7.....7\n"
                   "8.....8\n"
                   "9.....9")
        self.assertEqual(2, part1(example))

    def test_part1_larger_example(self):
        example = ("89010123\n"
                   "78121874\n"
                   "87430965\n"
                   "96549874\n"
                   "45678903\n"
                   "32019012\n"
                   "01329801\n"
                   "10456732\n")
        self.assertEqual(36, part1(example))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        example = (".....0.\n"
                   "..4321.\n"
                   "..5..2.\n"
                   "..6543.\n"
                   "..7..4.\n"
                   "..8765.\n"
                   "..9....\n")
        self.assertEqual(3, part2(example))

    def test_part2_larger_example(self):
        example = ("89010123\n"
                   "78121874\n"
                   "87430965\n"
                   "96549874\n"
                   "45678903\n"
                   "32019012\n"
                   "01329801\n"
                   "10456732\n")
        self.assertEqual(81, part2(example))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day10)
    unittest.TextTestRunner().run(suite)
