import re

def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        data = file.read().splitlines()
        data = [row.replace(' -> ', ' ').replace(',', '').split() for row in data]
    return data

import collections
grand_queue = collections.deque()

class FlipFlop:
    def __init__(self, name, outputs, TEST_CASE):
        self.name = name
        self.outputs = outputs
        self.state = False
        self.TEST_CASE = TEST_CASE

    # receive high -> nothing happens
    # receive low -> from off to on and SEND HIGH
    # receive low -> from on to off and SEND LOW

    def trigger(self, triggerer_name, pulse, DEBUG=False):

        high_counter, k = 0, 0
        low_counter, e = 0, 0

        match pulse, self.state:
            case True, _:
                pass
            case (False, False) | (False, True):

                self.state = not self.state

                for output in self.outputs:
                    grand_queue.appendleft((output.trigger, self.name, self.state, output.name))

                while grand_queue:
                    function, triggerer, pulse_type, to_who = grand_queue.pop()

                    if DEBUG:
                        print(f"{triggerer} -> {pulse_type} -> {to_who}")

                    if pulse_type:
                        high_counter += 1

                    else:
                        low_counter += 1
                        if to_who == self.TEST_CASE:
                            raise Exception(low_counter+e)
                            #return high_counter + k, low_counter + e

                    try:
                        k, e = function(triggerer, pulse_type, DEBUG)
                    except Exception as exception:
                        raise Exception(low_counter+e+int(f"{exception}"))

            case _:
                assert False

        return high_counter + k, low_counter + e

    def add_inputs(self, new_inputs):
        pass
    def __str__(self):
        return f"{self.name}: {self.state} -> {self.outputs}"
    def __repr__(self):
        return f"(state {self.state}) {self.outputs}"
    def __eq__(self, other):
        return self.name == other.name

class Conjunction:
    def __init__(self, name: str, outputs: list, TEST_CASE):
        self.name = name
        self.outputs = outputs
        self.memory = {}
        self.TEST_CASE = TEST_CASE

    def add_inputs(self, new_inputs):
        self.memory.update({incoming.name: False for incoming in new_inputs})

    def trigger(self,  triggerer_name, pulse=False, DEBUG=False):

        high_counter, low_counter = 0, 0
        k, e = 0, 0

        self.memory[triggerer_name] = pulse

        if all(self.memory.values()):
            new_pulse = False
        else:
            new_pulse = True

        for output in self.outputs:
            grand_queue.appendleft((output.trigger,  self.name, new_pulse, output.name))

        while grand_queue:
            function, triggerer, pulse_type, to_who = grand_queue.pop()

            if DEBUG:
                print(f"{triggerer} -> {pulse_type} -> {to_who}")

            if pulse_type:
                high_counter += 1
            else:
                low_counter += 1
                if to_who == self.TEST_CASE:
                    raise Exception(low_counter + e)

            k, e = function(triggerer, pulse_type, DEBUG)

        return high_counter + k, low_counter + e

    def __str__(self):
        return f"{self.name}: {self.outputs} (memory for inputs: {self.memory})"

    def __repr__(self):
        return f"{self.outputs} (memory for inputs: {self.memory})"

    def __eq__(self, other):
        return self.name == other.name


class Broadcaster:
    def __init__(self, outputs, TEST_CASE):
        self.outputs = outputs
        self.TEST_CASE = TEST_CASE

    def trigger(self, pulse=False, DEBUG=False):

        high_counter, low_counter = 0, 0
        k, e = 0, 0
        for output in self.outputs:
            grand_queue.appendleft((output.trigger, 'broadcaster', pulse, output.name))

        while grand_queue:
            function, triggerer_name, pulse_type, to_who = grand_queue.pop()

            if DEBUG:
                print(f"{triggerer_name} -> {pulse_type} -> {to_who}")

            if pulse_type:
                high_counter += 1
            else:
                low_counter += 1

                if to_who == self.TEST_CASE:
                    raise Exception(low_counter + e)

            try:
                k, e = function(triggerer_name, pulse_type, DEBUG)
            except Exception as exception:
                raise Exception(low_counter + e + int(f"{exception}"))

        return high_counter + k, low_counter + e

    def __str__(self):
        return f"BROADCASTER {self.outputs}"



def part1(data):
    system = {}

    for row in data:

        name, outputs = row[0][1:], row[1:]
        match row[0][0]:
            case 'b':
                broadcaster = Broadcaster(outputs=outputs)
                system["broadcaster"] = broadcaster
            case '%':
                flipflop = FlipFlop(name=name, outputs=outputs)
                system[name] = flipflop
            case '&':
                conjunction = Conjunction(name=name, outputs=outputs)
                system[name] = conjunction

    print()

    tmp = FlipFlop(name='test', outputs=[])

    for name in system:
        for output in system[name].outputs:
            system.get(output, tmp).add_inputs([system[name]])

    for name in system:
        to_fix = system.get(name, tmp)
        to_fix.outputs = [system.get(output, tmp) for output in to_fix.outputs]

    print()

    A, B = 0, 0

    for k in range(5):

        a, b = broadcaster.trigger()

        A += a
        B += b
        # print(f"{a} High, {b} Low")
        # print("-"*80)
    print(A, B + 1000, A * (B + 1000))
    # print(*system.items(), sep='\n')



def part2(data):

    TEST_CASE = 'rx'
    system = {}

    for row in data:

        name, outputs = row[0][1:], row[1:]
        match row[0][0]:
            case 'b':
                broadcaster = Broadcaster(outputs=outputs, TEST_CASE=TEST_CASE)
                system["broadcaster"] = broadcaster
            case '%':
                flipflop = FlipFlop(name=name, outputs=outputs, TEST_CASE=TEST_CASE)
                system[name] = flipflop
            case '&':
                conjunction = Conjunction(name=name, outputs=outputs, TEST_CASE=TEST_CASE)
                system[name] = conjunction


    tmp = FlipFlop(name='test', outputs=[], TEST_CASE=TEST_CASE)

    for name in system:
        for output in system[name].outputs:
            system.get(output, tmp).add_inputs([system[name]])

    for name in system:
        to_fix = system.get(name, tmp)
        to_fix.outputs = [system.get(output, tmp) for output in to_fix.outputs]

    i = 0
    while True:
        i += 1
        try:
            broadcaster.trigger(DEBUG=False)
            #print("-"*80)
        except:
            print(f"Button presses: {i}")
            break


data = get_data('input.txt')

part2(data)