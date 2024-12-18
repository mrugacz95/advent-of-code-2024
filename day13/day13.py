import heapq
import unittest

import numpy as np
from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=13)


def parse(input_data):
    prices = []
    for price_input in input_data.split("\n\n"):
        labels = ['A', 'B', 'P']
        price = {}
        for label, line in zip(labels, price_input.split("\n")):
            _, xy = line.split(': ')
            x, y = xy.split(', ')
            x = int(x[2:])
            y = int(y[2:])
            price[label] = (x, y)
        prices.append(price)
    return prices


def is_price_reachable(price):
    btn_a_x, btn_a_y = price['A']
    btn_b_x, btn_b_y = price['B']
    price_x, price_y = price['P']
    for a_presses in range(100):
        for b_presses in range(100):
            pos_x = btn_a_x * a_presses + btn_b_x * b_presses
            pos_y = btn_a_y * a_presses + btn_b_y * b_presses
            if price_x == pos_x and price_y == pos_y:
                return a_presses * 3 + b_presses
    return 0


def part1(input_data):
    data = parse(input_data)
    tokens = 0
    for price in data:
        tokens += is_price_reachable(price)
    return tokens


def part2(input_data, adjustment=10000000000000):
    data = parse(input_data)
    for price in data:
        price['P'] = (price['P'][0] + adjustment, price['P'][1] + adjustment)
    # equation
    tokens = 0
    for price in data:
        btn_a_x, btn_a_y = price['A']
        btn_b_x, btn_b_y = price['B']
        price_x, price_y = price['P']
        a = np.array([[btn_a_x, btn_b_x], [btn_a_y, btn_b_y]])
        b = np.array([price_x, price_y])
        x = np.linalg.solve(a, b)
        a_presses, b_presses = np.round(x).astype(int)
        if a_presses * btn_a_x + b_presses * btn_b_x == price_x and a_presses * btn_a_y + b_presses * btn_b_y == price_y:
            tokens += int(a_presses) * 3 + int(b_presses)
        print(price, a_presses, b_presses, x[0], x[1])
    return tokens


class Day13(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(480, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual(480, part2(puzzle.examples[0].input_data, adjustment=0))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day13)
    unittest.TextTestRunner().run(suite)
