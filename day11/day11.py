import unittest
from functools import cache

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=11)


def parse(input_data):
    return list(map(int, input_data.split(" ")))


def part1(input_data, times=25):
    stones = parse(input_data)
    for t in range(times):
        i = 0
        while i < len(stones):
            stone = stones[i]
            s = str(stone)
            l = len(s)
            if stone == 0:
                stones[i] = 1
                i += 1
            elif l % 2 == 0:
                stones[i] = int(s[:l // 2])
                stones.insert(i + 1, int(s[l // 2:]))
                i += 2
            else:
                stones[i] = 2024 * stone
                i += 1
        print(t, len(stones))

    return len(stones)

def part2_too_slow(input_data, times):
    stones = parse(input_data)
    next_stone = list(range(len(stones) + 1))[1:]
    next_stone[-1] = None
    for t in range(times):
        i = 0
        while i is not None:
            stone = stones[i]
            if stone == 0:
                stones[i] = 1
                i = next_stone[i]
            elif len(str(stone)) % 2 == 0:
                s = str(stone)
                l = len(s)
                stones[i] = int(s[:l // 2])
                stones.append(int(s[l // 2:]))
                next_stone.append(next_stone[i])
                next_i = next_stone[i]
                next_stone[i] = len(stones) - 1
                i = next_i
            else:
                stones[i] = 2024 * stone
                i = next_stone[i]
        print(t, len(stones))
        # print(t, len(stones), end=' | ')
        # i = 0
        # while i is not None:
        #     print(stones[i], end=', ')
        #     i = next_stone[i]
        # print()

    return len(stones)


@cache
def evolve(stone, times):
    if times == 0:
        return 1
    if stone == 0:
        return evolve(1, times - 1)
    elif len(str(stone)) % 2 == 0:
        s = str(stone)
        l = len(s)
        ans = evolve(int(s[:l // 2]), times - 1)
        ans += evolve(int(s[l // 2:]), times - 1)
        return ans
    else:
        return evolve(2024 * stone, times - 1)


def part2(input_data, times=75):
    stones = parse(input_data)
    final_length = 0
    for stone in stones:
        final_length += evolve(stone, times)
    return final_length


class Day11(unittest.TestCase):

    def test_part1_example(self):
        example = "0 1 10 99 999"
        self.assertEqual(7, part1(example, 1))

    def test_part1_second_example(self):
        example = "125 17"
        self.assertEqual(22, part1(example, 6))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        example = "0 1 10 99 999"
        self.assertEqual(7, part2(example, 1))

    def test_part2_second_example(self):
        example = "125 17"
        self.assertEqual(22, part2(example, 6))

    def test_evolve(self):
        self.assertEqual(7, evolve(125, 6))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data, 75)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day11)
    unittest.TextTestRunner().run(suite)
