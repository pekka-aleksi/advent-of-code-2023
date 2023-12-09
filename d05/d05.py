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

    seedpaths = {seed: [seed] + [-1]*len(mapping_types) for seed in seeds}

    for seed in seeds:
        print(f"Starting seed {seed}")

        for mapping_n, mapping_type in enumerate(mapping_types):

            keep_trying = True
            changed = False
            while keep_trying:

                print("TRYING")

                for src_start, dest_start, length in mapping_type:
                    LAST_NUMBER = seedpaths[seed][mapping_n] if seedpaths[seed][mapping_n+1] == -1 else seedpaths[seed][mapping_n+1]

                    print(LAST_NUMBER, src_start, dest_start, length)
                    # WE DON'T HAVE TO TRY IF 0 CHANGES HAPPENED DURING THE WHOLE LOOP

                    if LAST_NUMBER in range(src_start, src_start+length):

                        changed = True
                        print(f"The seed {seedpaths[seed][mapping_n]} is in the {range(src_start, src_start+length)}")

                        if src_start > dest_start:
                            delta = src_start - dest_start

                        elif dest_start > src_start:
                            delta = -(dest_start-src_start)


                        print(f"{src_start}-{src_start+length} to {dest_start}-{dest_start+length}, {delta = }")
                        new_home = LAST_NUMBER + delta
                        print(f"Setting new home {new_home} at level {mapping_n}")
                        seedpaths[seed][mapping_n+1] = new_home
                        print(f"\t{seed} {seedpaths[seed]}")
                        continue # we don't break but we continue trying
                    elif not changed:
                        print("The number has not been changed and we set the number by the default rule.")
                        seedpaths[seed][mapping_n+1] = seedpaths[seed][mapping_n]

                    elif changed:
                        print("The number has been changed but this rule didn't change the rule again.")
                else:
                    # we get here IF there was no more continuations or no more retries (or both)
                    keep_trying = False




        print("-"*80)


    print(seeds)
    print(*seedpaths.items(), sep='\n')


data = get_data('example.txt')

part1(data=data)

"""
Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
"""
