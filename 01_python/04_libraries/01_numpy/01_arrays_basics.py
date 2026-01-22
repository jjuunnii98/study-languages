"""
Day 22: NumPy Arrays — Basics

This file introduces the fundamentals of NumPy arrays,
which are the core data structure for numerical computing
in Python-based data analysis and machine learning.

NumPy 배열은 이후 pandas, scikit-learn, deep learning 라이브러리의
기반이 되는 핵심 자료구조다.
"""

import numpy as np

# --------------------------------------------------
# 1. Why NumPy?
# --------------------------------------------------
"""
Python list는 범용 자료구조이지만,
수치 계산(numerical computation)에는 비효율적이다.

NumPy 배열은:
- 고정된 자료형
- 연속된 메모리 구조
- 벡터화 연산 지원
으로 빠르고 안정적인 수치 계산이 가능하다.
"""

# --------------------------------------------------
# 2. Creating NumPy Arrays
# --------------------------------------------------

# (1) Python list -> NumPy array
data = [1, 2, 3, 4, 5]
arr = np.array(data)

print("array:", arr)
print("type:", type(arr))
print("dtype:", arr.dtype)

# (2) 다차원 배열 생성
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

print("matrix:\n", matrix)
print("shape:", matrix.shape)  # (rows, columns)
print("ndim:", matrix.ndim)    # number of dimensions

# --------------------------------------------------
# 3. Common Array Constructors
# --------------------------------------------------

zeros = np.zeros((3, 4))
ones = np.ones((2, 3))
identity = np.eye(3)
range_arr = np.arange(0, 10, 2)
linspace_arr = np.linspace(0, 1, 5)

print("zeros:\n", zeros)
print("ones:\n", ones)
print("identity:\n", identity)
print("arange:", range_arr)
print("linspace:", linspace_arr)

# --------------------------------------------------
# 4. Indexing and Slicing
# --------------------------------------------------

arr = np.array([10, 20, 30, 40, 50])

print("first element:", arr[0])
print("last element:", arr[-1])
print("slice:", arr[1:4])

matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

print("matrix[0, 1]:", matrix[0, 1])  # row 0, column 1
print("first row:", matrix[0])
print("second column:", matrix[:, 1])

# --------------------------------------------------
# 5. Vectorized Operations
# --------------------------------------------------
"""
NumPy의 가장 중요한 특징:
- 반복문 없이 배열 단위 연산 가능 (vectorization)
"""

arr = np.array([1, 2, 3, 4])

print("arr + 10:", arr + 10)
print("arr * 2:", arr * 2)
print("arr squared:", arr ** 2)

# 배열 간 연산
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("a + b:", a + b)
print("a * b:", a * b)

# --------------------------------------------------
# 6. Boolean Indexing
# --------------------------------------------------

arr = np.array([10, 25, 30, 5, 40])

mask = arr >= 25
print("mask:", mask)
print("filtered values:", arr[mask])

# --------------------------------------------------
# 7. Basic Aggregations
# --------------------------------------------------

arr = np.array([1, 2, 3, 4, 5])

print("sum:", arr.sum())
print("mean:", arr.mean())
print("min:", arr.min())
print("max:", arr.max())
print("std:", arr.std())

# --------------------------------------------------
# 8. Summary
# --------------------------------------------------
"""
- NumPy array는 고성능 수치 계산을 위한 핵심 구조
- shape, dtype, ndim은 반드시 익숙해져야 하는 속성
- 벡터화 연산은 반복문보다 빠르고 읽기 쉽다
- 이후 pandas, ML 모델 입력 데이터의 기반이 된다
"""