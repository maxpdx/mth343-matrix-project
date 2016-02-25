from Matrix import *

# reading matrices
def read_matrices(file_path="input.dat"):
    matrices = []
    f = open(file_path, "r")

    with f as file:
        for line in file:
            if line.startswith("#"):
                continue
            matrices.append(Matrix(line))

    f.close()
    return matrices

# writing function
def write_matrices(matrices, file_path="output.dat"):
    f = open(file_path, "w")

    for matrix in matrices:
        if isinstance(matrix, Matrix):
            f.write(str(matrix.get_sparse())  + " \t===\t " +
                    str(matrix.display("", True)) + "\n")
        else:
            f.write(str(matrix) + "\n")

    f.close()

store = []
m = read_matrices("input.dat")

for x in m:
    x.display_size()
    x.display()

m[0].add(m[1])
m[0].display("m[0] + m[1] = ")

write_matrices(m, "output.dat")
