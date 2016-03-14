from Matrix import *
import random
import time

start_time = time.time()

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
            size = "  Size: " + str(matrix.rows()) + " x " + str(matrix.cols())
            f.write(str(matrix.get_sparse()) + " \n " +
                    str(matrix.display(size, True)) + "\n")
        else:
            f.write(str(matrix) + "\n")

    f.close()


# Reading graphs
def read_graph(file_path="data/amazon_m_0.edgelist"):
    matrices = []
    a_tuples = []
    d_tuples = []
    l = 0
    prev_i = 0

    with open(file_path, "r", encoding='utf8') as file:
        for line in file:
            l += 1
            if l > 2:
                row = line.split("\n")[0].split(" ")[:2]
                i = int(row[0])
                j = int(row[1])
                v = random.choice([-1, 1])

                if prev_i < i:
                    v_ = ([item[2] for item in a_tuples if item[0] == prev_i])
                    d_tuples.append((prev_i, prev_i, sum(v_)))
                    prev_i = i

                a_tuples.append((i, j, v))

        v_ = sum([item[2] for item in a_tuples if item[0] == i])
        d_tuples.append((i, i, v_))

    r, c, v = Matrix().tuple2csr(a_tuples)
    a = Matrix().set(r, c, v)
    r, c, v = Matrix().tuple2csr(d_tuples)
    d = Matrix().set(r, c, v)

    matrices.append(d.sub(a))

    return matrices


# Writing graphs to file
def write_graph(matrices, file_path="data/output_amazon_m_0.edgelist"):
    f = open(file_path, "w", encoding='utf8')

    for matrix in matrices:
        if isinstance(matrix, Matrix):
            f.write("r: " + str(matrix.r) + " \n" +
                    "c: " + str(matrix.c) + " \n" +
                    "v: " + str(matrix.v) + " \n\n" +
                    str(matrix.display("", True)) + "\n")
        else:
            f.write(str(matrix) + "\n")

    f.close()


def testing_graph():
    m = read_graph("data/amazon_m_3.edgelist")

    # i = 0
    # for x in m:
    #     x.display("m[%s]: %sx%s" % (i, x.rows(), x.cols()))
    #     i += 1

    write_graph(m)
    return m


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
            n = random.randint(-10, 10)
            while n is 0:
                n = random.randint(-10, 10)
            x_list.append(n)
        x = Matrix([x_list]).transpose()
    if b is None:
        b_list = []
        for i in range(0, A.rows()):
            n = random.randint(-10, 10)
            while n is 0:
                n = random.randint(-10, 10)
            b_list.append(n)
        b = Matrix([b_list]).transpose()

    print(x.init_matrix)
    # b.display("b=")

    print("tolerance: %s | max: %s" % (tolerance, max))
    print("A = %sx%s" % (A.rows(), A.cols()))
    print("x = %sx%s" % (x.rows(), x.cols()))
    print("b = %sx%s" % (b.rows(), b.cols()))
    # A.display(str("tolerance: %s | max: %s | A:" % (tolerance, max)))

    r = b.sub(A.mul(x)).display("r_not = b - Ax")
    # for max in range(5, MAX_STEPS_ALLOWED, 5):
    print("~~~End GMREZ~~~")
    return


# matrices = testing()
matrices = testing_graph()

MAX_STEPS_ALLOWED = 20  # Should be << than n (the size of A)
# x = Matrix([[1, 2, 3]]).transpose().display("x=")
# b = Matrix([[10, 20, 30]]).transpose().display("b=")
for m in matrices:
    gmrez(m)

end_time = time.time()
print("Total time: %.2f mins" % ((end_time - start_time)/60))
