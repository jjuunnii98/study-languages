/*
Day 13: SQL Correlated Subqueries

This file introduces correlated subqueries.
A correlated subquery depends on values from the outer query
and is executed once per row.

이 파일은 상관 서브쿼리(correlated subquery)를 다룬다.
상관 서브쿼리는 바깥 쿼리의 값을 참조하며,
행(row)마다 반복 실행되는 특징을 가진다.
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
-- - customers와 orders는 customer_id로 연결됨
-- - 한 고객은 여러 주문을 가질 수 있음

-- ----------------------------------------------------
-- 1. Basic Correlated Subquery (WHERE)
-- ----------------------------------------------------
-- Find orders that are higher than the customer's average order amount
-- 각 고객의 평균 주문 금액보다 큰 주문 찾기

SELECT
  o.order_id,
  o.customer_id,
  o.amount
FROM orders o
WHERE o.amount > (
  SELECT AVG(i.amount)
  FROM orders i
  WHERE i.customer_id = o.customer_id
);

-- 설명:
-- - 바깥 쿼리(o)의 customer_id를
--   서브쿼리(i)가 참조함
-- - 고객별 평균 주문 금액이 매 행마다 다시 계산됨
-- - 이런 구조를 "상관 서브쿼리"라고 부른다


-- ----------------------------------------------------
-- 2. Correlated Subquery with EXISTS
-- ----------------------------------------------------
-- Find customers who have at least one order above 1000
-- 1000 초과 주문이 하나라도 있는 고객 찾기

SELECT
  c.customer_id,
  c.name
FROM customers c
WHERE EXISTS (
  SELECT 1
  FROM orders o
  WHERE o.customer_id = c.customer_id
    AND o.amount > 1000
);

-- 설명:
-- - EXISTS는 조건을 만족하는 행이 "존재하는지"만 확인
-- - 실제 반환 값은 중요하지 않으므로 SELECT 1 사용
-- - EXISTS는 IN보다 성능이 좋은 경우가 많음


-- ----------------------------------------------------
-- 3. Correlated Subquery with NOT EXISTS
-- ----------------------------------------------------
-- Find customers who have no orders
-- 주문 기록이 없는 고객 찾기

SELECT
  c.customer_id,
  c.name
FROM customers c
WHERE NOT EXISTS (
  SELECT 1
  FROM orders o
  WHERE o.customer_id = c.customer_id
);

-- 설명:
-- - NOT EXISTS는 NULL 문제에 강함
-- - NOT IN보다 실무에서 더 안전하게 사용됨


-- ----------------------------------------------------
-- 4. Correlated Subquery in SELECT clause
-- ----------------------------------------------------
-- Show each customer with their total spending
-- 고객별 총 지출 금액을 함께 표시

SELECT
  c.customer_id,
  c.name,
  (
    SELECT SUM(o.amount)
    FROM orders o
    WHERE o.customer_id = c.customer_id
  ) AS total_spent
FROM customers c;

-- 설명:
-- - SELECT 절의 상관 서브쿼리는
--   각 고객마다 다른 결과를 반환
-- - 분석용 컬럼 생성에 자주 사용됨


-- ----------------------------------------------------
-- 5. Performance Considerations
-- ----------------------------------------------------
-- Correlated subqueries can be expensive:
-- - Executed once per outer row
-- - May cause performance issues on large tables
--
-- 실무에서는:
-- - JOIN + GROUP BY로 대체 가능한지 검토
-- - EXISTS는 비교적 효율적
-- - 가독성과 성능을 함께 고려해야 함


-- ----------------------------------------------------
-- Summary
-- ----------------------------------------------------
-- - Correlated subqueries depend on outer query values
-- - They are executed per row
-- - Common patterns: WHERE, EXISTS, SELECT
-- - Powerful but potentially slow on large datasets
--
-- 요약:
-- - 상관 서브쿼리는 바깥 쿼리와 연결된 서브쿼리
-- - 행 단위 비교에 매우 유용
-- - 성능 이슈를 항상 염두에 두어야 함