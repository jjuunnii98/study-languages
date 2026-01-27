/*
Day 22: SQL Query Optimization

This file focuses on practical SQL query optimization techniques.
The goal is not only to write correct queries,
but to write queries that scale efficiently.

본 파일은 실행 계획(EXPLAIN)을 기반으로
쿼리 성능을 개선하는 실무 최적화 패턴을 다룬다.
*/


-- ------------------------------------------------------------
-- 1) Use EXPLAIN / EXPLAIN ANALYZE
-- ------------------------------------------------------------
-- 쿼리를 최적화하기 전에 반드시 실행 계획을 확인해야 한다.
-- 실제 데이터베이스에서는 "느린 이유"를 감으로 판단하면 안 된다.

-- PostgreSQL 예시
-- EXPLAIN ANALYZE
-- SELECT *
-- FROM orders
-- WHERE customer_id = 1001;


-- ------------------------------------------------------------
-- 2) Avoid SELECT *
-- ------------------------------------------------------------
-- SELECT * 는 불필요한 컬럼까지 모두 읽게 하여
-- I/O 비용과 메모리 사용량을 증가시킨다.

-- ❌ 비추천
SELECT *
FROM orders
WHERE order_date >= '2026-01-01';

-- ✅ 추천: 필요한 컬럼만 선택
SELECT order_id, customer_id, order_date, total_amount
FROM orders
WHERE order_date >= '2026-01-01';


-- ------------------------------------------------------------
-- 3) Filtering Early (WHERE 먼저 적용)
-- ------------------------------------------------------------
-- WHERE 조건은 가능한 한 빨리 적용되어야 한다.
-- 불필요한 데이터가 JOIN으로 확산되는 것을 막는다.

-- ❌ 비효율적인 패턴
SELECT o.order_id, c.customer_name
FROM orders o
JOIN customers c
  ON o.customer_id = c.customer_id
WHERE o.order_date >= '2026-01-01';

-- (개념적으로) orders에서 먼저 필터링된 결과가 JOIN되는 것이 이상적


-- ------------------------------------------------------------
-- 4) EXISTS vs IN
-- ------------------------------------------------------------
-- 서브쿼리에서는 IN보다 EXISTS가 더 효율적인 경우가 많다.

-- ❌ IN (서브쿼리 결과가 클 경우 비효율)
SELECT *
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM orders
    WHERE order_date >= '2026-01-01'
);

-- ✅ EXISTS (행 존재 여부만 확인)
SELECT *
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
      AND o.order_date >= '2026-01-01'
);


-- ------------------------------------------------------------
-- 5) Optimize GROUP BY
-- ------------------------------------------------------------
-- GROUP BY는 비용이 높은 연산이다.
-- 불필요한 컬럼을 포함하지 말아야 한다.

-- ❌ 과도한 GROUP BY
SELECT customer_id, order_date, SUM(total_amount)
FROM orders
GROUP BY customer_id, order_date;

-- ✅ 분석 목적에 맞게 최소화
SELECT customer_id, SUM(total_amount)
FROM orders
GROUP BY customer_id;


-- ------------------------------------------------------------
-- 6) LIMIT + ORDER BY Optimization
-- ------------------------------------------------------------
-- 최신 데이터나 상위 N개만 필요할 경우
-- LIMIT는 매우 강력한 성능 최적화 도구다.

SELECT order_id, order_date, total_amount
FROM orders
ORDER BY order_date DESC
LIMIT 10;

-- order_date에 인덱스가 있다면
-- 전체 정렬 대신 인덱스를 활용한 빠른 조회가 가능하다.


-- ------------------------------------------------------------
-- 7) JOIN Size Reduction Pattern
-- ------------------------------------------------------------
-- 대용량 테이블 간 JOIN은
-- 서브쿼리로 데이터 크기를 줄인 후 수행하는 것이 좋다.

SELECT o.order_id, o.total_amount, c.customer_name
FROM (
    SELECT order_id, customer_id, total_amount
    FROM orders
    WHERE order_date >= '2026-01-01'
) o
JOIN customers c
  ON o.customer_id = c.customer_id;


-- ------------------------------------------------------------
-- 8) Index-Aware Conditions
-- ------------------------------------------------------------
-- WHERE 절에서 컬럼에 함수를 적용하면
-- 인덱스를 사용할 수 없는 경우가 많다.

-- ❌ 인덱스 사용 불가
SELECT *
FROM orders
WHERE DATE(order_date) = '2026-01-01';

-- ✅ 인덱스 친화적
SELECT *
FROM orders
WHERE order_date >= '2026-01-01'
  AND order_date < '2026-01-02';


-- ------------------------------------------------------------
-- Day 22 Summary
-- ------------------------------------------------------------
-- - 쿼리 최적화는 반드시 실행 계획을 기반으로 한다
-- - SELECT * 대신 필요한 컬럼만 조회
-- - EXISTS, LIMIT, 인덱스 친화적 조건을 적극 활용
-- - "작은 데이터로 JOIN"하는 것이 핵심 전략