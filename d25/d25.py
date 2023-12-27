import networkx as nx
import re
import itertools
import math

def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        data = file.read().splitlines()
        regex = re.compile(r'([a-z]{3})')
        nodes = [regex.findall(row) for row in data]
        edges = [(row[0], entry) for row in nodes for entry in row[1:]]
        nodes = list(itertools.chain.from_iterable(nodes))
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
    return G

def part1(data):
    A = nx.minimum_edge_cut(data)
    data.remove_edges_from(A)
    lens = list(map(len, list(nx.connected_components(data))))
    return math.prod(lens)

data = get_data('input.txt')
print(part1(data))
