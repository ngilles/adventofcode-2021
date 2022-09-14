
from copy import deepcopy
from collections import deque

example = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''

small_example = '''11111
19991
19191
19991
11111'''

with open('inputs/day-11-input.txt') as input_file:
    data = input_file.read()

class Grid:
    _directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    def __init__(self, grid):
        self._grid = grid

    def neigbours(self, p):
        x, y = p
        for dx, dy in self._directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self._grid) and 0 <= ny < len(self._grid[0]):
                yield (nx, ny)


    def generation(self):
        flashes = 0
        flashed = set()

        # increase all by 1
        for x in range(len(self._grid)):
            for y in range(len(self._grid[0])):
                self._grid[x][y] += 1

        # look for flashers
        flashers = deque()
        for x in range(len(self._grid)):
            for y in range(len(self._grid[0])):
                if self._grid[x][y] > 9:
                    flashers.append((x,y))
                    flashed.add((x, y))
                    flashes += 1

        while flashers:
            p = flashers.popleft()

            for nx, ny in self.neigbours(p):
                self._grid[nx][ny] += 1
                if self._grid[nx][ny] > 9 and (nx, ny) not in flashed:
                    flashers.append((nx,ny))
                    flashed.add((nx, ny))
                    flashes += 1

        # reset flashed to 0
        for x in range(len(self._grid)):
            for y in range(len(self._grid[0])):
                if self._grid[x][y] > 9:
                    self._grid[x][y] = 0

        return flashes

    def print(self):
        for r in self._grid:
            print(r)

grid = Grid([[int(e) for e in r] for r in data.split()])

gen = 1
flashes = grid.generation()

while flashes < 100:
    gen += 1
    flashes = grid.generation()

print(gen)
