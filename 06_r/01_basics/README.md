# R Basics

This directory covers the **fundamental syntax and core programming concepts of R**.

R is a programming language widely used for:

- statistics
- data analysis
- visualization
- research workflows
- experimental modeling

Before using advanced R packages such as `dplyr`, `ggplot2`, or `survival`,
it is important to understand the language basics.

This module focuses on the foundational elements that every R learner should know first.

---

# 🎯 Learning Objectives

After completing this module, you should be able to:

- create and use variables in R
- understand vectors as the core data structure
- define and call functions
- use control flow such as `if`, `for`, and `while`
- build a solid foundation for later statistical and analytical work

---

# Why Learn R Basics?

Even though high-level packages are powerful, they become much easier to use
when you understand the underlying language.

R basics help you understand:

- how values are stored
- how data structures behave
- how functions are written
- how repeated logic is controlled

This is especially important for:

- reproducible research
- statistical modeling
- survival analysis
- academic and healthcare data workflows

### 한국어 설명
R은 통계 분석과 연구 환경에서 매우 자주 사용되는 언어다.  
특히 고급 패키지를 쓰기 전에 **기초 문법과 데이터 구조를 먼저 이해하는 것**이 중요하다.

이 모듈은 이후의 데이터 분석 / 생존분석 / 시각화 학습을 위한 **기초 토대**를 다룬다.

---

# Module Structure

| File | Description |
|---|---|
| `01_variables.R` | Basic variable assignment and data types |
| `02_vectors.R` | Vector creation, indexing, and vectorized operations |
| `03_functions.R` | Function definition, parameters, return values, and defaults |
| `04_control_flow.R` | Conditional logic and loops |

---

# 1️⃣ Variables

File  
`01_variables.R`

This file introduces the most basic elements of R programming:

- numeric values
- character values
- logical values
- variable assignment with `<-`
- output using `print()` and `cat()`
- type checking with `class()`

Example:

```r
name <- "Junyeong"
age <- 27
is_student <- TRUE
```

### 한국어 설명
변수(variable)는 값을 저장하는 이름표다.  
R에서는 `<-` 기호를 사용해 값을 변수에 할당하는 것이 가장 일반적이다.

이 파일에서는 숫자형, 문자형, 논리형 변수를 만들고 출력하는 가장 기본적인 흐름을 다룬다.

---

# 2️⃣ Vectors

File  
`02_vectors.R`

Vectors are one of the most important data structures in R.

This file covers:

- creating vectors with `c()`
- indexing vectors
- vectorized arithmetic
- summary functions such as `mean()`, `sum()`, `max()`, `min()`
- logical filtering
- named vectors

Example:

```r
scores <- c(85, 90, 78, 92, 88)
scores[scores > 85]
```

### Why vectors matter

R is designed around vectorized computation.
Many R operations become simple and powerful once vectors are understood.

### 한국어 설명
Vector는 R의 가장 핵심적인 데이터 구조다.  
같은 자료형의 값들을 묶어서 저장하며, R의 계산은 대부분 vector 중심으로 동작한다.

이해가 되면 이후의 matrix, data frame, 통계 계산도 훨씬 쉬워진다.

---

# 3️⃣ Functions

File  
`03_functions.R`

Functions help organize repeated logic into reusable code blocks.

This file covers:

- defining functions with `function()`
- using parameters
- returning values with `return()`
- default arguments
- simple decision logic inside functions

Example:

```r
add_numbers <- function(x, y) {
  return(x + y)
}
```

### Why functions matter

Functions improve:

- readability
- reusability
- maintainability

They are essential in all serious R workflows.

### 한국어 설명
함수(function)는 반복되는 작업을 재사용 가능한 코드 블록으로 묶는 방법이다.  
분석 코드가 길어질수록 함수를 사용하는 것이 훨씬 중요해진다.

특히 연구/분석 환경에서는 코드 재현성과 가독성을 위해 함수 작성이 필수적이다.

---

# 4️⃣ Control Flow

File  
`04_control_flow.R`

This file introduces the basic structures used to control execution flow:

- `if`
- `if ... else`
- `if ... else if ... else`
- `for`
- `while`
- `break`
- `next`

Example:

```r
if (score >= 80) {
  print("Pass")
} else {
  print("Fail")
}
```

### Why control flow matters

Control flow is necessary when code must:

- branch based on conditions
- repeat logic
- skip or stop iterations

These patterns are common in preprocessing, validation, and repeated calculations.

### 한국어 설명
제어문(control flow)은 코드의 실행 흐름을 조절하는 문법이다.  
조건에 따라 다른 코드를 실행하거나, 반복문으로 여러 번 계산할 때 꼭 필요하다.

데이터 전처리, 조건 분기, 통계 계산 로직에서 매우 자주 쓰인다.

---

# Recommended Learning Flow

A practical order for learning this module is:

```text
Variables
   ↓
Vectors
   ↓
Functions
   ↓
Control Flow
```

Why this order?

- variables are the smallest units of storage
- vectors are the core R data structure
- functions organize reusable logic
- control flow enables dynamic execution

---

# Run Examples

From the project root:

```bash
Rscript 06_r/01_basics/01_variables.R
Rscript 06_r/01_basics/02_vectors.R
Rscript 06_r/01_basics/03_functions.R
Rscript 06_r/01_basics/04_control_flow.R
```

Or inside an R session:

```r
source("06_r/01_basics/01_variables.R")
source("06_r/01_basics/02_vectors.R")
source("06_r/01_basics/03_functions.R")
source("06_r/01_basics/04_control_flow.R")
```

### 한국어 설명
터미널에서는 `Rscript`로 실행할 수 있고,  
R 콘솔 안에서는 `source()`를 사용하면 된다.

---

# Practical Importance

These basics are essential before moving on to:

- data frames
- lists
- matrices
- tidyverse workflows
- visualization
- statistical modeling
- survival analysis

Understanding these basics will make advanced R much easier to learn.

### 한국어 설명
이 기초 문법은 이후의 고급 주제들로 가기 위한 필수 기반이다.

특히 너처럼 연구/통계/생존분석에 관심이 있다면  
R 기초를 먼저 탄탄히 해두는 것이 장기적으로 큰 도움이 된다.

---

# Summary

This module introduces the foundations of R programming:

```text
Variables
→ store values

Vectors
→ work with grouped data

Functions
→ organize reusable logic

Control Flow
→ control how code runs
```

Together, these concepts form the starting point for more advanced R-based
data analysis and statistical programming.