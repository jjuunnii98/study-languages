# ============================================================
# Day 10 — R Data Manipulation: dplyr select() and filter()
# File: 06_r/03_data_manipulation/01_dplyr_select_filter.R
#
# 목표
# - dplyr 패키지의 select()와 filter()를 이해한다.
# - 필요한 열(column)만 선택하는 방법을 배운다.
# - 조건에 맞는 행(row)만 필터링하는 방법을 배운다.
# - dplyr 문법을 SQL-like 데이터 조작 관점에서 이해한다.
#
# 한국어 설명
# dplyr은 R에서 가장 널리 쓰이는 데이터 조작 패키지다.
# 특히 select()와 filter()는 거의 모든 데이터 분석의 시작점이다.
#
# select() = 필요한 열만 선택
# filter() = 조건에 맞는 행만 선택
#
# 즉, 데이터 전체를 그대로 쓰는 것이 아니라
# "분석 목적에 맞는 데이터만 남기는 과정"이라고 이해하면 된다.
# ============================================================


# ------------------------------------------------------------
# 0) Package Setup
# ------------------------------------------------------------
# 한국어 설명
# dplyr이 설치되어 있지 않으면 설치하고, 이후 library로 불러온다.
if (!requireNamespace("dplyr", quietly = TRUE)) {
  install.packages("dplyr", repos = "https://cloud.r-project.org")
}

library(dplyr)


# ------------------------------------------------------------
# 1) Example Data
# ------------------------------------------------------------
# 한국어 설명
# 실습용 학생 데이터셋 생성
students <- tibble(
  student_id = 1:8,
  name = c("Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Henry"),
  age = c(20, 21, 22, 21, 20, 23, 22, 21),
  major = c("Statistics", "Economics", "Computer Science", "Economics",
            "Statistics", "Mathematics", "Computer Science", "Economics"),
  score = c(88, 76, 91, 69, 95, 84, 73, 87),
  passed = c(TRUE, FALSE, TRUE, FALSE, TRUE, TRUE, FALSE, TRUE)
)

print(students)

# 한국어 설명
# tibble 구조 확인
glimpse(students)


# ------------------------------------------------------------
# 2) Basic select()
# ------------------------------------------------------------
# 한국어 설명
# 특정 열만 선택
selected_basic <- select(students, name, major, score)

print(selected_basic)

# 한국어 설명
# SQL 느낌:
# SELECT name, major, score FROM students


# ------------------------------------------------------------
# 3) select() with Column Range
# ------------------------------------------------------------
# 한국어 설명
# 연속된 열 범위를 선택할 수 있다.
selected_range <- select(students, name:score)

print(selected_range)


# ------------------------------------------------------------
# 4) select() with Exclusion
# ------------------------------------------------------------
# 한국어 설명
# 특정 열을 제외하고 싶을 때는 - 사용
selected_exclude <- select(students, -passed)

print(selected_exclude)


# ------------------------------------------------------------
# 5) Basic filter()
# ------------------------------------------------------------
# 한국어 설명
# 점수가 80 이상인 학생만 선택
filtered_score <- filter(students, score >= 80)

print(filtered_score)

# SQL 느낌:
# SELECT * FROM students WHERE score >= 80


# ------------------------------------------------------------
# 6) filter() with Multiple Conditions
# ------------------------------------------------------------
# 한국어 설명
# AND 조건: , 또는 & 사용 가능
filtered_major_score <- filter(
  students,
  major == "Economics",
  score >= 80
)

print(filtered_major_score)


# ------------------------------------------------------------
# 7) filter() with OR Condition
# ------------------------------------------------------------
# 한국어 설명
# OR 조건은 | 사용
filtered_or <- filter(
  students,
  major == "Statistics" | major == "Mathematics"
)

print(filtered_or)


# ------------------------------------------------------------
# 8) filter() with Logical Column
# ------------------------------------------------------------
# 한국어 설명
# passed가 TRUE인 학생만 선택
filtered_passed <- filter(students, passed)

print(filtered_passed)


# ------------------------------------------------------------
# 9) filter() with %in%
# ------------------------------------------------------------
# 한국어 설명
# 특정 값 집합 안에 포함되는지 확인
filtered_multiple_majors <- filter(
  students,
  major %in% c("Economics", "Computer Science")
)

print(filtered_multiple_majors)


# ------------------------------------------------------------
# 10) Chaining select() and filter()
# ------------------------------------------------------------
# 한국어 설명
# dplyr에서는 파이프(%>%)를 사용해 여러 조작을 연결한다.
selected_filtered <- students %>%
  filter(score >= 85) %>%
  select(name, major, score)

print(selected_filtered)

# 한국어 설명
# 해석:
# 1. 점수 85 이상 필터링
# 2. name, major, score 열만 선택


# ------------------------------------------------------------
# 11) Real-world Style Example
# ------------------------------------------------------------
# 한국어 설명
# "경제학 전공 중 합격한 학생들의 이름과 점수만 보고 싶다"
economics_passed <- students %>%
  filter(major == "Economics", passed == TRUE) %>%
  select(name, score)

print(economics_passed)


# ------------------------------------------------------------
# 12) Another Example: Young High Performers
# ------------------------------------------------------------
# 한국어 설명
# 나이가 21 이하이면서 점수가 85 이상인 학생 조회
young_high_performers <- students %>%
  filter(age <= 21, score >= 85) %>%
  select(student_id, name, age, score)

print(young_high_performers)


# ------------------------------------------------------------
# 13) Practical Summary Output
# ------------------------------------------------------------
cat("----- dplyr select() / filter() Summary -----\n")
cat("Total rows in original data:", nrow(students), "\n")
cat("Total rows with score >= 80:", nrow(filtered_score), "\n")
cat("Total passed students:", nrow(filtered_passed), "\n")
cat("Total Economics passed students:", nrow(economics_passed), "\n")
cat("---------------------------------------------\n")