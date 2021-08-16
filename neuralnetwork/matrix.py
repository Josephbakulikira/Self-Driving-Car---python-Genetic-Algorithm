import random

# ---- I used numpy matrices instead of this to improve the performance

class Matrix:
    def __init__(self, rows, cols, label=""):
        self.rows = rows
        self.cols = cols
        self.matrix = [[0 for i in range(cols)] for j in range(rows)]
        self.label = label
        #or you can simply use numpy
        """
        # import numpy as np
        # self.matrix = np.zeros((rows,cols))
        """

    def multiply(self, value):
        if type(value) is Matrix:
            #check if the we can multiply the two matrix
            if self.cols == value.rows:
                result = Matrix(self.rows, value.cols)
                for x in range(result.rows):
                    for y in range(result.cols):
                        sum = 0
                        for z in range(self.cols):
                            sum += self.matrix[x][z] * value.matrix[z][y]
                        result.matrix[x][y] = sum
                return result

            else:
                print("the number of column of the first matrix must be equal to the number of rows in the second matrix, error!")
        else:
            for x in range(self.rows):
                for y in range(self.cols):
                    self.matrix[x][y] *= value


    def transpose(m):
        result = Matrix(m.cols, m.rows)
        for x in range(m.rows):
            for y in range(m.cols):
                result.matrix[y][x] = m.matrix[x][y]
        return result

    def add(self, value):
        if type(value) is Matrix:
            for x in range(self.rows):
                for y in range(self.cols):
                    self.matrix[x][y] += value.matrix[x][y]
        else:
            for x in range(self.rows):
                for y in range(self.cols):
                    self.matrix[x][y] += value

    def subtract(self, value):
        if type(value) is Matrix:
            for x in range(self.rows):
                for y in range(self.cols):
                    self.matrix[x][y] -= value.matrix[x][y]
        else:
            for x in range(self.rows):
                for y in range(self.cols):
                    self.matrix[x][y] -= value

    def HadamartProduct(self, value):
        for x in range(self.rows):
            for y in range(self.cols):
                self.matrix[x][y] *= value.matrix[x][y]

    def __add__(self, _matrix):
        mat = Matrix(self.rows, self.cols)
        for x in range(self.rows):
            for y in range(self.cols):
                mat.matrix[x][y] = self.matrix[x][y] + _matrix.matrix[x][y]
        return mat

    def __sub__(self, _matrix):
        mat = Matrix(self.rows, self.cols)
        for x in range(self.rows):
            for y in range(self.cols):
                mat.matrix[x][y] = self.matrix[x][y] - _matrix.matrix[x][y]
        return mat

    def randomize(self):
        for x in range(self.rows):
            for y in range(self.cols):
                self.matrix[x][y] = random.uniform(-1, 1)

    def map(self, fn):
        #apply a function for every element in the matrix
        for x in range(self.rows):
            for y in range(self.cols):
                self.matrix[x][y] = fn(self.matrix[x][y])

    def staticMap(matrix, fn):
        result = Matrix(matrix.rows, matrix.cols)
        for x in range(matrix.rows):
            for y in range(matrix.cols):
                result.matrix[x][y] = fn(matrix.matrix[x][y])

        return result

    def Debug(self):
        if self.rows == 1:
            if self.label != "":
                print("{0} : {1}".format(self.label, self.toArray()))
                # print(self.label + " : " + self.toArray())
            else:
                print(self.toArray())
        else:
            if self.label != "":
                print("{0} : {1}".format(self.label, self.matrix))
            else:
                print(self.matrix)

    def fromArray(arr):
        rows = len(arr)
        cols = 1
        current = Matrix(rows, cols)
        for i in range(rows):
            current.matrix[i][0] = arr[i]
        return current

    def toArray(self):
        arr = []
        for x in range(self.rows):
            for y in range(self.cols):
                arr.append(self.matrix[x][y])

        return arr

    def matrix_multiplication(a, b):
        columns_a = len(a.matrix[0])
        rows_a = len(a.matrix)
        columns_b = len(b.matrix[0])
        rows_b = len(b.matrix)

        result_matrix = Matrix(rows_a, columns_b)
        if columns_a == rows_b:
            for x in range(rows_a):
                for y in range(columns_b):
                    sum = 0
                    for k in range(columns_a):
                        sum += a.matrix[x][k] * b.matrix[k][y]
                    result_matrix.matrix[x][y] = sum
            return result_matrix

        else:
            print("columns of the first matrix must be equal to the rows of the second matrix")
            return None

    def __repr__(self):
        return f'matrix ->rows: {self.rows}, cols: {self.cols}, content=>{self.matrix}'
