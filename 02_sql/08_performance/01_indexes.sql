/*
Day 21: SQL Indexes (Performance Optimization)

This file introduces SQL indexes and explains how they improve query performance.

Indexes are one of the most important tools for scaling databases.
A well-designed index can reduce query time from seconds to milliseconds.

본 파일은 SQL 인덱스의 개념, 생성 방법, 그리고 실무에서의 사용 패턴을 다룬다.
*/


-- ------------------------------------------------------------
-- 1) Why Indexes Matter
-- ------------------------------------------------------------
-- 인덱스가 없으면 데이터베이스는 Full Table Scan을 수행한다.
-- 즉, 조건에 맞는 행을 찾기 위해 테이블 전체를 순차적으로 읽는다.

-- 예시 쿼리 (인덱스 없음)
SELECT *
FROM orders
WHERE customer_id = 1001;


-- ------------------------------------------------------------
-- 2) Creating a Basic Index
-- ------------------------------------------------------------
-- 특정 컬럼에 대한 조회가 빈번하다면 인덱스를 생성하는 것이 좋다.

CREATE INDEX idx_orders_customer_id
ON orders (customer_id);

-- 이제 동일한 WHERE 조건의 쿼리는
-- 전체 테이블이 아니라 인덱스를 통해 빠르게 탐색된다.


-- ------------------------------------------------------------
-- 3) Index on Multiple Columns (Composite Index)
-- ------------------------------------------------------------
-- 여러 컬럼을 동시에 자주 조회할 경우 복합 인덱스를 고려한다.

CREATE INDEX idx_orders_customer_date
ON orders (customer_id, order_date);

-- 주의:
-- (customer_id, order_date)는
-- customer_id 단독 조회에는 사용 가능하지만
-- order_date 단독 조회에는 사용되지 않는다.
-- (인덱스 컬럼 순서가 중요)


-- ------------------------------------------------------------
-- 4) Indexes for JOIN Performance
-- ------------------------------------------------------------
-- JOIN 조건에 사용되는 컬럼은 거의 항상 인덱스 후보이다.

SELECT o.order_id, c.customer_name
FROM orders o
JOIN customers c
  ON o.customer_id = c.customer_id;

-- customers.customer_id 에 인덱스가 없다면 JOIN 성능이 급격히 저하된다.

CREATE INDEX idx_customers_customer_id
ON customers (customer_id);


-- ------------------------------------------------------------
-- 5) Indexes for ORDER BY and GROUP BY
-- ------------------------------------------------------------
-- ORDER BY / GROUP BY도 인덱스를 활용할 수 있다.

SELECT *
FROM orders
WHERE customer_id = 1001
ORDER BY order_date;

-- (customer_id, order_date) 복합 인덱스가 있다면
-- 정렬 비용을 크게 줄일 수 있다.


-- ------------------------------------------------------------
-- 6) When NOT to Use Indexes
-- ------------------------------------------------------------
-- 인덱스는 항상 좋은 것은 아니다.

-- ❌ 값의 종류가 매우 적은 컬럼 (예: gender, yes/no)
-- ❌ 데이터 변경(INSERT/UPDATE/DELETE)이 매우 잦은 테이블
-- ❌ 소규모 테이블 (Full Scan이 더 빠를 수 있음)

-- 인덱스는 조회 성능을 높이는 대신
-- 쓰기 성능과 저장 공간을 희생한다.


-- ------------------------------------------------------------
-- 7) Checking Query Plans (Conceptual)
-- ------------------------------------------------------------
-- 실제 성능 개선 여부는 실행 계획으로 확인해야 한다.

-- PostgreSQL / MySQL
-- EXPLAIN ANALYZE
-- SELECT *
-- FROM orders
-- WHERE customer_id = 1001;

-- 실행 계획을 통해
-- Index Scan vs Seq Scan 여부를 확인하는 것이 핵심이다.


-- ------------------------------------------------------------
-- Day 21 Summary
-- ------------------------------------------------------------
-- - 인덱스는 조회 성능을 극적으로 개선한다
-- - WHERE / JOIN / ORDER BY 조건에 맞춰 설계해야 한다
-- - 복합 인덱스는 컬럼 순서가 매우 중요하다
-- - 모든 컬럼에 인덱스를 만들면 오히려 성능이 나빠질 수 있다