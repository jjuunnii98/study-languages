# ============================================================
# Day 6 — R Data Structures: Matrices
# File: 06_r/02_data_structures/02_matrices.R
#
# 목표
# - R의 matrix 자료구조를 이해한다.
# - matrix 생성, 인덱싱, 행/열 연산 방법을 익힌다.
# - element-wise 연산과 matrix multiplication 차이를 이해한다.
# - apply()를 활용한 행/열 단위 계산을 실습한다.
#
# 한국어 설명
# matrix는 같은 자료형의 값들을 2차원 형태로 저장하는 데이터 구조다.
# 즉, vector가 1차원이라면 matrix는 2차원 구조라고 볼 수 있다.
#
# matrix는 다음과 같은 상황에서 자주 사용된다.
# - 수치 계산
# - 선형대수
# - 통계 계산
# - feature matrix 표현
#
# 중요한 점:
# matrix 안의 값들은 모두 같은 자료형이어야 한다.
# ============================================================


# ------------------------------------------------------------
# 1) Basic Matrix Creation
# ------------------------------------------------------------
# 1부터 6까지 값을 2행 3열 행렬로 생성
m1 <- matrix(1:6, nrow = 2, ncol = 3)

print(m1)

# 한국어 설명
# matrix() 함수로 행렬을 만든다.
# 기본적으로 값은 column-wise(열 우선)로 채워진다.


# ------------------------------------------------------------
# 2) Fill by Row
# ------------------------------------------------------------
m2 <- matrix(1:6, nrow = 2, ncol = 3, byrow = TRUE)

print(m2)

# 한국어 설명
# byrow = TRUE를 주면 row-wise(행 우선)로 채워진다.


# ------------------------------------------------------------
# 3) Check Matrix Type and Dimension
# ------------------------------------------------------------
print(class(m1))
print(dim(m1))
print(nrow(m1))
print(ncol(m1))

# 한국어 설명
# class() → 자료구조 종류
# dim()   → 전체 차원
# nrow()  → 행 개수
# ncol()  → 열 개수


# ------------------------------------------------------------
# 4) Indexing
# ------------------------------------------------------------
# [행, 열] 형식 사용
print(m2[1, 1])   # 1행 1열
print(m2[2, 3])   # 2행 3열

# 특정 행 전체
print(m2[1, ])

# 특정 열 전체
print(m2[, 2])

# 한국어 설명
# matrix는 [row, col] 방식으로 접근한다.
# 행 또는 열 중 하나를 비우면 전체를 가져온다.


# ------------------------------------------------------------
# 5) Matrix Row and Column Names
# ------------------------------------------------------------
rownames(m2) <- c("row1", "row2")
colnames(m2) <- c("A", "B", "C")

print(m2)

# 이름으로 접근
print(m2["row1", "B"])

# 한국어 설명
# rownames(), colnames()를 이용하면
# matrix의 행/열에 이름을 부여할 수 있다.
# 분석 코드 가독성이 좋아진다.


# ------------------------------------------------------------
# 6) Element-wise Arithmetic
# ------------------------------------------------------------
m3 <- matrix(c(10, 20, 30, 40, 50, 60), nrow = 2, byrow = TRUE)

print(m3)

print(m2 + m3)
print(m3 - 5)
print(m3 * 2)

# 한국어 설명
# 기본 사칙연산은 element-wise(원소별)로 계산된다.
# 즉 같은 위치의 값끼리 더해진다.


# ------------------------------------------------------------
# 7) Row and Column Sums / Means
# ------------------------------------------------------------
print(rowSums(m3))
print(colSums(m3))
print(rowMeans(m3))
print(colMeans(m3))

# 한국어 설명
# rowSums(), colSums()는 매우 자주 사용된다.
# 행/열 기준 요약 통계를 빠르게 계산할 수 있다.


# ------------------------------------------------------------
# 8) Transpose
# ------------------------------------------------------------
m3_t <- t(m3)

print(m3_t)

# 한국어 설명
# t()는 transpose(전치행렬) 함수다.
# 행과 열을 뒤바꾼다.


# ------------------------------------------------------------
# 9) Matrix Multiplication
# ------------------------------------------------------------
a <- matrix(c(1, 2, 3, 4), nrow = 2, byrow = TRUE)
b <- matrix(c(5, 6, 7, 8), nrow = 2, byrow = TRUE)

