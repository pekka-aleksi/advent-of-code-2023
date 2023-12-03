import collections
import string
import re

import math

def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        lines = file.read().splitlines()

        lines = [line for line in lines]

    return lines


def continue_left(ny, nx, dataset):
    LEFT = nx - 1

    if num := dataset[ny][LEFT] > 0 and LEFT > 0:
        return num
    return False


def continue_right(ny, nx, dataset):
    MAX_X = len(dataset[0]) - 1
    RIGHT = nx + 1

    if num := dataset[ny][RIGHT] > 0 and RIGHT < MAX_X:
        return num
    return False


def part1(data):
    # 1. find (y,x) coordinates for each non-numeric symbol
    # 2. check the symbols again for the 8 adjacent squares for numbers - add them to the list

    coords_to_check = list()

    checks = set(string.punctuation) - set('.')
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            if col in checks:
                coords_to_check.append((y,x))


    numbers_found = {}
    MAX_X = len(data[0]) - 1
    MAX_Y = len(data) - 1

    for y, x in coords_to_check:
        UPPER, SAME, LOWER = max(y - 1, 0), max(y, 0), min(y + 1, MAX_Y)
        LEFT, RIGHT = max(x - 1, 0), min(x + 1, MAX_X)

        A = data[UPPER][LEFT]
        B = data[UPPER][x]
        C = data[UPPER][RIGHT]

        D = data[SAME][LEFT]
        E = data[SAME][RIGHT]

        F = data[LOWER][LEFT]
        G = data[LOWER][x]
        H = data[LOWER][RIGHT]

        numbers_found[UPPER] = numbers_found.get(UPPER, list())
        numbers_found[UPPER].extend([(LEFT, A), (x, B), (RIGHT, C)])

        numbers_found[SAME] = numbers_found.get(SAME, list())
        numbers_found[SAME].extend([(LEFT, D), (RIGHT, E)])

        numbers_found[LOWER] = numbers_found.get(LOWER, list())
        numbers_found[LOWER].extend([(LEFT, F), (x, G), (RIGHT, H)])

    RE = re.compile(r'(\d+)')

    true_numbers = dict()
    for y, row in enumerate(data):
        for iter in re.finditer(RE, row):
            for coordinate, number in numbers_found[y]:

                if min(iter.span()) <= coordinate <= max(iter.span()) and number in string.digits:
                    true_numbers[(y, iter.span())] = int(iter.groups()[0])


    return sum(true_numbers.values())


def part2(data):
    coords_to_check = list()

    checks = '*'
    for operator_y, row in enumerate(data):
        for operator_x, col in enumerate(row):
            if col in checks:
                coords_to_check.append((operator_y,operator_x))

    RECURSION_RETURN = []
    def return_flow(dataset, ny, nx):

        MAX_X = len(dataset[0]) - 1
        MAX_Y = len(dataset) - 1

        # we only move nx + 1 and nx - 1
        if ny < 0 or ny > MAX_Y or nx < 0 or nx > MAX_X or dataset[ny][nx] not in string.digits:
            return RECURSION_RETURN

        if dataset[ny][nx] in string.digits:
            VAL = return_flow(dataset, ny, nx - 1)
            return [(ny, nx, dataset[ny][nx])] + (VAL if VAL else [])

    def return_flow_right(dataset, ny, nx):

        MAX_X = len(dataset[0]) - 1
        MAX_Y = len(dataset) - 1

        # we only move nx + 1 and nx - 1
        if ny < 0 or ny > MAX_Y or nx < 0 or nx > MAX_X or dataset[ny][nx] not in string.digits:
            return RECURSION_RETURN

        if dataset[ny][nx] in string.digits:
            VAL = return_flow_right(dataset, ny, nx + 1)
            return [(ny, nx, dataset[ny][nx])] + (VAL if VAL else [])


    EVERYTHING = {}

    for operator_y, operator_x in coords_to_check:

        A = return_flow(data, operator_y-1, operator_x-1)
        B = return_flow(data, operator_y-1, operator_x)
        C = return_flow(data, operator_y-1, operator_x+1)

        D = return_flow(data, operator_y, operator_x-1)
        E = return_flow(data, operator_y, operator_x+1)

        F = return_flow(data, operator_y+1, operator_x-1)
        G = return_flow(data, operator_y+1, operator_x)
        H = return_flow(data, operator_y+1, operator_x+1)

        EVERYTHING[(operator_y, operator_x)] = [x for x in [A, B, C, D, E, F, G, H] if x]

        A = return_flow_right(data, operator_y-1, operator_x-1)
        B = return_flow_right(data, operator_y-1, operator_x)
        C = return_flow_right(data, operator_y-1, operator_x+1)

        D = return_flow_right(data, operator_y, operator_x-1)
        E = return_flow_right(data, operator_y, operator_x+1)

        F = return_flow_right(data, operator_y+1, operator_x-1)
        G = return_flow_right(data, operator_y+1, operator_x)
        H = return_flow_right(data, operator_y+1, operator_x+1)

        EVERYTHING[(operator_y, operator_x)].extend([x for x in [A, B, C, D, E, F, G, H] if x])


    numbers_per_candidate = {}

    for candidate, candidates in EVERYTHING.items():
        numbers_per_candidate[candidate] = collections.defaultdict(set)
        for candidatelist in candidates:
            for y, x, number in candidatelist:
                numbers_per_candidate[candidate][y].add((x, number))

    A = list()

    for (candidate_y, candidate_x), candidatedata in numbers_per_candidate.items():


        for row, rowdata in candidatedata.items():

            if candidate_y == row and len(rowdata) > 1:
                left_cands = [entry for entry in rowdata if entry[0] < candidate_x]
                right_cands = [entry for entry in rowdata if entry[0] > candidate_x]


                if not(not len(left_cands) and not len(right_cands)):
                    continue

                LEFTS = int("".join(list(zip(*sorted(left_cands)))[1]))
                RIGHTS = int("".join(list(zip(*sorted(right_cands)))[1]))

                A.append(LEFTS)
                A.append(RIGHTS)

            else:
                cands = int("".join(list(zip(*sorted(rowdata)))[1]))
                A.append(cands)

    assert len(A) % 2 == 0

    return sum(list(map(math.prod, [A[2*i:2*(i+1)] for i, X in enumerate(A) if X])))


# 3*4
# 5*6
# 7*8
# 9*10
# 11*12
# 13*14
# 15*16

data = get_data('test.txt')
print(part2(data=data))
