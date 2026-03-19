# ============================================================
# Day 9 — R Data Structures: Tibbles
# File: 06_r/02_data_structures/05_tibbles.R
#
# 목표
# - tibble 자료구조를 이해한다.
# - data.frame과 tibble의 차이를 비교한다.
# - tibble 생성, 조회, 컬럼 추가, 부분 선택을 실습한다.
# - tidyverse 스타일 데이터 분석의 기초 구조를 익힌다.
#
# 한국어 설명
# tibble은 tidyverse에서 사용하는 현대적인 테이블 자료구조이다.
# data.frame과 비슷하지만, 더 안전하고 더 읽기 쉬운 출력을 제공한다.
#
# 특히 다음 점에서 장점이 있다.
# - 출력이 깔끔하다
# - 자동 형 변환이 덜 공격적이다
# - 부분 선택 시 예측 가능한 동작을 한다
# - tidyverse(dplyr, ggplot2)와 매우 잘 맞는다
#
# 실무적으로는:
# "R에서 현대적인 데이터 분석을 할 때 기본 테이블 구조"
# 라고 생각하면 된다.
# ============================================================


# ------------------------------------------------------------
# 1) Package Setup
# ------------------------------------------------------------
# tibble 패키지가 없으면 설치
if (!requireNamespace("tibble", quietly = TRUE)) {
  install.packages("tibble", repos = "https://cloud.r-project.org")
}

library(tibble)

# 한국어 설명
# tibble은 tidyverse 생태계의 핵심 패키지 중 하나다.


# ------------------------------------------------------------
# 2) Basic Tibble Creation
# ------------------------------------------------------------
tb <- tibble(
  id = 1:5,
  name = c("Alice", "Bob", "Charlie", "David", "Eva"),
  age = c(25, 30, 28, 35, 22),
  score = c(85, 90, 78, 88, 92)
)

print(tb)

# 한국어 설명
# tibble() 함수로 생성
# 출력 시 행/열 정보가 더 깔끔하게 보인다.


# ------------------------------------------------------------
# 3) Compare with data.frame
# ------------------------------------------------------------
df <- data.frame(
  id = 1:5,
  name = c("Alice", "Bob", "Charlie", "David", "Eva"),
  age = c(25, 30, 28, 35, 22),
  score = c(85, 90, 78, 88, 92)
)

print(df)
print(tb)

# 한국어 설명
# 같은 데이터라도 tibble이 더 현대적이고 읽기 쉬운 출력 형식을 제공한다.


# ------------------------------------------------------------
# 4) Check Class and Structure
# ------------------------------------------------------------
print(class(tb))
str(tb)

# 한국어 설명
# tibble의 class는 보통:
# "tbl_df", "tbl", "data.frame"
# 형태로 나온다.
#
# 즉 tibble은 data.frame을 확장한 형태다.


# ------------------------------------------------------------
# 5) Column Access
# ------------------------------------------------------------
print(tb$name)
print(tb[["score"]])

# 한국어 설명
# $ 또는 [[ ]] 로 컬럼 접근 가능
# data.frame과 유사하다.


# ------------------------------------------------------------
# 6) Single Bracket Behavior
# ------------------------------------------------------------
print(tb["name"])
print(class(tb["name"]))

# 한국어 설명
# tibble에서 [ ]는 항상 tibble을 반환한다.
# 이것이 data.frame보다 더 예측 가능한 동작 중 하나다.


# ------------------------------------------------------------
# 7) Row and Column Selection
# ------------------------------------------------------------
print(tb[1:3, ])
print(tb[, c("name", "score")])

# 한국어 설명
# 행과 열을 동시에 선택 가능
# SQL의 SELECT 느낌으로 이해해도 좋다.


# ------------------------------------------------------------
# 8) Add New Columns
# ------------------------------------------------------------
tb$pass <- tb$score >= 80
tb$grade <- ifelse(
  tb$score >= 90, "A",
  ifelse(tb$score >= 80, "B", "C")
)

print(tb)

# 한국어 설명
# tibble도 data.frame처럼 새로운 컬럼을 쉽게 추가할 수 있다.