print(a)
print(b)

# 원소별 곱
print(a * b)

# 행렬곱
print(a %*% b)

# 한국어 설명
# a * b   → element-wise multiplication
# a %*% b → matrix multiplication
#
# 이 둘은 완전히 다르다.
# 선형대수나 ML에서는 %*%가 매우 중요하다.


# ------------------------------------------------------------
# 10) Matrix Apply
# ------------------------------------------------------------
m4 <- matrix(1:12, nrow = 3, byrow = TRUE)
print(m4)

# 각 행의 최대값
row_max <- apply(m4, 1, max)
print(row_max)

# 각 열의 최소값
col_min <- apply(m4, 2, min)
print(col_min)

# 한국어 설명
# apply(matrix, margin, function)
# margin = 1 → 행 기준
# margin = 2 → 열 기준


# ------------------------------------------------------------
# 11) Reshaping Vector to Matrix
# ------------------------------------------------------------
values <- c(2, 4, 6, 8, 10, 12)
m5 <- matrix(values, nrow = 3, ncol = 2)

print(m5)

# 한국어 설명
# vector를 matrix로 재구성하는 패턴
# feature 데이터를 2차원 형태로 다룰 때 자주 사용된다.


# ------------------------------------------------------------
# 12) Matrix as Feature Table (Numeric Only)
# ------------------------------------------------------------
# 예: 3명의 학생, 3개의 numeric feature
feature_matrix <- matrix(
  c(
    170, 65, 85,
    180, 75, 90,
    175, 68, 88
  ),
  nrow = 3,
  byrow = TRUE
)

rownames(feature_matrix) <- c("student_1", "student_2", "student_3")
colnames(feature_matrix) <- c("height_cm", "weight_kg", "score")

print(feature_matrix)

# 한국어 설명
# matrix는 numeric feature table을 표현하는 데 유용하다.
# 단, 문자형/범주형이 섞이면 data.frame이 더 적절하다.


# ------------------------------------------------------------
# 13) Scale-like Manual Standardization Example
# ------------------------------------------------------------
# 각 열을 평균 0 중심으로 이동하는 간단 예시
column_means <- colMeans(feature_matrix)

centered_matrix <- sweep(feature_matrix, 2, column_means, FUN = "-")

print(column_means)
print(centered_matrix)

# 한국어 설명
# sweep()는 행/열 기준으로 연산을 적용할 때 유용하다.
# 여기서는 각 열의 평균을 빼서 centered matrix를 만든다.


# ------------------------------------------------------------
# 14) Type Coercion Warning
# ------------------------------------------------------------
mixed_matrix <- matrix(c(1, 2, "A", 4), nrow = 2)
print(mixed_matrix)
print(class(mixed_matrix))

# 한국어 설명
# matrix는 같은 자료형만 유지하려고 한다.
# 숫자와 문자를 섞으면 전체가 character로 바뀔 수 있다.
# 이를 type coercion이라고 한다.


# ------------------------------------------------------------
# 15) Practical Example
# ------------------------------------------------------------
# 간단한 점수 행렬
exam_matrix <- matrix(
  c(
    80, 75, 90,
    88, 92, 85,
    70, 78, 82
  ),
  nrow = 3,
  byrow = TRUE
)

rownames(exam_matrix) <- c("Alice", "Bob", "Charlie")
colnames(exam_matrix) <- c("Math", "English", "Science")

print(exam_matrix)

# 학생별 평균
student_avg <- rowMeans(exam_matrix)
print(student_avg)

# 과목별 평균
subject_avg <- colMeans(exam_matrix)
print(subject_avg)

# 80점 이상만 TRUE/FALSE
high_score_flags <- exam_matrix >= 80
print(high_score_flags)

# 한국어 설명
# matrix는 점수표, feature table, 실험값 정리 등에 매우 적합하다.


# ------------------------------------------------------------
# 16) Summary Output
# ------------------------------------------------------------
cat("----- Matrix Summary -----\n")
cat("Dimension of m2:", dim(m2), "\n")
cat("Rows in feature_matrix:", nrow(feature_matrix), "\n")
cat("Columns in feature_matrix:", ncol(feature_matrix), "\n")
cat("Student averages:\n")
print(student_avg)
cat("Subject averages:\n")
print(subject_avg)
cat("--------------------------\n")