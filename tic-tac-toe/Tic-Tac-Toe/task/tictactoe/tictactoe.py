# write your code here
# moves = input("Enter cells: ").replace('_', ' ')
field = [[i for i in range(3)] for j in range(3)]
field[0][:] = [' ', ' ', ' ']
field[1][:] = [' ', ' ', ' ']
field[2][:] = [' ', ' ', ' ']
# line_1 = moves[0:3]
# line_2 = moves[3:6]
# line_3 = moves[6:9]
is_player1 = True
x_count = 0
o_count = 0


def check(field):
    global x_count, o_count
    x3_in_row = False
    o3_in_row = False
    empty_cells = False

    if field[0][0] == "X":
        if field[0][1] == 'X' and field[0][2] == 'X':
            x3_in_row = True
        if field[1][0] == 'X' and field[2][0] == 'X':
            x3_in_row = True
        if field[1][1] == 'X' and field[2][2] == 'X':
            x3_in_row = True
    if field[0][1] == "X":
        if field[1][1] == 'X' and field[2][1] == 'X':
            x3_in_row = True
    if field[0][2] == "X":
        if field[1][2] == 'X' and field[2][2] == 'X':
            x3_in_row = True
        elif field[1][1] == 'X' and field[2][0] == 'X':
            x3_in_row = True
    if field[1][0] == "X":
        if field[1][1] == 'X' and field[1][2] == 'X':
            x3_in_row = True
    if field[2][0] == "X":
        if field[2][1] == 'X' and field[2][2] == 'X':
            x3_in_row = True

    if field[0][0] == "O":
        if field[0][1] == 'O' and field[0][2] == 'O':
            o3_in_row = True
        if field[1][0] == 'O' and field[2][0] == 'O':
            o3_in_row = True
        if field[1][1] == 'O' and field[2][2] == 'O':
            o3_in_row = True
    if field[0][1] == "O":
        if field[1][1] == 'O' and field[2][1] == 'O':
            o3_in_row = True
    if field[0][2] == "O":
        if field[1][2] == 'O' and field[2][2] == 'O':
            o3_in_row = True
        elif field[1][1] == 'O' and field[2][0] == 'O':
            o3_in_row = True
    if field[1][0] == "O":
        if field[1][1] == 'O' and field[1][2] == 'O':
            o3_in_row = True
    if field[2][0] == "O":
        if field[2][1] == 'O' and field[2][2] == 'O':
            o3_in_row = True

    if ' ' in field[0] or ' ' in field[1] or ' ' in field[2]:
        empty_cells = True

    if (x3_in_row and o3_in_row) or (x_count - o_count >= 2) or (o_count - x_count >= 2):
        return 'Impossible'
    elif not x3_in_row and not o3_in_row and empty_cells:
        return "Game not finished"
    elif not x3_in_row and not o3_in_row and not empty_cells:
        return "Draw"
    elif x3_in_row and not o3_in_row:
        return "X wins"
    elif o3_in_row and not x3_in_row:
        return "O wins"


def print_field(field):
    print(f"---------\n| {field[0][0]} {field[0][1]} {field[0][2]} |\n"
          f"| {field[1][0]} {field[1][1]} {field[1][2]} |\n"
          f"| {field[2][0]} {field[2][1]} {field[2][2]} |\n---------")


print_field(field)

while True:
    coordinates = [int(x) for x in input("Enter the coordinates: ").split()]

    if coordinates[0] not in [1, 2, 3, 4, 5, 6, 7, 8, 9] or coordinates[1] not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        print('You should enter numbers!')
    elif coordinates[0] not in [1, 2, 3] or coordinates[1] not in [1, 2, 3]:
        print('Coordinates should be from 1 to 3!')
    elif field[-coordinates[1]][coordinates[0] - 1] != ' ':
        print('This cell is occupied! Choose another one!')
    else:
        if is_player1:
            field[-coordinates[1]][coordinates[0] - 1] = 'X'
            is_player1 = False
            x_count += 1
        else:
            field[-coordinates[1]][coordinates[0] - 1] = 'O'
            is_player1 = True
            o_count += 1
        print_field(field)
        result = check(field)
        if result in ["Draw", "O wins", "X wins"]:
            print(result)
            break
