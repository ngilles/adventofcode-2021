from __future__ import annotations
from collections import deque

from parsy import seq, char_from, regex, generate, string
from dataclasses import dataclass
from functools import reduce
from pprint import pprint
from itertools import combinations_with_replacement, permutations, combinations
from copy import deepcopy


rules = (
    '..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##'
    '#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###'
    '.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.'
    '.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....'
    '.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..'
    '...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....'
    '..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#'
)

image_raw = [
    '#..#.',
    '#....',
    '##..#',
    '..#..',
    '..###',
]

with open('inputs/day-20-input.txt') as input_file:
    rules = input_file.readline().strip()
    input_file.readline() # empty
    image_raw = [l.strip() for l in input_file.readlines()]

image = {
    (r,c)
    for r in range(len(image_raw))
    for c in range(len(image_raw[0]))
    if image_raw[r][c] == '#'
}

window_lookup = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 0), (0, 1),
    (1, -1), (1, 0), (1, 1),
]
window_lookup.reverse() # LSB to MSB


def render(image):
    min_r = min(p[0] for p in image)
    max_r = max(p[0] for p in image)
    min_c = min(p[1] for p in image)
    max_c = max(p[1] for p in image)

    height = max_r - min_r + 1
    width = max_c - min_c + 1

    grid = [['.'] * width for _ in range(height)]

    for pr, pc in image:
        grid[pr - min_r][pc - min_c] = '#'

    for r in grid:
        print(''.join(r))

    print()


def generation(image, rules, odd=False):
    min_r = min(p[0] for p in image) - (3 if odd else 0)
    max_r = max(p[0] for p in image) + (3 if odd else 0)
    min_c = min(p[1] for p in image) - (3 if odd else 0)
    max_c = max(p[1] for p in image) + (3 if odd else 0)

    height = max_r - min_r + 1
    width = max_c - min_c + 1

    new_image = set()

    #print(min_r, max_r, min_c, max_c)

    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            window_points = [((r+wr-min_r) % height + min_r, (c+wc-min_c) % width + min_c) for (wr, wc) in window_lookup]
            
            idx = sum(
                2 ** idx
                for idx, (wr, wc) in enumerate(window_points)
                if (wr, wc) in image
            )

            if rules[idx] == '#':
                new_image.add((r,c))

    return new_image

render(image)

for i in range(50):
    image = generation(image, rules, odd=i % 2 == 0)

render(image)

print(len(image))