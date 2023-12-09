import collections
def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        lines = file.read().splitlines()
        lines = [line.split(':')[1] for line in lines]
        lines = [line.split('|') for line in lines]
        lines = [(list(map(int, a.split())), list(map(int, b.split()))) for a, b in lines]

    return lines


def part1(data):

    S = 0
    for card_id, (card_numbers, card_winners) in enumerate(data, 1):

        numbers = collections.Counter(card_numbers)
        winners = collections.Counter(card_winners)

        both = numbers & winners

        if both:
            print(card_id, both, 2**(len(both)-1))
            S += 2**(len(both)-1)

    return S

def part2(data):

    S = 0

    counts = {i: 1 for i, _ in enumerate(data, 1)}

    for card_id, ((card_numbers, card_winners), count) in enumerate(zip(data, counts), 1):

        print(*counts.items(), sep='\n')
        numbers = collections.Counter(card_numbers)
        winners = collections.Counter(card_winners)

        both = numbers & winners

        if both:
            more = len(both)

            S += count*more
            print(f"Card {card_id} won {more} x{count} times")

            for i in range(card_id+1, min(card_id+1+more, len(data))):
                print(f"Adding to {i}: {counts[i]}")
                counts[i] += 1*count

        print("-"*80)
    return S



data = get_data('example.txt')
#print(part1(data=data))
print(part2(data=data))
