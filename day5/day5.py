import re
import unittest
from collections import defaultdict

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=5)


def parse(input_data):
    rules_input, pages_input = input_data.split("\n\n")
    rules = defaultdict(list)
    pages = []
    for line in rules_input.splitlines():
        before, after = map(int,re.match(r"(\d+)\|(\d+)", line).groups())
        rules[before].append(after)
    for line in pages_input.splitlines():
        pages.append(list(map(int, line.split(","))))
    return rules, pages

def verify(page, rules):
    for idx1, page1 in enumerate(page):
        for idx2, page2 in enumerate(page[idx1 + 1:]):
            if page1 in rules[page2]:
                return False, (page2, page1)
    return True, None

def part1(input_data):
    rules, pages = parse(input_data)
    count = 0
    for page in pages:
        correct, _ = verify(page, rules)
        if correct:
            count += page[len(page) // 2]
    return count

def fix_page(page, rules):
    while True:
        correct, violation = verify(page, rules)
        if correct:
            return page
        num1, num2 = violation
        before = page.index(num1)
        after = page.index(num2)
        page[before], page[after] = page[after], page[before]

def sort_topology(rules):
    vertices = set()
    for k in rules.keys():
        vertices.add(k)
    for k,v in rules.items():
        for node in v:
            vertices.add(node)
    visited  = set()
    stack = []
    def visit(node):
        if node in visited:
            return
        visited.add(node)
        if node in rules:
            for neighbour in rules[node]:
                visit(neighbour)
        stack.append(node)
    for node in vertices:
        visit(node)
    ordered = stack[::-1]
    correct, violation = verify(ordered, rules)
    if not correct:
        raise Exception("Cycle detected")
    return ordered

def part2_incorrect(input_data):
    rules, pages = parse(input_data)
    count = 0
    topology_sort = sort_topology(rules)
    for page in pages:
        correct, _ = verify(page, rules)
        if correct:
           continue
        correct_order = []
        for num in topology_sort:
            if num in page:
                correct_order.append(num)
        assert(len(correct_order) == len(page))
        correct, violation = verify(correct_order, rules)
        if not correct:
            raise RuntimeError(f"Wrong order {violation} for page {page} changed to {correct_order}")
        count += correct_order[len(correct_order) // 2]
    return count

def part2(input_data):
    rules, pages = parse(input_data)
    count = 0
    for page in pages:
        correct, violation = verify(page, rules)
        if not correct:
            fixed = fix_page(page, rules)
            count += fixed[len(fixed) // 2]
    return count

class Day5(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(143, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_find_root(self):
        order = sort_topology({'e': ['f', 'g'], 'a': ['b', 'f'], 'c': ['e', 'h'], 'g': ['h'], 'b': ['c', 'h'], 'f': ['g']})
        self.assertEqual(order, ['a', 'b', 'c', 'e', 'f', 'g', 'h'])

    def test_part2_incorrect_example(self):
        self.assertEqual(123, part2_incorrect(puzzle.examples[0].input_data))

    def test_part2_example(self):
        self.assertEqual(123, part2(puzzle.examples[0].input_data))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day5)
    unittest.TextTestRunner().run(suite)
