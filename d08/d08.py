import re
import math

def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        data = file.read().split('\n\n')

        assignment, graph = data

        regex = re.compile(r'(?P<node>[A-Z0-9]{3}) = \((?P<left>[A-Z0-9]{3}), (?P<right>[A-Z0-9]{3})\)')

        graph = graph.split('\n')

        regexes = [regex.search(row) for row in graph]
        graph = {tr.group('node'): (tr.group('left'), tr.group('right')) for tr in regexes}

    return assignment, graph


def part1(data):
    #print(data)

    assignment, graph = data

    current = 'AAA'
    visited_count = 0

    while current != 'ZZZ':

        match assignment[visited_count % len(assignment)]:
            case 'L':
                visited_count += 1
                current = graph[current][0]
            case 'R':
                visited_count += 1
                current = graph[current][1]
            case _:
                assert False


    return visited_count

def part2(data):

    assignment, graph = data

    start_nodes = list(key for key in graph if key[-1] == 'A')

    solutions = [0]*len(start_nodes)

    for i in range(len(start_nodes)):
        while start_nodes[i][-1] != 'Z':

            match assignment[solutions[i] % len(assignment)]:
                case 'L':
                    start_nodes[i] = graph[start_nodes[i]][0]
                    solutions[i] += 1
                case 'R':
                    start_nodes[i] = graph[start_nodes[i]][1]
                    solutions[i] += 1
                case _:
                    assert False

    return math.lcm(*solutions)


data = get_data('input.txt')

print(part2(data))
