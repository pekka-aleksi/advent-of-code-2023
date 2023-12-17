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

    seedpaths = {(start, start+range): [(start, start + range)] + [(None, None)] * len(mapping_types) for start, range in
                 zip(starts, ranges)}

    # print(mapping_types)
    for index_seed_start, index_seed_range in zip(starts, ranges):

        for CURRENT_MAPPING, mappings in enumerate(mapping_types, 1):
            PREVIOUS_MAPPING = CURRENT_MAPPING - 1

            # koko seedpath liikahtaa

            # datarakenteen tarvitsee huomioida tämä --
            # tarvitsee tietää koko seed history koska halutaan tietää mihin seedit päätyvät
            # vastaus saattaa olla MIKÄ tahansa seed

            # toisin sanottuna tarvitsee katsoa kun tullaan tänne - montako varianttia löytyy
            # polut voivat kytkeytyä toisiinsa - tämä ei haittaa, kunhan tiedetään historiat.
            # historiat ovat täysin toisistaan vieraita vaikka ne päätyisivät samaan paikkaan.



            for dest_start, src_start, mapping_length in mappings:

                src_end = src_start + mapping_length

                seedhistory = seedpaths[(index_seed_start, index_seed_start+index_seed_range)]

                current_seed_start, current_seed_end = seedhistory[PREVIOUS_MAPPING]

                if src_start < current_seed_end:
                    print("--|-------|-A")
                    print(src_start, current_seed_end)
                    print(*seedpaths.items(), sep='\n')
                    seedpaths[(index_seed_start, index_seed_start+index_seed_range)][CURRENT_MAPPING] = seedpaths[(index_seed_start, index_seed_start+index_seed_range)][PREVIOUS_MAPPING]


                elif src_start <= current_seed_start <= src_end:
                    if src_start <= current_seed_end <= src_end:
                        print("--|----A--|--")






                    elif current_seed_end <= src_end:
                        print("--|----AAA|AA")

                        # katkaistaan seedpath ja luodaan toinen (jolla oma range)

                    else:
                        assert False
                elif current_seed_start < src_start:
                    if src_start >= current_seed_end:
                        print("AA|AA-----|--")

                        # katkaistaan seedpath ja luodaan toinen (jolla oma range)

                    else:  # voiko tulla 1-off?
                        print("A-|-------|--")
                        seedpaths[(index_seed_start, index_seed_start+index_seed_range)][CURRENT_MAPPING] = seedpaths[(index_seed_start, index_seed_start+index_seed_range)][PREVIOUS_MAPPING]


    # print(seeds)
    vals = seedpaths.values()

    return seedpaths.items()


data = get_data('example.txt')

print(*part2(data=data), sep='\n')
