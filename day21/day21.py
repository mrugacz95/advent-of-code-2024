import unittest
import re
from functools import cache

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=21)


def parse(input_data):
    return input_data.splitlines()


def pad_to_dict(pad):
    positions = {}
    for y, line in enumerate(pad):
        for x, c in enumerate(line):
            if c != " ":
                positions[c] = (y, x)
    return positions


numpad = [
    "789",
    "456",
    "123",
    " 0A"
]

NUM_POS = pad_to_dict(numpad)

dirpad = [
    " ^A",
    "<v>",
]

DIR_POS = pad_to_dict(dirpad)

@cache
def find_path(pos, num, use_numpad):
    if use_numpad:
        positions = NUM_POS
        pad = numpad
    else:
        positions = DIR_POS
        pad = dirpad


    def next_move(from_pos, to_pos):
        h_diff = abs(from_pos[1] - to_pos[1])
        v_diff = abs(from_pos[0] - to_pos[0])
        if from_pos[0] < to_pos[0] and pad[from_pos[0] + v_diff][from_pos[1]] != " ":
            return v_diff, 0, "v" * v_diff
        elif from_pos[1] < to_pos[1] and pad[from_pos[0]][from_pos[1] + h_diff] != " ":
            return 0, h_diff, ">" * h_diff
        elif from_pos[1] > to_pos[1] and pad[from_pos[0]][from_pos[1] - h_diff] != " ":
            return 0, -h_diff, "<" * h_diff
        elif from_pos[0] > to_pos[0] and pad[from_pos[0] - v_diff][from_pos[1]] != " ":
            return -v_diff, 0, "^" * v_diff
        raise ValueError(f"Cannot move from {from_pos} to {to_pos}")

    path = ""
    num_pos = positions[num]
    while pos != num_pos:
        dy, dx, move = next_move(pos, num_pos)
        pos = (pos[0] + dy, pos[1] + dx)
        path += move
        if pos not in positions.values():
            raise ValueError(f"Went outside of pad on position {pos} on pad {pad}")
        if pad[pos[0]][pos[1]] == " ":
            raise ValueError(f"Invalid position {pos} on pad {pad}")
    if not re.match(r"^((<+)|(>+)|(v+)|(\^+)){0,2}$", path):
        raise ValueError(f"Invalid path {path} to {num} from {pos} on pad {pad}")
    return path, pos


def find_movement(numcode: str) -> str:
    pos = (3, 2)
    num_robot_path = ""
    for num in numcode:
        path, pos = find_path(pos, num, use_numpad=True)
        num_robot_path += path
        num_robot_path += "A"
    pos = (0, 2)
    first_robot_path = ""
    for d in num_robot_path:
        path, pos = find_path(pos, d, use_numpad=False)
        first_robot_path += path
        first_robot_path += "A"
    pos = (0, 2)
    second_robot_path = ""
    for d in first_robot_path:
        path, pos = find_path(pos, d, use_numpad=False)
        second_robot_path += path
        second_robot_path += "A"
    return second_robot_path


def validate_path(path: str) -> bool:
    num_pos = (3, 2)
    first_pos = (0, 2)
    second_pos = (0, 2)

    move_to_delta = {
        '>': (0, 1),
        '<': (0, -1),
        'v': (1, 0),
        '^': (-1, 0),
    }

    first_path = ""
    for move in path:
        if move == 'A':
            first_path += dirpad[second_pos[0]][second_pos[1]]
        else:
            delta = move_to_delta[move]
            second_pos = (second_pos[0] + delta[0], second_pos[1] + delta[1])

    num_path = ""
    for move in first_path:
        if move == 'A':
            num_path += dirpad[first_pos[0]][first_pos[1]]
        else:
            delta = move_to_delta[move]
            first_pos = (first_pos[0] + delta[0], first_pos[1] + delta[1])

    code = ""
    for move in num_path:
        if move == 'A':
            code += numpad[num_pos[0]][num_pos[1]]
        else:
            delta = move_to_delta[move]
            num_pos = (num_pos[0] + delta[0], num_pos[1] + delta[1])

    return code


def part1(input_data):
    codes = parse(input_data)
    ans = 0
    for code in codes:
        path = find_movement(code)
        print(f"Code: {code}, Path: {path} Num: {int(code[:-1])}, Path length: {len(path)}")
        ans += len(path) * int(code[:-1])
    return ans


def find_longer_movement(numcode: str, dir_robots: int ) -> str:
    pos = (3, 2)
    num_robot_path = ""
    for num in numcode:
        path, pos = find_path(pos, num, True)
        num_robot_path += path
        num_robot_path += "A"

    prev_robot_path = num_robot_path
    for i in range(dir_robots):
        pos = (0, 2)
        new_robot_path = ""
        for d in prev_robot_path:
            path, pos = find_path(pos, d, False)
            new_robot_path += path
            new_robot_path += "A"
        prev_robot_path = new_robot_path
        print("Length of robot path", i + 1, ":", len(prev_robot_path)) # :)

    return prev_robot_path


def part2(input_data, dir_robots = 25):
    codes = parse(input_data)
    ans = 0
    for code in codes:
        path = find_longer_movement(code, dir_robots)
        print(f"Code: {code}, Path: {path} Num: {int(code[:-1])}, Path length: {len(path)}")
        ans += len(path) * int(code[:-1])
    return ans


class Day21(unittest.TestCase):

    def test_find_movement_dir(self):
        self.assertEqual(find_path((0, 1), '<', False), ("v<", (1, 0)))

    def test_find_movement_num(self):
        self.assertEqual(find_path((0, 0), 'A', True), (">>vvv", (3, 2)))

    def test_find_path(self):
        self.assertEqual(find_movement('343'), 'v<<A>>^AvA^A<vA<AA>>^AAvA<^A>AvA^A<vA>^AAv<<A>>^AvA<^A>A')
        # v<<A>>^AvA^A<vA<AA>>^AAvA<^A>AvA^A<vA>^AAv<<A>>^AvA<^A>A
        # <A>Av<<AA>^A>AvAA<A>^A
        # ^A<<^A>>vA
        # 34

    def test_validate_path(self):
        self.assertEqual(validate_path(find_movement('343A')), '343A')

    def test_part1_example(self):
        self.assertEqual(126384, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    # 227898

    def test_part2_example(self):
        self.assertEqual(126384, part2(puzzle.examples[0].input_data, 2))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day21)
    unittest.TextTestRunner().run(suite)
