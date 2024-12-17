import unittest

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=12)


def parse(input_data):
    return input_data.splitlines()


DIR = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def part1(input_data):
    garden = parse(input_data)
    fences = {}
    for y, row in enumerate(garden):
        for x, plant in enumerate(row):
            sides = 4
            for dy, dx in DIR:
                if (0 <= y + dy < len(garden) and
                        (0 <= x + dx < len(row)) and
                        garden[y + dy][x + dx] == garden[y][x]):
                    sides -= 1
            fences[(y, x)] = sides
    visited = set()

    def dfs(y, x, symbol):
        if (y, x) in visited:
            return 0, 0
        visited.add((y, x))
        area = 1
        nonlocal fences
        node_fences = fences[(y, x)]
        for dy, dx in DIR:
            if (0 <= y + dy < len(garden) and
                    (0 <= x + dx < len(row)) and
                    (garden[y + dy][x + dx] == symbol)):
                a, f = dfs(y + dy, x + dx, symbol)
                area += a
                node_fences += f
        return area, node_fences

    result = 0
    for y, row in enumerate(garden):
        for x, plant in enumerate(row):
            a, f = dfs(y, x, plant)
            result += a * f
    return result


def calc_sides(points):
    sides = 0
    marked = set()
    min_y = min(y for y, x in points)
    max_y = max(y for y, x in points)
    min_x = min(x for y, x in points)
    max_x = max(x for y, x in points)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (y, x) not in points:
                continue
            if (y, x - 1) in points:
                continue
            edge_y = y
            if (edge_y, x) not in marked:
                sides += 1
            else:
                continue
            while (edge_y, x) in points:
                left = (edge_y, x - 1) in points
                if not left:
                    marked.add((edge_y, x))
                else:
                    break
                edge_y += 1
    return sides


def rotate(points):
    max_y = max(y for y, x in points)
    rotated = set()
    for y, x in points:
        rotated.add((x, max_y - y))
    return rotated


def print_shape(points, char):
    min_y = min(y for y, x in points)
    max_y = max(y for y, x in points)
    min_x = min(x for y, x in points)
    max_x = max(x for y, x in points)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (y, x) not in points:
                print('.', end='')
            else:
                print(char, end='')
        print()


def part2(input_data):
    garden = parse(input_data)
    shape = set()

    def dfs(y, x, symbol):
        if (y, x) in shape:
            return 0
        shape.add((y, x))
        area = 1
        for dy, dx in DIR:
            if (0 <= y + dy < len(garden) and
                    (0 <= x + dx < len(row)) and
                    (garden[y + dy][x + dx] == symbol)):
                a = dfs(y + dy, x + dx, symbol)
                area += a
        return area

    result = 0
    counted = set()
    for y, row in enumerate(garden):
        for x, plant in enumerate(row):
            if (y, x) in counted:
                continue
            area = dfs(y, x, plant)
            counted.update(shape)
            sides = 0
            for s in range(4):
                new_sides = calc_sides(shape)
                sides += new_sides
                print_shape(shape, plant)
                print('counted', new_sides)
                shape = rotate(shape)
            print('A region of', garden[y][x], 'plants with price', area, '*', sides, '=', area * sides)
            print()
            result += area * sides
            shape = set()
    return result


class Day12(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(140, part1(puzzle.examples[0].input_data))

    def test_part1_larger_example(self):
        example = ("RRRRIICCFF\n"
                   "RRRRIICCCF\n"
                   "VVRRRCCFFF\n"
                   "VVRCCCJFFF\n"
                   "VVVVCJJCFE\n"
                   "VVIVCCJJEE\n"
                   "VVIIICJJEE\n"
                   "MIIIIIJJEE\n"
                   "MIIISIJEEE\n"
                   "MMMISSJEEE")
        self.assertEqual(1930, part1(example))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_calc_sides_example(self):
        shape = [(0, 0), (0, 1), (0, 2),
                 (1, 2),
                 (2, 0), (2, 1), (2, 2),
                 (3, 2),
                 (4, 0), (4, 1), (4, 2),
                 (5, 1), (5, 2), (5, 3)]
        self.assertEqual(6, calc_sides(shape))

    def test_calc_sides_concave_example(self):
        shape = [(0, 0), (0, 1), (0, 2), (0, 3),
                 (1, 0), (1, 2), (1, 3)]
        self.assertEqual(2, calc_sides(shape))

    def test_calc_sides_concave2_example(self):
        """
        ..X
        ..X
        XXX
        X.X
        """
        shape = [(0, 2),
                 (1, 2),
                 (2, 0), (2, 1), (2, 2),
                 (3, 0), (3, 2)]
        self.assertEqual(3, calc_sides(shape))

    def test_calc_sides_rectangle_horizontal_example(self):
        shape = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.assertEqual(1, calc_sides(shape))

    def test_calc_sides_rectangle_vertical_example(self):
        shape = [(0, 0), (1, 0), (2, 0), (3, 0)]
        self.assertEqual(1, calc_sides(shape))

    def test_rotate_example(self):
        """
        XXX    .X
        ..X -> .X
               XX
        """
        shape = [(0, 0), (0, 1), (0, 2),
                 (1, 2), ]
        self.assertEqual({(0, 1), (1, 1), (2, 0), (2, 1)}, rotate(shape))

    def test_part2_example(self):
        self.assertEqual(80, part2(puzzle.examples[0].input_data))

    def test_part2_second_example(self):
        example = ("AAAAAA\n"
                   "AAABBA\n"
                   "AAABBA\n"
                   "ABBAAA\n"
                   "ABBAAA\n"
                   "AAAAAA")
        self.assertEqual(28 * 12 + 4 * 4 + 4 * 4, part2(example))

    def test_part2_larger_example(self):
        example = ("RRRRIICCFF\n"
                   "RRRRIICCCF\n"
                   "VVRRRCCFFF\n"
                   "VVRCCCJFFF\n"
                   "VVVVCJJCFE\n"
                   "VVIVCCJJEE\n"
                   "VVIIICJJEE\n"
                   "MIIIIIJJEE\n"
                   "MIIISIJEEE\n"
                   "MMMISSJEEE")
        self.assertEqual(1206, part2(example))

    def test_part2_C_example(self):
        example = ("......CC..\n"
                   "......CCC.\n"
                   ".....CC...\n"
                   "...CCC....\n"
                   "....C..C..\n"
                   "....CC....\n"
                   ".....C....\n")
        self.assertEqual(1104, part2(example))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day12)
    unittest.TextTestRunner().run(suite)
