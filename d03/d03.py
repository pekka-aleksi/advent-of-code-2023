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


def part2(data):
    coords_to_check = list()

    checks = '*'

    for operator_y, neighbor_row in enumerate(data):
        for operator_x, col in enumerate(neighbor_row):
            if col in checks:
                coords_to_check.append((operator_y,operator_x))

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


    all_neighbors_per_mult = {}

    for candidate, candidates in EVERYTHING.items():
        all_neighbors_per_mult[candidate] = collections.defaultdict(set)
        for candidatelist in candidates:
            for y, x, number in candidatelist:
                all_neighbors_per_mult[candidate][y].add((x, number))

    built_up_numbers = list()

    for (multiplier_y, multiplier_x), neighbor_value_and_x in all_neighbors_per_mult.items():

        for neighbor_row, neighbor_row_full_data in neighbor_value_and_x.items():

            if multiplier_y == neighbor_row and len(neighbor_row_full_data) > 1:

                left_cands = [entry for entry in neighbor_row_full_data if entry[0] - multiplier_x < 0]
                right_cands = [entry for entry in neighbor_row_full_data if multiplier_x - entry[0] < 0]

                LEFTS, RIGHTS = 0, 0
                match len(left_cands), len(right_cands):
                    case 0, 0:
                        continue

                    case left_cands_len, right_cands_len:

                        L, R = list(zip(*sorted(left_cands))), list(zip(*sorted(right_cands)))
                        print(multiplier_y, multiplier_x, neighbor_value_and_x, L, R)

                        match len(L), len(R):
                            case l, 0:

                                LEFTS = int("".join(L[1]))
                                assert LEFTS != 0
                                built_up_numbers.append(LEFTS)

                            case 0, r:
                                RIGHTS = int("".join(R[1]))
                                assert RIGHTS != 0, f"RIGHTS {r}, {LEFTS}, {RIGHTS}, {neighbor_value_and_x.items()}"
                                built_up_numbers.append(RIGHTS)


                            case l, r:

                                LEFTS = int("".join(L[1]))
                                RIGHTS = int("".join(R[1]))
                                assert RIGHTS != 0, f"LEFTS RIGHTS {l}, {r}, {LEFTS}, {RIGHTS}, {neighbor_value_and_x.items()}"
                                built_up_numbers.append(LEFTS)
                                built_up_numbers.append(RIGHTS)


                            case _:
                                print("WHAT")

            else:

                cands = int("".join(list(zip(*sorted(neighbor_row_full_data)))[1]))
                assert cands != 0
                built_up_numbers.append(cands)

    assert len(built_up_numbers) % 2 == 0, built_up_numbers

    print("Nämä rakennettiin", built_up_numbers)
    #print(*all_neighbors_per_mult.items(), sep='\n')

    R = [built_up_numbers[2*i:2*(i+1)] for i, X in enumerate(built_up_numbers) if X]
    V = [x for x in map(math.prod, R) if x > 1]

    print(R, V)
    return sum(V)


data = get_data('test.txt')
print(part2(data=data))
