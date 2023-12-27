import operator
import re
import dataclasses

def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        data = file.read().split('\n\n')
        rules, inputs = data

        rule_regex = re.compile(r'^([a-z]+)\{(.*)\}$')

        input_regex = re.compile(r'.*=(\d+).*=(\d+).*=(\d+).*=(\d+).*')
        inputs = [[int(x) for x in input_regex.findall(row)[0]] for row in inputs.split('\n')]

        rules = [rule_regex.findall(row)[0] for row in rules.split('\n')]
        rules = {a: b for a, b in rules}

        singular_rule = re.compile(r'(([xmas])([\<\>])(\d+):(A|R|[a-z]+))|(A|R|[a-z]+)')
        rules = {name: [singular_rule.findall(rule)[0][1:] for rule in rulecomplex.split(',')] for name, rulecomplex in rules.items()}

    return rules, inputs


class Rule:
    def __init__(self, rule: tuple):

        if rule[-1]:
            self.unconditional = True
            self.letter = "DEFAULT"
            self.compare = None
            self.value = None
            self.next = rule[-1]
        else:
            self.unconditional = False
            self.letter = rule[0]
            self.compare = operator.lt if rule[1] == '<' else operator.gt
            self.value = rule[2]
            self.next = rule[3]

    def __str__(self):
        return f'{self.letter} {self.compare} {self.value} -> {self.next} ({self.unconditional})'

    def __repr__(self):
        return f'{self.letter} {self.compare} {self.value} -> {self.next} ({self.unconditional})'


    def run(self, myinput):

        if self.unconditional:

            if self.next == 'A':
                return 'A'
            elif self.next == 'R':
                return 'R'
            else:
                return self.next

        reference_value = getattr(myinput, self.letter)

        truthiness = self.compare(int(reference_value), int(self.value))

        if truthiness:
            return self.next

        return False




class Workflow:
    def __init__(self, name: str, rulelist):

        self.rules = []

        for rule in rulelist:
            self.rules.append(Rule(rule))

        self.name = name

    def run(self, xmas):

        for i, rule in enumerate(self.rules, 1):

            #print(f"{self.name} {i}/{len(self.rules)} {rule = } {rule.unconditional}")
            result = rule.run(xmas)
            #print(f"{result = }")
            #print("-"*80)

            match result:
                case 'A':
                    return False, result
                case 'R':
                    return False, result
                case False:
                    continue
                case _:
                    return True, result

    def __repr__(self):
        return f'{self}'

    def __str__(self):
        return f'{self.name}: {self.rules}'

    def __eq__(self, other):
        return self.name == other.name

@dataclasses.dataclass
class Input:
    x: int
    m: int
    a: int
    s: int

def part1(data):
    rules, inputs = data

    XMAS = [Input(*myinput) for myinput in inputs]

    workflows = {}



    for name, ruletuple in rules.items():
        workflow = Workflow(name=name, rulelist=ruletuple)
        workflows[name] = workflow
        #print(workflow)

    accepts = 0

    for xmas in XMAS:

        flowname = "in"
        #print(f"{xmas = }")
        continues = True

        while continues:
            continues, flowname = workflows[flowname].run(xmas)
            #print(f"{continues = } {flowname = }")

        if flowname == 'A':
            accepts += (xmas.x + xmas.a + xmas.s + xmas.m)

        #print(xmas, flowname)
    return accepts

data = get_data('input.txt')
print(part1(data))