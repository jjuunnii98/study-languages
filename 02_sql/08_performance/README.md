# SQL Performance

This directory covers **SQL performance fundamentals** and practical optimization patterns.
The focus is on writing SQL that not only works correctly, but also scales efficiently
as data volume grows.

본 폴더는 SQL의 **성능(Performance) 최적화**를 다룹니다.  
단순히 “동작하는 쿼리”를 넘어, 데이터가 커져도 안정적으로 동작하는
**확장 가능한 쿼리 작성 패턴**을 목표로 합니다.

---

## 🎯 Learning Objectives

- Understand how indexes speed up data access
- Design effective single-column and composite indexes
- Read and interpret query plans (EXPLAIN / EXPLAIN ANALYZE)
- Optimize queries by reducing I/O and avoiding unnecessary work
- Write index-friendly filters and scalable joins/aggregations

---

## 📂 Files & Progress

### `01_indexes.sql` (Day 21, indexes)
Indexes and index design patterns

- Why indexes matter (full scan vs index scan)
- Basic index creation for frequent filters (WHERE)
- Composite index design and column order considerations
- Join performance and indexing join keys
- Index-aware sorting (ORDER BY) and grouping implications
- When **not** to index (low-cardinality columns, heavy writes)
- Query plan mindset (conceptual EXPLAIN usage)

**한국어 요약**
- 인덱스의 목적과 성능 개선 원리 이해
- 단일/복합 인덱스 설계 기준 및 컬럼 순서의 중요성
- JOIN/ORDER BY 상황에서 인덱스 활용 패턴
- “인덱스가 항상 정답은 아니다”는 비용 관점까지 포함

---

### `02_query_optimization.sql` (Day 22, performance)
Query optimization patterns guided by execution plans

- Always start with EXPLAIN / EXPLAIN ANALYZE (plan-driven optimization)
- Avoid `SELECT *` to reduce I/O and memory usage
- Filter early to prevent join explosion
- Prefer `EXISTS` over `IN` in large subqueries (when appropriate)
- Reduce GROUP BY scope to only required dimensions
- Use ORDER BY + LIMIT for top-N patterns
- Join after reducing the dataset (subquery/CTE pre-filtering)
- Write index-friendly conditions (avoid functions on indexed columns)

**한국어 요약**
- 실행 계획 기반 최적화 사고(EXPLAIN 중심)
- 불필요한 컬럼 조회/정렬/집계를 줄이는 전략
- 대용량 JOIN 전 “데이터 축소” 패턴
- 인덱스를 타는 WHERE 조건 작성법(함수 적용 회피)

---

## 🧠 Why Performance Matters

Performance optimization is essential because:
- Slow queries block pipelines and dashboards
- Costs increase with data size (compute, memory, I/O)
- Well-optimized SQL improves reliability and scalability

SQL 성능은 단순 “속도” 문제가 아니라,
- 파이프라인/대시보드 안정성
- 비용(컴퓨팅/스토리지)
- 서비스 확장성  
까지 직결되는 핵심 역량입니다.

---

## 🚧 Status

**Completed — Performance (Day 21–22)**

Next recommended extensions:
- Advanced analytics patterns (cohorts, funnels, retention)
- Data modeling for analytics (fact/dimension, star schema)
- SQL for ML (feature engineering, leakage prevention)

본 파트는 Day 21–22까지 완료되었습니다.  
이후 단계는 분석 패턴/데이터 모델링/ML용 SQL로 확장됩니다.