import heapq
import unittest
from collections import defaultdict

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=16)

DIRS = {
    'l': (1, 0),
    'r': (0, 1),
    'u': (-1, 0),
    'd': (0, -1),
}


def get_neighbours(y, x, grid):
    for dy, dx in DIRS.values():
        new_y = y + dy
        new_x = x + dx
        if 0 <= new_y < len(grid) and 0 <= new_x < len(grid[0]) and grid[new_y][new_x] != '#':
            yield new_y, new_x


def parse(input_data):
    grid = input_data.splitlines()
    start = None
    end = None
    nodes = defaultdict(list)
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == 'S':
                start = (y, x)
            elif c == 'E':
                end = (y, x)
            if c != '#':
                nodes[(y, x)].extend(get_neighbours(y, x, grid))
    return start, end, nodes


def get_dir(from_y, from_x, to_y, to_x):
    if from_y < to_y:
        return 'd'
    if from_y > to_y:
        return 'u'
    if from_x < to_x:
        return 'r'
    if from_x > to_x:
        return 'l'
    raise ValueError("Invalid direction")


def turn_right(direction):
    if direction == 'l':
        return 'u'
    if direction == 'r':
        return 'd'
    if direction == 'u':
        return 'r'
    if direction == 'd':
        return 'l'
    raise ValueError("Invalid direction")


def turn_left(direction):
    if direction == 'l':
        return 'd'
    if direction == 'r':
        return 'u'
    if direction == 'u':
        return 'l'
    if direction == 'd':
        return 'r'
    raise ValueError("Invalid direction")


def dfs(sy, sx, ey, ex, sd, nodes):
    queue = [(0, sy, sx, sd)]  # cost x y dir
    visited = set()
    while len(queue) > 0:
        ccost, cy, cx, cd = queue.pop(0)
        cnode = cy, cx
        if cnode == (ey, ex):
            return ccost
        if (cy, cx, cd) in visited:
            continue
        visited.add((cy, cx, cd))
        for (ny, nx) in nodes[cnode]:
            next_dir = get_dir(cy, cx, ny, nx)
            if next_dir == cd:
                heapq.heappush(queue, (ccost + 1, ny, nx, cd))
        heapq.heappush(queue, (ccost + 1000, cy, cx, turn_right(cd)))
        heapq.heappush(queue, (ccost + 1000, cy, cx, turn_left(cd)))
    raise ValueError("No path found")


def part1(input_data):
    start, end, nodes = parse(input_data)
    direction = 'r'
    return dfs(start[0], start[1], end[0], end[1], direction, nodes)


def make_direct(sx, sy, nodes):
    queue = [0, sx, sy]
    visited = set()
    while len(queue) > 0:
        node = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        for next_node in nodes[node]:
            heapq.heappush(queue, next_node)


def find_paths_with_cost(sy, sx, ey, ex, sd, nodes, best_cost):
    queue = [(0, sy, sx, sd, [(sy, sx, sd)])]  # cost, x, y, dir, from_dir, path
    cost = defaultdict(lambda: float('inf'))
    best_paths_to_node = defaultdict(list)
    while len(queue) > 0:
        ccost, cy, cx, cd, path = heapq.heappop(queue)
        cnode = cy, cx
        if cnode == (ey, ex) and best_cost == ccost:
            best_paths_to_node[cy, cx, cd].append(path)
            print(f"Exit reached with length {len(path)} path {path}")
            continue

        if (cy, cx, cd) in cost: # visited
            if ccost == cost[(cy, cx, cd)] and ccost <= best_cost:
                best_paths_to_node[cy, cx, cd].append(path)
            continue
        cost[(cy, cx, cd)] = min(ccost, cost[(cy, cx, cd)])

        if ccost <= best_cost:
            best_paths_to_node[cy, cx, cd].append(path)
        else:
            continue

        for (ny, nx) in nodes[cnode]:
            if (ny, nx) in path:
                continue
            next_dir = get_dir(cy, cx, ny, nx)
            if (ny, nx, next_dir) in cost:
                continue
            if next_dir == cd:
                heapq.heappush(queue, (ccost + 1, ny, nx, cd, path + [(ny, nx, next_dir)]))
            elif turn_left(cd) == next_dir:
                heapq.heappush(queue, (ccost + 1000, cy, cx, turn_left(cd), path + [(cy, cx, turn_left(cd))]))
            elif turn_right(cd) == next_dir:
                heapq.heappush(queue, (ccost + 1000, cy, cx, turn_right(cd), path + [(cy, cx, turn_right(cd))]))
    return best_paths_to_node


