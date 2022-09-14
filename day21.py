from __future__ import annotations
from abc import abstractmethod
from collections import Counter, defaultdict, deque
import re

import numpy as np
from parsy import seq, char_from, regex, generate, string
from dataclasses import dataclass
from functools import reduce, cache
from pprint import pprint
from itertools import permutations, combinations, cycle, product
from copy import deepcopy

from typing import Dict, List, Optional
from time import perf_counter



class Dice:
    @abstractmethod
    def roll(self) -> int: ...


class DeterministicDice(Dice):
    def __init__(self, sides=6):
        self._roller = cycle(range(1,sides+1))
        self.rolls = 0


    def roll(self):
        self.rolls += 1
        return next(self._roller)


class DiracDiceGame:
    def __init__(self, dice: Dice, start_positions: List[int]):
        self.dice = dice
        self.player_positions = start_positions
        self.players = len(start_positions)

    def play(self):
        scores = [0] * self.players

        for player in cycle(range(self.players)):
            rolled = self.dice.roll() + self.dice.roll() + self.dice.roll()
            self.player_positions[player] = (self.player_positions[player] - 1 + rolled) % 10 + 1
            scores[player] += self.player_positions[player]
            if scores[player] >= 1000:
                print(f'player {player+1} wins!')
                print(scores)
                print(min(scores) * self.dice.rolls)
                return

            
    rolls = Counter([sum(rolls) for rolls in product([1, 2, 3], repeat=3)])

    @cache
    def play_diracly(self, pos1: int, pos2: int, score1: int = 0, score2: int = 0):
        wins = [0, 0]

        for roll, freq in self.rolls.items():
            pos = [pos1, pos2]
            scores = [score1, score2]

            pos[0] = (pos[0] - 1 + roll) % 10 + 1
            scores[0] += pos[0]

            # Did the current player win?
            if scores[0] >= 21:
                wins[0] += freq
            else:
                p2_wins, p1_wins = self.play_diracly(pos[1], pos[0], scores[1], scores[0])
                wins[0] += p1_wins * freq
                wins[1] += p2_wins * freq

        return wins



game = DiracDiceGame(DeterministicDice(100), [9, 10])
s = perf_counter()
game.play()
e = perf_counter()
print(e-s)

# example:
# P1 wins: 444356092776315
# P2 wins: 341960390180808
# real:
# [157595953724471, 121908465540796]
s = perf_counter()
print(game.play_diracly(9, 10))
e = perf_counter()
print(e-s)
# print(max(game.play_diracly(9, 10)))