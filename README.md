# Sparse Matrices (in Python)
PSU - MTH343 Linear Algebra. This project is being done by Max Litvinenko in Winter 2016 instead of taking the final in this class. External usage of this project is allowed, but for your own risk, code is likely to contain bugs.

The purpose of Matrix.py:
- Store matrix in a 'Sparse' format
- Provide methods to perform elementary matrix operations(EMO) with this matrix in 'Sparse' format. (This format aims to optimize memory usage, however it decreases the performance by increases the number of computations)
- WARNING: In current version, matrix will ignore 'zero rows' and 'zero columns' when converting a matrix to a sparse matrix

The purpose of Main.py:
- Read the file (Ex: input.dat) where matrices in array format are stored.
- Call methods from Matrix.py to perform EMO
- Store matrices in a file (Ex: output.dat)

Example of input.dat:
  1. [[1,0,0],[0,1,0],[0,0,1]]
  2. [[1,2,3],[4,5,6],[7,8,9]]
  3. [[0,1,2,3], [4,5,6,7], [8,9,10,11], [12,13,14,15]]
  4. [[1,0,2,0], [0,5,0,0], [0,9,10,0], [12,13,0,0]]
  5. [[1,0,2,0,1,0], [0,5,0,0,2,0], [0,9,6,0,10,0], [1,2,1,3,0,0], [0,0,0,0,0,0]]
  6. [[1,2]]
  7. [1]
  8. [[2]]
  9. 3,2,4
  10. [[0,1],[2,3]]

Example of generated output.dat:
  1. [[0, 1, 2], [0, 1, 2], [1.0, 1.0, 1.0]] 	===	 [[1.0, '_', '_'], ['_', 1.0, '_'], ['_', '_', 1.0]]
  2. [[0, 3, 6], [0, 1, 2, 0, 1, 2, 0, 1, 2], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]] 	===	 [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
  3. [[0, 3, 7, 11], [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0]] 	===	 [['_', 1.0, 2.0, 3.0], [4.0, 5.0, 6.0, 7.0], [8.0, 9.0, 10.0, 11.0], [12.0, 13.0, 14.0, 15.0]]
  4. [[0, 2, 3, 5], [0, 2, 1, 1, 2, 0, 1], [1.0, 2.0, 5.0, 9.0, 10.0, 12.0, 13.0]] 	===	 [[1.0, '_', 2.0], ['_', 5.0, '_'], ['_', 9.0, 10.0], [12.0, 13.0, '_']]
  5. [[0, 3, 5, 8], [0, 2, 4, 1, 4, 1, 2, 4, 0, 1, 2, 3], [1.0, 2.0, 1.0, 5.0, 2.0, 9.0, 6.0, 10.0, 1.0, 2.0, 1.0, 3.0]] 	===	 [[1.0, '_', 2.0, '_', 1.0], ['_', 5.0, '_', '_', 2.0], ['_', 9.0, 6.0, '_', 10.0], [1.0, 2.0, 1.0, 3.0, '_']]
  6. [[0], [0, 1], [1.0, 2.0]] 	===	 [[1.0, 2.0]]
  7. [[0], [0], [1.0]] 	===	 [[1.0]]
  8. [[0], [0], [2.0]] 	===	 [[2.0]]
  9. [[0], [0, 1, 2], [3.0, 2.0, 4.0]] 	===	 [[3.0, 2.0, 4.0]]
  10. [[0, 1], [1, 0, 1], [1.0, 2.0, 3.0]] 	===	 [['_', 1.0], [2.0, 3.0]]
