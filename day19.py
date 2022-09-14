from __future__ import annotations
from collections import defaultdict, deque
import re

import numpy as np
from parsy import seq, char_from, regex, generate, string
from dataclasses import dataclass
from functools import reduce
from pprint import pprint
from itertools import permutations, combinations
from copy import deepcopy

from typing import Dict

example ='''--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14'''

with open('inputs/day-19-input.txt') as input_file:
    data = input_file.read()

rotate_i = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])
rotate_x = np.array([
    [ 1,  0,  0],
    [ 0,  0, -1],
    [ 0,  1,  0],
])
rotate_x2 = rotate_x @ rotate_x
rotate_x3 = rotate_x2 @ rotate_x

rotate_y = np.array([
    [ 0,  0,  1],
    [ 0,  1,  0],
    [-1,  0,  0],
])
rotate_y2 = rotate_y @ rotate_y
rotate_y3 = rotate_y2 @ rotate_y

rotate_z = np.array([
    [ 0, -1,  0],
    [ 1,  0,  0],
    [ 0,  0,  1],
])
rotate_z2 = rotate_z @ rotate_z
rotate_z3 = rotate_z2 @ rotate_z

rotations = [rotate_i, rotate_x, rotate_y, rotate_z]

rotations = [
    rotate_i @ rotate_i,
    rotate_i @ rotate_x,
    rotate_i @ rotate_x2,
    rotate_i @ rotate_x3,

    rotate_y @ rotate_i,
    rotate_y @ rotate_x,
    rotate_y @ rotate_x2,
    rotate_y @ rotate_x3,

    rotate_y2 @ rotate_i,
    rotate_y2 @ rotate_x,
    rotate_y2 @ rotate_x2,
    rotate_y2 @ rotate_x3,

    rotate_y3 @ rotate_i,
    rotate_y3 @ rotate_x,
    rotate_y3 @ rotate_x2,
    rotate_y3 @ rotate_x3,

    rotate_z @ rotate_i,
    rotate_z @ rotate_x,
    rotate_z @ rotate_x2,
    rotate_z @ rotate_x3,

    #rotate_z2 @ rotate_i,
    #rotate_z2 @ rotate_x,
    #rotate_z2 @ rotate_x2,
    #rotate_z2 @ rotate_x3,

    rotate_z3 @ rotate_i,
    rotate_z3 @ rotate_x,
    rotate_z3 @ rotate_x2,
    rotate_z3 @ rotate_x3,
]

class ScannerReport:
    def __init__(self, info):
        scanner_id, beacon_positions = info
        self.scanner_id = scanner_id
        self.beacon_positions = beacon_positions
        self.relative_distances = self._relative_distances()
        self.refrence_pos = np.array([0, 0, 0])
        self.rotation = rotations[0]


    def __repr__(self):
        return f'<ScannerReport id={self.scanner_id}, beacons={len(self.beacon_positions)}>'

    def _relative_distances(self):
        count = 0
        dists = set()
        for p1, p2 in combinations(self.beacon_positions, 2):
            count += 1
            dist = sum((a-b)**2 for a, b in zip(p1, p2))
            dists.add(dist)

        assert len(dists) == count
        return dists

    @property
    def referenced_points(self):
        return [(self.rotation @ p) + self.refrence_pos for p in self.beacon_positions]

    def rereference(self, ref: ScannerReport):
        for rot_idx, rot in enumerate(rotations):
            rotated_points = [rot @ p for p in self.beacon_positions]

            for p in rotated_points:
                ref_points = ref.referenced_points
                ref_points_set = {tuple(ref_point) for ref_point in ref_points}
                for ref_point in ref_points:
                    offset = ref_point - p

                    shifted_points = {tuple(rot_point + offset) for rot_point in rotated_points}
                    matches = shifted_points & ref_points_set
                    if len(matches) >= 12:
                        print(rot_idx, offset)
                        self.refrence_pos = offset
                        self.rotation = rot
                        return
                    #print(rot_idx, len(shifted_points & ref_points_set))




number_literal = regex(r'-?[0-9]+').map(int)
report_header = string('--- scanner ') >> number_literal << string(' ---')
point3d_literal = seq(number_literal, string(',') >> number_literal, string(',') >> number_literal).map(np.array)
report_points = point3d_literal.sep_by(string('\n'))
report_literal = seq(report_header, string('\n') >> report_points).map(ScannerReport)
reports_literal = report_literal.sep_by(string('\n\n'))



reports: Dict[int, ScannerReport] = {r.scanner_id: r for r in reports_literal.parse(data)}
matches = [(r1.scanner_id, r2.scanner_id) for r1, r2 in combinations(reports.values(), 2) if len(r1.relative_distances & r2.relative_distances) >= 66]
matches = defaultdict(list)
for r1, r2 in combinations(reports.values(), 2):
    if len(r1.relative_distances & r2.relative_distances) >= 66:
        matches[r1.scanner_id].append(r2.scanner_id)
        matches[r2.scanner_id].append(r1.scanner_id)

referenced = {0}
Q = deque([(0, matches[0])])

while Q:
    rid, matching = Q.popleft()
    for match in matching:
        if match not in referenced:
            referenced.add(match)
            print('reffing', match, 'to', rid)
            reports[match].rereference(reports[rid])
            Q.append((match, matches[match]))
            

all_points = set()
for report in reports.values():
    all_points |= {tuple(p) for p in report.referenced_points}

print(len(all_points))
print(max(sum(abs(a.refrence_pos-b.refrence_pos)) for a, b in combinations(reports.values(), 2)))