rows = 'ABCDEFGHI'
cols = '123456789'
assignments = []

def cross(A, B):
    """
    Cross product of elements in A and elements in B.
    """
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

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins, stored as a pair in twinie in array twins
    twins = []
    for unit in unitlist:
        for box1 in range(len(unit)):
            for box2 in range(box1, len(unit)):
                if box1 != box2 and values[unit[box1]] == values[unit[box2]] and len(values[unit[box1]]) == 2:
                    twinie = []
                    twinie.append(unit[box1])
                    twinie.append(unit[box2])
                    if twinie not in twins:
                        twins.append(twinie)

    # Eliminate the naked twins as possibilities for their peers
    for twinie in twins:
        #shared_peers stores the common peers to the twins
        shared_peers = set(peers[twinie[0]]&peers[twinie[1]])
        twin_value = values[twinie[0]]
        for peer in shared_peers:
            replacement_value1 = values[peer].replace(twin_value[0], '')
            replacement_value2 = replacement_value1.replace(twin_value[1], '')
            values = assign_value(values, peer, replacement_value2)
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width_of_box = 1+max(len(values[s]) for s in values)
    horizontal_line = '+'.join(['-'*width_of_box*3]*3)
    for r in rows:
        print(''.join(values[r+c].center(width_of_box)+
            ('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print(horizontal_line)

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value,
    eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_boxes:
        solved_value = values[box]
        for peer in peers[box]:
            replacement_value = values[peer].replace(solved_value, '')
            values = assign_value(values, peer, replacement_value)

    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only
    fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            boxes_with_digit = [box for box in unit if digit in values[box]]
            if len(boxes_with_digit) == 1:
                values = assign_value(values, boxes_with_digit[0], digit)
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a
    box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the
    same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_boxes_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        #Checks for error (prevent unnecessary iterations)
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

        values = only_choice(values)
        #Checks for error (prevent unnecessary iterations)
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

        values = naked_twins(values)
        #Checks for error (prevent unnecessary iterations)
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

        solved_boxes_after = len([box for box in values.keys() if len(values[box]) == 1])
        if solved_boxes_after == solved_boxes_before:
            stalled = True
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    values = reduce_puzzle(values)
    if values is False:
        #There are at least one box in grid with no values
        return False
    if all(len(values[box]) == 1 for box in values):
        return values #Solved
    min_value, min_box = min((len(values[box]), box) for box in values if len(values[box]) > 1)
    for value in values[min_box]:
        new_value = values.copy()
        new_value[min_box] = value
        attempt = search(new_value)
        if attempt:
            print("Returning attempt")
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
