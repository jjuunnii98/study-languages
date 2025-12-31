/*
Day (SQL): FULL OUTER JOIN

FULL OUTER JOIN returns all rows from both tables:
- matched rows are merged
- unmatched rows from either side are kept
- missing side columns become NULL

FULL OUTER JOIN은 양쪽 테이블의 모든 행을 유지한다.
- 매칭되면 한 행으로 합쳐지고
- 매칭되지 않은 행도 각각 유지되며
- 반대편 컬럼은 NULL로 채워진다.

⚠️ Important:
- PostgreSQL, SQL Server, Oracle: FULL OUTER JOIN 지원
- MySQL: FULL OUTER JOIN 미지원 (대체 구현 필요)
- SQLite: FULL OUTER JOIN 미지원 (대체 구현 필요)

실무에서는 DB 엔진에 따라 "FULL JOIN 대체 쿼리"를 알아야 한다.
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
-- | 104      | 4           | 60.00  |  -- customers에 없는 customer_id

--------------------------------------------------
-- 2. FULL OUTER JOIN (지원하는 DB에서)
--------------------------------------------------
-- ✅ PostgreSQL / SQL Server / Oracle 등에서는 아래 쿼리 사용 가능

SELECT
    c.customer_id AS customer_id_left,
    c.name,
    o.order_id,
    o.customer_id AS customer_id_right,
    o.amount
FROM customers c
FULL OUTER JOIN orders o
    ON c.customer_id = o.customer_id;

--------------------------------------------------
-- 결과 해석 (중요)
--------------------------------------------------
-- (1) customer_id=1: 고객(Alice) + 주문(101, 102) → 2행
-- (2) customer_id=2: 고객(Bob)   + 주문(103)      → 1행
-- (3) customer_id=3: 고객(Chris) + 주문 없음       → order쪽 컬럼 NULL
-- (4) customer_id=4: 고객 없음   + 주문(104)       → customer쪽 컬럼 NULL

--------------------------------------------------
-- 3. FULL OUTER JOIN을 활용한 "불일치 데이터" 탐지
--------------------------------------------------
-- 고객은 있는데 주문이 없는 경우 (LEFT-only)
-- 주문은 있는데 고객이 없는 경우 (RIGHT-only)

SELECT
    c.customer_id,
    c.name,
    o.order_id,
    o.amount,
    CASE
        WHEN c.customer_id IS NULL THEN 'RIGHT_ONLY (order without customer)'
        WHEN o.order_id IS NULL THEN 'LEFT_ONLY (customer without order)'
        ELSE 'MATCHED'
    END AS match_status
FROM customers c
FULL OUTER JOIN orders o
    ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL
   OR o.order_id IS NULL;

-- ✅ 데이터 품질 점검 / FK 무결성 확인 / 누락 데이터 탐지에 유용

--------------------------------------------------
-- 4. MySQL/SQLite에서 FULL OUTER JOIN 대체 구현
--------------------------------------------------
-- MySQL/SQLite는 FULL OUTER JOIN을 지원하지 않으므로,
-- 보통 아래 방식으로 대체한다:
--
-- FULL OUTER JOIN ≈ (LEFT JOIN) UNION (RIGHT JOIN에서 LEFT-only 제거)
--
-- 핵심 아이디어:
-- 1) LEFT JOIN으로 왼쪽 기준 전체 확보
-- 2) RIGHT JOIN(or 반대로 LEFT JOIN)으로 오른쪽 기준 전체 확보
-- 3) 중복되는 "매칭된 행"은 UNION으로 제거되거나,
--    UNION ALL + 조건으로 중복 제거를 제어한다.
--
-- 아래는 "개념적 대체 쿼리"이며,
-- 실제 엔진에 맞게 컬럼/테이블명을 조정해서 사용한다.

--------------------------------------------------
-- 4-1) (개념) LEFT JOIN 결과
--------------------------------------------------
-- SELECT ...
-- FROM customers c
-- LEFT JOIN orders o ON c.customer_id = o.customer_id

--------------------------------------------------
-- 4-2) (개념) RIGHT JOIN 결과 중, LEFT JOIN에서 이미 포함된 MATCH 행 제외
--------------------------------------------------
-- MySQL은 RIGHT JOIN은 지원하지만,
-- SQLite는 RIGHT JOIN도 제한적일 수 있어 "반대 방향 LEFT JOIN"으로 통일하는 것이 안전하다.
--
-- ✅ MySQL 기준 대체 예시 (RIGHT JOIN 사용 가능):

/*
SELECT
    c.customer_id AS customer_id_left,
    c.name,
    o.order_id,
    o.customer_id AS customer_id_right,
    o.amount
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id

UNION

SELECT
    c.customer_id AS customer_id_left,
    c.name,
    o.order_id,
    o.customer_id AS customer_id_right,
    o.amount
FROM customers c
RIGHT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL;
*/

-- 위 UNION 두 번째 쿼리는 "오른쪽에만 있는 행"만 가져오도록
-- WHERE c.customer_id IS NULL로 필터링한다.

--------------------------------------------------
-- 4-3) SQLite 등 RIGHT JOIN이 없을 때(반대 방향 LEFT JOIN으로 통일)
--------------------------------------------------
-- orders를 왼쪽으로 두고 customers를 오른쪽으로 붙인다:
-- "orders LEFT JOIN customers"는 RIGHT JOIN의 역할을 한다.

/*
SELECT
    c.customer_id AS customer_id_left,
    c.name,
    o.order_id,
    o.customer_id AS customer_id_right,
    o.amount
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id

UNION

SELECT
    c.customer_id AS customer_id_left,
    c.name,
    o.order_id,
    o.customer_id AS customer_id_right,
    o.amount
FROM orders o
LEFT JOIN customers c
    ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL;
*/

--------------------------------------------------
-- 5. Summary (실무 요약)
--------------------------------------------------
-- FULL OUTER JOIN 핵심:
-- - 양쪽 테이블의 모든 행을 유지
-- - 매칭되지 않은 행은 반대편 컬럼이 NULL
-- - 데이터 누락/무결성 점검에 매우 유용
--
-- 실무 팁:
-- - DB 엔진이 FULL OUTER JOIN을 지원하는지 먼저 확인
-- - 미지원이면 LEFT JOIN + (반대방향)LEFT JOIN + UNION으로 대체 구현