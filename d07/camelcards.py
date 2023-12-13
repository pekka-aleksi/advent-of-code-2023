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



def part2(data):

    HIGH = 7
    ONE_PAIR = 6
    TWO_PAIR = 5
    THREE_SAME = 4
    FULL_HOUES = 3
    FOUR_OF_A_KIND = 2
    FIVE_OF_A_KIND = 1


    hands_by_priority = collections.defaultdict(list)

    for hand_points_ in data:

        hand_points = []

        for i, x in enumerate(hand_points_):
            if i == len(hand_points_)-1:
                hand_points.append(x)
            elif x == 11:
                hand_points.append(1)
            else:
                hand_points.append(x)

        hand = hand_points[:-1]

        count = collections.Counter(hand)

        match count[1]:
            case 0:
                print("5 other cards", hand)
                handset = set(hand)

                match len(handset):
                    case 5:
                        # PRIORITY 7 (HIGH CARD)
                        hands_by_priority[HIGH].append(hand_points)

                    case 4:
                        # PRIORITY 6 (ONE PAIR)
                        hands_by_priority[ONE_PAIR].append(hand_points)

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

                        # AABB or AAAB or AAAC
                        if hand_with_4_cards.count(least_present_with_4_cards) in {2}:
                            hands_by_priority[TWO_PAIR].append(hand_points)
                        else:
                            hands_by_priority[THREE_SAME].append(hand_points)

                    case 2:
                        # PRIORIRTY 3 (FULL HOUSE)
                        # PRIORITY 2 (4 OF A KIND)
                        other_card = min(hand)

                        if hand.count(other_card) in {1, 4}:
                            hands_by_priority[FOUR_OF_A_KIND].append(hand_points)
                        else:
                            hands_by_priority[FULL_HOUES].append(hand_points)
                    case 1:
                        # PRIORITY 1 (5 OF A KIND)
                        hands_by_priority[FIVE_OF_A_KIND].append(hand_points)
                    case _:
                        assert False

            case 1:
                jokerless_count = collections.Counter([x for x in hand if x != 1])

                match max(jokerless_count.values()):
                    case 1:   # Jxyzw
                        print("1 pair", hand)
                        hands_by_priority[ONE_PAIR].append(hand_points)

                    case 2:   # Jxxyz |  Jxxyy

                        if len(jokerless_count) == 2:
                            #print(jokerless_count)
                            hands_by_priority[FULL_HOUES].append(hand_points)
                        elif len(jokerless_count) == 3:
                            hands_by_priority[THREE_SAME].append(hand_points)
                        else:
                            assert False

                    case 3:   # Jxxxy
                        print("4 of a kind", hand)
                        hands_by_priority[FOUR_OF_A_KIND].append(hand_points)
                    case 4:  # Jxxxx
                        print("5 of a kind", hand)
                        hands_by_priority[FIVE_OF_A_KIND].append(hand_points)
                    case _:
                        assert False
            case 2:
                jokerless_count = collections.Counter([x for x in hand if x != 1])

                match max(jokerless_count.values()):
                    case 1:   # JJxyz
                        print("3 of a kind", hand)
                        hands_by_priority[THREE_SAME].append(hand_points)
                    case 2:   # JJxxy
                        print("4 of a kind", hand)
                        hands_by_priority[FOUR_OF_A_KIND].append(hand_points)
                    case 3:   # JJxxx
                        print("5 of a kind", hand)
                        hands_by_priority[FIVE_OF_A_KIND].append(hand_points)
                    case _:
                        assert False
            case 3:
                jokerless_count = collections.Counter([x for x in hand if x != 1])

                match max(jokerless_count.values()):
                    case 1:  # JJJxy
                        print("4 of a kind", hand)
                        hands_by_priority[FOUR_OF_A_KIND].append(hand_points)
                    case 2:  # JJJxx
                        print("5 of a kind", hand)
                        hands_by_priority[FIVE_OF_A_KIND].append(hand_points)
                    case _:
                        assert False
            case 4 | 5:
                print("5 of a kind", hand)
                #print("Automatic 5 of a kind", hand) # this will regardless be better than any 4 of a kind by jokers
                hands_by_priority[FIVE_OF_A_KIND].append(hand_points)
            case _:
                assert False


    counted_hands = 0
    total_points = 0


    final_hand_ranked = []
    for priority, handlist in reversed(sorted(hands_by_priority.items())):
        for i, hand in enumerate(sorted(handlist), counted_hands+1):
            print('\t', i, hand)
            total_points += (hand[-1]*i)

            #if 1 not in hand:
            #    final_hand_ranked.append((i, hand, priority))
        counted_hands += len(handlist)

    #assert counted_hands == 1000

    #print(*hands_by_priority.items(), sep='\n')
    print(*reversed(final_hand_ranked), len(final_hand_ranked), sep='\n')
    return total_points


data = get_data('input.txt')

print(part2(data))
