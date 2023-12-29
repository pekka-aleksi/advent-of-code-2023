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


def part2(data):
    seeds, mapping_types = data

    starts, ranges = seeds[::2], seeds[1::2]

    seedpaths = {(start, start+range): [[(start, start + range)]] + [[(None, None)]] * len(mapping_types) for start, range in
                 zip(starts, ranges)}

    # print(mapping_types)
    for index_seed_start, index_seed_range in zip(starts, ranges):

        for CURRENT_MAPPING, mappings in enumerate(mapping_types, 1):
            PREVIOUS_MAPPING = CURRENT_MAPPING - 1


            for remapping_dest_start, remapping_src_start, mapping_length in mappings:

                remapping_src_end = remapping_src_start + mapping_length

                seedhistory = seedpaths[(index_seed_start, index_seed_start+index_seed_range)]

                seedpaff = seedhistory[PREVIOUS_MAPPING]

                print(seedpaff)

                for current_seed_start, current_seed_end in seedpaff:

                    print(f"{remapping_src_start}-{remapping_src_end}, {current_seed_start}-{current_seed_end}")
                    print(*seedpaths.items(), sep='\n')

                    if remapping_src_end < current_seed_start:
                        print("--|--REMAP--|--SEEDS")
                        seedpaths[(index_seed_start, index_seed_start+index_seed_range)][CURRENT_MAPPING] = seedpaths[(index_seed_start, index_seed_start+index_seed_range)][PREVIOUS_MAPPING]

                    elif remapping_src_start <= current_seed_end <= remapping_src_end and current_seed_start <= remapping_src_start:
                        print("-MORE-SEEDS--|--REMAP-AND-SEEDS--|------")
                        new_left_start, new_left_end = remapping_src_start, current_seed_start
                        new_center_start, new_center_end = new_left_end, new_left_end + (current_seed_end - current_seed_start)
                        new_right_start, new_right_end = new_center_end, new_center_end + (remapping_src_end - current_seed_end)

                        print(new_left_start, new_left_end, new_center_start, new_center_end, new_right_start, new_right_end)

                        seedpaths[(index_seed_start, index_seed_start + index_seed_range)][CURRENT_MAPPING] = [(new_left_start, new_left_end), (new_center_start, new_center_end), (new_right_start, new_right_end)]


                    elif remapping_src_start <= current_seed_start <= remapping_src_end and  remapping_src_end <= current_seed_end:
                        print("--|--REMAP-AND-SEEDS--|-MORE-SEEDS--")
                        new_left_start, new_left_end = remapping_src_start, current_seed_start
                        new_center_start, new_center_end = new_left_end, new_left_end + (current_seed_end - current_seed_start)
                        new_right_start, new_right_end = new_center_end, new_center_end + (remapping_src_end - current_seed_end)

                        print(new_left_start, new_left_end, new_center_start, new_center_end, new_right_start, new_right_end)

                        seedpaths[(index_seed_start, index_seed_start + index_seed_range)][CURRENT_MAPPING] = [(new_left_start, new_left_end), (new_center_start, new_center_end), (new_right_start, new_right_end)]


                    elif remapping_src_start <= current_seed_start <= remapping_src_end and remapping_src_start <= current_seed_end <= remapping_src_end:
                        print("--|-REMAP-AND-SEEDS-|--")
                        new_left_start, new_left_end = remapping_src_start, current_seed_start
                        new_center_start, new_center_end = new_left_end, new_left_end + (current_seed_end - current_seed_start)
                        new_right_start, new_right_end = new_center_end, new_center_end + (remapping_src_end - current_seed_end)

                        print(new_left_start, new_left_end, new_center_start, new_center_end, new_right_start, new_right_end)

                        seedpaths[(index_seed_start, index_seed_start + index_seed_range)][CURRENT_MAPPING] = [(new_left_start, new_left_end), (new_center_start, new_center_end), (new_right_start, new_right_end)]

                    elif remapping_src_start > current_seed_end:
                        print("SEEDS--|--REMAP--|--")
                    elif current_seed_start <= remapping_src_start and remapping_src_end <= current_seed_end:
                        print("REMAP INSIDE SEEDS?")

    # print(seeds)
    vals = seedpaths.values()

    return seedpaths.items()


data = get_data('example.txt')

print(*part2(data=data), sep='\n')
