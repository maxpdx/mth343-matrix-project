from Matrix import *

# reading matrices
def read_matrices(file_path="input.dat"):
    matrices = []
    f = open(file_path, "r")

    with f as file:
        for line in file:
            if line.startswith("#") or line.startswith("\n"):
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

def testing():
    m = read_matrices("input.dat")

    i = 0
    for x in m:
        x.display("m[%s]: %sx%s" % (i, x.rows(), x.cols()))
        i += 1

    print(" --- --- --- --- --- --- \n")

    m[0].copy().transpose().display("m[0]^T = ")
    m[1].copy().transpose().display("m[1]^T = ")
    m[0].display("Is symmetric: " + str(m[0].is_symmetric()))
    m[1].display("Is symmetric: " + str(m[1].is_symmetric()))
    m[0].copy().add(m[1]).display("m[0] + m[1] = ")
    m[0].copy().sub(m[1]).display("m[0] - m[1] = ")
    m[0].copy().mul(m[1]).display("m[0] * m[1] = ")
    m[1].copy().mul(m[0]).display("m[1] * m[0] = ")

    write_matrices(m, "output.dat")
    return m

testing()
