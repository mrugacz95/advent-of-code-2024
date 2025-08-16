import unittest

import graphviz
from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=24)


def parse(input_data):
    graph = {}

    initial, gates = input_data.split("\n\n")

    for line in initial.splitlines():
        variable, value = line.split(": ")
        graph[variable] = int(value)

    for line in gates.splitlines():
        gate = line.split(" ")
        lhs = gate[0]
        operator = gate[1]
        rhs = gate[2]
        result = gate[4]
        if lhs < rhs:
            graph[result] = (lhs, operator, rhs)
        else:
            graph[result] = (rhs, operator, lhs)

    return graph


def calc_value(graph, node):
    current = graph[node]
    if type(current) == int:
        return current

    lhs, operator, rhs = current
    lhs_value = calc_value(graph, lhs)
    rhs_value = calc_value(graph, rhs)

    if operator == "AND":
        return lhs_value & rhs_value
    elif operator == "OR":
        return lhs_value | rhs_value
    elif operator == "XOR":
        return lhs_value ^ rhs_value

    raise RuntimeError(f"Unknown operator: {operator}")


def part1(input_data):
    graph = parse(input_data)

    bits = sorted(filter(lambda x: x[0] == 'z', graph.keys()), reverse=True)

    value = 0
    for bit in bits:
        value <<= 1
        value |= calc_value(graph, bit)
        print(bit, value)

    return value


def part2(input_data):
    graph = parse(input_data)

    bits = sorted(filter(lambda x: x[0] == 'z', graph.keys()), reverse=True)
    last_index = len(bits) - 1

    # manual fixes for the graph
    # graph['z05'], graph['hdt'] = graph['hdt'], graph['z05']
    # graph['z09'], graph['gbf'] = graph['gbf'], graph['z09']
    # graph['mht'], graph['jgt'] = graph['jgt'], graph['mht']
    # graph['z30'], graph['nbf'] = graph['nbf'], graph['z30']

    # visualize the graph
    dot = graphviz.Digraph(comment='The Round Table')
    for result_node, edge in graph.items():
        if isinstance(edge, tuple):
            lhs, operator, rhs = edge
            joined = f"{lhs} {operator} {rhs} = {result_node}"
            dot.node(joined, label="", shape="point")
            dot.edge(lhs, joined)
            dot.edge(rhs, joined)
            dot.edge(joined, result_node, label=f"{operator}")
    dot.render(directory='doctest-output', view=True)

    carry = {}

    graph_inv = {v: k for k, v in graph.items() if isinstance(v, tuple)}

    def find_node(lhs, operator, rhs):
        if (lhs, operator, rhs) in graph_inv:
            return graph_inv[lhs, operator, rhs]
        if (rhs, operator, lhs) in graph_inv:
            return graph_inv[rhs, operator, lhs]
        print(f"Cannot find node for {lhs} {operator} {rhs}")
        return None

    # find problems in graph, fix if possible
    fixed_joins = []
    i = 0
    while f'z{i:02d}' in graph:
        index = f'{i:02d}'
        print(index)
        if index == '00':

            and_connection = find_node(f'x{index}', 'AND', f'y{index}')
            xor_connection = find_node(f'x{index}', 'XOR', f'y{index}')

            assert xor_connection == 'z00'
            carry[f'c{index}'] = and_connection
        elif i == last_index:
            assert carry['c44'] == 'z45'
        else:

            and_connection = find_node(f'x{index}', 'AND', f'y{index}')
            xor_connection = find_node(f'x{index}', 'XOR', f'y{index}')

            prev_carry = carry[f'c{int(index) - 1:02d}']
            sum_connection = find_node(prev_carry, 'XOR', xor_connection)

            if sum_connection is None:
                print(f"Cannot find sum node for {prev_carry} XOR {xor_connection}")
                print('Fixing it')
                def fix_xor_connection():
                    for node in graph.values():
                        if isinstance(node, tuple):
                            lhs, op, rhs = node
                            if op == 'XOR' and (lhs == prev_carry or rhs == prev_carry):
                                print('candidate found:', lhs, op, rhs)
                                candidate = lhs if lhs != prev_carry else rhs
                                graph[candidate], graph[xor_connection] = graph[xor_connection], graph[candidate]
                                fixed_joins.extend([candidate, xor_connection])
                                return True
                    return False
                if fix_xor_connection():
                    print('restarting..')
                    graph_inv = {v: k for k, v in graph.items() if isinstance(v, tuple)}
                    i = 0
                    continue
                else:
                    raise RuntimeError('Cannot fix it, exiting')

            elif sum_connection != f'z{index}' and i != last_index:
                print(f"bit z{index} doesnt match: {sum_connection} != z{index}")
                print('Fixing it')
                graph[sum_connection], graph[f'z{index}'] = graph[f'z{index}'], graph[sum_connection]
                fixed_joins.extend([sum_connection, f'z{index}'])
                print('restarting..')
                graph_inv = {v: k for k, v in graph.items() if isinstance(v, tuple)}
                i = 0
                continue

            carry_and = find_node(prev_carry, 'AND', xor_connection)
            carry_node = find_node(carry_and, 'OR', and_connection)
            carry[f'c{index}'] = carry_node
        i += 1

    # graph should be fixed now
    def calc_answer(x, y):
        x = f'{x:b}'.zfill(last_index)
        y = f'{y:b}'.zfill(last_index)

        for i in range(len(bits)):
            graph[f'x{i:02d}'] = int(x[last_index - i - 1])
            graph[f'y{i:02d}'] = int(y[last_index - i - 1])

        value = 0
        for bit in bits:
            value <<= 1
            value |= calc_value(graph, bit)

        return value

    def verify_graph():
        value = 1
        for i in range(last_index):
            z = calc_answer(value, value)
            if value + value != z:
                print(f"bit {i} doesnt match: {value} + {value} != {value}")
        return True

    if verify_graph():
        print("Graph is verified successfully.")
    else:
        raise RuntimeError("Graph verification failed.")

    return ','.join(sorted(fixed_joins))


class Day24(unittest.TestCase):

    def test_part1_example(self):
        self.assertEqual(4, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day24)
    unittest.TextTestRunner().run(suite)
