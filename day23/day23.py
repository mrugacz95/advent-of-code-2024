import unittest
from collections import defaultdict

from aocd.models import Puzzle
from pebble.functions import new_method

puzzle = Puzzle(year=2024, day=23)


def parse(input_data):
    graph = defaultdict(list)
    for line in input_data.splitlines():
        node1, node2 = line.split('-')
        graph[node1].append(node2)
        graph[node2].append(node1)

    return graph


def part1(input_data):
    graph = parse(input_data)

    triplets = set()
    for node1 in graph.keys():
        for node2 in graph[node1]:
            for node3 in graph[node1]:
                if node3 == node2:
                    continue
                if 't' not in [node1[0], node2[0], node3[0]]:
                    continue
                if node3 in graph[node2]:
                    triplet = tuple(sorted((node1, node2, node3)))
                    triplets.add(triplet)
    print(triplets)
    return len(triplets)


def part2(input_data):
    graph = parse(input_data)

    clusters = {}

    def dfs(start, num):
        if start in clusters:
            return
        clusters[start] = num
        for neighbor in graph[start]:
            dfs(neighbor, num)

    for node in graph:
        if node not in clusters:
            cluster_num = len(clusters) + 1
            dfs(node, cluster_num)

    grouped = defaultdict(list)
    for node, node_id in clusters.items():
        grouped[node_id].append(node)

    def is_all_connected(clique, candidate):
        for node in clique:
            if node not in graph[candidate]:
                return False
        return True

    def enlarge_clique(clique, nodes, used):
        if len(nodes) == 0:
            return clique

        for candidate in nodes:
            if is_all_connected(clique, candidate):
                new_clique = clique | {candidate}
                new_nodes = nodes - {candidate}
                new_used = used + [candidate]
                return enlarge_clique(new_clique, new_nodes, new_used)

        return clique

    max_size = 1
    max_clique = [list(graph.keys())[0]]
    for nodes in grouped.values():
        all_nodes = set(nodes)
        for node in nodes:
            new_clique = enlarge_clique({node}, all_nodes - {node}, [node])
            if len(new_clique) > max_size:
                max_size = len(new_clique)
                max_clique = new_clique

    return ','.join(sorted(max_clique))


class Day23(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(7, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual("co,de,ka,ta", part2(puzzle.examples[0].input_data))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day23)
    unittest.TextTestRunner().run(suite)
