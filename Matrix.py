class Matrix:
    """
    Matrix library that will store matrix in a 'Sparse' format and provides
    methods to perform elementary matrix operations with this matrix in this
    format. (This format aims to optimise memory usage, but increases
    number of computations)

    WARNING: In current solution, matrix will ignore 'zero rows' and 'zero
    columns' in a matrix.
    """

    # Class variables
    r = []      # row pointer (points to an index of changing row value)
    c = []      # stores the column index of the value(self.v)
    v = []      # stores a list of values
    isSparse = False    # marks the current type of storage is sparse of not

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
        if isinstance(matrix, str):
            raise Exception("You passed a string into a matrix!")

        self.clean_up()
        self.init_matrix = matrix
        if matrix and not self.isSparse:
            self.to_sparse()

    def clean_up(self):
        """
        Clean Up: initializes lists of sparse storage to empty lists
        :return: self [Matrix]
        """
        self.r = []
        self.c = []
        self.v = []
        self.isSparse = False

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

    def is_sparse(self):
        """
        Is Sparse: checks if the current instance of a Matrix class is
        already stored in a sparse format
        :return: [Boolean] - is in sparse format? True or False
        """
        return self.isSparse

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

    def to_sparse(self):
        """
        To Sparse: converts the array of arrays of ints/floats to sparse
        matrix and stores in needed data structure (list [r, c, v]). NOTE:
        make sure self.init_matrix is set before calling this method.
        :return: [Matrix] - self object
        """
        if not self.init_matrix:
            raise Exception("Nothing to convert to sparse matrix, "
                            "self.init_matrix = []")

        if not self.is_sparse():
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
            self.isSparse = True
        return self

    def to_array(self):
        """
        To Array: converts current sparse matrix to an array of arrays of
        ints/floats
        :return: [Matrix] - self object
        """
        if self.is_sparse():
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

    def get_matrix(self):
        """
        FOR TESTING ONLY
        Get Matrix: gets the initially entered matrix w/o any computations
        :return: [list] - array of arrays of floats/ints
        """
        return self.init_matrix

    def display(self, returns=False):
        """
        Displays the matrix in whatever format it is
        :param returns:
        :return:
        """
        if self.is_sparse():
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

    def _sp2triples(self):
        current_row = 0
        triples_list = []
        for j, v in enumerate(self.v):
            if j == self.r[current_row + 1]:
                current_row += 1
            triples_list.append((current_row, self.c[j], v))
        return triples_list

    def _triples2sp(self, list):
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
        for triple in self._sp2triples():
            # Making transpose: (x, y, v) => (y, x, v)
            triples.append((triple[1], triple[0], triple[2]))

        # Need to sort for 1st element in tuple(x) so we will be able to go
        # back to sparse matrix by re-computing self.r (rows list)
        triples = sorted(triples)

        self.r, self.c, self.v = self._triples2sp(triples)
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

    def convert(self, matrix):
        if isinstance(matrix, str):
            raise Exception("You passed a string instead of a matrix!")
        elif isinstance(matrix, list):
            matrix = Matrix(matrix)

        if not isinstance(matrix, Matrix):
            raise Exception("Can't convert to a Matrix!")

        return matrix

    def add(self, matrix):
        """
        Add
        :param matrix:
        :return: [Matrix] - self object
        """
        matrix = self.convert(matrix)

        if self.rows() != matrix.rows() or self.cols() != matrix.cols():
            raise Exception("Wrong size matrix passed to add!")

        result = []
        a_triple = self._sp2triples()
        b_triple = matrix._sp2triples()

        for triple in a_triple:
            for v in b_triple:
                if v[0] == triple[0] and v[1] == triple[1]:
                    result.append((v[0], v[1], triple[2] + v[2]))
                    b_triple.remove((v[0], v[1], v[2]))

        result += b_triple
        result = sorted(result)
        self.r, self.c, self.v = self._triples2sp(result)

        return self

    def subtract(self, matrix):
        """
        Subtract
        :param matrix:
        :return: [Matrix] - self object
        """
        raise Exception("Not implemented")
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
        raise Exception("Not implemented")
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

