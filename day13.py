from functools import reduce

example = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''

with open('inputs/day-13-input.txt') as input_file:
    data = input_file.read()

from parsy import (
    any_char,
    char_from,
    digit,
    eof,
    generate,
    letter,
    peek,
    regex,
    seq,
    string,
    string_from,

)

number_literal = regex(r'-?[0-9]+').map(int)
point_literal = seq(number_literal, char_from(',') >> number_literal).map(tuple)

fold_instruction = seq(string('fold along ') >> char_from('xy'), char_from('=') >> number_literal).map(tuple)

point_list = point_literal.sep_by(char_from('\n'))
fold_list = fold_instruction.sep_by(char_from('\n'))

instructions = seq(point_list, string('\n\n') >> fold_list)

points, folds = instructions.parse(data)

points = set(points)
print(points, folds)

def display(points):
    x_max = max(x for (x, _) in points)
    y_max = max(y for (_, y) in points)

    grid = [['.'] * (x_max+1) for _ in range(y_max+1)]

    for x, y in points:
        grid[y][x] = '#'

    for row in grid:
        print(''.join(row))

#  .... #...  5
#             4
#  ...#       3
#  pos - (x-pos)
def paper_fold(points, fold):
    axis, pos = fold
    if axis == 'x':
        return {(pos - (x - pos), y) if x > pos else (x, y) for (x,y) in points}
    else:
        return {(x, pos - (y - pos)) if y > pos else (x, y) for (x,y) in points}

#display(points)
points = reduce(paper_fold, folds, points)
display(points)