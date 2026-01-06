/*
Day 11: SQL Aggregation - COUNT / SUM / AVG

This file explains the most common aggregation functions:
COUNT, SUM, and AVG, with practical notes on NULL handling.

이 파일은 SQL 집계 함수 COUNT / SUM / AVG를 다룬다.
실무에서 가장 많이 쓰이며, NULL 처리 방식 때문에 실수하기 쉬운 파트다.
*/

-- -----------------------------------------
-- Example Table (Conceptual)
-- -----------------------------------------
-- Assume we have a table named 'payments'
--
-- payments
-- | payment_id | customer_id | category | amount |
-- |------------|-------------|----------|--------|
-- | 1          | 101         | Food     | 120    |
-- | 2          | 101         | Food     | NULL   |
-- | 3          | 102         | Tech     | 450    |
-- | 4          | 102         | Tech     | 0      |
-- | 5          | 103         | Fashion  | 200    |
--
-- Note:
-- - amount can be NULL (missing)
-- - amount can be 0 (valid value)
--
-- 주의:
-- - NULL은 "값이 없음" (결측)
-- - 0은 "값이 0" (유효한 값)

-- -----------------------------------------
-- 1. COUNT(*) vs COUNT(column)
-- -----------------------------------------

-- (1) COUNT(*) counts all rows, including rows where amount is NULL
-- COUNT(*)는 NULL 여부와 상관없이 "행(row) 수"를 센다.
SELECT
  category,
  COUNT(*) AS row_count
FROM payments
GROUP BY category;

-- (2) COUNT(amount) counts only non-NULL values in amount
-- COUNT(amount)는 amount가 NULL이 아닌 행만 센다.
SELECT
  category,
  COUNT(amount) AS non_null_amount_count
FROM payments
GROUP BY category;

-- 실무 포인트:
-- - "데이터가 몇 건 있나?" → COUNT(*)
-- - "금액이 실제로 기록된 건수는?" → COUNT(amount)


-- -----------------------------------------
-- 2. SUM(column) and NULL behavior
-- -----------------------------------------

-- SUM ignores NULL values (it sums only non-NULL values)
-- SUM은 NULL을 무시하고, NULL이 아닌 값만 더한다.
SELECT
  category,
  SUM(amount) AS total_amount
FROM payments
GROUP BY category;

-- If all values in a group are NULL, SUM(amount) may return NULL (DBMS dependent)
-- 그룹 내 값이 전부 NULL이면 SUM 결과가 NULL이 될 수 있다.
-- 이 경우 COALESCE로 안전하게 0 처리하는 패턴이 흔하다.
SELECT
  category,
  COALESCE(SUM(amount), 0) AS total_amount_safe
FROM payments
GROUP BY category;

-- 실무 포인트:
-- - SUM(NULL)처럼 "전부 NULL"인 그룹이 생길 수 있는 데이터(로그/의료/설문)는
--   COALESCE(SUM(col), 0) 패턴을 자주 사용한다.


-- -----------------------------------------
-- 3. AVG(column) and NULL behavior
-- -----------------------------------------

-- AVG ignores NULL values
-- AVG 역시 NULL을 무시하고 평균을 계산한다.
SELECT
  category,
  AVG(amount) AS avg_amount
FROM payments
GROUP BY category;

-- AVG is equivalent to SUM(amount)/COUNT(amount) for non-NULL values
-- AVG는 SUM(amount)/COUNT(amount)와 같은 의미(비NULL 기준)
SELECT
  category,
  SUM(amount) AS sum_amount,
  COUNT(amount) AS cnt_amount,
  SUM(amount) / COUNT(amount) AS avg_amount_manual
FROM payments
GROUP BY category;

-- 주의:
-- - amount가 정수형(integer)일 때,
--   DBMS에 따라 정수 나눗셈이 발생할 수 있다.
--   이 경우 CAST를 사용해 소수점 평균을 보장한다.
SELECT
  category,
  CAST(SUM(amount) AS DOUBLE) / NULLIF(COUNT(amount), 0) AS avg_amount_float
FROM payments
GROUP BY category;

-- 한국어 설명:
-- - NULLIF(x,0): 0이면 NULL로 바꿔서 나눗셈 오류(0으로 나눔)를 방지
-- - CAST: 정수 나눗셈 방지 (DBMS별 타입명은 다를 수 있음)


-- -----------------------------------------
-- 4. Aggregation by customer (feature engineering example)
-- -----------------------------------------
-- Example: build customer-level features
-- 고객 단위 파생변수(feature) 예시 (ML feature engineering)
SELECT
  customer_id,
  COUNT(*) AS payment_rows,                  -- 전체 결제 기록 수
  COUNT(amount) AS amount_recorded_rows,     -- 금액이 기록된 결제 수
  COALESCE(SUM(amount), 0) AS total_spent,   -- 총 지출
  AVG(amount) AS avg_spent_per_payment       -- 결제당 평균 지출(비NULL 기준)
FROM payments
GROUP BY customer_id
ORDER BY total_spent DESC;

-- 실무 포인트:
-- - 이런 집계 테이블은 모델링/리포트의 핵심 베이스가 된다.


-- -----------------------------------------
-- 5. Common mistakes (핵심 실수 방지)
-- -----------------------------------------

-- (1) COUNT(amount) != COUNT(*) when NULL exists
-- NULL이 있으면 COUNT(amount)와 COUNT(*)는 다르게 나온다.

-- (2) SUM/AVG ignore NULL, but "all NULL group" can yield NULL
-- 전체가 NULL인 그룹은 SUM/AVG가 NULL이 될 수 있으니 COALESCE 고려

-- (3) 0 vs NULL are different
-- 0은 유효 값, NULL은 결측 → 데이터 의미가 완전히 다름


-- -----------------------------------------
-- Summary
-- -----------------------------------------
-- - COUNT(*) counts rows
-- - COUNT(col) counts non-NULL values
-- - SUM/AVG ignore NULL values
-- - Use COALESCE and NULLIF to make aggregations robust
--
-- 요약:
-- - COUNT(*)는 행 개수
-- - COUNT(col)은 결측 제외 개수
-- - SUM/AVG는 NULL 무시
-- - COALESCE/NULLIF로 안정적인 집계 쿼리 작성