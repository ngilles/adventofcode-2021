example = '''0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
'''

from collections import defaultdict
from itertools import repeat
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
vent_literal = seq(point_literal, string(' -> ') >> point_literal).map(tuple)
vent_list = vent_literal.sep_by(char_from('\n'))

vents, the_rest = vent_list.parse_partial(example)
vents, the_rest = vent_list.parse_partial(open('inputs/day-5-input.txt').read()) #example)

print(vents, the_rest)

grid = defaultdict(int)


def _range(v1, v2):
    if v1 <= v2:
        return range(v1, v2 + 1)
    else:
        return range(v1, v2 - 1, -1)

def _points(x1, y1, x2, y2):
    if x1 == x2:
        return zip(repeat(x1), _range(y1, y2))
    elif y1 == y2:
        return zip(_range(x1, x2), repeat(y1))
    else:
        return zip(_range(x1, x2), _range(y1,y2))


for (x1, y1), (x2,y2) in vents:
    for x, y in _points(x1,y1, x2, y2):
        grid[(x, y)] += 1

print(sum(1 for v in grid.values() if v >= 2))