# ------------------------------------------------------------
# 9) Create Tibble from Vectors
# ------------------------------------------------------------
heights <- c(170, 180, 175)
weights <- c(65, 75, 68)

student_tb <- tibble(
  student_id = 1:3,
  height_cm = heights,
  weight_kg = weights
)

print(student_tb)

# 한국어 설명
# 실무에서는 여러 벡터를 묶어 하나의 분석 테이블을 만들 때 자주 사용


# ------------------------------------------------------------
# 10) Tibble Does Not Change Names Aggressively
# ------------------------------------------------------------
weird_names_tb <- tibble(
  `student name` = c("A", "B"),
  `exam score` = c(88, 91)
)

print(weird_names_tb)

# 한국어 설명
# tibble은 컬럼 이름을 비교적 그대로 유지하려는 경향이 있다.
# data.frame보다 이름 처리 측면에서 더 직관적일 수 있다.


# ------------------------------------------------------------
# 11) List Columns
# ------------------------------------------------------------
# tibble의 강력한 기능 중 하나: list-column
model_like_tb <- tibble(
  id = 1:3,
  tags = list(
    c("ml", "python"),
    c("sql", "analytics"),
    c("r", "statistics")
  )
)

print(model_like_tb)

# 특정 list-column 요소 확인
print(model_like_tb$tags[[1]])

# 한국어 설명
# tibble은 list-column을 자연스럽게 다룰 수 있다.
# 이것은 모델 결과, 토큰 리스트, nested data 등을 저장할 때 매우 유용하다.


# ------------------------------------------------------------
# 12) Convert data.frame to tibble
# ------------------------------------------------------------
converted_tb <- as_tibble(df)

print(converted_tb)

# 한국어 설명
# 기존 data.frame을 tibble로 바꾸는 가장 쉬운 방법


# ------------------------------------------------------------
# 13) Basic Summary Calculations
# ------------------------------------------------------------
average_score <- mean(tb$score)
max_score <- max(tb$score)
min_score <- min(tb$score)

print(average_score)
print(max_score)
print(min_score)

# 한국어 설명
# tibble도 기본 통계 함수와 함께 그대로 사용할 수 있다.


# ------------------------------------------------------------
# 14) Practical Example: Analysis-Friendly Table
# ------------------------------------------------------------
sales_tb <- tibble(
  product = c("A", "B", "C", "D"),
  sales = c(120, 200, 150, 90),
  cost = c(70, 110, 90, 50)
)

sales_tb$profit <- sales_tb$sales - sales_tb$cost
sales_tb$margin <- round(sales_tb$profit / sales_tb$sales, 2)

print(sales_tb)

# 한국어 설명
# tibble은 실전 데이터 분석에서
# 계산 컬럼을 추가하면서 테이블을 확장하기 좋다.


# ------------------------------------------------------------
# 15) Tibble Printing Advantage
# ------------------------------------------------------------
big_tb <- tibble(
  a = 1:20,
  b = 21:40,
  c = 41:60
)

print(big_tb)

# 한국어 설명
# tibble은 큰 데이터에서도 일부만 깔끔하게 출력한다.
# 콘솔이 과도하게 지저분해지는 것을 막아준다.


# ------------------------------------------------------------
# 16) Mini Real-World Example
# ------------------------------------------------------------
risk_tb <- tibble(
  patient_id = 1:4,
  age = c(45, 62, 51, 70),
  biomarker = c(2.1, 3.8, 2.9, 4.2),
  event = c(0, 1, 0, 1)
)

risk_tb$risk_group <- ifelse(risk_tb$biomarker >= 3.0, "High", "Low")

print(risk_tb)

# 한국어 설명
# 헬스케어 분석에서도 tibble은 매우 잘 맞는다.
# 이후 dplyr, ggplot2, survival 패키지와 자연스럽게 연결된다.


# ------------------------------------------------------------
# 17) Summary Output
# ------------------------------------------------------------
cat("----- Tibble Summary -----\n")
cat("Class:", class(tb), "\n")
cat("Rows:", nrow(tb), "\n")
cat("Columns:", ncol(tb), "\n")
cat("Average score:", mean(tb$score), "\n")
cat("--------------------------\n")