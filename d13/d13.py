import collections

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


def part1(data):

    tdata = transpose(data)

    top_down = {i: [hex(int(row, 2)) for row in entry] for i, entry in enumerate(data)}
    left_right = {i: [hex(int(row, 2)) for row in entry] for i, entry in enumerate(tdata)}


    #data_entry_pops = {i: {'below': 0,
    #                       'above': 0,
    #                       'left': 0,
    #                       'right': 0} for i, _ in enumerate(data)}


    for i, entry in top_down.items():
        #left_queue, right_queue = collections.deque(entry), collections.deque()

        print(entry)
        #from_left = True
        # when we pop from left - the test is on N-1 right --- we have to repeat this until there are 2 rows left
        # when we pop from right - the test is on N-1 left --- we have to repeat this until there are 2 rows left

        queue = collections.deque(entry)

        while len(queue):

            if len(queue) % 2 == 0:

                #print(f"{queue = }")
                Q = list(queue)
                L = len(Q)

                top_side, bottom_side = Q[:L//2], list(reversed(Q[L//2:]))

                if top_side == bottom_side:
                    print(f"FOUND BY POPPING FROM BOTTOM {top_side = }, {bottom_side = }")
                    break

            thing = queue.pop()  # POP FROM BOTTOM
            #print(f"- {thing} popped -")

            #data_entry_pops[i]['below'] += 1
        else:
            print("POPPING FROM BOTTOM NO RESULTS")

        queue = collections.deque(entry)

        while len(queue):

            if len(queue) % 2 == 0:

                #print(len(queue), queue)
                Q = list(queue)
                L = len(Q)

                top_side, bottom_side = Q[:L//2], list(reversed(Q[L//2:]))

                if top_side == bottom_side:
                    print(f"FOUND BY POPPING FROM TOP {top_side = }, {bottom_side = }")
                    break

            thing = queue.popleft()  # POP FROM TOP
            #print(f"- {thing} popped -")
        else:
            print("POPPING FROM TOP PRODUCED NO RESULT")

        print("-"*80)

data = get_data('trivials.txt')

part1(data)
