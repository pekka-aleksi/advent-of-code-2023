import re


def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        data = file.read().splitlines()
        regex = re.compile(r'(\d+), (\d+), (\d+) @ ([-| ]\d+), ([-| ]\d+), ([-| ]\d+)')
        data = [regex.findall(row)[0] for row in data]
        data = [[int(x) for x in row] for row in data]
    return data


import numpy as np
import itertools


def part1(data):
    p = list()
    v = list()

    rows = data[:2]
    LEN = len(rows)

    W = 0

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

    s = np.array(p).T
    v = np.array(v).T
    s_x, s_y = s[0], s[1]
    v_x, v_y = v[0], v[1]

    
    print(s_x, s_y)
    print(v_x, v_y)



data = get_data('example.txt')
part1(data)

# Hailstone A: 19, 13 @ -2, 1
# Hailstone B: 18, 19 @ -1, -1
# Hailstones' paths will cross inside the test area (at x=14.333, y=15.333).


# Hailstone A: 19, 13 @ -2, 1
# Hailstone B: 20, 25 @ -2, -2
# Hailstones' paths will cross inside the test area (at x=11.667, y=16.667).
