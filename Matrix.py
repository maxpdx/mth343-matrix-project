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


    # Constructor: initializes variables, checks the type, converts to
    # sparse matrix iff the input matrix is not a sparse matrix.
    # Inputs:
    #   matrix [list] - array of arrays of floats/ints
    def __init__(self, matrix):
        if isinstance(matrix, str):
            raise Exception("You passed a string into a matrix!")

        self.clean_up()
        self.init_matrix = matrix
        if matrix and not self.isSparse:
            self.to_sparse()

    # Clean Up: initializes lists of sparse storage to empty lists
    # Returns:
    #   self [Matrix] - in order to easily invoke next method
    def clean_up(self):
        self.r = []
        self.c = []
        self.v = []
        self.isSparse = False

        self.r_ = []    # FOR TESTING ONLY
        return self

    # Get Sparse:
    # Returns: [list] of following lists:
    #   self.r [list] - row pointer (points to an index of changing row value)
    #   self.c [list] - column indexes of the values(self.v)
    #   self.v [list] - list of plain matrix values
    def get_sparse(self):
        return [self.r, self.c, self.v]

    # Is Sparse: checks if the current instance of a Matrix class is already
    #  stored in a sparse format
    # Returns:
    #   self.isSparse [Boolean] - is in sparse format? True or False
    def is_sparse(self):
        return self.isSparse

    # Number of Rows: computes the number of rows in current matrix.
    # Returns:
    #   [Int] - number of rows
    def rows(self):
        return len(self.r)

    # Number of Columns: computes the number of cols in current matrix.
    # Returns:
    #   [Int] - number of cols
    def cols(self):
        return max(self.c)+1

    # To Sparse: converts the array of arrays of ints/floats to sparse
    # matrix and stores in needed data structure (list [r, c, v]). NOTE: make
    # sure self.init_matrix is set before calling this method.
    # Returns:
    #   self [Matrix] - in order to easily invoke next method
    def to_sparse(self):
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
            self.isSparse = True
            # self.init_matrix = []     # FOR TESTING ONLY
        return self

    # To Array: converts current sparse matrix to an array of arrays of
    # ints/floats
    # Returns:
    #   self [Matrix] - in order to easily invoke next method
    def to_array(self):
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

    # FOR TESTING ONLY
    # Get Matrix: gets the initially entered matrix w/o any computations
    # Returns:
    #   self.init_matrix [list] - array of arrays of floats/ints
    def get_matrix(self):
        return self.init_matrix

    # Displays the matrix in whatever format it is
    def display(self,returns=False):
        if self.is_sparse():
            return self.display_sparse(returns)
        else:
            return self.display_matrix(returns)

    # Prints the size of a matrix
    def display_size(self,string=""):
        print "%s %sx%s" % (string, self.rows(), self.cols())

    # displays the matrix of array of arrays
    def display_matrix(self,returns=True):
        if returns:
            return self.get_matrix()
        else:
            for row in self.get_matrix():
                print row

    # display the matrix in a sparse format (replacing 0s with '_')
    # NOTE: comutation happens from a sparse matrix directly.
    def display_sparse(self,returns=True):
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
                print row

    # Transpose:
    # Returns:
    #   self [Matrix] - in order to easily invoke next method
    def transpose(self):
        return self

    # Add:
    # Returns:
    #   self [Matrix] - in order to easily invoke next method
    def add(self, matrix):
        return self

    # Subtract
    # Returns:
    #   self [Matrix] - in order to easily invoke next method
    def subtract(self, matrix):
        return self
    def sub(self, matrix):  # Alias of function
        return self.subtract(matrix)

    # Multiply
    # Returns:
    #   self [Matrix] - in order to easily invoke next method
    def multiply(self, matrix):
        return self
    def mul(self,matrix):  # Alias of function
        return self.multiply(matrix)

    # Divide
    # Returns:
    #   self [Matrix] - in order to easily invoke next method
    def divide(self, matrix):
        return self
    def div(self,matrix):  # Alias of function
        return self.divide(matrix)

