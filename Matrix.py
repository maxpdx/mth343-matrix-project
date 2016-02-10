class Matrix:

    def __init__(self, matrix):
        if isinstance(matrix, str):
            raise Exception("You passed a string into a matrix!")

        self.matrix = []
        self.n_rows = []
        self.n_cols = []
        self.r = []
        self.r_ = []
        self.c = []
        self.v = []
        self.isSparse = False

        self.matrix = matrix
        if not self.isSparse:
            self.to_sparse()

    def get_matrix(self):
        return self.matrix

    def get_sparse(self):
        return [self.r, self.c, self.v]

    def is_sparse(self):
        return self.isSparse

    def to_sparse(self):
        if not self.is_sparse():
            self.n_cols = len(self.matrix[0])
            self.n_rows = len(self.matrix)
            prev_r = -1
            for n, row in enumerate(self.matrix):
                for col, val in enumerate(row):
                    if val != 0:
                        if prev_r != n:
                            prev_r = n
                            self.r.append(len(self.v))
                        self.r_.append(n)
                        self.c.append(col)
                        self.v.append(val)
            self.isSparse = True
        return self.is_sparse()

    def rows(self):
        return self.n_rows

    def cols(self):
        return self.n_cols

    def from_sparse(self):
        if self.is_sparse():

            self.isSparse = False
        return self.is_sparse()

    def display_size(self):
        print "\t%sx%s" % (self.rows(), self.cols())

    def display_matrix(self,display_size=True):
        if display_size:
            self.display_size()

        for row in self.matrix:
            print row

    def display_sparse(self,display_size=True):
        if display_size:
            self.display_size()

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

        for row in rows:
            print row


    def transpose(self, matrix):
        return

    def add(self, matrix):
        return

    def subtract(self, matrix):
        return
