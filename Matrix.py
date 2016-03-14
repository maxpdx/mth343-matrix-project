# To install use 'pip install numpy'
import numpy as np
import copy
from math import sqrt


class Matrix:
    """
    Matrix library that will store matrix in a CSR (Compressed Sparse Row)
    format and provides methods to perform elementary matrix operations with
    this matrix in this format. (This format aims to optimise memory usage,
    but increases number of computations)

    WARNING: In current solution, matrix will ignore 'zero rows' and 'zero
    columns' in a matrix.
    """

    # Class variables
    r = []      # row pointer (points to an index of changing row value)
    c = []      # stores the column index of the value(self.v)
    v = []      # stores a list of values
    isCSR = False    # marks the current type of storage is sparse of not

    # FOR TESTING while developing ONLY
    init_matrix = [] # stores the matrix in array of arrays of ints/floats
    r_ = []     # stores the row index of the value(self.v)

    def __init__(self, matrix=None):
        """
        Constructor: initializes variables, checks the type, converts to
        sparse matrix iff the input matrix is not a sparse matrix.
        :param matrix: [list] - array of arrays of floats/ints
        :return:
        """

        if matrix and not isinstance(matrix, Matrix):
            if isinstance(matrix, str):
                matrix = self.str2list(matrix)

            self.clean_up()
            self.init_matrix = matrix
            if matrix and not self.isCSR:
                self.list2csr()

    def set(self, r, c, v):
        self.r = r
        self.c = c
        self.v = v
        self.isCSR = True
        return self

    def copy(self):
        """
        Copies the object into a new one
        :return: [Matrix] a new instance copy of the current object
        """
        return copy.deepcopy(self)

    def clean_up(self):
        """
        Clean Up: initializes lists of sparse storage to empty lists
        :return: self [Matrix]
        """
        self.r = []
        self.c = []
        self.v = []
        self.isCSR = False

        self.r_ = []    # FOR TESTING ONLY
        return self

    def get_sparse(self):
        """
        Get Matrix in sparse form
        :return: [list] of following lists:
            self.r [list] - row pointer (points to an index of changing row value)
            self.c [list] - column indexes of the values(self.v)
            self.v [list] - list of plain matrix values
        """
        return [self.r, self.c, self.v]

    def is_csr(self):
        """
        Is Sparse: checks if the current instance of a Matrix class is
        already stored in a sparse format
        :return: [Boolean] - is in sparse format? True or False
        """
        return self.isCSR

    def rows(self):
        """
        Number of Rows: computes the number of rows in current matrix.
        :return: [Int] - number of rows
        """
        return len(self.r)-1

    def cols(self):
        """
        Number of Columns: computes the number of cols in current matrix.
        :return: [Int] - number of cols
        """
        return max(self.c)+1

    def list2csr(self):
        """
        List To Sparse: converts the array of arrays of ints/floats to sparse
        matrix and stores in needed data structure (list [r, c, v]). NOTE:
        make sure self.init_matrix is set before calling this method.
        :return: [Matrix] - self object
        """
        if not self.init_matrix:
            print("!!! Exception: Nothing to convert to sparse matrix, "
                            "self.init_matrix = []")

        if not self.is_csr():
            prev_r = -1
            for n, row in enumerate(self.init_matrix):
                for col, val in enumerate(row):
                    if val != 0:
                        if prev_r != n:
                            prev_r = n
                            self.r.append(len(self.v))
                        self.r_.append(n)
                        self.c.append(col)
                        self.v.append(val)
            self.r.append(len(self.v))
            self.isCSR = True
        return self

    def csr2list(self):
        """
        CSR To List: converts current sparse matrix to an array of arrays of
        ints/floats
        :return: [Matrix] - self object
        """
        if self.is_csr():
            rows = []
            for i in range(0, self.rows()):
                row = []
                for j in range(0, self.cols()):
                    row.append(0.0)
                rows.append(row)

            prev_i = i = 0
            for x, val in enumerate(self.v):
                if x == self.r[prev_i]:
                    i = prev_i
                    if len(self.r) > prev_i+1:
                        prev_i += 1

                j = self.c[x]
                rows[i][j] = val

            self.clean_up()
            self.init_matrix = rows
        return self

    @staticmethod
    def combine_vectors(vectors):
        """
        Combines list of vectors and outputs a new matrix
        :param vectors: [list] of [Matrix] or [list]
        :return: [Matrix]
        """
        prev_rows = vectors[0].rows()
        new_tuples = []
        j = 0
        for vector in vectors:
            if prev_rows != vector.rows():
                print("!!! Exception: Can't combine vectors that are not "
                      "the same dimension!")
                return Matrix()

            if isinstance(vector, Matrix):
                tuples = vector.csr2tuple()
            else:
                tuples = vector.list2csr().csr2tuple()
            print(tuples)
            for tup in tuples:
                new_tuples.append((tup[0], j, tup[2]))

            j += 1

        print(new_tuples)
        new_tuples = sorted(new_tuples)
        print(new_tuples)

        r, c, v = Matrix.tuple2csr(new_tuples)

        result = Matrix().set(r, c, v)

        return result

    @staticmethod
    def combine(vectors):
        """
        Alias method for calling combine_vectors()
        :param vectors:
        :return:
        """
        return Matrix.combine_vectors(vectors)

    @staticmethod
    def str2list(matrix_str):
        """
        Converts a string into a list format which could be converted to Matrix
        :param matrix_str: [str]
        :return: [list]
        """
        matrix = []
        matrix_str = matrix_str.replace(" ", "")
        rows = matrix_str.split("],")
        for row in rows:
            row = row.replace("[", "")
            row = row.replace("]", "")
            row = row.replace("\r", "")
            row = row.replace("\n", "")

            # converting to floats
            values = row.split(",")
            for i, v in enumerate(values):
                values[i] = float(v)

            matrix.append(values)
        return matrix

    @staticmethod
    def list2str(matrix_rows):
        """
        Converts a list into a string format
        :param matrix_rows:
        :return:
        """
        text = ""
        for row in matrix_rows:
            text += str(row) + "\n"
        return text

    def display(self, text="", returns=False, nl="\n"):
        """
        Displays the matrix in whatever format it is
        :param text: [string] any text that you want to display before matrix
        :param returns: [boolean] Whether to print the matrix or return
        :param nl: [string] new line tag. (cold be '\n', ' ', '|' or anything)
        :return:
        """
        if self.is_csr():
            matrix = self.get_sparse_display()
        else:
            matrix = self.init_matrix

        result = ""
        if text != "":
            result += text + nl

        c = 0

        for row in matrix:
            c += 1

            first = "[" if c == 1 else " "              # first row has '['
            last = " ]" if c == len(matrix) else ","    # last row has ' ]'

            e = [float("%.2f" % x) if isinstance(x, float) else x for x in row]
            result += str("\t%s%s%s" % (first, e, last)) + nl

        if not returns:
            print(result)

        return result

    def get_sparse_display(self):
        """
        Display the matrix in a sparse format (replacing 0s with '_')
        NOTE: comutation happens from a sparse matrix directly.
        :param returns:
        :return:
        """
        rows = []
        for i in range(0, self.rows()):
            row = []
            for j in range(0, self.cols()):
                row.append("__")
            rows.append(row)

        prev_i = i = 0
        for x, val in enumerate(self.v):
            if x == self.r[prev_i]:
                i = prev_i
                if len(self.r) > prev_i+1:
                    prev_i += 1

            j = self.c[x]
            rows[i][j] = val

        return rows

    def _type_check(self, matrix):
        """
        Converts given matrix in Matrix format.
        :param matrix:  [str]
                        [list]
                        [matrix]
        :return:
        """
        if isinstance(matrix, str):
            matrix = self.str2list(matrix)
        if isinstance(matrix, list):
            matrix = Matrix(matrix)
            matrix.display()

        if not isinstance(matrix, Matrix):
            print("!!! Exception: Can't convert to a Matrix!")

        return matrix

    def csr2tuple(self):
        current_row = 0
        triples_list = []
        for j, v in enumerate(self.v):
            if j == self.r[current_row + 1]:
                current_row += 1
            triples_list.append((current_row, self.c[j], v))
        return triples_list

    @staticmethod
    def tuple2csr(list):
        new_r = []
        new_c = []
        new_v = []
        prev_r = -1
        for triple in list:
            if prev_r != triple[0]:
                prev_r = triple[0]
                new_r.append(len(new_v))
            new_c.append(triple[1])
            new_v.append(triple[2])
        new_r.append(len(new_v))
        return new_r, new_c, new_v

    def transpose(self, to_self=False):
        """
        Takes transpose of a matrix
        :param to_self: [Boolean] if this operation should return a new object
        :return: [Matrix] - self object
        """
        new_tuple = []
        for a_tuple in self.csr2tuple():
            # Making transpose: (x, y, v) => (y, x, v)
            new_tuple.append((a_tuple[1], a_tuple[0], a_tuple[2]))

        # Need to sort for 1st element in tuple(x) so we will be able to go
        # back to sparse matrix by re-computing self.r (rows list)
        result = sorted(new_tuple)

        r, c, v = Matrix.tuple2csr(result)

        if to_self:
            self.r, self.c, self.v = r, c, v
            result = self
        else:
            result = Matrix().set(r, c, v)

        return result

    def t(self, to_self=False):
        return self.transpose(to_self)

    def is_symmetric(self):
        """
        Checks if the current Matrix object (is CSR format) is symmetric
        :return: [bool] True or False
        """
        result = False

        t = self.t()

        if self.r == t.r and self.c == t.c and self.v == t.v and\
           self != t:  # Making sure we are not comparing the same object
            result = True

        return result

    def qr(self, normalized=True):
        """
        Computes the QR Factorization where where Q is an orthogonal matrix
        and R is an upper triangular matrix.

        NOTE: using external library to compute it since have no time to
        implement it.
        :param normalized:
        :return: [Matrix], [Matrix] Q, R matrices
        """
        a = self.copy().csr2list().init_matrix

        q, r = np.linalg.qr(a)
        if normalized:
            q = q / q.max(axis=0)

        return Matrix(q.tolist()), Matrix(r.tolist())

    def dot(self, vector=None):
        """
        Computes the dot product with a vector. Both self and vector should
        be 1 column [Matrix].
        :param vector: [Matrix] to take the dot product with. If None,
        then we duplicate the current [Matrix]
        :return: [float] or [int]
        """
        if vector is None or vector == self:
            vector = self.copy()

        if self.cols() > 1:
            print("!!! Exception: Can't compute dot product self, dimension "
                  "is > 1 !")
        if vector.cols() > 1:
            print("!!! Exception: Can't compute dot product vector, dimension "
                  "is > 1 !")
        if self.rows() != vector.rows():
            print("!!! Exception: Can't compute dot product, vectors have "
                  "different number of rows !")

        result = 0
        for i in range(0, self.rows()):
            result += self.v[i] * vector.v[i]

        return result

    def length(self):
        """
        Computes the length of a current Matrix (NOTE: dot() assumes its a
        vector, 1 column).
        :return: [float] or [int]
        """
        d = self.dot(self.copy())
        return sqrt(d)

    def norm(self):
        """
        Alias function for computing length of a vector
        :return: [float] or [int]
        """
        return self.length()

    def scalar(self, scalar=1.0, to_self=False):
        """
        Scalar - multiplies all values of a matrix to a scalar number
        :param scalar: [float]
        :param to_self: [Boolean] if this operation should return a new object
        :return: [Matrix] - self object
        """
        if scalar == 0:
            print("!!! Exception: Scalar number can't be '0'!")

        if to_self:
            self.v = [x*scalar for x in self.v]
            result = self
        else:
            matrix = self.copy()
            matrix.v = [x*scalar for x in matrix.v]
            result = matrix

        return result

    def scale(self, scalar=1.0, to_self=False):
        return self.scalar(scalar, to_self)

    def add(self, matrix, to_self=False):
        """
        Add
        :param matrix:
        :param to_self: [Boolean] if this operation should return a new object
        :return: [Matrix] - self object
        """
        matrix = self._type_check(matrix)

        if self.rows() != matrix.rows() or self.cols() != matrix.cols():
            print("!!! Exception: Wrong size matrix passed to add!")

        a_tuple = self.csr2tuple()
        b_tuple = matrix.csr2tuple()
        a_new = []
        b_new = []
        result = []

        for a in a_tuple:
            a_new.append(a)
            for b in b_tuple:
                b_new.append(b)
                if a[0] == b[0] and a[1] == b[1]:
                    result.append((b[0], b[1], a[2] + b[2]))
                    if a in a_new:
                        a_new.remove(a)
                    if b in b_new:
                        b_new.remove(b)

        for a in a_new:
            result.append((a[0], a[1], a[2]))
        for b in b_new:
            result.append((b[0], b[1], b[2]))

        result = sorted(result)
        r, c, v = Matrix.tuple2csr(result)

        if to_self:
            self.r, self.c, self.v = r, c, v
            result = self
        else:
            result = Matrix().set(r, c, v)

        return result

    def subtract(self, matrix, to_self=False):
        """
        Subtract
        :param matrix:
        :param to_self: [Boolean] if this operation should return a new object
        :return: [Matrix] - self object
        """
        matrix = self._type_check(matrix)

        if self.rows() != matrix.rows() or self.cols() != matrix.cols():
            print("!!! Exception: Wrong size matrix passed to subtract!")

        a_tuple = self.csr2tuple()
        b_tuple = matrix.csr2tuple()
        result = []

        for i in range(0, self.rows()):
            for j in range(0, self.cols()):
                a = [x for x in a_tuple if x[0] == i and x[1] == j]
                b = [x for x in b_tuple if x[0] == i and x[1] == j]
                if a and b:
                    a = a[0]
                    b = b[0]
                    result.append((i, j, a[2] - b[2]))
                    a_tuple.remove(a)
                    b_tuple.remove(b)

        for a in a_tuple:
            result.append((a[0], a[1], a[2]))
        for b in b_tuple:
            result.append((b[0], b[1], -b[2]))

        result = sorted(result)
        r, c, v = Matrix.tuple2csr(result)

        if to_self:
            self.r, self.c, self.v = r, c, v
            result = self
        else:
            result = Matrix().set(r, c, v)

        return result

    def sub(self, matrix):
        """
        Alias of function
        :param matrix:
        :return:
        """
        return self.subtract(matrix)

    def multiply(self, matrix, to_self=False):
        """
        Multiply
        :param matrix:
        :param to_self: [Boolean] if this operation should return a new object
        :return: [Matrix] - self object
        """
        matrix = self._type_check(matrix)

        if self.cols() != matrix.rows():
            print("!!! Exception: Wrong size matrix passed to multiply! "
                            "Should be MxN * NxR")

        a_tuple = self.csr2tuple()
        b_tuple = matrix.csr2tuple()
        result = []

        a_rows = {}
        b_cols = {}
        for i in range(0, self.rows()):
            a_rows[i] = {}
            for a in a_tuple:
                if a[0] == i:
                    a_rows[i][a[1]] = a[2]

        for i in range(0, matrix.rows()):
            b_cols[i] = {}
            for b in b_tuple:
                if b[1] == i:
                    b_cols[i][b[0]] = b[2]

        for row in a_rows:
            for col in b_cols:
                sum = 0
                for i in range(0, max(self.rows(), matrix.rows())):
                    if i in a_rows[row] and i in b_cols[col]:
                        a = a_rows[row][i]
                        b = b_cols[col][i]
                        sum += a * b
                        for item in result:
                            if item[0] == row and item[1] == col:
                                result.remove(item)
                        result.append((row, col, sum))

        result = sorted(result)
        r, c, v = Matrix.tuple2csr(result)

        if to_self:
            self.r, self.c, self.v = r, c, v
            result = self
        else:
            result = Matrix().set(r, c, v)

        return result

    def mul(self, matrix):
        """
        Alias of function
        :param matrix:
        :return: [Matrix] - self object
        """
        return self.multiply(matrix)

    def divide(self, matrix):
        """
        Divide
        :param matrix:
        :return: [Matrix] - self object
        """
        print("!!! Exception: Not implemented")
        return self

    def div(self, matrix):
        """
        Alias of function
        :param matrix:
        :return:
        """
        return self.divide(matrix)
