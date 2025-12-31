/*
Day (SQL): RIGHT JOIN

This file demonstrates how RIGHT JOIN works in SQL.
RIGHT JOIN returns all rows from the right table,
and matching rows from the left table.
If there is no match, NULL values are returned on the left side.

본 파일은 RIGHT JOIN의 개념과 사용 목적을 설명한다.
RIGHT JOIN은 "오른쪽 테이블의 모든 행을 유지"하면서,
왼쪽 테이블과 매칭되는 데이터가 있으면 붙이고,
없으면 왼쪽 컬럼을 NULL로 채운다.

실무에서는 LEFT JOIN을 더 자주 사용하지만,
RIGHT JOIN의 동작 원리를 이해하는 것은 JOIN 사고력을 높이는 데 중요하다.
*/

--------------------------------------------------
-- 1. Example Tables (가상 예시)
--------------------------------------------------
-- customers
-- | customer_id | name  |
-- |-------------|-------|
-- | 1           | Alice |
-- | 2           | Bob   |

-- orders
-- | order_id | customer_id | amount |
-- |----------|-------------|--------|
-- | 101      | 1           | 120.00 |
-- | 102      | 1           | 80.00  |
-- | 103      | 2           | 50.00  |
-- | 104      | 4           | 60.00  |  -- 고객 테이블에 없는 customer_id

--------------------------------------------------
-- 2. RIGHT JOIN 기본 문법
--------------------------------------------------
-- 오른쪽 테이블(orders)의 모든 행을 유지
-- 왼쪽 테이블(customers)은 매칭되는 경우만 연결

SELECT
    c.customer_id,
    c.name,
    o.order_id,
    o.amount
FROM customers c
RIGHT JOIN orders o
    ON c.customer_id = o.customer_id;

--------------------------------------------------
-- 결과 해석 (중요)
--------------------------------------------------
-- order_id=101,102 → Alice
-- order_id=103     → Bob
-- order_id=104     → 고객 정보 없음 → c.customer_id, c.name = NULL

--------------------------------------------------
-- 3. RIGHT JOIN vs LEFT JOIN
--------------------------------------------------
-- RIGHT JOIN은 다음과 같은 LEFT JOIN과 동일한 결과를 낸다:

-- SELECT ...
-- FROM orders o
-- LEFT JOIN customers c
--     ON c.customer_id = o.customer_id;

-- 👉 대부분의 SQL 분석에서는
-- RIGHT JOIN 대신 LEFT JOIN으로 방향을 통일하는 것이 가독성이 좋다.

--------------------------------------------------
-- 4. WHERE 조건 주의사항
--------------------------------------------------
-- RIGHT JOIN에서도 WHERE 절 조건에 따라
-- JOIN의 의미가 바뀔 수 있다.

-- ❌ 잘못된 예:
SELECT
    c.customer_id,
    c.name,
    o.order_id,
    o.amount
FROM customers c
RIGHT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE c.customer_id IS NOT NULL;

-- 위 쿼리는 고객 정보가 없는 주문(order_id=104)을 제거한다.

--------------------------------------------------
-- 5. 올바른 조건 처리 (ON 절 활용)
--------------------------------------------------
SELECT
    c.customer_id,
    c.name,
    o.order_id,
    o.amount
FROM customers c
RIGHT JOIN orders o
    ON c.customer_id = o.customer_id
   AND c.customer_id IS NOT NULL;

-- 이렇게 하면 RIGHT JOIN의 "오른쪽 기준 유지" 의미를 보존할 수 있다.

--------------------------------------------------
-- 6. NULL 기반 분석 패턴
--------------------------------------------------
-- 고객 정보가 없는 주문 찾기
-- (데이터 품질 점검, FK 무결성 검사)

SELECT
    o.order_id,
    o.customer_id,
    o.amount
FROM customers c
RIGHT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL;

--------------------------------------------------
-- 7. 실무 요약
--------------------------------------------------
-- RIGHT JOIN 핵심 포인트:
-- - 오른쪽 테이블을 기준으로 데이터 유지
-- - 대부분 LEFT JOIN으로 대체 가능
-- - 데이터 품질 점검, 참조 누락 탐지에 유용
--
-- 분석 표준:
-- 👉 LEFT JOIN 중심으로 사고하고,
-- 👉 RIGHT JOIN은 "방향 전환 개념"으로 이해하자.