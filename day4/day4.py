import re
import unittest

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=4)


def parse(input_data):
    return input_data.splitlines()


def rotate(data):
    new_data = ["" for _ in range(len(data[0]))]
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            new_data[len(data) - 1 - x] += c
    return new_data


def count_horizontal(data):
    count = 0
    for line in data:
        left_to_right = len(re.findall(r'XMAS', line))
        count += left_to_right
    return count


def slice_diagonal(data):
    diag = []
    for x in range(-len(data[0]) + 1, len(data[0])):
        pos_y = 0
        pos_x = x
        diag_line = ""
        while pos_y < len(data):
            if 0 <= pos_y < len(data) and 0 <= pos_x < len(data[0]):
                diag_line += data[pos_y][pos_x]
            pos_x += 1
            pos_y += 1
        diag.append(diag_line)
    return diag


def count_diagonal(data):
    diags = slice_diagonal(data)
    return count_horizontal(diags)


def part1(input_data):
    data = parse(input_data)
    count = 0
    for _ in range(4):
        count += count_horizontal(data)
        count += count_diagonal(data)
        data = rotate(data)
    return count


def count_x(data):
    count = 0
    mask = ["M.S", ".A.", "M.S"]
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            def mask_matches():
                matches = 0
                for my, mline in enumerate(mask):
                    for mx, mc in enumerate(mline):
                        if mc == ".":
                            continue
                        if (0 > my + y or my + y >= len(data)) or (0 > mx + x or mx + x >= len(data[0])):
                            continue
                        if mc != data[my + y][mx + x]:
                            return False
                        matches += 1
                return matches == 5

            if mask_matches():
                count += 1
    return count

def part2(input_data):
    data = parse(input_data)
    count = 0
    for _ in range(4):
        count += count_x(data)
        data = rotate(data)
    return count

class Day4(unittest.TestCase):
    example = ("MMMSXXMASM\n"
               "MSAMXMSMSA\n"
               "AMXSXMAAMM\n"
               "MSAMASMSMX\n"
               "XMASAMXAMM\n"
               "XXAMMXXAMA\n"
               "SMSMSASXSS\n"
               "SAXAMASAAA\n"
               "MAMMMXMMMM\n"
               "MXMXAXMASX")

    def test_part1_example(self):
        self.assertEqual(4, part1(puzzle.examples[0].input_data))

    def test_diagonals(self):
        example = ["ABC", "DEF", "GHI"]
        self.assertEqual(['G', 'DH', 'AEI', 'BF', 'C'], slice_diagonal(example))

    def test_part1_example2(self):
        self.assertEqual(18, part1(self.example))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual(9, part2(self.example))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day4)
    unittest.TextTestRunner().run(suite)
