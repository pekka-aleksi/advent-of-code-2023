def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        data = file.read().splitlines()
        data = [list(map(int, row.split())) for row in data]
    return data


def part1(data):

    all_results = {}
    for i, row in enumerate(data):
        all_results[i] = [row[-1]]
        apply_to_this = row.copy()

        while True:
            apply_to_this = list(map(lambda x: x[1] - x[0], zip(apply_to_this, apply_to_this[1:])))
            all_results[i].append(apply_to_this[-1])
            if min(apply_to_this) == max(apply_to_this):
                break

    tulokset = []

    for _, v in all_results.items():

        rivi = []
        popattava_rivi = v.copy()

        while len(popattava_rivi):

            rivi = rivi + [popattava_rivi.pop()]

            if len(rivi) > 1:
                rivi = [rivi.pop() + rivi.pop()]

        tulokset.extend(rivi)

    return sum(tulokset)


def part2(data):

    all_results = {}
    for i, row in enumerate(data):

        all_results[i] = [row[0]]
        apply_to_this = row.copy()

        while True:
            apply_to_this = list(map(lambda x: x[1] - x[0], zip(apply_to_this, apply_to_this[1:])))
            all_results[i].append(apply_to_this[0])
            if min(apply_to_this) == max(apply_to_this):
                break

    tulokset = []
    for v in all_results.values():

        rivi = []
        popattava_rivi = v.copy()

        while len(popattava_rivi):

            rivi = rivi + [popattava_rivi.pop()]

            if len(rivi) > 1:
                rivi = [rivi.pop() - rivi.pop()]

        tulokset.extend(rivi)

    return sum(tulokset)

data = get_data('input.txt')

print(part2(data))
