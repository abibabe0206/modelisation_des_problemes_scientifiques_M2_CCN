from collections import Counter
"Each of the 7 boxes can contain 4 different potions (poison, wine, forward, backward) coded 0, 1, 2, 3"
def harry_potter(case):
    if case[1] != case[5]: return False
    if case[5] == 0: return False
    if case[2] == 0: return False
    if case[0] == case[6] : return False
    if case[0] == 2: return False
    if case[6] == 2: return False
    c = Counter(case)
    if c[0] != 3: return False
    if c[1] != 2: return False
    if c[2] != 1: return False
    if c[3] != 1: return False
    for k in range(1, 7):
        if case[k] == 1 and case[k-1] != 0:
            return False
    return True
result = []
for i in range(4**6):
    l = [(i % (4**k)) // (4**(k-1)) for k in range(1,7)]
    l.insert(5, l[1])
    if harry_potter(l):
        result.append(l)
print(result)