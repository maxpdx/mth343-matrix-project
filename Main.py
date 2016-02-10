from Matrix import *


# reading matrices
def read_matrices(file_path="input.dat"):
    matrices = []
    f = open(file_path, "r")

    with f as file:
        for line in file:
            matrices.append(Matrix(parse(line)))

    f.close()
    return matrices


# writing function
def write_matrices(matrices, file_path="output.dat"):
    f = open(file_path, "w")

    for matrix in matrices:
        f.write(str(matrix) + "\n")

    f.close()


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
            values[i] = float(v)

        matrix.append(values)
    return matrix

m = read_matrices("input.dat")

m[0].display()
m[0].to_array().display()
print ""
m[1].display()
m[1].display()
print ""
m[2].display()
m[2].to_array().display()

m[0].add(m[1])

write_matrices(m, "output.dat")
