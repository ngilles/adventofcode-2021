from itertools import product

steps =    [   5,    5,    1,   15,    2, None,    5, None, None, None,    7, None, None, None]
required = [None, None, None, None, None,    1, None,    8,    7,    8, None,    2,    2,   13]

def works(digits):
    z = 0
    res = [0] * 14

    digits_idx = 0

    for i in range(14):
        increment, mod_req = steps[i], required[i]

        if increment == None:
            assert mod_req != None
            res[i] = ((z % 26) - mod_req)
            z //= 26
            if not (1 <= res[i] <= 9):
                return False

        else:
            assert increment != None
            z = z * 26 + digits[digits_idx] + increment
            res[i] = digits[digits_idx]
            digits_idx += 1

    return res


for digits in product(range(9, 0, -1), repeat=7):
    res = works(digits)
    if res:
        print("".join([str(i) for i in res]))
        break
    
for digits in product(range(1,10), repeat=7):
    res = works(digits)
    if res:
        print("".join([str(i) for i in res]))
        break