def read_matrix(dimension, name='first'):
    matrix = []
    if name == '':
        print('Enter matrix')
    else:
        print(f'Enter {name} matrix')
    for i in range(dimension[0]):
        matrix.append([float(x) for x in input().split(' ')])
    return matrix


def check_dim_equality(dim_a, dim_b, mode='addition'):
    if mode == 'addition':
        if (dim_a[0] == dim_b[0]) and (dim_a[1] == dim_b[1]):
            return True
        else:
            return False
    else:
        if dim_a[1] == dim_b[0]:
            return True
        else:
            return False


def transpose_matrix(matrix, mode='main'):
    if mode == 'main':
        return list(map(list, zip(*matrix)))
    elif mode == 'side':
        matrix.reverse()
        for row in matrix:
            row.reverse()
        return list(map(list, zip(*matrix)))
    elif mode == 'vertical':
        for row in matrix:
            row.reverse()
        return matrix
    elif mode == 'horizontal':
        matrix.reverse()
        return matrix


def calc_sum(matrix_a, matrix_b):
    sum_matrix = []
    for row_a, row_b in zip(matrix_a, matrix_b):
        sum_matrix.append([x + y for x, y in zip(row_a, row_b)])
    return sum_matrix


def calc_multiplication(matrix_a, matrix_b):
    sum_matrix = []
    for row_a in matrix_a:
        temp_row = []
        for row_b in list(map(list, zip(*matrix_b))):
            temp_row.append(sum([x * y for x, y in zip(row_a, row_b)]))
        sum_matrix.append(temp_row)
    return sum_matrix


def print_matrix(matrix):
    print('The result is:')
    for i in matrix:
        for j in i:
            print(j, end=' ')
        print()


def multiply_constant(matrix, constant):
    sum_matrix = []
    for row_a in matrix:
        sum_matrix.append([x * constant for x in row_a])
    return sum_matrix


def calculate_determinant(matrix, matrix_dim):
    if matrix_dim[0] == 1 and matrix_dim[1] == 1:
        return matrix[0][0]
    if matrix_dim[0] == 2 and matrix_dim[1] == 2:
        return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])
    determinant = 0
    for j in range(matrix_dim[1]):
        minor = [[item for idx, item in enumerate(items) if idx != j] for items in matrix][1:]
        determinant += matrix[0][j] * (
                    ((-1) ** (1 + (j + 1))) * (calculate_determinant(minor, [len(minor), len(minor[0])])))
    return determinant


def calculate_inverse(matrix, matrix_dim):
    determinant = calculate_determinant(matrix, matrix_dim)
    if determinant == 0:
        return -1
    else:
        cofactor_matrix = []
        for i in range(matrix_dim[0]):
            row = []
            for j in range(matrix_dim[1]):
                minor = [[item for idx, item in enumerate(items) if idx != j] for i_idx, items in enumerate(matrix) if i_idx != i]
                row.append(((-1) ** ((i + 1) + (j + 1))) * calculate_determinant(minor, [len(minor), len(minor[0])]))
            cofactor_matrix.append(row)
        cofactor_transposed = transpose_matrix(cofactor_matrix, "main")
        inverse = multiply_constant(cofactor_transposed, (1 / determinant))
        return inverse



while True:
    print("1. Add matrices\n2. Multiply matrix by a constant\n3. Multiply matrices\n4. Transpose matrix\n5. Calculate "
          "a determinant\n6. Inverse matrix\n0. Exit")
    action = int(input())
    if action == 1:
        dim_a = [int(x) for x in input('Enter size of first matrix:').split(' ')]
        matrix_a = read_matrix(dim_a)
        dim_b = [int(x) for x in input('Enter size of second matrix:').split(' ')]
        matrix_b = read_matrix(dim_b, name='second')
        if check_dim_equality(dim_a, dim_b):
            print_matrix(calc_sum(matrix_a, matrix_b))
        else:
            print('The operation cannot be performed.')
    elif action == 2:
        dim_a = [int(x) for x in input('Enter size of matrix:').split(' ')]
        matrix_a = read_matrix(dim_a, name='')
        constant = int(input('Enter constant:'))
        print_matrix(multiply_constant(matrix_a, constant))
    elif action == 3:
        dim_a = [int(x) for x in input('Enter size of first matrix:').split(' ')]
        matrix_a = read_matrix(dim_a)
        dim_b = [int(x) for x in input('Enter size of second matrix:').split(' ')]
        matrix_b = read_matrix(dim_b, name='second')
        if check_dim_equality(dim_a, dim_b, mode='multiplication'):
            print_matrix(calc_multiplication(matrix_a, matrix_b))
        else:
            print('The operation cannot be performed.')
    elif action == 4:
        print("1. Main diagonal\n2. Side diagonal\n3. Vertical line\n4. Horizontal line")
        transpose_choice = int(input())
        dim_matrix = [int(x) for x in input('Enter matrix size:').split(' ')]
        matrix = read_matrix(dim_matrix, name='')
        if transpose_choice == 1:
            print_matrix(transpose_matrix(matrix, 'main'))
        elif transpose_choice == 2:
            print_matrix(transpose_matrix(matrix, 'side'))
        elif transpose_choice == 3:
            print_matrix(transpose_matrix(matrix, 'vertical'))
        elif transpose_choice == 4:
            print_matrix(transpose_matrix(matrix, 'horizontal'))
    elif action == 5:
        dim_matrix = [int(x) for x in input('Enter matrix size:').split(' ')]
        matrix = read_matrix(dim_matrix, name='')
        print(f'The result is:\n{calculate_determinant(matrix, dim_matrix)}\n')
    elif action == 6:
        dim_matrix = [int(x) for x in input('Enter matrix size:').split(' ')]
        matrix = read_matrix(dim_matrix, name='')
        inverse_matrix = calculate_inverse(matrix, dim_matrix)
        if inverse_matrix == -1:
            print("This matrix doesn't have an inverse.")
        else:
            print_matrix(inverse_matrix)
    elif action == 0:
        break
