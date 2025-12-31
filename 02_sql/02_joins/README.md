# SQL Joins

This directory covers essential SQL JOIN patterns used in real-world analytics,
data engineering, and research workflows.

Each file focuses on one JOIN type and emphasizes:
- row preservation logic
- NULL interpretation
- common filtering pitfalls
- practical analytics use cases

본 폴더는 실무 데이터 분석, 데이터 엔지니어링, 연구 환경에서
반드시 이해해야 할 SQL JOIN 패턴을 정리합니다.

각 JOIN 파일은 다음에 초점을 둡니다:
- 어떤 테이블의 행이 유지되는지
- NULL이 발생하는 이유와 해석 방법
- WHERE 조건으로 JOIN 의미가 바뀌는 함정
- 분석 실무에서의 활용 맥락

---

## 🎯 Learning Objectives / 학습 목표

- Understand how different JOIN types preserve or discard rows
- Interpret NULL values correctly in JOIN results
- Avoid common mistakes that unintentionally change JOIN semantics
- Apply JOINs to analytics tasks such as retention, coverage, and data-quality checks

- JOIN 유형별 행 보존 기준을 정확히 이해
- JOIN 결과의 NULL을 올바르게 해석
- WHERE 조건으로 JOIN 의미가 바뀌는 실수 방지
- 분석 실무(유저 기준 분석, 결측 탐지, 무결성 점검)에 JOIN 적용

---

## 📂 Files Overview / 파일 구성

### `01_inner_join.sql`
**INNER JOIN**  
Returns only rows that exist in both tables (intersection).

- 양쪽 테이블에 모두 존재하는 데이터만 반환
- 기준 데이터 손실 가능
- 매칭된 데이터만 분석할 때 사용

---

### `02_left_join.sql`
**LEFT JOIN**  
Keeps all rows from the left table and matches rows from the right table.
Unmatched right-side values become NULL.

- 왼쪽 테이블 기준 분석의 핵심
- “존재하지 않는 경우”도 분석 대상에 포함 가능
- 사용자 기준 분석, 미구매/미이용 탐지에 필수

> ⚠️ Progress Tracking Correction  
> The original commit message mistakenly labeled the day number.  
> **Correct mapping: Day 6 = LEFT JOIN**
>
> ⚠️ 진행 기록 정정  
> `02_left_join.sql`의 최초 커밋 메시지에 Day 표기가 잘못 입력되었습니다.  
> **정확한 매핑: Day 6 = LEFT JOIN**

---

### `03_right_join.sql`
**RIGHT JOIN**  
Keeps all rows from the right table and matches rows from the left table.
Unmatched left-side values become NULL.

- RIGHT JOIN은 LEFT JOIN의 방향 반전 개념
- 실무에서는 LEFT JOIN으로 치환해 사용하는 경우가 많음
- 참조 누락, 데이터 품질 점검에 활용

✅ **Day 7 = RIGHT JOIN**

---

### `04_full_join.sql`
**FULL OUTER JOIN**  
Keeps all rows from both tables.
Unmatched rows from either side are preserved with NULLs.

- 양쪽 테이블의 모든 데이터 보존
- 데이터 누락/불일치 탐지에 최적
- DB 엔진별 지원 여부 차이 존재

DB support:
- PostgreSQL / SQL Server / Oracle: 지원
- MySQL / SQLite: 미지원 → UNION 기반 대체 구현 필요

✅ **Day 8 = FULL OUTER JOIN**

---

## ⚠️ Critical Pitfalls / 핵심 주의사항

### 1) WHERE vs ON clause
Filtering on the joined table in the WHERE clause can unintentionally remove NULL rows,
making LEFT/RIGHT JOIN behave like an INNER JOIN.

LEFT/RIGHT JOIN에서 보존되어야 할 행이  
WHERE 절 조건으로 제거되면 INNER JOIN처럼 동작할 수 있습니다.

✅ Best practice:
- 행 보존이 목적일 경우 → 조건은 `ON` 절에 위치
- 필터링이 목적일 경우 → JOIN 이후 `WHERE` 절 사용

---

## 🧠 Practical Analytics Patterns / 실무 활용 패턴

- LEFT JOIN + `IS NULL`
  - 미구매 고객, 미이용 사용자 탐지
- FULL JOIN
  - 데이터 누락 / 참조 무결성 검사
- JOIN 결과 NULL 분석
  - 데이터 품질 진단, 파이프라인 점검
- JOIN 기준 테이블 명확화
  - “무엇을 기준으로 분석하는가?”를 항상 먼저 결정

---

## ✅ Progress Summary / 진행 요약 (Day 기준)

- Day 6: `02_left_join.sql` — LEFT JOIN *(Day 표기 정정)*
- Day 7: `03_right_join.sql` — RIGHT JOIN
- Day 8: `04_full_join.sql` — FULL OUTER JOIN

Next:
- `03_aggregation` (GROUP BY, HAVING, aggregation functions)
- JOIN + aggregation combined analytics patterns

---

## 📌 Final Note

JOIN is not just a SQL syntax problem.
It is a **data interpretation problem**.

Understanding which rows are kept,
which are lost,
and why NULL appears
is essential for trustworthy analytics.

JOIN은 단순 문법이 아니라,
**데이터를 어떻게 해석할 것인가의 문제**입니다.