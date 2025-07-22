import unittest
from itertools import pairwise, combinations_with_replacement

from aocd.models import Puzzle
from tqdm import tqdm

puzzle = Puzzle(year=2024, day=22)


def parse(input_data):
    return list(map(int, input_data.splitlines()))


def part1(input_data):
    data = parse(input_data)
    total = 0
    for secret in data:
        total += list(next_price(secret))[-1]
    return total


def next_price(secret):
    for i in range(2000):
        secret = mix(secret, secret * 64)
        secret = prune(secret)

        secret = mix(secret, secret // 32)
        secret = prune(secret)

        secret = mix(secret, secret * 2048)
        secret = prune(secret)
        yield secret


def mix(value, secret):
    return value ^ secret


def prune(number):
    return number % 16777216


def part2(input_data):
    data =  parse(input_data)
    # preprocess data
    sellers_secrets = [list(next_price(secret)) for secret in data]
    sellers_prices = [list(map(lambda x: x % 10, secrets)) for secrets in sellers_secrets]
    sellers_deltas = []
    for price in sellers_prices:
        deltas = []
        for i1, i2 in pairwise(price):
            deltas.append(i2 - i1)
        sellers_deltas.append(deltas)
    # find a sequence
    max_banana = 0
    for seq in  tqdm(combinations_with_replacement(range(-9, 9), 4)):
        current_price = calculate_bananas_from_sequence(sellers_deltas, sellers_prices, seq)
        max_banana = max(current_price, max_banana)
    return max_banana


def calculate_bananas_from_sequence(sellers_deltas, sellers_prices, seq):
    current_price = 0
    for seller_idx, delta in enumerate(sellers_deltas):
        price_idx = find_seq(sellers_deltas[seller_idx], seq)
        if price_idx != -1:
            price = sellers_prices[seller_idx][price_idx + 4]
            current_price += price
    return current_price


def find_seq(deltas, seq):
    for idx in range(len(deltas) - len(seq) + 1):
        if deltas[idx:idx + len(seq)] == seq:
            return idx
    return -1


class Day22(unittest.TestCase):

    def test_mix(self):
        self.assertEqual(mix(42, 15), 37)

    def test_prune(self):
        self.assertEqual(prune(100000000), 16113920)

    def test_process(self):
        gen = next_price(123)
        self.assertEqual([next(gen) for _ in range(10)][-1], 5908254)

    def test_part1_example(self):
        self.assertEqual(37327623, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual(23, part2("1\n2\n3\n2024"))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day22)
    unittest.TextTestRunner().run(suite)
