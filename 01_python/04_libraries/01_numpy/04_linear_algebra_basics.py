"""
Day 25: NumPy Linear Algebra Basics

This module introduces fundamental linear algebra operations using NumPy.
Linear algebra is the mathematical backbone of machine learning,
data analysis, and scientific computing.

본 파일은 NumPy를 활용한 선형대수 기초 연산을 다룬다.
선형대수는 머신러닝, 데이터 분석, 과학 계산의 핵심 수학 도구이다.
"""

import numpy as np

# --------------------------------------------------
# 1. Vectors and Matrices
# --------------------------------------------------
# 벡터(Vector): 1차원 배열
vector = np.array([1, 2, 3])

# 행렬(Matrix): 2차원 배열
matrix = np.array([
    [1, 2],
    [3, 4]
])

print("Vector:")
print(vector)
print("\nMatrix:")
print(matrix)


# --------------------------------------------------
# 2. Matrix Shape and Transpose
# --------------------------------------------------
# shape: 행렬의 차원 확인
print("\nMatrix shape:", matrix.shape)

# transpose (전치 행렬)
matrix_T = matrix.T
print("\nTransposed matrix:")
print(matrix_T)


# --------------------------------------------------
# 3. Matrix Addition and Scalar Multiplication
# --------------------------------------------------
# 행렬 덧셈 (같은 차원)
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print("\nA + B:")
print(A + B)

# 스칼라 곱
print("\n2 * A:")
print(2 * A)


# --------------------------------------------------
# 4. Matrix Multiplication (Dot Product)
# --------------------------------------------------
# 행렬 곱: 선형대수에서 가장 중요한 연산
# (m x n) · (n x k) → (m x k)

C = np.array([[1, 2], [3, 4]])
D = np.array([[2, 0], [1, 2]])

# 방법 1: np.dot
print("\nMatrix multiplication (np.dot):")
print(np.dot(C, D))

# 방법 2: @ 연산자 (권장)
print("\nMatrix multiplication (@ operator):")
print(C @ D)


# --------------------------------------------------
# 5. Identity Matrix and Inverse Matrix
# --------------------------------------------------
# 단위 행렬 (Identity matrix)
I = np.eye(2)
print("\nIdentity matrix:")
print(I)

# 역행렬 (Inverse)
E = np.array([[4, 7], [2, 6]])
E_inv = np.linalg.inv(E)

print("\nMatrix E:")
print(E)
print("\nInverse of E:")
print(E_inv)

# E · E_inv ≈ I 인지 확인
print("\nE @ inverse(E):")
print(E @ E_inv)


# --------------------------------------------------
# 6. Determinant
# --------------------------------------------------
# 행렬식 (determinant)
det_E = np.linalg.det(E)
print("\nDeterminant of E:", det_E)


# --------------------------------------------------
# 7. Solving Linear Equations
# --------------------------------------------------
# Ax = b 형태의 선형 방정식 풀기
# 예: 2x + y = 5, x + 3y = 6

A = np.array([[2, 1],
              [1, 3]])
b = np.array([5, 6])

x = np.linalg.solve(A, b)
print("\nSolution of Ax = b:")
print(x)


# --------------------------------------------------
# 8. Why This Matters (Conceptual)
# --------------------------------------------------
"""
선형대수는 다음과 같은 영역의 핵심이다:
- 선형 회귀 (Normal Equation)
- 신경망의 가중치 연산
- 차원 축소 (PCA, SVD)
- 최적화 문제

NumPy의 선형대수 연산에 익숙해지면
머신러닝 라이브러리 내부 동작을 더 깊이 이해할 수 있다.
"""