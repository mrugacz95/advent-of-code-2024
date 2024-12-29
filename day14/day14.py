import unittest
from collections import defaultdict
from time import sleep

import matplotlib.pyplot as lt
import numpy as np
import tqdm
from aocd.models import Puzzle
from matplotlib import pyplot as plt

puzzle = Puzzle(year=2024, day=14)


def parse(input_data):
    for line in input_data.split("\n"):
        pos, vec = line.split(" ")
        pos = pos[2:].split(",")
        vec = vec[2:].split(",")
        pos_x = int(pos[0])
        pos_y = int(pos[1])
        vec_x = int(vec[0])
        vec_y = int(vec[1])
        yield pos_y, pos_x, vec_y, vec_x


def print_grid(grid, width, height, t):
    for y in range(height):
        for x in range(width):
            if (y, x) in grid:
                print(grid[(y, x)], end="")
            else:
                print('.', end='')
        print()
    print()


def print_grid_plot(grid, width, height, time):
    image = np.zeros((height, width), dtype=int)
    for y in range(height):
        for x in range(width):
            if (y, x) in grid:
                image[y, x] = 1
            else:
                image[y, x] = 0
    plt.imshow(image)
    plt.title(f"time = {time}")
    plt.show()
    # sleep(0.01)


def part1(input_data, width=101, height=103, debug=False, time=100, print_func=print_grid):
    data = list(parse(input_data))
    for t in range(time):
        grid = defaultdict(int)
        new_data = []
        for pos_y, pos_x, vec_y, vec_x in data:
            new_pos_y, new_pos_x = pos_y + vec_y, pos_x + vec_x
            new_pos_y %= height
            new_pos_x %= width
            grid[(new_pos_y, new_pos_x)] += 1
            new_data.append((new_pos_y, new_pos_x, vec_y, vec_x))
        if debug:
            print_func(grid, width, height, t)
        data = new_data
    # split to quadrants
    q = [0, 0, 0, 0]
    for pos_y, pos_x, vec_y, vec_x in data:
        if pos_y < height // 2:
            if pos_x < width // 2:
                q[0] += 1
            elif pos_x > width // 2:
                q[1] += 1
        elif pos_y > height // 2:
            if pos_x < width // 2:
                q[2] += 1
            elif pos_x > width // 2:
                q[3] += 1
    return q[0] * q[1] * q[2] * q[3]


def part2(input_data, width=101, height=103, time=101 * 103, print_func=print_grid_plot):
    data = list(parse(input_data))
    vars = []
    for t in tqdm.tqdm(range(time)):
        for i in range(len(data)):
            pos_y, pos_x, vec_y, vec_x = data[i]
            new_pos_y, new_pos_x = (pos_y + vec_y) % height, (pos_x + vec_x) % width
            data[i] = (new_pos_y, new_pos_x, vec_y, vec_x)

        grid = defaultdict(int)
        for pos_y, pos_x, _, _ in data:
            grid[(pos_y, pos_x)] += 1

        all_y, all_x = zip(*grid.keys())
        var_y, var_x = np.var(all_y), np.var(all_x)
        if len(vars) > 0 and (var_y < min(y for y, x in vars) and var_x < min(x for y, x in vars)):
            print(t)
            print_func(grid, width, height, t + 1)
            print("Found")
            return t + 1
        vars.append((var_y, var_x))


class Day14(unittest.TestCase):

    def test_part1_simple_example(self):
        part1("p=2,4 v=2,-3", 11, 7, debug=True)

    def test_part1_example(self):
        self.assertEqual(12, part1(puzzle.examples[0].input_data, 11, 7))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day14)
    unittest.TextTestRunner().run(suite)
