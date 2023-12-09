import math

def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        lines = file.read().splitlines()
        times = [int(k) for k in lines[0].split()[1:]]
        distances = [int(k) for k in lines[1].split()[1:]]

    return times, distances


def part1(data):

    total = []
    for time, distance in zip(*data):

        discriminant = math.sqrt(time**2 - 4*distance)/2
        rest = time / 2.0

        lower = rest - discriminant
        lower_int = math.ceil(lower)

        upper = rest + discriminant
        upper_int = math.floor(upper)

        match abs(lower_int-lower) < 1e-5, abs(upper_int-upper) < 1e-5:
            case True, True:
                something = -1
            case True, False:
                something = 0
            case False, True:
                something = 0
            case False, False:
                something = 1

        total.append((upper_int-lower_int)+something)

    return math.prod(total), total


def part2(data):

    time =int("".join([str(x) for x in data[0]]))
    distance = int("".join([str(x) for x in data[1]]))

    discriminant = math.sqrt(time**2 - 4*distance)/2
    rest = time / 2.0

    lower = rest - discriminant
    lower_int = math.ceil(lower)

    upper = rest + discriminant
    upper_int = math.floor(upper)

    match abs(lower_int-lower) < 1e-5, abs(upper_int-upper) < 1e-5:
        case True, True:
            something = -1
        case True, False:
            something = 0
        case False, True:
            something = 0
        case False, False:
            something = 1

    return (upper_int-lower_int)+something


data = get_data('input.txt')

#print(part1(data))
print(part2(data))