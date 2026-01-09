# SQL Subqueries

This directory covers **SQL subqueries**, which allow queries
to be composed hierarchically and evaluated step by step.

Subqueries are essential when query logic depends on
aggregated results, conditional existence checks,
or row-by-row comparisons.

본 폴더는 SQL의 **서브쿼리(Subquery)** 개념을 다룹니다.  
서브쿼리는 하나의 쿼리 안에 또 다른 쿼리를 포함하여,
복잡한 조건과 계산을 단계적으로 표현할 수 있게 해줍니다.

---

## 🎯 Learning Objectives

- Understand what subqueries are and how they are executed
- Use subqueries in WHERE, SELECT, and FROM clauses
- Apply correlated subqueries for row-level comparisons
- Distinguish between IN / EXISTS / NOT EXISTS patterns
- Recognize performance implications of subqueries
- Prepare for window functions and advanced analytical SQL

---

## 📂 Files & Progress

Each file represents a focused learning unit with
**practical SQL examples and detailed Korean explanations**.

각 파일은 실무에서 자주 사용되는 패턴을 중심으로 구성되어 있으며,
서브쿼리의 장점과 주의점을 함께 설명합니다.

---

### ✅ Completed

#### `01_subquery_basic.sql` (Day 12)
**Basic subqueries**

- Subqueries in WHERE clauses
- Scalar subqueries for comparison
- IN / NOT IN patterns
- Subqueries in SELECT and FROM clauses (derived tables)
- NULL handling considerations

> 서브쿼리를 처음 접할 때 반드시 알아야 할
> 기본 구조와 실행 흐름을 다룹니다.

---

#### `02_correlated_subquery.sql` (Day 13)
**Correlated subqueries**

- Subqueries that depend on outer query values
- Row-by-row evaluation
- EXISTS / NOT EXISTS patterns
- Comparing per-row values to group-level aggregates
- Performance considerations

> 상관 서브쿼리는 강력하지만,
> 대용량 데이터에서는 성능을 반드시 고려해야 합니다.

---

## 🧠 Why Subqueries Matter

Subqueries are particularly useful when:

- Filtering data based on aggregated results
- Expressing step-by-step logic clearly
- Checking existence or non-existence of related records
- Performing row-level comparisons without complex joins

However, they can be less efficient than JOINs on large datasets,
so understanding when (and when not) to use them is critical.

---

## 📌 Practical Takeaways (한국어 요약)

- 서브쿼리는 쿼리를 계층적으로 구성하는 핵심 도구
- WHERE / SELECT / FROM 어디든 사용 가능
- 상관 서브쿼리는 행 단위 비교에 매우 유용
- NOT EXISTS는 NULL 문제에 안전한 패턴
- 성능 이슈를 항상 염두에 두고 JOIN 대안 검토 필요

---

## 🚧 Status

**Completed – SQL Subqueries (Day 12–13)**

This module serves as a conceptual bridge
between aggregation and window functions.

본 단원은 Day 13까지 완료되었으며,  
이후 윈도우 함수(Window Functions) 학습으로 자연스럽게 이어집니다.