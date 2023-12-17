import collections
import string
import re

import math


def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        lines = file.read().splitlines()

        lines = [line for line in lines]

    return lines


def part1(data):
    # 1. find (y,x) coordinates for each non-numeric symbol
    # 2. check the symbols again for the 8 adjacent squares for numbers - add them to the list

    coords_to_check = list()

    checks = set(string.punctuation) - set('.')
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            if col in checks:
                coords_to_check.append((y, x))

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


def my_span(test_list, all_operators, operator_y, operator_x):
    for (span_low, span_high), number in test_list:
        match operator_x, span_low, span_high:
            case centerpoint, start, end if start <= centerpoint <= end or centerpoint+1 == start or centerpoint == end:
                print(f"We found {number} ({operator_y}, {operator_x})")
                all_operators[(operator_y, operator_x)].add(number)
            case _:
                print(operator_x, number, span_low, span_high)


def part2(data):
    RE_number = re.compile(r'(?P<number>\d+)')
    RE_oper = re.compile(r'(?P<operator>\*)')

    all_operators = collections.defaultdict(set)
    for y, (row1, row2, row3) in enumerate(zip(data, data[1:], data[2:])):

        numero1 = re.finditer(RE_number, row1)
        numero2 = re.finditer(RE_number, row2)
        numero3 = re.finditer(RE_number, row3)

        oper1 = re.finditer(RE_oper, row1)
        oper2 = re.finditer(RE_oper, row2)
        oper3 = re.finditer(RE_oper, row3)

        n1 = [(x.span(), x.group('number')) for x in numero1]
        n2 = [(x.span(), x.group('number')) for x in numero2]
        n3 = [(x.span(), x.group('number')) for x in numero3]

        for oper_x in [min(x.span()) for x in oper1]:
            my_span(n1, all_operators, operator_y=y, operator_x=oper_x)
            my_span(n2, all_operators, operator_y=y, operator_x=oper_x)

        for oper_x in [min(x.span()) for x in oper2]:
            my_span(n1, all_operators, operator_y=y+1, operator_x=oper_x)
            my_span(n2, all_operators, operator_y=y+1, operator_x=oper_x)
            my_span(n3, all_operators, operator_y=y+1, operator_x=oper_x)

        for oper_x in [min(x.span()) for x in oper3]:
            my_span(n2, all_operators, operator_y=y+2, operator_x=oper_x)
            my_span(n3, all_operators, operator_y=y+2, operator_x=oper_x)

    juttu = {k: v for k, v in all_operators.items() if len(v) > 1}

    vektorit = map(list, list(juttu.values()))

    summa = 0
    for vektori in vektorit:
        result = math.prod(list(map(int, vektori)))
        summa += result

    return summa


data = get_data('input.txt')
print(part2(data=data))
