def get_data(filename='input.txt'):
    with open(filename, 'rt', encoding='ascii') as file:
        data = file.read().splitlines()

        chars = {}
        for y, row in enumerate(data):
            for x, ch in enumerate(row):
                if ch in r"\/|-":
                    chars[(y, x)] = ch  # .replace('\\', '+')

    return chars


class Beam:
    def __init__(self, y, x, direction):
        self.y, self.x = y, x
        self.direction = direction
        self.path = {(y,x)}

    def __str__(self):
        return f'({self.y}, {self.x}) -> {self.direction}'

    def __repr__(self):
        return f'{self}'

    def run(self, towards_y, towards_x, splitter_type):

        beamset = set()

        match self.direction:
            case 'left'|'right':

                new_path = {(self.y, x) for x in range(min(self.x, towards_x), max(self.x, towards_x) + 1)}
                self.path = self.path.union(new_path)
            case 'up'|'down':

                new_path = {(y, self.x) for y in range(min(self.y, towards_y), max(self.y, towards_y) + 1)}
                self.path = self.path.union(new_path)

        self.y = towards_y
        self.x = towards_x

        match self.direction:
            case 'right':
                match splitter_type:
                    case '|':
                        self.direction = 'down'
                        new_beam = Beam(towards_y, towards_x, 'up')
                        beamset.add(new_beam)
                    case '-':
                        pass
                    case '/':
                        self.direction = 'up'
                    case '\\':
                        self.direction = 'down'

            case 'left':
                match splitter_type:
                    case '|':
                        self.direction = 'down'
                        new_beam = Beam(towards_y, towards_x, 'up')
                        beamset.add(new_beam)
                    case '-':
                        pass
                    case '/':
                        self.direction = 'down'
                    case '\\':
                        self.direction = 'up'

            case 'up':
                match splitter_type:
                    case '|':
                        pass
                    case '-':
                        self.direction = 'right'
                        new_beam = Beam(towards_y, towards_x, 'left')
                        beamset.add(new_beam)
                    case '/':
                        self.direction = 'right'
                    case '\\':
                        self.direction = 'left'

            case 'down':
                match splitter_type:
                    case '|':
                        pass
                    case '-':
                        self.direction = 'right'
                        new_beam = Beam(towards_y, towards_x, 'left')
                        beamset.add(new_beam)
                    case '/':
                        self.direction = 'left'
                    case '\\':
                        self.direction = 'right'
            case _:
                assert False
        return beamset

class Grid:
    def __init__(self, splitters, MAX_Y, MAX_X):

        self.H, self.W = MAX_Y, MAX_X
        self.beams = [Beam(y=0, x=0, direction='right')]
        self.splitters = splitters

    @property
    def splitters(self):
        return self._splitters

    @splitters.setter
    def splitters(self, value):
        self._splitters = value

    def get(self, y, x, direction):

        match direction:
            case 'down':
                return next(((sy, sx), chr) for (sy, sx), chr in self.splitters.items() if (x == sx) and (y < sy))
            case 'up':
                return [((sy, sx), chr) for (sy, sx), chr in self.splitters.items() if (x == sx) and (sy < y)][-1]
            case 'right':
                return next(((sy, sx), chr) for (sy, sx), chr in self.splitters.items() if (y == sy) and (x < sx))
            case 'left':
                return [((sy, sx), chr) for (sy, sx), chr in self.splitters.items() if (y == sy) and (sx < x)][-1]





    def run(self, beam):

        new_beams = []
        while True:

            try:
                (y, x), splitter_type = self.get(y=beam.y, x=beam.x, direction=beam.direction)
            except StopIteration:
                match beam.direction:
                    case 'left':
                        beamset = beam.run(towards_y=beam.y, towards_x=0, splitter_type='-')
                    case 'right':
                        beamset = beam.run(towards_y=beam.y, towards_x=self.W, splitter_type='-')
                    case 'up':
                        beamset = beam.run(towards_y=0, towards_x=beam.x, splitter_type='|')
                    case 'down':
                        beamset = beam.run(towards_y=self.H, towards_x=beam.x, splitter_type='|')

                #new_beams.extend([x for x in beamset])
                #self.plot()
                #print("-" * 80)
                break

            print(beam.y, beam.x, beam.direction, splitter_type, '->', end=' ')
            beamset = beam.run(towards_y=y, towards_x=x, splitter_type=splitter_type)
            new_beams.extend([x for x in beamset])

            print(beam.y, beam.x, beam.direction)
            self.plot()
            print("-"*80)
        return new_beams

    def __str__(self):
        return "{beams:}:\n\t{splitters:}".format(beams=self.beams,
                                                  splitters="\n\t".join([f"{x}" for x in self.splitters.items()]))

    def plot(self):



        all_coords = {t  for beam in self.beams for t in beam.path}

        for y in range(self.H):
            for x in range(self.W):
                if (y,x) in all_coords:
                    print('#', end='')
                else:
                    print('.', end='')
            print('')



def part1(data):
    grid = Grid(splitters=data, MAX_Y=10, MAX_X=10)
    grid.plot()

    new_beams = grid.beams

    while new_beams:

        beams = []
        for beam in new_beams:
            nbeams = grid.run(beam)
            beams.extend(nbeams)
            print(f"{nbeams = }")
        #grid.beams.extend([x for x in new_beams])

        if not beams:
            break


        grid.plot()

data = get_data('example.txt')
part1(data)
