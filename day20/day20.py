import heapq
import unittest
from collections import defaultdict, OrderedDict, Counter

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=20)


def parse(input_data):
    grid = list(map(lambda s: list(s), input_data.splitlines()))
    start = (-1, -1)
    end = (-1, -1)
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "S":
                start = (y, x)
            elif c == "E":
                end = (y, x)
    grid[start[0]][start[1]] = "."
    grid[end[0]][end[1]] = "."
    return grid, start, end


def count_dists(grid, start, end):
    queue = [(start[0], start[1], 0)]
    visited = {}  # (y, x, dist)
    cheats = list()  # (from, to)
    while len(queue) > 0:
        y, x, dist = queue.pop(0)
        if (y, x) in visited:
            continue
        visited[(y, x)] = dist
        if (y, x) == end:
            break
        for dy, dx in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            ny = y + dy
            nx = x + dx
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]):
                if grid[ny][nx] != "#":
                    queue.append((ny, nx, dist + 1))
        for dy, dx in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            ny = y + dy * 2
            nx = x + dx * 2
            mid_y = y + dy
            mid_x = x + dx
            if (0 <= ny < len(grid) and
                    0 <= nx < len(grid[ny]) and
                    grid[mid_y][mid_x] == "#" and
                    grid[ny][nx] != "#" and
                    (ny, nx) not in visited):
                cheats.append(((y, x), (ny, nx)))
    return visited, cheats


def group_cheats(costs, cheats):
    cheats_count = defaultdict(int)  # (time saved, count)
    for ((from_y, from_x), (to_y, to_x)) in cheats:
        if (from_y, from_x) in costs and (to_y, to_x) in costs:
            diff = costs[(to_y, to_x)] - costs[(from_y, from_x)] - 2
            if diff > 0:
                cheats_count[diff] += 1
    return cheats_count


def part1(input_data, threshold=100):
    grid, start, end = parse(input_data)
    costs, cheats = count_dists(grid, start, end)
    cheats_count = group_cheats(costs, cheats)

    return sum(map(lambda x: x[1], filter(lambda x: x[0] >= threshold, cheats_count.items())))


def walk_normal(grid, start, ):
    queue = [(start[0], start[1], 0)]
    visited = {}  # (y, x, dist)
    while len(queue) > 0:
        y, x, dist = queue.pop(0)
        if (y, x) in visited:
            continue
        visited[(y, x)] = dist
        for dy, dx in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            ny = y + dy
            nx = x + dx
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]):
                if grid[ny][nx] != "#":
                    queue.append((ny, nx, dist + 1))
    return visited


def distance(a, b):
    ay, ax = a
    by, bx = b
    return abs(ay - by) + abs(ax - bx)


def longer_cheats(grid, start, end):
    no_cheat_distances = walk_normal(grid, start)
    queue = [(True, 0, start[0], start[1], 20, (-1, -1))]  # (normal_move, y, x, dist, cheat_count, cheat_start)
    visited = set()  # (y, x, cheat_start)
    cheats = list()  # (from, to, diff)
    while len(queue) > 0:
        normal_move, dist, y, x, cheat_count, cheat_start = heapq.heappop(queue)
        if (y, x, cheat_start) in visited:
            continue
        visited.add((y, x, cheat_start))
        if normal_move:
            for dy, dx in ((-1, 0), (0, -1), (1, 0), (0, 1)):  # normal move
                ny = y + dy
                nx = x + dx
                if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]):
                    if grid[ny][nx] != "#":
                        heapq.heappush(queue, (normal_move, dist + 1, ny, nx, cheat_count, cheat_start))
                    elif cheat_count > 0:  # start cheating if haven't yet
                        heapq.heappush(queue, (False, dist, y, x, cheat_count, (y, x)))
        elif cheat_count >= 0:  # during cheating and able to cheat more
            if cheat_count > 0:
                for dy, dx in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                    ny = y + dy
                    nx = x + dx
                    if (0 <= ny < len(grid) and
                            0 <= nx < len(grid[ny])):
                        heapq.heappush(queue, (normal_move, dist + 1, ny, nx, cheat_count - 1, cheat_start))
            if grid[y][x] != "#" and no_cheat_distances[(y, x)] > dist:  # stop cheating if is profitable
                diff = no_cheat_distances[(y, x)] - no_cheat_distances[cheat_start] - distance(cheat_start, (y, x))
                cheats.append((cheat_start, (y, x), diff))
    return visited, cheats

def part2(input_data, threshold=100):
    grid, start, end = parse(input_data)
    costs, cheats = longer_cheats(grid, start, end)
    cheats_count = Counter(map(lambda x: x[2], cheats))
    return sum([count for saving, count in cheats_count.items() if saving >= threshold])


class Day20(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(4, part1(puzzle.examples[0].input_data, threshold=30))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual(285, part2(puzzle.examples[0].input_data, threshold=50))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day20)
    unittest.TextTestRunner().run(suite)
