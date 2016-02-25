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

    def __init__(self, matrix):
        """
        Constructor: initializes variables, checks the type, converts to
        sparse matrix iff the input matrix is not a sparse matrix.
        :param matrix: [list] - array of arrays of floats/ints
        :return:
        """
        # copy matrix variables
        if isinstance(matrix, Matrix):
            self.r = matrix.r
            self.c = matrix.c
            self.v = matrix.v
            self.isCSR = matrix.isCSR
            # FOR TESTING ONLY
            self.init_matrix = matrix.init_matrix
            self.r_ = matrix.r_
        # convert to Matrix
        else:
            if isinstance(matrix, str):
                matrix = self.str2list(matrix)

            self.clean_up()
            self.init_matrix = matrix
            if matrix and not self.isCSR:
                self.list2csr()

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
            raise Exception("Nothing to convert to sparse matrix, "
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

    def get_matrix(self):
        """
        FOR TESTING ONLY
        Get Matrix: gets the initially entered matrix w/o any computations
        :return: [list] - array of arrays of floats/ints
        """
        return self.init_matrix

    def display(self, text="", returns=False):
        """
        Displays the matrix in whatever format it is
        :param text: [string] any text that you want to display before matrix
        :param returns:
        :return:
        """
        if text:
            print(text)

        if self.is_csr():
            matrix = self.display_sparse(returns)
        else:
            matrix = self.display_matrix(returns)

        print()

        return matrix

    def display_size(self,string=""):
        """
        Prints the size of a matrix
        :param string:
        :return:
        """
        print("%s %sx%s" % (string, self.rows(), self.cols()))

    def display_matrix(self, returns=True):
        """
        Displays the matrix of array of arrays
        :param returns:
        :return:
        """
        if returns:
            return self.get_matrix()
        else:
            for row in self.get_matrix():
                print(row)

    def display_sparse(self, returns=True):
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
                row.append("_")
            rows.append(row)

        prev_i = i = 0
        for x, val in enumerate(self.v):
            if x == self.r[prev_i]:
                i = prev_i
                if len(self.r) > prev_i+1:
                    prev_i += 1

            j = self.c[x]
            rows[i][j] = val

        if returns:
            return rows
        else:
            for row in rows:
                print(row)

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
            raise Exception("Can't convert to a Matrix!")

        return matrix

    def csr2tuple(self):
        current_row = 0
        triples_list = []
        for j, v in enumerate(self.v):
            if j == self.r[current_row + 1]:
                current_row += 1
            triples_list.append((current_row, self.c[j], v))
        return triples_list

    def tuple2csr(self, list):
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

    def transpose(self):
        """
        Takes transpose of a matrix
        :return: [Matrix] - self object
        """
        triples = []
        for triple in self.csr2tuple():
            # Making transpose: (x, y, v) => (y, x, v)
            triples.append((triple[1], triple[0], triple[2]))

        # Need to sort for 1st element in tuple(x) so we will be able to go
        # back to sparse matrix by re-computing self.r (rows list)
        triples = sorted(triples)

        self.r, self.c, self.v = self.tuple2csr(triples)
        return self

    def scalar(self, scalar=1.0):
        """
        Scalar - multiplies all values of a matrix to a scalar number
        :param scalar: [float]
        :return: [Matrix] - self object
        """
        if scalar == 0:
            raise Exception("Scalar number can't be '0'!")

        self.v = map(lambda x: x * scalar, self.v)
        return self

    def add(self, matrix):
        """
        Add
        :param matrix:
        :return: [Matrix] - self object
        """
        matrix = self._type_check(matrix)

        if self.rows() != matrix.rows() or self.cols() != matrix.cols():
            raise Exception("Wrong size matrix passed to add!")

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
                    a_new.remove(a)
                    b_new.remove(b)

        for a in a_new:
            result.append((a[0], a[1], a[2]))
        for b in b_new:
            result.append((b[0], b[1], b[2]))

        result = sorted(result)
        self.r, self.c, self.v = self.tuple2csr(result)

        return self

    def subtract(self, matrix):
        """
        Subtract
        :param matrix:
        :return: [Matrix] - self object
        """
        matrix = self._type_check(matrix)

        if self.rows() != matrix.rows() or self.cols() != matrix.cols():
            raise Exception("Wrong size matrix passed to subtract!")

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
                    result.append((b[0], b[1], a[2] - b[2]))
                    a_new.remove(a)
                    b_new.remove(b)

        for a in a_new:
            result.append((a[0], a[1], -a[2]))
        for b in b_new:
            result.append((b[0], b[1], -b[2]))

        result = sorted(result)
        self.r, self.c, self.v = self.tuple2csr(result)

        return self

    def sub(self, matrix):
        """
        Alias of function
        :param matrix:
        :return:
        """
        return self.subtract(matrix)

    def multiply(self, matrix):
        """
        Multiply
        :param matrix:
        :return: [Matrix] - self object
        """
        matrix = self._type_check(matrix)

        if self.cols() != matrix.rows():
            raise Exception("Wrong size matrix passed to multiply! "
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
                        result.append((row, col, sum))

        result = sorted(result)
        self.r, self.c, self.v = self.tuple2csr(result)

        return self

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
        raise Exception("Not implemented")
        return self

    def div(self, matrix):
        """
        Alias of function
        :param matrix:
        :return:
        """
        return self.divide(matrix)