def print_best_seats(best_seats, input_data):
    data = input_data.splitlines()
    yx_best_seats = set(map(lambda x: (x[0], x[1]), best_seats))
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if (y, x) in yx_best_seats:
                print('\033[42m' + 'O', end='\033[0m')
            else:
                print(c, end='')
        print()
    print()


def part2(input_data):
    start, end, nodes = parse(input_data)
    direction = 'r'
    cost = dfs(start[0], start[1], end[0], end[1], direction, nodes)
    best_paths = find_paths_with_cost(start[0], start[1], end[0], end[1], direction, nodes, cost)

    best_seats = set()

    def update_seats(y, x, d):
        if (y, x, d) in best_seats:
            return
        # print(f"Updating seats for {y} {x} {d} with the best paths {len(best_paths[(y, x, d)])}")
        best_seats.add((y, x, d))
        for path in best_paths[(y, x, d)]:
            for ny, nx, nd in path:
                update_seats(ny, nx, nd)

    for direction in DIRS.keys():
        update_seats(end[0], end[1], direction)

    print_best_seats(best_seats, input_data)

    only_nodes = set(map(lambda x: (x[0], x[1]), best_seats))

    return len(only_nodes)


class Day16(unittest.TestCase):
    def test_part1_example(self):
        self.assertEqual(7036, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual(45, part2(puzzle.examples[0].input_data))

    def test_part2_hard_example(self):
        example = ("#################\n"
                   "#...#...#...#..E#\n"
                   "#.#.#.#.#.#.#.#.#\n"
                   "#.#.#.#...#...#.#\n"
                   "#.#.#.#.###.#.#.#\n"
                   "#...#.#.#.....#.#\n"
                   "#.#.#.#.#.#####.#\n"
                   "#.#...#.#.#.....#\n"
                   "#.#.#####.#.###.#\n"
                   "#.#.#.......#...#\n"
                   "#.#.###.#####.###\n"
                   "#.#.#...#.....#.#\n"
                   "#.#.#.#####.###.#\n"
                   "#.#.#.........#.#\n"
                   "#.#.#.#########.#\n"
                   "#S#.............#\n"
                   "#################")
        self.assertEqual(64, part2(example))

    def test_part2_own_example1(self):
        example = ("########\n"
                   "#......E#\n"
                   "#.#.#.###\n"
                   "#S....###\n"
                   "#########")
        self.assertEqual(15, part2(example))

    def test_part2_own_example2(self):
        example = ("########\n"
                   "#.#....E#\n"
                   "#.#.#.###\n"
                   "#.#.#...#\n"
                   "#.#.#.#.#\n"
                   "#S......#\n"
                   "#########")
        self.assertEqual(16, part2(example))

    def test_part2_own_example3(self):
        example = ("##################\n"
                   "#.#.............E#\n"
                   "#.#.###.####.#####\n"
                   "#.#.###.#.##.#####\n"
                   "#.#.###.####.#####\n"
                   "#.#.###......#####\n"
                   "#.#.###.##########\n"
                   "#.#..............#\n"
                   "#S..##############\n"
                   "##################")
        self.assertEqual(23, part2(example))

    def test_part2_own_example4(self):
        example = ("#####################################\n"
                   "##.........................#.#.....##\n"
                   "######.#.###.#######.#####.#.#.#.####\n"
                   "#S.....#.#...#.....#...............E#\n"
                   "######.#.#.###.#.#####.#.#.###.#.#.##\n"
                   "#......#.................#...#.....##\n"
                   "#####################################")
        self.assertEqual(46, part2(example))

    def test_part2_own_example5(self):
        example = ("##########################\n"
                   "#S.....#.#.........#....E#\n"
                   "####.#.#.#.#####.###.#.###\n"
                   "#........#.....#.#...#.###\n"
                   "####.#.#.#.###.#.#.###.###\n"
                   "##...#.#.....#.#...#...###\n"
                   "##.#.#.#.#.###.#####.#####\n"
                   "#..#.#.#.#.........#...###\n"
                   "####.###.#.#####.#####.###\n"
                   "#..#.#.....#...#.#...#.###\n"
                   "##.#.#.#.#.#.#.###.#.#.###\n"
                   "#............#.....#...###\n"
                   "##########################")
        self.assertEqual(52, part2(example))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day16)
    unittest.TextTestRunner().run(suite)
