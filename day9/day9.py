import unittest

from aocd.models import Puzzle

puzzle = Puzzle(year=2024, day=9)


def parse(input_data):
    return list(map(int, list(input_data)))


def place_blocks(disk):
    space = [0] * sum(disk)
    i = 0
    pos = 0
    full = True
    for part in disk:
        if full:
            space[pos:pos + part] = [i] * part
            i += 1
        else:
            space[pos:pos + part] = [None] * part
        pos += part
        full = not full
    return space


def rearrange(disk):
    space = place_blocks(disk)
    last_full_index = len(space) - 1
    first_empty = disk[0]
    while True:
        while first_empty < len(space) and space[first_empty] is not None :
            first_empty += 1
        if first_empty >= len(space):
            return space
        while space[last_full_index] is None:
            last_full_index -= 1
            # if last_full_index < 0:
            #     return space
        space[first_empty] = space[last_full_index]
        space = space[:last_full_index]
        last_full_index -= 1
        first_empty += 1
        # for b in space:
        #     if b is None:
        #         print('.', end='')
        #     else:
        #         print(b, end='')
        # print()

def part1(input_data):
    disk = parse(input_data)
    disk = rearrange(disk)
    result = 0
    for idx, b in enumerate(disk):
        result += idx * b
    return result

def update_spaces(old_spaces):
    new_spaces = []
    for pos, len in sorted(old_spaces):
        if len > 0:
            new_spaces.append((pos, len))
    return new_spaces


def print_state(disk, files, spaces):
    for i in range(len(disk)):
        is_space = False
        file = None
        for sp, sl in spaces:
            if sp <= i < sp + sl:
                is_space = True
                break
        for file_pos, file_len, file_id in files:
            if file_pos <= i < file_pos + file_len:
                if is_space:
                    raise RuntimeError(f"Already space but file {file_id} found at pos {i}")
                file = file_id
        if is_space:
            print('.', end='')
        else:
            print(file, end='')
    print()

def part2(input_data):
    disk = parse(input_data)
    files = []
    spaces = []
    i = 0
    pos = 0
    full = True
    for part in disk:
        if full:
            files.append((pos,  part, i)) # start_pos, length, id
            i += 1
        else:
            spaces.append((pos,  part)) # start_pos, length,
        pos += part
        full = not full
    # print_state(disk, files, spaces) # validation
    for array_pos in reversed(range(len(files))):
        file_pos, file_len, file_id = files[array_pos]
        for space_array_pos in range(len(spaces)):
            space_pos, space_len = spaces[space_array_pos]
            if space_pos >= file_pos: # move only to left
                break
            if space_len >= file_len: # found space
                files[array_pos] = (space_pos, file_len, file_id)
                spaces[space_array_pos] = (space_pos + file_len, space_len - file_len)
                # spaces.append((file_pos, file_len))  # not needed
                # spaces = update_spaces(spaces) # not needed
                # print(f'moving {file_id} to {space_pos}, space id {space_pos} left {space_len - file_len} length, new pos is {space_pos + file_len}')
                break
            # print_state(disk, files, spaces)
    result = 0
    for file_pos, file_len, file_id in files:
        for i in range(file_len):
            result += (file_pos + i) * file_id
    return result

class Day9(unittest.TestCase):
    def test_placing_blocks(self):
        blocks = place_blocks(parse(puzzle.examples[0].input_data))
        result = ""
        for b in blocks:
            if b is not None:
                result += str(b)
            else:
                result += "."
        self.assertEqual("00...111...2...333.44.5555.6666.777.888899",
                         result)

    def test_part1_example(self):
        self.assertEqual(1928, part1(puzzle.examples[0].input_data))

    def test_part1(self):
        puzzle.answer_a = part1(puzzle.input_data)

    def test_part2_example(self):
        self.assertEqual(2858, part2(puzzle.examples[0].input_data))

    def test_part2(self):
        puzzle.answer_b = part2(puzzle.input_data)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Day9)
    unittest.TextTestRunner().run(suite)
