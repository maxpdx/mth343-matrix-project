from Matrix import *


# reading matrices
def read_matrices(file_path="input.dat"):
    f = open(file_path, "r")
    with f as file:
        a_ = Matrix(parse(file.readline()))
        b_ = Matrix(parse(file.readline()))
        c_ = Matrix(parse(file.readline()))
    f.close()
    return a_, b_, c_


# writing function
def write_matrices(matrices, file_path="output.dat"):
    f = open(file_path, "w")

    for matrix in matrices:
        f.write(str(matrix) + "\n")

    f.close()
    return True


# Parsing a str to a matrix
def parse(matrix_str):
    matrix = []
    matrix_str = matrix_str.replace(" ", "")
    rows = matrix_str.split("],")
    for row in rows:
        row = row.replace("[", "")
        row = row.replace("]", "")
        row = row.replace("\r", "")
        row = row.replace("\n", "")

        # converting to ints
        values = row.split(",")
        for i, v in enumerate(values):
            values[i] = int(v)

        matrix.append(values)
    return matrix

(a, b, c) = read_matrices("input.dat")

print a.get_matrix()
print a.get_sparse()

print b.get_matrix()
print b.get_sparse()

print c.get_matrix()
print c.get_sparse()

# a.add(b)

write_matrices([a.get_sparse(), b.get_sparse(), c.get_sparse()], "output.dat")
