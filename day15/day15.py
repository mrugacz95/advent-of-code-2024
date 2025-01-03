import unittest
from collections import defaultdict
from copy import deepcopy
from typing import Optional, List, Tuple

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=15)

BOX = "O"
ROBOT = "@"
EMPTY = "."
WALL = "#"


def parse(input_data) -> Tuple[List[List[chr]], str, Tuple[int, int]]:
    store, moves = input_data.split("\n\n")
    moves = moves.replace("\n", "")
    store = [list(line) for line in store.split("\n")]

    def find_robot():
        for y, row in enumerate(store):
            for x, row in enumerate(row):
                if row == ROBOT:
                    store[y][x] = EMPTY
                    return y, x

    pos = find_robot()
    return store, moves, pos


def dir_to_delta(dir) -> Tuple[int, int]:
    if dir not in ('^', 'v', '<', '>'):
        raise ValueError(f"Invalid direction {dir}")
    return {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1),
    }.get(dir)


def print_store(store, pos):
    for y, line in enumerate(store):
        for x, c in enumerate(line):
            if y == pos[0] and x == pos[1]:
                print(ROBOT, end="")
            else:
                print(c, end="")
        print()
    print()


def print_store_with_boxes(store, pos, boxes):
    printable = deepcopy(store)
    for box in boxes:
        assert printable[box[0]][box[1]] != WALL and printable[box[0]][box[1] + 1] != WALL
        printable[box[0]][box[1]] = '['
        printable[box[0]][box[1] + 1] = ']'
    print_store(printable, pos)


def part1(input_data):
    store, moves, pos = parse(input_data)
    print_store(store, pos)
    for move in moves:
        # print(f"Move {move}:")
        dy, dx = dir_to_delta(move)
        ny, nx = pos[0] + dy, pos[1] + dx
        if store[ny][nx] == EMPTY:
            pos = (ny, nx)
        else:
            while store[ny][nx] != WALL and store[ny][nx] != EMPTY:
                ny += dy
                nx += dx
            if store[ny][nx] == WALL:  # dont move
                pass
            else:  # push boxes
                store[ny][nx] = BOX
                pos = pos[0] + dy, pos[1] + dx
                store[pos[0]][pos[1]] = EMPTY
        # print_store(store, pos)
    checksum = 0
    for y, line in enumerate(store):
        for x, c in enumerate(line):
            if store[y][x] == BOX:
                checksum += y * 100 + x
    return checksum


def enlarge_warehouse(store, pos):
    new_store = []
    boxes = []
    for y, line in enumerate(store):
        row = []
        for x, c in enumerate(line):
            if c == BOX:
                boxes.append((y, x * 2))
                row.append('.')
                row.append('.')
            elif c == EMPTY:
                row.append('.')
                row.append('.')
            elif c == WALL:
                row.append('#')
                row.append('#')
        new_store.append(row)
    pos = pos[0], pos[1] * 2
    return new_store, boxes, pos


def get_box_id(boxes, y, x):
    for i, box in enumerate(boxes):
        if box[0] == y:
            if box[1] == x or box[1] + 1 == x:
                return i
    return None


def get_object(boxes, store, y, x):
    if (y, x) in boxes:
        return BOX
    elif (y, x - 1) in boxes:
        return BOX
    elif store[y][x] == WALL:
        return WALL
    return EMPTY


def get_box_fields(store, boxes):
    occupied: List[List[Optional[int]]] = []
    for y, line in enumerate(store):
        occupied.append([None] * len(line))
    for i, box in enumerate(boxes):
        occupied[box[0]][box[1]] = i
        occupied[box[0]][box[1] + 1] = i
    return occupied


def get_new_affected_positions(boxes, dy, dx, py, px):
    box_id = get_box_id(boxes, py, px)
    positions = []
    box_pos = boxes[box_id]
    left, right = (box_pos[0], box_pos[1]), (box_pos[0], box_pos[1] + 1)
    # left side
    ny, nx = left[0] + dy, left[1] + dx
    positions.append((ny, nx))
    # right side
    ny, nx = right[0] + dy, right[1] + dx
    positions.append((ny, nx))
    return box_id, positions


def part2(input_data):
    store, moves, pos = parse(input_data)
    store, boxes, pos = enlarge_warehouse(store, pos)
    print_store_with_boxes(store, pos, boxes)

    for move in moves:
        # print(f"Move {move}:")
        dy, dx = dir_to_delta(move)
        ny, nx = pos[0] + dy, pos[1] + dx
        if get_object(boxes, store, ny, nx) == EMPTY:
            pos = (ny, nx)
        elif get_object(boxes, store, ny, nx) == WALL:
            pass  # dont move
        else:  # one or more boxes
            queue: List[Tuple[int, int]] = [(ny, nx)]
            visited = defaultdict(lambda: False)
            affected_boxes = set()
            moving = True
            while len(queue) != 0:
                py, px = queue.pop(0)
                if visited[(py, px)]:
                    continue
                visited[(py, px)] = True
                obj = get_object(boxes, store, py, px)
                if obj == WALL:
                    moving = False
                    break
                if obj == EMPTY:
                    continue
                if obj == BOX:
                    box_id, positions = get_new_affected_positions(boxes, dy, dx, py, px)
                    affected_boxes.add(box_id)
                    queue.extend(positions)
            # affect boxes, move robot
            if moving:
                for box_id in affected_boxes:
                    y, x = boxes[box_id]
                    by, bx = y + dy, x + dx
                    boxes[box_id] = (by, bx)
                pos = pos[0] + dy, pos[1] + dx
        # print_store_with_boxes(store, pos, boxes)
    checksum = 0
    for by, bx in boxes:
        checksum += by * 100 + bx
    return checksum


class Day15(unittest.TestCase):

    def test_part1_smaller_example(self):
        example = "\n".join(("########",
                             "#..O.O.#",
                             "##@.O..#",
                             "#...O..#",
                             "#.#.O..#",
                             "#...O..#",
                             "#......#",
                             "########",
                             "",
                             "<^^>>>vv<v>>v<<"))
        self.assertEqual(2028, part1(example))

    def test_part1_example(self):
        self.assertEqual(10092, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_small_example(self):
        example = "\n".join(("#######",
                             "#...#.#",
                             "#.....#",
                             "#..OO@#",
                             "#..O..#",
                             "#.....#",
                             "#######",
                             "",
                             "<vv<<^^<<^^",))
        self.assertEqual(618, part2(example))

    def test_part2_example(self):
        self.assertEqual(9021, part2(puzzle.examples[0].input_data))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day15)
    unittest.TextTestRunner().run(suite)
