# SQL CTE (Common Table Expressions)

This module covers **Common Table Expressions (CTE)**,
a powerful SQL feature used to structure complex queries,
improve readability, and model hierarchical or iterative logic.

본 파트는 SQL의 **CTE(Common Table Expression)**를 다루며,
복잡한 쿼리를 단계적으로 구성하고,
계층 구조 및 반복 로직을 SQL로 표현하는 방법을 학습합니다.

---

## 🎯 Learning Objectives

- Understand how CTEs improve SQL readability and maintainability
- Replace deeply nested subqueries with named query blocks
- Build step-by-step analytical pipelines inside SQL
- Model hierarchical and recursive relationships using SQL
- Safely control recursion and prevent infinite loops

---

## 📂 Files & Progress

Each file represents a focused concept and is completed incrementally
as part of a day-based learning plan.

각 파일은 하루 단위 학습 목표를 기준으로 작성되며,
실무에서 바로 활용 가능한 패턴을 중심으로 구성됩니다.

---

### ✅ Completed

#### `01_with_clause.sql` (Day 16)
**Basic CTE using WITH**

**Key topics**
- Basic `WITH` clause syntax
- Improving query readability
- Reusing aggregated results
- Step-by-step query pipelines
- Combining CTE with window functions

**핵심 내용 (한국어 요약)**
- 복잡한 SQL을 단계별로 분해하여 가독성 향상
- 동일한 서브쿼리 반복 제거
- 집계 결과 재사용
- 분석/ETL 파이프라인에서 자주 사용하는 구조

---

#### `02_recursive_cte.sql` (Day 17)
**Recursive CTE for hierarchical and iterative problems**

**Key topics**
- `WITH RECURSIVE` syntax
- Anchor member vs Recursive member
- Organizational hierarchy traversal
- Tree / graph-style data modeling
- Number and date sequence generation
- Path accumulation and cycle prevention

**핵심 내용 (한국어 요약)**
- 조직도, 카테고리 트리 등 계층 구조 전개
- 재귀 종료 조건 설계
- 무한 루프 및 순환 참조 방지
- 날짜/숫자 시퀀스 생성
- SQL을 이용한 반복 로직 모델링

---

## 🧠 Why CTEs Matter

CTEs allow SQL to move beyond simple data retrieval and into:

- Readable, maintainable analytical logic
- Modular query construction
- Hierarchical and graph-style modeling
- Safer handling of complex transformations
- Cleaner collaboration between analysts and engineers

CTE를 이해하면 SQL은
단순 조회 언어가 아니라 **분석과 모델링을 위한 언어**가 됩니다.

---

## 📌 학습 요약 (한국어)

- WITH 절을 이용한 SQL 구조화
- 복잡한 서브쿼리 제거 및 가독성 개선
- Recursive CTE를 통한 계층/트리 문제 해결
- SQL 기반 반복·순환 로직 이해
- 이후 Window Function, Performance 튜닝으로 확장 가능한 기반 확보

---

## 🚧 Status

**Completed — CTE Module (Day 16–17)**

This module provides the foundation for:
- Advanced analytics
- Performance optimization
- Data modeling patterns

본 파트는 Day 16–17 기준으로 완료되었으며,
이후 Window Functions, Performance, Data Cleaning 파트로 자연스럽게 연결됩니다.