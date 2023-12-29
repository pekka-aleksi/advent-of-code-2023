import collections


def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        data = file.read().splitlines()

    return data


import re

def part1(data):

    cols = len(data[0])
    rows = len(data)
    rocks = {i: {'O': list(), '#': list()} for i in range(cols)}

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            match char:
                case 'O':
                    rocks[x]['O'].append(rows-y)
                case '#':
                    rocks[x]['#'].append(rows-y)
                case _:
                    pass

    points = 0
    point_boulders = list()

    for column, vals in rocks.items():
        boulders = vals.get('#', []) + [0]
        to_get = vals.get('O', [])

        if not boulders:
            point_boulder = [rows-i for i in range(len(to_get))]
            print(column, boulders, point_boulder)
            points += sum(point_boulder)
            point_boulders.extend(point_boulder)
        else:
            counter_per_column = 0

            higher_stop = rows+1

            for lower_stop in sorted(boulders, reverse=True):

                for_points = []
                for value in to_get[counter_per_column:]:
                    if lower_stop < value < higher_stop:
                        counter_per_column += 1
                        for_points.append(value)

                point_boulder = [higher_stop-1-i for i in range(len(for_points))]
                point_boulders.extend(point_boulder)

                points += sum(point_boulder)

                assert higher_stop > lower_stop
                higher_stop = lower_stop

    print(points)

    print(point_boulders)
    #print(*data, sep='\n')



def part2(data):

    cols = len(data[0])
    rows = len(data)
    rocks = {i: {'O': list(), '#': list()} for i in range(cols)}

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            match char:
                case 'O':
                    rocks[x]['O'].append(rows-y)
                case '#':
                    rocks[x]['#'].append(rows-y)
                case _:
                    pass

    def roll(direction, rocks, W, H):

        for column, vals in rocks.items():
            boulders = vals.get('#', []) + [0]
            to_get = vals.get('O', [])

            match direction:
                case 'north':

                    higher_stop = H + 1
                    boulders = [higher_stop] + boulders

                    counter_per_column = 0
                    for lower_stop in sorted(boulders, reverse=True):
                        counter_per_stop = 0

                        stop_rewrites = []

                        for value in to_get[counter_per_column:]:
                            if lower_stop < value < higher_stop:
                                counter_per_stop += 1
                                counter_per_column += 1
                                stop_rewrites.append(value)


                        assert lower_stop <= higher_stop, f"{lower_stop = } < {higher_stop = }"
                        higher_stop = lower_stop

                case 'west':
                    pass  # x does down
                case 'south':
                    pass  # y goes down
                case 'east':
                    pass  # x goes up




    roll('north', rocks, W=cols, H=rows)
    print(*rocks.items(), sep='\n')



data = get_data('example.txt')
part2(data)
