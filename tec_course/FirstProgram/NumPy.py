import numpy as np

array1 = np.array([10, 20, 30, 40])
array2 = np.array([1, 2, 3, 4])

sum_result = array1 + array2
print("Sum: ", sum_result)

multiplication = array1 * array2
print("Multiplication: ", multiplication)

division = array1 / 10
print("Division: ", division)

square_root = np.sqrt(array1)
print("Square root: ", array1)

array2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])

value_position = array2d[1, 2]
print("Value at position [1, 2]: ", value_position)

print("Pseudo Inverse: ", np.linalg.pinv(array2d))
