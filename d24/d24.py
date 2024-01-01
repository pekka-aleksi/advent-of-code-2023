import re
import sympy
from sympy.abc import x, y


def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        data = file.read().splitlines()
        new_data = list()
        try:
            for row in data:
                first, second = row.replace(',', '').split(' @ ')
                entries = first + " " + second
                new_data.append(entries.split())
        except IndexError as indexerror:
            print(indexerror)
        new_data = [[int(x) for x in row] for row in new_data]
    return new_data


import numpy as np
import itertools


def get_quadrant(given_line, intersection_point):
    points = given_line.points
    start_point, direction_point = points
    direction_point = direction_point - start_point

    k = start_point.x <= intersection_point.x, start_point.y <= intersection_point.y, direction_point.x <= 0, direction_point.y <= 0

    match k:

        case T if T == (True, True, False, False):
            return True  # OK

        case T if T == (False, False, True, True):
            return True  # OK

        case T if T == (True, False, False, True):
            return True  # OK

        case T if T == (False, True, True, False):
            return True

        case _:
            #print(start_point, direction_point)
            return False


def part1(data):
    p = list()
    v = list()

    rows = data
    LEN = len(rows)

    W = 0
    BOX_MIN, BOX_MAX = 200_000_000_000_000, 400_000_000_000_000
    #BOX_MIN, BOX_MAX = 7, 27

    for i, (row_a, row_b) in enumerate(itertools.product(rows, repeat=2)):

        if i % LEN == 0:
            W += 1

        if i % LEN in range(W):
            continue

        positions = row_a[0:2]
        velocities = row_a[3:5]
        p.append(positions)
        v.append(velocities)

        positions = row_b[0:2]
        velocities = row_b[3:5]
        p.append(positions)
        v.append(velocities)

    s = np.array(p)
    v = np.array(v)

    counter = 0

    for i, (a, b) in enumerate(zip(s, v), 1):

        if i % 10000 == 0:
            print(f"{i}/{len(s)}")

        if i % 2 == 0:
            continue

        if i == len(s):
            break

        s_x1, s_x2 = a, s[i]
        v_x1, v_x2 = b, v[i]

        start1 = sympy.Point(s_x1)
        direction1 = sympy.Point(s_x1 + v_x1)

        start2 = sympy.Point(s_x2)
        direction2 = sympy.Point(s_x2 + v_x2)

        line1 = sympy.Line(start1, direction1)
        line2 = sympy.Line(start2, direction2)

        all_points = line1.intersection(line2)

        in_square = [point for point in all_points if
                     (BOX_MIN <= point.x <= BOX_MAX) and (BOX_MIN <= point.y <= BOX_MAX)]

        if in_square:
            intersection_point = in_square[0]
            ok = get_quadrant(line1, intersection_point) and get_quadrant(line2, intersection_point)
            if ok:
                counter += 1

    return counter

data = get_data('input.txt')
print(part1(data))
