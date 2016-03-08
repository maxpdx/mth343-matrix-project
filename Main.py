from Matrix import *
from random import randint

# reading matrices
def read_matrices(file_path="input.dat"):
    matrices = []
    f = open(file_path, "r", encoding='utf8')

    with f as file:
        for line in file:
            if line.startswith("#") or line.startswith("\n"):
                continue
            matrices.append(Matrix(line))

    f.close()
    return matrices

# writing function
def write_matrices(matrices, file_path="output.dat"):
    f = open(file_path, "w", encoding='utf8')

    for matrix in matrices:
        if isinstance(matrix, Matrix):
            f.write(str(matrix.get_sparse()) + " \t===\t " +
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

    # m[0].transpose().display("m[0]^T = ")
    # m[1].transpose().display("m[1]^T = ")
    # m[0].display("Is symmetric: " + str(m[0].is_symmetric()))
    # m[1].display("Is symmetric: " + str(m[1].is_symmetric()))
    # m[0].add(m[1]).display("m[0] + m[1] = ")
    # m[0].sub(m[1]).display("m[0] - m[1] = ")
    # m[0].mul(m[1]).display("m[0] * m[1] = ")
    # m[1].mul(m[0]).display("m[1] * m[0] = ")
    #
    # q, r = m[0].qr()
    # q.display("Q")
    # r.display("R")
    #
    # d = Matrix([[1, -2, 3, 4]]).transpose()
    # v = Matrix([[4, 3, -2, 1]]).transpose()
    # v.display("v = ")
    # d.display("DOT: %s (d.dot(v) ?= '-4') | d = " % d.dot(v))
    # d.display("Length: %s (d.length() ?= '30') | d = " % d.length())

    write_matrices(m, "output.dat")
    return m

def gmrez(A, x=None, b=None, tolerance=10**-6, max=5):
    """
    A GENERALIZED MINIMUM RESIDUAL ALGORITHM (GMRES): AN ITERATIVE
    LEAST-SQUARES ALGORITHM FOR SOLVING Ax = b
    :param A: [Matrix] matrix in csr format
    :param x: [Matrix] starting vector in csr format
    :param b: [Matrix] vector in csr format
    :param tolerance:
    :param max:
    :return:
    """
    print("~~~Start GMREZ~~~")
    if x is None:
        x_list = []
        for i in range(0, A.cols()):
            x_list.append(randint(0, 100))
        x = Matrix([x_list]).transpose().display("x=")
    if b is None:
        b_list = []
        for i in range(0, A.rows()):
            b_list.append(randint(0, 100))
        b = Matrix([b_list]).transpose().display("b=")


    A.display(str("tolerance: %s | max: %s | A:" % (tolerance, max)))

    r = b.sub(A.mul(x)).display("r_not = b - Ax")
    # for max in range(5, MAX_STEPS_ALLOWED, 5):
    print("~~~End GMREZ~~~")
    return

matrices = testing()

MAX_STEPS_ALLOWED = 20  # Should be << than n (the size of A)
# x = Matrix([[1, 2, 3]]).transpose().display("x=")
# b = Matrix([[10, 20, 30]]).transpose().display("b=")
for m in matrices:
    gmrez(m)

