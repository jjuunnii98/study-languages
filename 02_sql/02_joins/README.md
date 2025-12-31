# SQL Joins

This directory covers essential SQL JOIN patterns used in real-world analytics and data engineering.
Each file focuses on one JOIN type with practical interpretation notes (especially around NULL behavior and filtering).

본 폴더는 실무 데이터 분석/엔지니어링에서 필수로 쓰이는 SQL JOIN 패턴을 정리합니다.  
각 파일은 JOIN 유형별로 “어떻게 동작하는지 + NULL/필터링 주의점”을 중심으로 구성되어 있습니다.

---

## 🎯 Learning Objectives / 학습 목표

- Understand JOIN semantics (matching logic and row preservation)
- Interpret NULL results correctly in JOIN outputs
- Avoid common filtering mistakes that change JOIN behavior
- Apply JOIN patterns for analytics (cohort, retention, missing reference checks)

- JOIN의 의미(매칭 로직, 행 보존 기준)를 정확히 이해
- JOIN 결과에서 NULL이 발생하는 이유를 해석
- WHERE 조건으로 JOIN 의미가 바뀌는 실수를 방지
- 분석 실무(유저 기준 분석, 결측 탐지, 무결성 점검)에 JOIN을 적용

---

## 📂 Files / 파일 구성

### `01_inner_join.sql`
**INNER JOIN**: returns only matched rows (intersection).  
INNER JOIN: 양쪽 테이블에 모두 존재하는 행만 반환(교집합)

### `02_left_join.sql`
**LEFT JOIN**: keeps all rows from the left table and matches right table rows; unmatched right-side values become NULL.  
LEFT JOIN: 왼쪽 테이블의 모든 행을 유지하고 오른쪽을 붙임. 매칭이 없으면 오른쪽 컬럼이 NULL

> ⚠️ Note (Progress Tracking Correction)  
> The original commit message for `02_left_join.sql` mistakenly labeled the day number.  
> **Correct mapping: Day 6 = LEFT JOIN**  
>
> ⚠️ 진행 기록 정정  
> `02_left_join.sql`의 최초 커밋 메시지에 Day 표기가 잘못 들어갔습니다.  
> **정확한 매핑: Day 6 = LEFT JOIN**

### `03_right_join.sql`
**RIGHT JOIN**: keeps all rows from the right table; unmatched left-side values become NULL.  
RIGHT JOIN: 오른쪽 테이블의 모든 행을 유지. 매칭이 없으면 왼쪽 컬럼이 NULL  
✅ **Day 7 = RIGHT JOIN**

### `04_full_join.sql`
**FULL OUTER JOIN**: keeps all rows from both sides; unmatched columns become NULL.  
FULL OUTER JOIN: 양쪽 테이블의 모든 행을 유지. 매칭이 없으면 반대쪽 컬럼이 NULL  
(지원 여부는 DB 엔진에 따라 다를 수 있음)

---

## 🧠 Key Pitfalls / 핵심 주의사항

### 1) WHERE 조건이 JOIN 의미를 바꾸는 문제
Filtering on the right table in a LEFT JOIN (or left table in a RIGHT JOIN) can unintentionally remove NULL rows and behave like an INNER JOIN.

LEFT JOIN에서 오른쪽 테이블 컬럼에 WHERE 조건을 걸면,  
NULL 행이 제거되어 결과적으로 INNER JOIN처럼 동작할 수 있습니다.

✅ Fix: put conditions in the `ON` clause when you want to preserve left/right rows.  
✅ 해결: “행 보존”이 목적이면 조건을 `ON` 절로 이동하는 것을 우선 고려합니다.

---

## ✅ Progress (Day Mapping) / 진행 상황 (Day 기준)

- Day 6: `02_left_join.sql` (LEFT JOIN)  *(Day 표기 정정: 최초 커밋 메시지 오류)*
- Day 7: `03_right_join.sql` (RIGHT JOIN)

Next:
- `04_full_join.sql` (FULL OUTER JOIN, engine-dependent)
- JOIN summary examples (analytics patterns)

다음 작업:
- `04_full_join.sql` 작성 (DB 엔진별 지원 여부 확인)
- JOIN 요약/분석 패턴 예시 추가