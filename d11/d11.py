import re
import itertools
from scipy.spatial import distance_matrix  # type: ignore
import copy

def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        data = file.read().splitlines()
        coords = [(y, [min(match.span()) for match in re.finditer('#', row)]) for y, row in enumerate(data)]

    return coords


def plot(coords):
    MAX_Y = max([(y, x) for y, x in coords], key=lambda c: c[0])[0] + 1
    MAX_X = max([(y, x) for y, x in coords], key=lambda c: c[1])[1] + 1

    for y in range(MAX_Y):
        for x in range(MAX_X):
            if [y, x] in coords:
                print('#', end='')
            else:
                print(".", end='')
        print()


def part1(data):
    y_data = copy.deepcopy(data)

    valid_cols = set()
    for row, col in data:
        valid_cols |= set(col)
    all_cols = set(range(0, max(valid_cols) + 1))

    missing_cols = all_cols - valid_cols
    missing_rows = [row for row, entries in y_data if not entries]

    original_stars = [[row, entry] for row, col in data for entry in col]

    new_stars = copy.deepcopy(original_stars)

    for missing_x in sorted(missing_cols):
        for star_index in range(len(original_stars)):
            if missing_x < original_stars[star_index][1]:
                new_stars[star_index][1] = new_stars[star_index][1] + (1_000_000 - 1)

    for missing_y in sorted(missing_rows):
        for star_index in range(len(original_stars)):
            if missing_y < original_stars[star_index][0]:
                new_stars[star_index][0] = new_stars[star_index][0] + (1_000_000 - 1)

    #plot(new_stars)



    results = distance_matrix(new_stars, new_stars, p=1)

    print(results.sum() / 2)

    return results.sum() / 2


    
    def dist(A, B):
        x1, y1 = A
        x2, y2 = B
        return abs(x1 - x2) + abs(y1 - y2)

    done_pairs = list()

    S = 0

    
    for i, (one, two) in enumerate(itertools.product(new_stars, repeat=2)):

        if i % 10000 == 0:
            print("Progress: {}/{}".format(i, len(new_stars)**2))

        if one == two:
            continue

        if (one, two) not in done_pairs:

            done_pairs.append((one, two))
            done_pairs.append((two, one))

            X = dist(one, two)

            #print(X, one, two)
            #print(i, one, two, X)
            S += X


    print(f"\n{S}\n{new_stars}")
    print("-" * 80)


data = get_data('trivial1.txt')
part1(data)
data = get_data('trivial2.txt')
part1(data)
data = get_data('trivial3.txt')
part1(data)
data = get_data('trivial4.txt')
part1(data)
data = get_data('trivial5.txt')
part1(data)
data = get_data('trivial6.txt')
part1(data)
data = get_data('input.txt')
part1(data)
