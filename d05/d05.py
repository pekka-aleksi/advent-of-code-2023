import collections
import itertools


def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        blocks = file.read().split('\n\n')
        lines = [block.split('\n') for block in blocks]
        seeds = lines[0][0].split()[1:]
        del lines[0]

        for i in range(len(lines)):
            for j in range(len(lines[i])):
                lines[i][j] = lines[i][j].split()
            del lines[i][0]

        lines = [[list(map(int, y)) for y in x] for x in lines]
        seeds = list(map(int, seeds))
    return seeds, lines


def part1(data):
    seeds, mapping_types = data

    seedpaths = {seed: [seed] + [-1] * len(mapping_types) for seed in seeds}

    # print(mapping_types)
    for seed in seeds:

        for CURRENT_MAPPING, mappings in enumerate(mapping_types, 1):
            PREVIOUS_MAPPING = CURRENT_MAPPING - 1

            for dest_start, src_start, length in mappings:
                if src_start <= seedpaths[seed][PREVIOUS_MAPPING] < src_start + length:
                    delta = dest_start - src_start
                    new_mapping = seedpaths[seed][PREVIOUS_MAPPING] + delta
                    seedpaths[seed][CURRENT_MAPPING] = new_mapping

            if seedpaths[seed][CURRENT_MAPPING] == -1:
                seedpaths[seed][CURRENT_MAPPING] = seedpaths[seed][PREVIOUS_MAPPING]

            print("-" * 80)

    # print(seeds)
    vals = seedpaths.values()

    return min([val[-1] for val in vals])


data = get_data('input.txt')

print(part1(data=data))
