# SQL Window Functions

This directory covers **SQL window functions**, which enable advanced
analytics without collapsing rows like traditional aggregation.

Window functions are essential for:
- Ranking and ordering within groups
- Time-aware analytics
- Deduplication and latest-record selection
- Advanced analytical queries used in real-world data pipelines

본 폴더는 **윈도우 함수(Window Functions)**를 다루며,  
그룹별 순위, 누적 계산, 중복 제거 등 **실무 SQL 분석의 핵심 기법**을 정리합니다.

---

## 🎯 Learning Objectives

- Understand how window functions differ from GROUP BY
- Apply ranking and ordering within partitions
- Perform time-aware and group-aware analytics
- Write readable and deterministic analytical SQL
- Prepare for advanced analytics and reporting queries

---

## 📂 Files & Progress

### ✅ Completed

#### `01_ever_clause.sql` (Day 13)
**OVER clause fundamentals**

- Window function의 기본 구조 이해
- `PARTITION BY`와 `ORDER BY`의 역할
- 집계 함수와 윈도우 함수의 차이
- 누적 합계, 이동 평균 등 분석 패턴 소개

> 윈도우 함수의 “문법적 뼈대”를 다지는 단계

---

#### `02_rank_dense_rank.sql` (Day 14)
**RANK vs DENSE_RANK**

- 그룹 내 순위 계산 방식 비교
- 동점(tie)이 발생했을 때의 차이
- 비즈니스 랭킹/등급 산정에서의 활용

| Function | Tie Handling | Example |
|--------|--------------|---------|
| RANK | Skips ranks | 1,1,3 |
| DENSE_RANK | No gaps | 1,1,2 |

> “순위의 의미”를 명확히 구분하는 것이 핵심

---

#### `03_row_number.sql` (Day 15)
**ROW_NUMBER practical patterns**

- 그룹별 고유 순번 생성
- 고객별 최신 레코드 선택 (Top-1)
- Top-N 분석
- 중복 제거(Deduplication)
- 페이징/배치 처리용 순번 생성

핵심 포인트:
- `ROW_NUMBER()`는 **항상 고유한 순번**을 부여
- 재현 가능한 결과를 위해 **ORDER BY에 tie-breaker 필수**

> 실무에서 가장 많이 사용되는 윈도우 함수 패턴

---

## 🧠 Why Window Functions Matter

Window functions allow you to:
- Keep row-level detail while performing analytics
- Answer questions like:
  - “각 그룹에서 가장 최신 데이터는?”
  - “누적 값은 어떻게 변하는가?”
  - “상위 N개는 무엇인가?”
- Replace complex subqueries with readable SQL

GROUP BY는 “요약”에 강하고,  
Window Functions는 “분석 흐름”에 강하다.

---

## 📌 한국어 요약

- 윈도우 함수는 **행을 유지한 채 분석**을 가능하게 한다
- OVER 절은 모든 윈도우 함수의 핵심
- RANK / DENSE_RANK / ROW_NUMBER는 각각 다른 목적을 가진다
- 최신 데이터 선택, 중복 제거, 순위 분석은 실무에서 매우 빈번하다
- ORDER BY 기준이 곧 “비즈니스 규칙”이 된다

---

## 🚧 Status

**Completed (Day 13–15)**  
Window function fundamentals and core ranking patterns are complete.

본 단계는 윈도우 함수의 핵심 개념과 실무 패턴을 모두 다루었으며,  
이후 고급 분석 SQL의 기반이 됩니다.