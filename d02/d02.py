import re

def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        lines = file.read().splitlines()

        regexes = r"(\d+) red", r"(\d+) green", r"(\d+) blue"

        all_games = {}
        for game_id, entry in enumerate(lines, 1):
            data = entry.split(':', 1)[-1]
            data = data.split(';')

            draws_per_game = []

            for draw_id, draw in enumerate(data):
                this_draw = []
                for pattern in regexes:
                    rgbs = re.findall(pattern, draw)
                    this_draw.append(int(rgbs[0]) if len(rgbs) else 0)

                draws_per_game.append(this_draw)
            all_games[game_id] = draws_per_game
    return all_games


def part1(data):

    impossible_ids = set()


    for game_id, gamedata in data.items():
        for r, g, b in gamedata:

            legal = r <= 12 and g <= 13 and b <= 14

            if not legal:
                #print(game_id, r, g, b)
                impossible_ids.add(game_id)

    possible_ids = set(data.keys()) - impossible_ids
    print(possible_ids)
    return sum(possible_ids)

def part2(data):

    S = 0
    for game_id, gamedata in data.items():
        largest_r, largest_g, largest_b = 0, 0, 0

        for r, g, b in gamedata:
            largest_r = r if r > largest_r else largest_r
            largest_g = g if g > largest_g else largest_g
            largest_b = b if b > largest_b else largest_b

        P = largest_r*largest_g*largest_b
        S += P

    return S



data = get_data('input.txt')

#print(part1(data))
print(part2(data))