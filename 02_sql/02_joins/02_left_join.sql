/*
Day (SQL): LEFT JOIN

This file demonstrates how LEFT JOIN works in SQL.
LEFT JOIN returns all rows from the left table,
and matching rows from the right table.
If there is no match, NULL values are returned.

본 파일은 LEFT JOIN의 개념과 사용 목적을 설명한다.
LEFT JOIN은 "왼쪽 테이블의 모든 행을 유지"하면서,
오른쪽 테이블과 매칭되는 데이터가 있으면 붙이고,
없으면 NULL로 채운다.

데이터 분석에서 매우 중요하며,
"기준 테이블을 보존"해야 할 때 필수적으로 사용된다.
*/

--------------------------------------------------
-- 1. Example Tables (가상 예시)
--------------------------------------------------
-- customers
-- | customer_id | name  |
-- |-------------|-------|
-- | 1           | Alice |
-- | 2           | Bob   |
-- | 3           | Chris |

-- orders
-- | order_id | customer_id | amount |
-- |----------|-------------|--------|
-- | 101      | 1           | 120.00 |
-- | 102      | 1           | 80.00  |
-- | 103      | 2           | 50.00  |

--------------------------------------------------
-- 2. LEFT JOIN 기본 문법
--------------------------------------------------
-- 왼쪽 테이블(customers)의 모든 행을 유지
-- 오른쪽 테이블(orders)은 매칭되는 경우만 연결

SELECT
    c.customer_id,
    c.name,
    o.order_id,
    o.amount
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id;

--------------------------------------------------
-- 결과 해석 (중요)
--------------------------------------------------
-- Alice (id=1): 주문 2건 → 2행 생성
-- Bob   (id=2): 주문 1건 → 1행 생성
-- Chris(id=3): 주문 없음 → order_id, amount = NULL

--------------------------------------------------
-- 3. LEFT JOIN vs INNER JOIN 차이
--------------------------------------------------
-- INNER JOIN:
-- - 양쪽 테이블에 모두 존재하는 데이터만 반환
-- LEFT JOIN:
-- - 왼쪽 테이블 기준으로 데이터 보존
--
-- 분석에서는 "데이터가 없는 경우"도
-- 중요한 정보가 되는 경우가 많기 때문에
-- LEFT JOIN이 더 자주 사용된다.

--------------------------------------------------
-- 4. WHERE 조건 주의사항 (매우 중요)
--------------------------------------------------
-- ❌ 잘못된 예:
-- WHERE 절에서 오른쪽 테이블 컬럼에 조건을 걸면
-- LEFT JOIN이 사실상 INNER JOIN처럼 동작할 수 있다.

SELECT
    c.customer_id,
    c.name,
    o.order_id,
    o.amount
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.amount > 50;

-- 위 쿼리는 주문이 없는 고객(Chris)을 제거해버린다.

--------------------------------------------------
-- 5. 올바른 조건 처리 방법
--------------------------------------------------
-- 방법 1: ON 절에 조건을 포함

SELECT
    c.customer_id,
    c.name,
    o.order_id,
    o.amount
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
   AND o.amount > 50;

-- 이렇게 하면 주문이 없는 고객도 유지된다.

--------------------------------------------------
-- 6. NULL을 활용한 분석 패턴
--------------------------------------------------
-- 주문이 "없는" 고객 찾기

SELECT
    c.customer_id,
    c.name
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- 👉 미구매 고객, 미이용 사용자 분석에 매우 중요

--------------------------------------------------
-- 7. 실무 활용 예시 요약
--------------------------------------------------
-- LEFT JOIN은 다음 상황에서 핵심적으로 사용된다:
-- - 전체 사용자 기준 분석
-- - 결측 데이터(없는 경우) 확인
-- - 유지율, 이탈률 분석
-- - 기준 테이블을 보존해야 하는 리포트
--
-- LEFT JOIN은 "데이터를 버리지 않는 JOIN"이다.