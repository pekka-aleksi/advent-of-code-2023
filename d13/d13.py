import collections
import operator
import math

def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        data = [entry.split('\n') for entry in file.read().replace('#','1').replace('.', '0').split('\n\n')]


    return data
def transpose(data):
    new_data = []

    for entry in data:
        new_rows = [list() for _ in range(len(entry[0]))]
        for old_y, row in enumerate(entry):
            for old_x, col in enumerate(row):
                new_rows[old_x].append(col)

        new_rows = ["".join(row) for row in new_rows]
        new_data.append(new_rows)
    return new_data




def do_pops(queue, from_back=False, left_right=False, part2=False):

    original_len = len(queue)

    while len(queue):

        if len(queue) % 2 == 0:
            Q = list(queue)
            L = len(Q)

            top_side, bottom_side = Q[:L // 2], list(reversed(Q[L // 2:]))

            if not part2:
                if top_side == bottom_side:
                    break
            elif part2:
                if my_comp(top_side, bottom_side):
                    break

        if from_back:
            queue.popleft()  # POP FROM TOP/LEFT
        else:
            queue.pop()  # POP FROM BOTTOM/RIGHT

    else:
        return 0

    if from_back:
        return (1 if left_right else 100) *(original_len - len(queue)//2)
    else:
        return (1 if left_right else 100) *(len(queue) // 2)



def my_comp(A, B):
    N = [x for x in map(operator.xor, A, B) if x]

    if len(N) == 1:
        n = N[0]
        cand = math.log(n, 2)
        cand_floor = math.floor(cand)

        if abs(cand_floor - cand) < 1e-10:
            return True
        else:
            return False
    return False


def part2(data):


    tdata = transpose(data)
    top_down = {i: [int(row, 2) for row in entry] for i, entry in enumerate(data)}
    left_right = {i: [int(row, 2) for row in entry] for i, entry in enumerate(tdata)}

    loppusumma = 0

    for i, entry in top_down.items():
        q = collections.deque(entry)
        loppusumma += do_pops(q, from_back=True, part2=True)
        q = collections.deque(entry)
        loppusumma += do_pops(q, from_back=False, part2=True)


    for i, entry in left_right.items():
        q = collections.deque(entry)
        loppusumma += do_pops(q, from_back=True, left_right=True, part2=True)
        q = collections.deque(entry)
        loppusumma += do_pops(q, from_back=False, left_right=True, part2=True)

    return loppusumma




def part1(data):

    tdata = transpose(data)

    top_down = {i: [hex(int(row, 2)) for row in entry] for i, entry in enumerate(data)}
    left_right = {i: [hex(int(row, 2)) for row in entry] for i, entry in enumerate(tdata)}

    loppusumma = 0

    for i, entry in top_down.items():
        q = collections.deque(entry)
        loppusumma += do_pops(q, from_back=True)
        q = collections.deque(entry)
        loppusumma += do_pops(q, from_back=False)

    for i, entry in left_right.items():
        q = collections.deque(entry.copy())
        loppusumma += do_pops(q, from_back=True, left_right=True)
        q = collections.deque(entry.copy())
        loppusumma += do_pops(q, from_back=False, left_right=True)

    return loppusumma


data = get_data('input.txt')

print(part2(data))
