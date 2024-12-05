import unittest

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=2)


def parse(input_data):
    return list(map(lambda line: list(map(int, line.split(" "))), input_data.split("\n")))


def is_safe(row):
    if row == sorted(row) or row == sorted(row, reverse=True):
        def safe_diff():
            for i, j in zip(row, row[1:]):
                if 1 <= abs(i - j) <= 3:
                    continue
                else:
                    return False
            return True

        if safe_diff():
            return True
        return False


def part1(input_data):
    data = parse(input_data)
    safe = 0
    for row in data:
        if is_safe(row):
            safe += 1
    return safe


def part2(input_data):
    data = parse(input_data)
    safe = 0
    for row in data:
        if is_safe(row):
            safe += 1
            continue
        for idx, num in enumerate(row):
            c2 = row[:idx] + row[idx + 1:]
            if is_safe(c2):
                safe += 1
                break
    return safe


class Day2(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(2, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual(4, part2(puzzle.examples[0].input_data))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day2)
    unittest.TextTestRunner().run(suite)
