/*
Day 13: SQL Window Functions - OVER Clause

This file introduces the OVER clause, which is the foundation
of SQL window (analytic) functions.

OVER allows calculations across a set of rows
related to the current row without collapsing rows.

본 파일은 SQL 윈도우 함수의 핵심인 OVER 절을 다룬다.
OVER 절은 집계 결과를 유지하면서
행 단위 분석을 가능하게 한다.
*/

-- --------------------------------------------------
-- Sample Table Assumption
-- --------------------------------------------------
-- orders
-- | order_id | customer_id | order_date | amount |
--
-- 이 예제들은 위와 같은 주문 테이블이 존재한다고 가정한다.


-- --------------------------------------------------
-- 1. OVER() without PARTITION BY
-- --------------------------------------------------
-- Calculate total sales while keeping each row

SELECT
    order_id,
    customer_id,
    amount,
    SUM(amount) OVER () AS total_sales
FROM orders;

-- 설명:
-- 전체 테이블을 하나의 윈도우로 보고,
-- 모든 행에 동일한 총 매출(total_sales)을 표시한다.
-- GROUP BY와 달리 행 수가 줄어들지 않는다.


-- --------------------------------------------------
-- 2. OVER() with PARTITION BY
-- --------------------------------------------------
-- Calculate total sales per customer

SELECT
    order_id,
    customer_id,
    amount,
    SUM(amount) OVER (PARTITION BY customer_id) AS customer_total
FROM orders;

-- 설명:
-- PARTITION BY는 그룹을 나누는 기준이다.
-- 각 고객(customer_id)별로 독립적인 윈도우가 생성된다.
-- 고객별 총 구매 금액을 각 주문 행에 함께 표시한다.


-- --------------------------------------------------
-- 3. OVER() with ORDER BY
-- --------------------------------------------------
-- Calculate cumulative sales over time

SELECT
    order_id,
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (
        ORDER BY order_date
    ) AS cumulative_sales
FROM orders;

-- 설명:
-- ORDER BY를 사용하면 누적 계산이 가능하다.
-- 시간 흐름에 따른 누적 매출을 계산할 때 매우 자주 사용된다.


-- --------------------------------------------------
-- 4. PARTITION BY + ORDER BY
-- --------------------------------------------------
-- Cumulative sales per customer

SELECT
    order_id,
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS customer_cumulative_sales
FROM orders;

-- 설명:
-- 고객별로 파티션을 나눈 뒤,
-- 각 고객 내부에서 날짜 순서대로 누적 합계를 계산한다.
-- 고객 행동 분석, LTV 분석의 기본 패턴이다.


-- --------------------------------------------------
-- 5. OVER vs GROUP BY (Conceptual Difference)
-- --------------------------------------------------
-- GROUP BY:
--   - Aggregates rows
--   - Reduces result set
--
-- OVER:
--   - Preserves rows
--   - Adds analytical insight per row

-- OVER는 분석 SQL, GROUP BY는 요약 SQL에 가깝다.


-- --------------------------------------------------
-- Summary
-- --------------------------------------------------
-- - OVER() is the foundation of window functions
-- - PARTITION BY defines analysis groups
-- - ORDER BY enables cumulative calculations
-- - OVER keeps row-level detail while adding context
-- - Essential for analytics, finance, and time-series analysis