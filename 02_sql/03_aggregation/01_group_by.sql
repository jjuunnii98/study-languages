/*
Day 8: SQL Aggregation - GROUP BY

This file introduces GROUP BY, which is used to aggregate data
by one or more columns.

이 파일은 SQL의 GROUP BY 문법을 다룬다.
GROUP BY는 데이터를 특정 기준으로 묶어
요약 통계(집계 결과)를 계산할 때 사용한다.
*/

-- -----------------------------------------
-- Example Table (Conceptual)
-- -----------------------------------------
-- Assume we have a table named 'orders'
--
-- orders
-- | order_id | customer_id | category | amount |
-- |----------|-------------|----------|--------|
-- | 1        | 101         | Food     | 120    |
-- | 2        | 102         | Tech     | 450    |
-- | 3        | 101         | Food     | 80     |
-- | 4        | 103         | Fashion  | 200    |

-- -----------------------------------------
-- 1. Basic GROUP BY
-- -----------------------------------------
-- Aggregate total amount by category
-- 카테고리별 총 매출액 계산

SELECT
    category, 
    SUM(amount) AS total_amount
FROM orders
GROUP BY category;

-- 핵심 포인트:
-- SELECT 절에 집계 함수(SUM)가 아닌 컬럼은
-- 반드시 GROUP BY 절에 포함되어야 한다.

-- -----------------------------------------
-- 2. GROUP BY with COUNT
-- -----------------------------------------
-- Count number of orders per customer
-- 고객별 주문 건수 계산

SELECT
    customer_id, 
    COUNT(*) AS order_count
FROM orders
GROUP BY customer_id;

-- COUNT(*)는 NULL 여부와 상관없이 행(row) 수를 센다.

-- -----------------------------------------
-- 3. GROUP BY with AVG
-- -----------------------------------------
-- Average order amount per category
-- 카테고리별 평균 주문 금액 계산

SELECT
    category, 
    AVG(amount) AS avg_amount
FROM orders
GROUP BY category;

-- -----------------------------------------
-- 4. GROUP BY multiple columns
-- -----------------------------------------
-- Aggregate by customer and category
-- 고객 + 카테고리 조합별 매출 합계

SELECT
    customer_id, 
    category, 
    SUM(amount) AS total_amount
FROM orders
GROUP BY customer_id, category;

-- GROUP BY는 여러 컬럼을 동시에 사용할 수 있으며, 
-- 이 경우 각 조합이 하나의 그룹이 된다. 

-- -----------------------------------------
-- 5. GROUP BY + ORDER BY
-- -----------------------------------------
-- Sort aggregated results
-- 집계 결과를 기준으로 정렬

SELECT
    category,
    SUM(amount) AS total_amount
FROM orders
GROUP BY category
ORDER BY total_amount DESC;

-- -----------------------------------------
-- Summary
-- -----------------------------------------
-- GROUP BY is essential for:
-- - Exploratory Data Analysis (EDA)
-- - Business reporting
-- - Feature engineering for ML
--
-- GROUP BY는 데이터 분석과 머신러닝 전처리의 핵심 도구이다.