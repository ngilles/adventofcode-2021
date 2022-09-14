import collections
from dataclasses import dataclass
from collections import defaultdict
from io import StringIO, TextIOWrapper
from typing import Tuple, List

example = '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''


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
bingo_numbers = number_literal.sep_by(char_from(',')) << char_from('\n')    

bingo_row = regex(' *') >> number_literal.sep_by(regex(' +'), min=5, max=5) << char_from('\n')
bingo_board = bingo_row.times(5)

bingo_input = seq(bingo_numbers << string('\n'), bingo_board.sep_by(char_from('\n')))

(numbers, boards), the_rest = bingo_input.parse_partial(open('inputs/day-4-input.txt').read()) #example)
print('numbers:', numbers)
print('boards:', boards)
print('the rest:', the_rest)

@dataclass
class BingoCardState:
    rows: List[int] 
    cols: List[int]

bingo_card_index = defaultdict(list)
bingo_card_states = [BingoCardState([0]*5, [0]*5) for _ in boards]

for board_idx, board in enumerate(boards):
    for row_idx, row in enumerate(board):
        for col_idx, col in enumerate(row):
            bingo_card_index[col].append((board_idx, row_idx, col_idx))


played = set()
board_won = set()

for number in numbers:
    played.add(number)
    print('plaing number:', number)
    for board_idx, row_idx, col_idx in bingo_card_index[number]:
        bingo_card_states[board_idx].rows[row_idx] += 1
        if board_idx not in board_won and bingo_card_states[board_idx].rows[row_idx] == 5:
            print('bingo card', board_idx, 'finished row', row_idx)
            bsum = sum(v for br in boards[board_idx] for v in br if v not in played)
            print(bsum)
            print(bsum * number)
            board_won.add(board_idx)
        bingo_card_states[board_idx].cols[col_idx] += 1
        if board_idx not in board_won and bingo_card_states[board_idx].cols[col_idx] == 5:
            print('bingo card', board_idx, 'finished col', col_idx)
            bsum = sum(v for br in boards[board_idx] for v in br if v not in played)
            print(bsum)
            print(bsum * number)
            board_won.add(board_idx)
            