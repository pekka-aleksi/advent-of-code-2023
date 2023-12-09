import collections


def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        lines = file.read().splitlines()
        lines = [line.split() for line in lines]

        mappings = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}

        lines = [(*[int(mappings.get(k, k)) for k in x], int(y)) for x, y in lines]
    return lines


def part1(data):

    hands_by_priority = collections.defaultdict(list)

    for hand_points in data:
        hand = hand_points[:-1]
        handset = set(hand)

        match len(handset):
            case 5:
                # PRIORITY 7 (HIGH CARD)
                hands_by_priority[7].append(hand_points)

            case 4:
                # PRIORITY 6 (ONE PAIR)
                hands_by_priority[6].append(hand_points)

            case 3:  # AABBC or AAABC
                # PRIORITY 5 (TWO PAIRS)
                # PRIORITY 4 (THREE OF A KIND)

                values = {}

                for value in hand:
                    values[value] = values.get(value, 0) + 1

                least_present = min(values.items(), key=lambda x: x[1])[0]

                hand_with_4_cards = list(hand).copy()
                hand_with_4_cards.remove(least_present)

                least_present_with_4_cards = min(hand_with_4_cards)

                if hand_with_4_cards.count(least_present_with_4_cards) in {2}:
                    hands_by_priority[5].append(hand_points)
                else:
                    hands_by_priority[4].append(hand_points)

            case 2:
                # PRIORIRTY 3 (FULL HOUSE)
                # PRIORITY 2 (4 OF A KIND)
                other_card = min(hand)

                if hand.count(other_card) in {1, 4}:
                    hands_by_priority[2].append(hand_points)
                else:
                    hands_by_priority[3].append(hand_points)
            case 1:
                # PRIORITY 1 (5 OF A KIND)
                hands_by_priority[1].append(hand_points)
            case _:

                hands_by_priority[8].append(hand_points)


    counted_hands = 0
    total_points = 0
    for priority, handlist in reversed(sorted(hands_by_priority.items())):
        for i, hand in enumerate(sorted(handlist), counted_hands+1):
            #print('\t', i, hand)
            total_points += (hand[-1]*i)
        counted_hands += len(handlist)

    return total_points

data = get_data('input.txt')

print(part1(data))
