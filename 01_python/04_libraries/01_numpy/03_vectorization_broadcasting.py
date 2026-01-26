"""
Day 24: NumPy Vectorization & Broadcasting

This file explains two core performance concepts in NumPy:
1) Vectorization: performing computations on whole arrays without Python loops
2) Broadcasting: automatic expansion of shapes to make element-wise operations possible

NumPy에서 "빠른 코드"는 for-loop를 줄이고,
배열 연산(벡터화)과 broadcasting 규칙을 활용하는 것에서 시작된다.

이 파일의 목표:
- 벡터화가 왜 빠른지 개념적으로 이해한다.
- broadcasting 규칙을 예제로 체득한다.
- 실무에서 자주 사용하는 패턴(표준화, 거리 계산, 행/열 연산)을 다룬다.
"""

import numpy as np


# ------------------------------------------------------------
# 1) Vectorization vs Python loop
# ------------------------------------------------------------
"""
벡터화(vectorization)는 "파이썬 레벨 반복"을 줄이는 전략이다.
NumPy는 내부적으로 C로 최적화된 루프를 사용하므로,
배열 연산은 Python for-loop보다 보통 훨씬 빠르다.
"""

x = np.arange(1, 6)  # [1, 2, 3, 4, 5]
print("x:", x)

# 벡터화 연산: 전체 배열에 대해 한 번에 계산
y_vec = x ** 2 + 2 * x + 1
print("y_vec:", y_vec)

# (비교용) for-loop 방식 (학습 목적)
y_loop = []
for v in x:
    y_loop.append(v ** 2 + 2 * v + 1)
y_loop = np.array(y_loop)

print("y_loop:", y_loop)
print("same result:", np.array_equal(y_vec, y_loop))


# ------------------------------------------------------------
# 2) Broadcasting 기본 규칙
# ------------------------------------------------------------
"""
Broadcasting은 shape가 다른 배열끼리도 원소별 연산이 가능하도록
NumPy가 자동으로 차원을 확장(expand)하는 규칙이다.

핵심 규칙(오른쪽부터 비교):
- 두 차원이 같거나
- 둘 중 하나가 1이면
=> 호환 가능

예) (3, 1) 과 (1, 4) => (3, 4)로 확장 가능
"""

a = np.arange(3).reshape(3, 1)   # shape (3, 1)
b = np.arange(4).reshape(1, 4)   # shape (1, 4)

print("\na shape:", a.shape)
print("b shape:", b.shape)

c = a + b  # broadcasting => (3,4)
print("c shape:", c.shape)
print("c:\n", c)


# ------------------------------------------------------------
# 3) Row/Column-wise operations (실무 패턴)
# ------------------------------------------------------------
"""
실무에서 가장 많이 쓰는 형태:
- (n, d) 데이터 행렬 X에 대해
- 각 열(column)별로 평균/표준편차를 적용하거나
- 특정 벡터를 모든 행에 더하거나 빼는 작업

=> broadcasting으로 간단히 해결 가능
"""

X = np.array([
    [1.0,  10.0, 100.0],
    [2.0,  20.0, 200.0],
    [3.0,  30.0, 300.0],
])
print("\nX:\n", X)
print("X shape:", X.shape)

# 열 평균 (shape: (3,))
col_mean = X.mean(axis=0)
print("col_mean:", col_mean, "shape:", col_mean.shape)

# broadcasting: (3,3) - (3,)  => (3,3)
X_centered = X - col_mean
print("X_centered:\n", X_centered)

# 열 표준편차
col_std = X.std(axis=0, ddof=0)
X_standardized = (X - col_mean) / col_std
print("col_std:", col_std)
print("X_standardized:\n", X_standardized)


# ------------------------------------------------------------
# 4) Broadcasting으로 거리 계산 (실무/ML 핵심 패턴)
# ------------------------------------------------------------
"""
(예) 1차원에서 모든 점 간 거리 |xi - xj| 계산
- x shape: (n,)
- x[:, None] shape: (n,1)
- x[None, :] shape: (1,n)
=> 결과 shape: (n,n)

이 패턴은 KNN, 클러스터링, 커널 계산 등에서 자주 등장한다.
"""

x = np.array([0.0, 1.0, 3.0, 6.0])  # n=4
dist_matrix = np.abs(x[:, None] - x[None, :])
print("\nx:", x)
print("dist_matrix:\n", dist_matrix)


# ------------------------------------------------------------
# 5) Broadcasting이 실패하는 경우 (에러 이해)
# ------------------------------------------------------------
"""
shape가 호환되지 않으면 ValueError가 발생한다.
이 때는:
- reshape, expand_dims, 또는 차원 정렬을 통해 shape를 맞춰야 한다.

예) (3,2) 와 (3,)은 호환될 수도/안될 수도 있다.
(3,)은 (1,3)처럼 해석될 수 있어, 열 방향/행 방향에 따라 결과가 달라진다.
"""

M = np.ones((3, 2))
v = np.array([1, 2, 3])

print("\nM shape:", M.shape)
print("v shape:", v.shape)

try:
    _ = M + v  # (3,2) + (3,) => 호환 불가 (오른쪽부터 비교: 2 vs 3)
except ValueError as e:
    print("Broadcasting error:", e)

# 해결: v를 (3,1)로 변형하면 (3,2)와 호환 가능
v_col = v.reshape(3, 1)  # shape (3,1)
print("v_col shape:", v_col.shape)
print("M + v_col:\n", M + v_col)


# ------------------------------------------------------------
# 6) 성능/가독성 관점 실무 가이드
# ------------------------------------------------------------
"""
실무에서의 결론:
- 가능하면 for-loop 대신 벡터화
- shape를 명시적으로 관리 (특히 (n,) vs (n,1))
- broadcasting을 "의도적으로" 사용해야 버그가 줄어든다

Tip:
- x[:, None] 또는 np.newaxis로 차원 확장 습관화
- 연산 전 print(x.shape)로 확인하는 습관도 매우 도움이 된다
"""

# Day 24 요약
"""
- 벡터화: Python loop 없이 배열 연산으로 계산 (빠르고 간결)
- broadcasting: shape가 달라도 규칙에 따라 자동 확장되어 연산 가능
- (n,) vs (n,1) 차이를 명확히 이해하면 실무 버그가 크게 줄어든다
"""