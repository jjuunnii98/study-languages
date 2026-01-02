/*
Day 10: SQL Aggregation - HAVING

HAVING is used to filter aggregated results (groups).
WHERE filters rows before grouping.
HAVING filters groups after GROUP BY.

HAVING은 "집계된 결과(그룹)"를 필터링할 때 사용한다.
- WHERE: 그룹핑 이전의 개별 행(row)을 필터링
- HAVING: GROUP BY 이후의 그룹 결과를 필터링

즉, 집계 함수(SUM, COUNT, AVG 등)를 조건에 쓰고 싶으면
대부분 HAVING을 사용해야 한다.
*/

-- -----------------------------------------
-- Example Table (Conceptual)
-- -----------------------------------------
-- orders
-- | order_id | customer_id | category | amount |
-- |----------|-------------|----------|--------|
-- | 1        | 101         | Food     | 120    |
-- | 2        | 102         | Tech     | 450    |
-- | 3        | 101         | Food     | 80     |
-- | 4        | 103         | Fashion  | 200    |
-- | 5        | 101         | Tech     | 300    |

-- -----------------------------------------
-- 1. Basic HAVING with SUM
-- -----------------------------------------
-- Find categories with total sales >= 300
-- 카테고리별 총 매출이 300 이상인 카테고리만 추출

SELECT
    category,
    SUM(amount) AS total_amount
FROM orders
GROUP BY category
HAVING SUM(amount) >= 300;

-- 한국어 해설:
-- - WHERE SUM(amount) >= 300 은 대부분 DB에서 오류 또는 의도와 다르게 동작
-- - 집계값 조건은 HAVING에 작성

-- -----------------------------------------
-- 2. HAVING with COUNT
-- -----------------------------------------
-- Find customers with 2 or more orders
-- 주문 건수가 2건 이상인 고객만 추출

SELECT
    customer_id,
    COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 2;

-- -----------------------------------------
-- 3. WHERE + GROUP BY + HAVING (실무에서 가장 흔함)
-- -----------------------------------------
-- Step 1) WHERE: filter rows first (e.g., only Food category orders)
-- Step 2) GROUP BY: aggregate
-- Step 3) HAVING: filter groups

-- 예: Food 카테고리 주문만 대상으로,
-- 고객별 총 매출이 150 이상인 고객만 추출

SELECT
    customer_id,
    SUM(amount) AS total_amount
FROM orders
WHERE category = 'Food'
GROUP BY customer_id
HAVING SUM(amount) >= 150;

-- 핵심:
-- - WHERE는 "Food 주문 행"만 남긴 뒤 그룹핑
-- - HAVING은 그 결과 그룹(고객)의 SUM(amount) 조건 적용

-- -----------------------------------------
-- 4. HAVING with AVG (평균 기준 필터링)
-- -----------------------------------------
-- Find categories with average order amount > 200
-- 카테고리별 평균 주문 금액이 200 초과인 카테고리만 추출

SELECT
    category,
    AVG(amount) AS avg_amount
FROM orders
GROUP BY category
HAVING AVG(amount) > 200;

-- -----------------------------------------
-- 5. HAVING with multiple conditions
-- -----------------------------------------
-- Find categories that satisfy multiple aggregate constraints
-- 여러 집계 조건을 동시에 적용

SELECT
    category,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount
FROM orders
GROUP BY category
HAVING COUNT(*) >= 2
   AND SUM(amount) >= 300;

-- -----------------------------------------
-- 6. Common Mistake (실수 포인트)
-- -----------------------------------------
-- ❌ Wrong idea: trying to filter aggregated results with WHERE
-- 아래는 대부분 DB에서 오류를 발생시키거나(집계함수 사용 불가),
-- 의도와 다르게 동작한다.

-- SELECT category, SUM(amount)
-- FROM orders
-- WHERE SUM(amount) >= 300
-- GROUP BY category;

-- ✅ Correct: use HAVING

-- -----------------------------------------
-- Summary
-- -----------------------------------------
-- - WHERE filters rows BEFORE grouping
-- - HAVING filters groups AFTER grouping
-- - Use HAVING for aggregate conditions (SUM/COUNT/AVG)
--
-- - WHERE: 그룹 이전 행 필터
-- - HAVING: 그룹 이후 집계 결과 필터
-- - 집계 조건은 HAVING이 정석