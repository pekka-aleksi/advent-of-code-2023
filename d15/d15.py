
import dataclasses

def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        data = file.read().strip().split(',')
    return data

def hash(sample):
    curr = 0
    for ch in sample:
        ASCII = ord(ch)
        curr += ASCII
        curr *= 17
        curr %= 256

    return curr


def part1(data):
    return sum([hash(sample) for sample in data])


@dataclasses.dataclass
class Lense:
    focal_length: int = 0
    name: str = ""

    def __eq__(self, other):
        return self.name == other.name


class Box:
    def __init__(self):
        self.list_of_lenses = list()

    def __add__(self, other):
        if isinstance(other, Lense):
            if other not in self.list_of_lenses:
                print(f"Added lense {other}")
                self.list_of_lenses.append(other)
            elif other in self.list_of_lenses:
                index = self.list_of_lenses.index(other)
                self.list_of_lenses[index] = other
                print(f"Replaced lense at index {index}")
        return self

    def __str__(self):
        if len(self.list_of_lenses):
            boxname = hash(self.list_of_lenses[0].name)
            return str([boxname] + [(i, lense) for i, lense in enumerate(self.list_of_lenses, 1)])
        else:
            return ""
    def __len__(self):
        return len(self.list_of_lenses)

class System:
    def __init__(self):
        self.boxes = []
        for i in range(256):
            self.boxes.append(Box())

    def new_lense(self, lense):
        box_index = hash(lense.name)
        self.boxes[box_index] += lense

    def remove_lense(self, lense):
        try:
            box_index = hash(lense.name)

            self.boxes[box_index].list_of_lenses.remove(lense)

            print("Removed lense", lense)
        except ValueError:
            print("No such lense", lense)

    def __str__(self):
        return "\n".join([f"{x}" for x in self.boxes if len(x)])

def part2(data):


    system = System()

    for row in data:
        print(row)
        if '=' in row:
            name, focal_length = row.split('=')
            lense = Lense(focal_length, name)
            system.new_lense(lense)
        elif '-' in row:
            name = row.rstrip('-')
            lense = Lense(None, name)
            system.remove_lense(lense)
        #print("--"*40)


    totals = []
    for box_number, box in enumerate(system.boxes, 1):
        for slot, lense in enumerate(box.list_of_lenses, 1):
            #print(box_number, slot, int(lense.focal_length))
            totals.append(box_number*slot*int(lense.focal_length))

    return sum(totals)

data = get_data('input.txt')

print(part2(data), sep='\n')

