import re

def plot(S, coords, rows):
    MAX_Y = max([(y, x) for y, x in coords], key=lambda c: c[0])[0] + 2
    MAX_X = max([(y, x) for y, x in coords], key=lambda c: c[1])[1] + 2

    for y in range(MAX_Y):
        for x in range(MAX_X):

            if (y, x) == S:
                print("S", end='')
            elif (y, x) in coords:
                print(rows[y][x], end='')
            else:
                print(".", end='')
        print()


def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        data = file.read().splitlines()

    for y, row in enumerate(data):
        k = re.search(r'S', row)
        if k:
            start_position = (y, min(k.span()))
            # print(start_position)

    return start_position, data

def get_neighbors(position, given_data):
    y, x = position

    UPPER = max(y - 1, 0)
    LOWER = min(y + 1, len(given_data) - 1)
    LEFT = max(x - 1, 0)
    RIGHT = min(x + 1, len(given_data[0]) - 1)

    neighbors_wrt_to_current = {(UPPER, x), (y, LEFT), (y, RIGHT), (LOWER, x)} - {(y,x)}

    print(f"{UPPER = } {LOWER = } {RIGHT = } {LEFT = }")

    all_possibilities = {
        '|': {'below': 'N', 'above': 'S'}, '-': {'right': 'W', 'left': 'E'},
        'L': {'below': 'N', 'left': 'E'}, 'J': {'below': 'N', 'right': 'W'},
        '7': {'above': 'S', 'right': 'W'}, 'F': {'above': 'S', 'left': 'E'}
    }
    piecewise = {key: {val for val in inner.values()} for key, inner in all_possibilities.items()}

    interesting_neighbors = set()

    for neighbor_y, neighbor_x in neighbors_wrt_to_current:

        print(neighbor_y, neighbor_x, end='\t')

        current_piece = given_data[y][x]
        neighbor_piece = given_data[neighbor_y][neighbor_x]
        neighbor_data = all_possibilities.get(neighbor_piece, dict())

        match neighbor_y, neighbor_x:
            case t, _ if t == UPPER and UPPER != y:
                print("LOOKING UP")
                NEIGHBOR_ALLOWS = neighbor_data.get('above', "")
                NEIGHBOR_WHAT = piecewise.get(neighbor_piece, set())

                if {NEIGHBOR_ALLOWS}.intersection(NEIGHBOR_WHAT):
                    print("- added")
                    interesting_neighbors.add((neighbor_y, neighbor_x))

            case _, t if t == LEFT and LEFT != x:
                print("LOOKING LEFT")
                NEIGHBOR_ALLOWS = neighbor_data.get('left', "")
                NEIGHBOR_WHAT = piecewise.get(neighbor_piece, set())

                if {NEIGHBOR_ALLOWS}.intersection(NEIGHBOR_WHAT):
                    print("- added")
                    interesting_neighbors.add((neighbor_y, neighbor_x))

            case _, t if t == RIGHT and RIGHT != x:
                print("LOOKING RIGHT")
                NEIGHBOR_ALLOWS = neighbor_data.get('right', "")
                NEIGHBOR_WHAT = piecewise.get(neighbor_piece, set())

                if {NEIGHBOR_ALLOWS}.intersection(NEIGHBOR_WHAT):
                    print("- added")
                    interesting_neighbors.add((neighbor_y, neighbor_x))

            case t, _ if t == LOWER and LOWER != y:
                print("LOOKING DOWN")

                NEIGHBOR_ALLOWS = neighbor_data.get('below', "")
                #NEIGHBOR_WHAT = piecewise.get(neighbor_piece, set())  # we're not this
                WE_ALLOW = all_possibilities.get(current_piece, dict()).get('above', set())


                # there's a problem here -- python is intersecting the LETTERS of the string
                # not the strings
                new_set = set()
                new_set.add(NEIGHBOR_ALLOWS)
                if new_set.intersection(WE_ALLOW):
                    print(new_set)
                    print(WE_ALLOW)
                    print(new_set.intersection(WE_ALLOW))
                    print(f"- added")
                    interesting_neighbors.add((neighbor_y, neighbor_x))
            case _:
                assert False

    return interesting_neighbors




def part1(data):
    start_position, rows = data


    known_neighbors = get_neighbors(position=start_position, given_data=rows)

    neighbor = list(known_neighbors)[-1]

    while True:
        plot(neighbor, known_neighbors, rows)

        new_neighbors = get_neighbors(position=neighbor, given_data=rows)

        completely_new_neighbors = new_neighbors - known_neighbors
        print(f"{known_neighbors = } {new_neighbors = } {completely_new_neighbors = }")

        if not completely_new_neighbors:
            break
        else:
            neighbor = list(completely_new_neighbors)[0]
            known_neighbors = known_neighbors.union(new_neighbors)



    plot(start_position, known_neighbors, rows)





data = get_data('loop.txt')
part1(data)
print("-" * 80)
"""
data = get_data('loop2.txt')
part1(data)
print("-" * 80)

data = get_data('loop2mess.txt')
part1(data)

print("-" * 80)
data = get_data('wrong.txt')
part1(data)
print("-" * 80)
"""

"""
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

.....
.....
SJ...
|F--J
LJ.LJ
"""



"JL" # laiton

"LJ" # laillinen


"--" # laillinen
"--" # laillinen

"-J" # laillinen
"J-" # laiton

#
