# >>> pprint(''.join(['1' if f['1'] > f['0'] else '0' for f in [Counter([e[i] for e in data.split()]) for i in range(5)]]))
# >>> pprint(''.join(['1' if f['1'] > f['0'] else '0' for f in [Counter([e[i] for e in data.split()]) for i in range(12)]]))

from collections import Counter

with open('inputs/day-3-input.txt') as input_file:
    data = set(input_file.read().split())

# data = {
#     '00100',
#     '11110',
#     '10110',
#     '10111',
#     '10101',
#     '01111',
#     '00111',
#     '11100',
#     '10000',
#     '11001',
#     '00010',
#     '01010',
# }

oxygen_data = data.copy()
co2_data = data.copy()


def reduction(data: set, width: int, keep_most: bool):
    for idx in range(width):
        counts = Counter([e[idx] for e in data])
        most = '1' if counts['1'] >= counts['0'] else '0'
        for e in data.copy():
            if keep_most:
                if e[idx] != most:
                    data.remove(e)
            else:
                if e[idx] == most:
                    data.remove(e)    

        if len(data) == 1:
            return data


print('oxygen', reduction(oxygen_data, 12, True))
print('co2', reduction(co2_data, 12, False))
