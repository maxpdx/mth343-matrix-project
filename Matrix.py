class Matrix:

    def __init__(self, matrix):
        if isinstance(matrix, str):
            raise Exception("You passed a string into a matrix!")

        self.matrix = []
        self.r = []
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

    def to_sparse(self):
        if not self.isSparse:
            for n, row in enumerate(self.matrix):
                for col, val in enumerate(row):
                    self.r.append(n)
                    self.c.append(col)
                    self.v.append(val)
            self.isSparse = True
        return self.isSparse

    def transpose(self, matrix):
        return

    def add(self, matrix):
        return

    def subtract(self, matrix):
        return
