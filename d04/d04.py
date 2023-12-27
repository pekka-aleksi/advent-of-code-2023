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

def part2(data, DEBUG=False):


    card_counts = {i: 1 for i, _ in enumerate(data, 1)}

    for card_id, (card_numbers, card_winners) in enumerate(data, 1):

        if DEBUG:
            print(*card_counts.items(), sep='\n')

        count = card_counts[card_id]


        assert len(set(card_numbers)) == len(card_numbers)
        assert len(set(card_winners)) == len(card_winners), f"{card_winners = }"

        numbers = collections.Counter(card_numbers)
        winners = collections.Counter(card_winners)

        this_card_wins = numbers & winners

        if DEBUG:
            print(f"{card_id = }, {this_card_wins = }")

        if this_card_wins:
            if DEBUG:
                print(f"Card {card_id} wins {count} times.")

            how_many_more_cards = len(this_card_wins)

            for C in range(count):


                R = min(card_id+1+how_many_more_cards, len(data)+1)
                if DEBUG:
                    print(f"{C = } {R = }")

                for i in range(card_id+1, R):

                    if DEBUG:
                        print(f"{i = }")
                        print(f"\tAdding 1 to {card_id+1}")
                    TO_ADD = 1
                    card_counts[i] += TO_ADD
        else:
            if DEBUG:
                print(f"Card {card_id} did NOT win se we're not doing anything")
            else:
                pass


    print(card_counts)
        #print("-"*80)
    return sum(card_counts.values())



data = get_data('input.txt')
#print(part1(data=data))
print(part2(data=data, DEBUG=False))
