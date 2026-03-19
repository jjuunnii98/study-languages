# R Data Structures

This module covers the fundamental data structures in R, forming the foundation for data analysis, statistical modeling, and machine learning workflows.

---

## 📌 Overview

R provides several core data structures, each designed for different analytical purposes:

```text
vector  → 1D data (basic unit)
matrix  → 2D numeric data (linear algebra)
list    → flexible container (any type)
data.frame → tabular data (core analysis structure)
tibble  → modern data.frame (tidyverse standard)
```

---

## 📂 Directory Structure

| File | Description |
|------|-------------|
| 01_vectors.R | Basic vector operations and numeric handling |
| 02_matrices.R | Matrix creation, indexing, and operations |
| 03_lists.R | Flexible container and nested structures |
| 04_data_frames.R | Core tabular data structure and mini EDA workflow |
| 05_tibbles.R | Modern table structure for tidyverse workflows |

---

## 🔑 Core Concepts

#### 1. Vector (기본 단위)
	•	R의 모든 데이터 구조의 기반
	•	동일한 자료형만 저장 가능
```
x <- c(1, 2, 3)
```

#### 2. Matrix (2차원 숫자 구조)
	•	2D numeric structure
	•	선형대수, 통계 계산에 사용
```
m <- matrix(1:6, nrow = 2)
```

#### 3. List (유연한 컨테이너)
	•	서로 다른 데이터 타입 저장 가능
	•	nested 구조 가능 (JSON과 유사)
```
lst <- list(a = 1:3, b = "text", c = TRUE)
```

#### 4. Data Frame ⭐ (핵심)
	•	테이블 구조 (row + column)
	•	각 컬럼은 서로 다른 타입 가능
	•	실제 데이터 분석의 중심
```
df <- data.frame(
  id = 1:3,
  score = c(80, 90, 85)
)
```

#### 5. Tibble (Modern Data Frame)
	•	tidyverse 기반 구조
	•	더 안전하고 읽기 쉬운 출력
	•	실무 분석에서 가장 많이 사용
```
library(tibble)

tb <- tibble(
  id = 1:3,
  score = c(80, 90, 85)
)
```

---

## 🔄 Data Structure Relationships
```
vector → matrix → data.frame → tibble
           ↓
          list (can contain everything)
```

---

## 📊 Practical Analysis Workflow

Real-world data analysis in R typically follows this pipeline:
```
data.frame / tibble
→ data cleaning
→ filtering
→ feature engineering
→ aggregation
→ modeling
→ interpretation
```

---

## ⚙️ Key Operations Summary

#### Data Access
```
df$column
df[, "column"]
df[1, ]
```

#### Filtering
```
df[df$score > 80, ]
```

#### Column Creation
```
df$pass <- df$score >= 80
```

#### Aggregation
```
aggregate(score ~ group, data = df, mean)
```

---

## 🚀 Why This Matters

Understanding these structures is essential because:

	•	모든 데이터 분석은 결국 테이블 구조로 진행된다
	•	머신러닝 입력 데이터는 대부분 matrix / data.frame 형태
	•	R의 통계 및 시각화 패키지는 data.frame/tibble 기반으로 동작

---

## 🔥 Key Takeaways
```
vector = 모든 구조의 시작
matrix = 수치 계산용 2D 구조
list = 모든 것을 담는 컨테이너
data.frame = 분석의 핵심
tibble = 실무 표준
```

---

## 📈 Next Step (Critical)

After mastering data structures, move to:
```
→ dplyr (data manipulation)
→ ggplot2 (data visualization)
```
These are essential for real-world data science workflows.

---

## 💡 Summary

```
Data Structure Learning Flow:

vector
→ matrix
→ list
→ data.frame
→ tibble
→ (next) dplyr + ggplot2
```
