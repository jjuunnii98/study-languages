# SQL Window Functions

This module covers **SQL window functions**, a core analytical feature that allows
calculations across related rows **without collapsing them** like GROUP BY.

Window functions are essential for:
- Ranking and ordering within groups
- Selecting latest or top-N records
- Deduplication
- Time-aware and analytical queries in production data pipelines

본 파트는 SQL의 **윈도우 함수(Window Functions)**를 다루며,  
그룹별 순위 계산, 최신 데이터 선택, 중복 제거 등  
**실무 분석 SQL의 핵심 패턴**을 정리합니다.

---

## 🎯 Learning Objectives

- Understand how window functions differ from GROUP BY
- Apply analytical functions using OVER, PARTITION BY, ORDER BY
- Rank rows within logical groups
- Select latest or top-N records deterministically
- Write readable, reproducible analytical SQL

---

## 📂 Files & Progress

각 파일은 하루 단위 학습 목표에 맞춰 구성되며,  
실무에서 가장 많이 사용되는 윈도우 함수 패턴을 중심으로 작성되었습니다.

---

### ✅ Completed

#### `01_ever_clause.sql` (Day 13)
**OVER clause fundamentals**

**Key topics**
- Window function 기본 문법
- `OVER`, `PARTITION BY`, `ORDER BY` 구조 이해
- 집계 함수와 윈도우 함수의 차이
- 누적 합계, 이동 평균 등 분석 패턴 소개

**한국어 요약**
- OVER 절은 모든 윈도우 함수의 핵심
- 행을 유지한 채 분석 가능
- 이후 랭킹/정렬 함수의 기반이 되는 파일

---

#### `02_rank_dense_rank.sql` (Day 14)
**RANK vs DENSE_RANK**

**Key topics**
- 그룹 내 순위 계산
- 동점(tie) 발생 시 순위 처리 차이
- 비즈니스 랭킹/등급 산정에 적합한 함수 선택

| Function | Tie Handling | Result Example |
|--------|--------------|----------------|
| RANK | Skips ranks | 1, 1, 3 |
| DENSE_RANK | No gaps | 1, 1, 2 |

**한국어 요약**
- RANK는 순위 공백 발생
- DENSE_RANK는 연속 순위
- “순위의 의미”를 정의하는 것이 중요

---

#### `03_row_number.sql` (Day 15)
**ROW_NUMBER practical patterns**

**Key topics**
- 그룹별 고유 순번 생성
- 최신 레코드 선택 (Top-1 per group)
- Top-N 분석
- Deduplication (중복 제거)
- Pagination / batch 처리 패턴

**핵심 포인트**
- `ROW_NUMBER()`는 항상 고유한 순번을 부여
- 재현 가능한 결과를 위해 `ORDER BY`에 tie-breaker 필수
- 실무에서 가장 빈번히 사용되는 윈도우 함수

**한국어 요약**
- 고객별 최신 데이터 선택
- 중복 제거 기준 명확화
- 분석/ETL 파이프라인에서 필수 패턴

---

## 🧠 Why Window Functions Matter

Window functions enable:
- Row-level analytics without data loss
- Clean solutions to “latest record”, “top-N”, and ranking problems
- Simpler SQL compared to deeply nested subqueries

GROUP BY는 “요약”에 강하고,  
Window Functions는 “분석 흐름”에 강합니다.

---

## 📌 학습 요약 (한국어)

- OVER 절을 기반으로 한 분석 SQL 작성
- RANK / DENSE_RANK / ROW_NUMBER의 차이 명확화
- 최신 데이터 선택 및 중복 제거 실무 패턴 습득
- 이후 CTE, Performance 튜닝으로 확장 가능한 기반 확보

---

## 🚧 Status

**Completed — Window Functions Module (Day 13–15)**

This module establishes a strong foundation for
advanced analytics, reporting, and SQL-based data modeling.

본 파트는 Day 13–15 기준으로 완료되었으며,  
실무 SQL 분석의 핵심 단원으로 마무리되었습니다.