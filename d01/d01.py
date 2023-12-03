import re


def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        lines = file.read().splitlines()

    return lines


def part1(data):
    regex = re.compile(r'(\d)')

    all = []
    for row in data:
        numbers = re.findall(pattern=regex, string=row)
        first, last = numbers[0], numbers[-1]
        all.append(int(f"{first}{last}"))

    return sum(all)


def part2(data):
    NUMS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    combos = {"oneight": [1, 8], "twone": [2, 1], "threeight": [3, 8], "fiveight": [5, 8], "sevenine": [7, 9], "eighthree": [8, 3], "eightwo": [8, 2], "nineight": [9,8]}
    mapping = {a: i for i, a in enumerate(NUMS, 1)}

    new_data = []

    for entry in data:
        replaced_row = entry
        for comboname, (first, second) in combos.items():
            A, B = NUMS[first-1], NUMS[second-1]
            replaced_row = re.sub(comboname, f"{A}{B}", replaced_row)
        new_data.append(replaced_row)

    print("NEW DATA", new_data)

    regex = re.compile(r"(" + "\d" + '|' + "|".join(NUMS) + ")")

    all = []

    for row in new_data:
        numbers = re.findall(pattern=regex, string=row)
        A, B = numbers[0], numbers[-1]
        first, last = mapping.get(A, A), mapping.get(B, B)
        all.append(int(f"{first}{last}"))

    return sum(all)


data = get_data('input.txt')
print(part2(data=data))

#
