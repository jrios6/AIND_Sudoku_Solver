rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def generate_diagonal_units():
    diagonal_units = [[],[]]
    length = len(rows)
    for i in range(length):
        diagonal_units[0].append(rows[i]+cols[i])
    for i in range(length):
        diagonal_units[1].append(rows[i]+cols[length-i-1])
    return diagonal_units

boxes = cross(rows, cols)
diagonal_units = generate_diagonal_units()
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

x = peers["A2"]
y = peers["I7"]
print(x)
print(y)
print(set(x&y))
"""
for unit in unitlist:
    twins = []
    for box1 in range(len(unit)):
        for box2 in range(box1, len(unit)):
            if box1 != box2 and values[unit[box1]] == values[unit[box2]]:
                twinie = []
                twinie.append(unit[box1])
                twinie.append(unit[box2])
                twins.append(twinie)

# Eliminate the naked twins as possibilities for their peers
for twinie in twins:
    for box in twinie:
        twin_value = values[box]
        for peer in peers:
            replacement_value = values[peer].replace(twin_value, '')
            values = assign_value(values, peer, replacement_value)
"""
