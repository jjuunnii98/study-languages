# ============================================================
# Day 3 — R Functions
# File: 06_r/01_basics/03_functions.R
#
# 목표
# - R에서 함수를 정의하고 사용하는 방법을 이해한다.
# - 입력값(parameter)을 받아 계산하는 구조를 배운다.
# - return()과 기본값(default argument) 개념을 익힌다.
#
# 한국어 설명
# 함수(function)는 "반복되는 작업을 하나로 묶은 코드 블록"이다.
# 같은 계산을 여러 번 할 때 함수를 만들면
# 코드가 더 짧고, 읽기 쉽고, 재사용 가능해진다.
# ============================================================


# ------------------------------------------------------------
# 1) 가장 기본적인 함수
# ------------------------------------------------------------
# function() 으로 함수를 만든다.
# 아래 함수는 이름을 받아 인사말을 출력한다.
greet_user <- function(name) {
  print(paste("Hello,", name))
}

# 함수 실행
greet_user("Junyeong")
greet_user("Alice")


# ------------------------------------------------------------
# 2) 숫자를 계산하는 함수
# ------------------------------------------------------------
# 두 숫자를 받아 더한 값을 출력한다.
add_numbers <- function(x, y) {
  result <- x + y
  print(result)
}

add_numbers(10, 20)
add_numbers(3, 7)


# ------------------------------------------------------------
# 3) 값을 반환(return)하는 함수
# ------------------------------------------------------------
# print()는 화면에 보여주기만 하지만,
# return()은 계산 결과를 바깥으로 돌려준다.
multiply_numbers <- function(x, y) {
  result <- x * y
  return(result)
}

product_result <- multiply_numbers(4, 5)
print(product_result)


# ------------------------------------------------------------
# 4) 기본값(default argument)이 있는 함수
# ------------------------------------------------------------
# y의 기본값을 10으로 설정
power_number <- function(x, y = 2) {
  return(x ^ y)
}

print(power_number(3))     # y를 안 넣으면 기본값 2 사용
print(power_number(3, 3))  # y를 직접 넣으면 그 값 사용


# ------------------------------------------------------------
# 5) 문자 처리 함수
# ------------------------------------------------------------
# 문자열 길이를 계산하는 함수
get_name_length <- function(name) {
  return(nchar(name))
}

print(get_name_length("Junyeong"))
print(get_name_length("Statistics"))


# ------------------------------------------------------------
# 6) 논리값을 반환하는 함수
# ------------------------------------------------------------
# 점수가 80 이상이면 TRUE, 아니면 FALSE
is_pass <- function(score) {
  return(score >= 80)
}

print(is_pass(85))
print(is_pass(72))


# ------------------------------------------------------------
# 7) 여러 줄 로직이 있는 함수
# ------------------------------------------------------------
# 점수를 받아 grade를 반환
get_grade <- function(score) {
  if (score >= 90) {
    return("A")
  } else if (score >= 80) {
    return("B")
  } else if (score >= 70) {
    return("C")
  } else {
    return("F")
  }
}

print(get_grade(95))
print(get_grade(84))
print(get_grade(71))
print(get_grade(60))


# ------------------------------------------------------------
# 8) 벡터를 입력으로 받는 함수
# ------------------------------------------------------------
# 점수 벡터의 평균을 계산
calculate_mean <- function(scores) {
  return(mean(scores))
}

score_vector <- c(80, 85, 90, 88, 92)
print(calculate_mean(score_vector))


# ------------------------------------------------------------
# 9) 함수 안에서 cat() 사용
# ------------------------------------------------------------
# cat()은 문장 형태 출력에 적합하다.
introduce_user <- function(name, age, major) {
  cat("Name :", name, "\n")
  cat("Age  :", age, "\n")
  cat("Major:", major, "\n")
}

introduce_user("Junyeong", 27, "Economics")


# ------------------------------------------------------------
# 10) 요약 출력
# ------------------------------------------------------------
cat("----- Function Practice Summary -----\n")
cat("multiply_numbers(4, 5) =", multiply_numbers(4, 5), "\n")
cat("power_number(3) =", power_number(3), "\n")
cat("get_grade(84) =", get_grade(84), "\n")
cat("Mean of score_vector =", calculate_mean(score_vector), "\n")
cat("-------------------------------------\n")