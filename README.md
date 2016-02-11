# Sparse Matrices (in Python)
PSU - MTH343 Linear Algebra. This project is being done by Max Litvinenko in Winter 2016 instead of taking the final in this class.

The purpose of Matrix.py:
- Store matrix in a 'Sparse' format
- Provide methods to perform elementary matrix operations(EMO) with this matrix in 'Sparse' format. (This format aims to optimize memory usage, however it decreases the performance by increases the number of computations)
- WARNING: In current version, matrix will ignore 'zero rows' and 'zero columns' in a matrix.

The purpose of Main.py:
- Read the file (Ex: input.dat) where matrices in array format are stored.
- Call methods from Matrix.py to perform EMO
- Store matrices in a file (Ex: output.dat)
