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
                    v_ = [item[2] for item in a_tuples if item[0] == prev_i]
                    d_tuples.append((prev_i, prev_i, sum(v_)))
                    prev_i = i

                a_tuples.append((i, j, v))

        v_ = sum([item[2] for item in a_tuples if item[0] == i])
        d_tuples.append((i, i, v_))

    r, c, v = Matrix.tuple2csr(a_tuples)
    a = Matrix().set(r, c, v)
    r, c, v = Matrix.tuple2csr(d_tuples)
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

    # i = 0
    # for x in m:
    #     x.display("m[%s]: %sx%s" % (i, x.rows(), x.cols()))
    #     print(x.get_sparse())
    #     i += 1
    #
    # print(" --- --- --- --- --- --- \n")

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
    # d.display("Length: %s (d.norm() ?= '30') | d = " % d.norm())

    # Matrix.combine_vectors([m[0], m[1]]).display()

    write_matrices(m, "output.dat")
    return m


def gmres(A, x0=None, b0=None, tolerance=10**-6, max=5):
    """
    A GENERALIZED MINIMUM RESIDUAL ALGORITHM (GMRES): AN ITERATIVE
    LEAST-SQUARES ALGORITHM FOR SOLVING Ax = b
    :param A: [Matrix] matrix in csr format
    :param x0: [Matrix] starting vector in csr format
    :param b: [Matrix] vector in csr format
    :param tolerance:
    :param max:
    :return:
    """
    print("~~~Start GMRES~~~")

    x = {}
    b = {}
    r = {}
    p = {}
    ph = {}
    P = {}
    Beta = {}
    B = []

    if x0 is None:
        # x_list = []
        # for i in range(0, A.cols()):
        #     n = random.randint(-10, 10)
        #     while n is 0:
        #         n = random.randint(-10, 10)
        #     x_list.append(n)
        x_list = [1, 2, 3]
        x[0] = (Matrix([x_list]).transpose())
    else:
        x[0] = x0

    if b0 is None:
        # b_list = []
        # for i in range(0, A.rows()):
        #     n = random.randint(-10, 10)
        #     while n is 0:
        #         n = random.randint(-10, 10)
        #     b_list.append(n)
        b_list = [1, 1, 1]
        b[0] = (Matrix([b_list]).transpose())
    else:
        b[0] = b0

    x[0].display("x[0]=", False, '')
    b[0].display("b[0]=", False, '')

    # print("tolerance: %s | max: %s" % (tolerance, max))
    # print("x = %sx%s" % (x[0].rows(), x[0].cols()))
    # print("b = %sx%s" % (b[0].rows(), b[0].cols()))
    # print("A = %sx%s" % (A.rows(), A.cols()))
    A.display(str("tolerance: %s | max: %s | A:" % (tolerance, max)))

    r[0] = b[0].sub(A.mul(x[0]))
    r[0].display("r_not = b - Ax", False, '')

    r_norm = r[0].norm()
    # We form p_1 = (1 / ||r_0||) * r_0
    p[1] = r[0].scale(1/r_norm)
    # Compute b1 = Ap1.
    b[1] = A.mul(p[1])

    # Solve the least-squares problem ||r − t*b_1|| → min, which gives
    t = b[1].t().mul(r[0]).v[0] / b[1].t().mul(b[1]).v[0]

    # x1 = x0 + tp1
    x[1] = x[0].add(p[1].scale(t))
    # r1 = r0 − tb1 (= b − Ax1).
    r[1] = r[0].sub(b[1].scale(t))

    # print(1/r_norm)
    # p1.display("p = ")
    # b1.display("b = ")
    # print(t)

    x[1].display("x[1] = \t\t", False, '')
    r[1].display("r[1] = \t\t", False, '')

    # ph[0] = ph[1] = 0
    # p[0].display("p_0")
    # p[1].display("p_1")
    # print(p)
    # print(r)
    # print(ph)

    for m in range(2, max+1):
        print("LOOP: m=%s" % m)
        # ph[m] = r[m-1].copy()

        for i in range(1, m):
            print("\tloop: m=%s i=%s" % (m, i))
            # B_i = p[i]^T*r_(m-1), for i = 1, . . . , m − 1.
            # B[i] = p[i].t().mul(r[m-1])
            p[m-1].display("\t\t\tp[m-1] = ", indent="\t\t\t")
            r[m-1].display("\t\t\tr[m-1] = ", indent="\t\t\t")
            Beta[i] = p[m-1].t().mul(r[m-1])
            Beta[i].display("\t\tBeta = ", indent="\t\t")

            # ph_m = r_(m−1) − β_1*p_1 − β_2*p_2 − . . . − β_(m−1)p_(m−1).

            ph[m] = ph[m].sub(Beta[m-1].mul(p[m-1]))
            # ph[m] = ph[m].sub(p[m-1].t().mul(r[m-1]).mul(p[m]))
            ph[m].display("ph = ")

        # print(p[m])
        # print(r[m-1])
        # t = p[m].t().mul(r[m-1]).mul(p[m])
        # ph[m] = r[m-1].sub(t)

        # Then p_m = (1 / ||ph_m||)*ph_m
        p[m] = ph[m].scale(1 / ph[m].norm())

        # Form P = [p_1, p_2, . . . , p_m].
        print(p)
        print(list(p.values()))
        print("printing p = %s" % p.values()[0])
        P = Matrix.combine(list(p.values()))
        P.display("P = ")

        # Compute b_m = Ap_m and form B = [b1, b2, . . . , bm] (= AP)
        b[m] = A.mul(p[m])
        B = Matrix.combine(list(b.values()))
        B.display("B = ")

        # Solve the least-squares problem. ||r_m−1 − Bt||→ min .
        # This can be done by using QR factorization of B.
        #   (1) Compute B = QR.
        #   (2) Solve Rt = Q^T r_(m−1) by back substitution.
        t = least_squares(B, r[m-1])

        # The next iterate is: x_m = x_(m−1) + Pt.
        x[m] = x[m-1].add(P.mul(t))

        # The next residual is: r_m = r_(m−1) − Bt (= b − Ax_m).
        r[m] = r[m-1].sub(B.mul(t))

        # Stopping criterion
        if r[m].norm() < tolerance:
            break
        print("END LOOP: m=%s" % m)

    last_r = sorted(r.keys())[-1]
    last_x = sorted(x.keys())[-1]
    r[last_r].display("r (Final) = ")
    x[last_x].display("x (Final) = ")

    # for max in range(5, MAX_STEPS_ALLOWED, 5):
    print("~~~End GMRES~~~")
    return


def least_squares(B, r):
    """
    Solve the least-squares problem. ||r_m−1 − Bt||→ min .
    This can be done by using QR factorization of B.
      (1) Compute B = QR.
      (2) Solve Rt = Q^T r_(m−1) by back substitution.
    :param B:
    :param r:
    :return:
    """

    Q, R = B.qr()
    Q.display("Q = ")
    R.display("R = ")
    rhs = Q.t().mul(r)
    rhs.display("rhs = ")
    # lhs = R.
    return rhs


matrices = testing()
# matrices = testing_graph()

MAX_STEPS_ALLOWED = 20  # Should be << than n (the size of A)
for m in matrices:
    gmres(m)

end_time = time.time()
print("Total time: %.2f mins" % ((end_time - start_time)/60))
