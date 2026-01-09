/*
Day 12: SQL Subqueries - Basic Concepts

This file introduces basic SQL subqueries and how they are used
to build more expressive and readable queries.

이 파일은 SQL 서브쿼리(subquery)의 기본 개념을 다룬다.
서브쿼리는 하나의 쿼리 안에 또 다른 쿼리를 포함하여
복잡한 조건과 계산을 단계적으로 표현할 수 있게 해준다.
*/

-- ----------------------------------------------------
-- Example Tables (Conceptual)
-- ----------------------------------------------------
-- customers
-- | customer_id | name  | country |
--
-- orders
-- | order_id | customer_id | amount |
--
-- 가정:
-- - customers와 orders는 customer_id로 연결된다
-- - 한 고객은 여러 주문을 가질 수 있다

-- ----------------------------------------------------
-- 1. Subquery in WHERE (Scalar Subquery)
-- ----------------------------------------------------
-- Find customers whose order amount is higher than the average order amount
-- 평균 주문 금액보다 큰 주문을 한 고객 찾기

SELECT
  order_id,
  customer_id,
  amount
FROM orders
WHERE amount > (
  SELECT AVG(amount)
  FROM orders
);

-- 설명:
-- - 괄호 안의 서브쿼리가 먼저 실행됨
-- - 전체 주문의 평균 금액을 계산
-- - 바깥 쿼리는 그 평균보다 큰 주문만 선택


-- ----------------------------------------------------
-- 2. Subquery with IN
-- ----------------------------------------------------
-- Find customers who have placed at least one order
-- 주문을 한 번이라도 한 고객 찾기

SELECT
  customer_id,
  name
FROM customers
WHERE customer_id IN (
  SELECT DISTINCT customer_id
  FROM orders
);

-- 설명:
-- - 서브쿼리는 주문 테이블에 존재하는 customer_id 목록 반환
-- - IN은 해당 목록에 포함된 고객만 필터링
-- - DISTINCT는 중복 제거 목적


-- ----------------------------------------------------
-- 3. Subquery with NOT IN
-- ----------------------------------------------------
-- Find customers who have never placed an order
-- 주문 기록이 없는 고객 찾기

SELECT
  customer_id,
  name
FROM customers
WHERE customer_id NOT IN (
  SELECT customer_id
  FROM orders
  WHERE customer_id IS NOT NULL
);

-- 주의:
-- - NOT IN 서브쿼리에 NULL이 포함되면 결과가 비어질 수 있음
-- - 따라서 서브쿼리에서 NULL을 반드시 제거하는 것이 안전함


-- ----------------------------------------------------
-- 4. Subquery in SELECT clause
-- ----------------------------------------------------
-- Show each order with the overall average amount
-- 각 주문과 전체 평균 주문 금액을 함께 표시

SELECT
  order_id,
  amount,
  (
    SELECT AVG(amount)
    FROM orders
  ) AS overall_avg_amount
FROM orders;

-- 설명:
-- - SELECT 절의 서브쿼리는 각 행마다 동일한 값 반환
-- - 분석/비교용 컬럼으로 자주 사용됨


-- ----------------------------------------------------
-- 5. Subquery in FROM clause (Derived Table)
-- ----------------------------------------------------
-- Calculate total spending per customer, then filter
-- 고객별 총 지출을 계산한 뒤 조건 적용

SELECT
  customer_id,
  total_spent
FROM (
  SELECT
    customer_id,
    SUM(amount) AS total_spent
  FROM orders
  GROUP BY customer_id
) AS customer_totals
WHERE total_spent > 1000;

-- 설명:
-- - FROM 절의 서브쿼리는 임시 테이블(derived table)처럼 동작
-- - 복잡한 집계 로직을 단계적으로 분리할 수 있음


-- ----------------------------------------------------
-- 6. When to use Subqueries
-- ----------------------------------------------------
-- Use subqueries when:
-- - A value depends on aggregated results
-- - Step-by-step logic improves readability
-- - JOIN would make the query harder to understand
--
-- 서브쿼리는:
-- - 평균/합계 등 집계 결과를 기준으로 필터링할 때
-- - 복잡한 로직을 단계적으로 표현하고 싶을 때 유용함


-- ----------------------------------------------------
-- Summary
-- ----------------------------------------------------
-- - Subqueries are queries inside queries
-- - They can appear in WHERE, SELECT, FROM
-- - IN / NOT IN are common patterns
-- - NULL handling is critical for NOT IN
--
-- 요약:
-- - 서브쿼리는 쿼리를 계층적으로 구성하는 도구
-- - WHERE / SELECT / FROM 어디든 사용 가능
-- - NOT IN 사용 시 NULL 처리 주의
-- - 가독성과 논리 분리를 위해 적극 활용 가능