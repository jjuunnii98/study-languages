"""
Day 23: NumPy Indexing & Slicing

This file covers how to access and manipulate NumPy arrays
using indexing and slicing techniques.

NumPy indexing is significantly more powerful than Python lists
and is a core skill for data analysis and machine learning.

이 파일은 NumPy 배열의 인덱싱과 슬라이싱을 다룬다.
이는 데이터 분석과 머신러닝에서 가장 많이 사용되는 핵심 기능 중 하나다.
"""

import numpy as np

# ----------------------------------------
# 1. Basic Indexing (1D Array)
# ----------------------------------------

arr = np.array([10, 20, 30, 40, 50])

print(arr[0])     # 첫 번째 요소
print(arr[-1])    # 마지막 요소

# Python 리스트와 동일하지만, NumPy는 수치 연산에 최적화됨


# ----------------------------------------
# 2. Slicing (1D Array)
# ----------------------------------------

print(arr[1:4])    # index 1부터 3까지
print(arr[:3])     # 처음부터 index 2까지
print(arr[::2])    # 간격(step) 지정

# 슬라이싱은 "view"를 반환함 (복사 아님)


# ----------------------------------------
# 3. Indexing & Slicing (2D Array)
# ----------------------------------------

matrix = np.array([
    [1,  2,  3],
    [4,  5,  6],
    [7,  8,  9]
])

print(matrix[0, 0])      # 첫 행, 첫 열
print(matrix[1, :])      # 두 번째 행 전체
print(matrix[:, 1])      # 두 번째 열 전체
print(matrix[:2, :2])    # 좌상단 2x2 영역


# ----------------------------------------
# 4. Boolean Indexing
# ----------------------------------------

data = np.array([10, 25, 30, 18, 5])

print(data[data > 20])   # 조건을 만족하는 값만 선택
print(data[data % 2 == 0])

# Boolean indexing은 데이터 필터링의 핵심 기법


# ----------------------------------------
# 5. Fancy Indexing
# ----------------------------------------

indices = [0, 2, 4]
print(arr[indices])

# 특정 위치의 값들을 한 번에 선택 가능


# ----------------------------------------
# 6. View vs Copy
# ----------------------------------------

slice_view = arr[1:4]
slice_view[0] = 999

print(arr)  # 원본 배열도 함께 변경됨

# NumPy 슬라이싱은 기본적으로 view를 반환함
# 원본 보호가 필요하면 copy() 사용


safe_copy = arr[1:4].copy()
safe_copy[0] = -1

print(arr)
print(safe_copy)


# ----------------------------------------
# 7. Practical Example (Data Filtering)
# ----------------------------------------

scores = np.array([72, 85, 90, 60, 77, 95])

passed = scores[scores >= 80]
print(passed)

# 실전 데이터 분석에서 가장 자주 사용되는 패턴