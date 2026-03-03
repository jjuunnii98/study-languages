/*
Day 44 — Primary & Foreign Keys
파일: 01_primary_foreign_keys.sql

목표
- Primary Key / Foreign Key의 정확한 역할 이해
- 참조 무결성(Referential Integrity) 구현
- ON DELETE / ON UPDATE 전략 비교
- 인덱스와 FK 관계 이해
- 무결성 위반 테스트

설계 관점 (한국어)

1) Primary Key (PK)
   - 테이블의 각 행을 고유하게 식별
   - NOT NULL + UNIQUE
   - 가능한 경우 surrogate key (정수 기반) 사용 권장

2) Foreign Key (FK)
   - 다른 테이블의 PK를 참조
   - 데이터 정합성 보장
   - 고아 레코드(orphan row) 방지

3) ON DELETE / ON UPDATE 전략
   - CASCADE
   - RESTRICT
   - SET NULL
   - NO ACTION

실무 권장:
- Fact → Dimension은 일반적으로 RESTRICT
- 종속 관계는 CASCADE 고려
*/

------------------------------------------------------------
-- 0️⃣ 기존 테이블 제거 (재현 가능 DDL)
------------------------------------------------------------

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

------------------------------------------------------------
-- 1️⃣ Parent Table (customers)
------------------------------------------------------------

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,   -- PK: 고유 식별자
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,         -- 이메일은 유니크
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PK는 자동 인덱스를 생성한다.
-- customer_id는 클러스터링 키 역할을 수행할 수 있음(DBMS에 따라 다름)

------------------------------------------------------------
-- 2️⃣ Child Table (orders)
------------------------------------------------------------

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_amount DECIMAL(12,2) NOT NULL CHECK (order_amount >= 0),
    order_date DATE NOT NULL,

    -- Foreign Key 제약조건
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE RESTRICT   -- 부모 삭제 시 자식이 있으면 삭제 불가
        ON UPDATE CASCADE    -- 부모 PK 변경 시 자동 반영
);

------------------------------------------------------------
-- 3️⃣ FK 컬럼 인덱스 생성 (성능 최적화)
------------------------------------------------------------

/*
중요:

FK 제약조건은 자동 인덱스를 생성하지 않는 DB도 많다.
조인 성능을 위해 FK 컬럼에는 인덱스를 생성하는 것이 일반적.
*/

CREATE INDEX idx_orders_customer_id
    ON orders(customer_id);

------------------------------------------------------------
-- 4️⃣ 정상 데이터 삽입 테스트
------------------------------------------------------------

INSERT INTO customers (customer_id, customer_name, email)
VALUES
(1, 'Alice Kim', 'alice@example.com'),
(2, 'Bob Lee', 'bob@example.com');

INSERT INTO orders (order_id, customer_id, order_amount, order_date)
VALUES
(101, 1, 120000.00, '2026-01-10'),
(102, 1, 80000.00, '2026-01-15'),
(103, 2, 45000.00, '2026-01-20');

------------------------------------------------------------
-- 5️⃣ FK 무결성 테스트 (실패 케이스)
------------------------------------------------------------

/*
아래 쿼리는 실패해야 한다.
customer_id=999는 존재하지 않기 때문.
*/

-- INSERT INTO orders (order_id, customer_id, order_amount, order_date)
-- VALUES (200, 999, 10000.00, '2026-02-01');

------------------------------------------------------------
-- 6️⃣ ON DELETE RESTRICT 테스트
------------------------------------------------------------

/*
아래는 실패해야 한다.
customer_id=1은 orders에 존재하므로 삭제 불가.
*/

-- DELETE FROM customers WHERE customer_id = 1;

------------------------------------------------------------
-- 7️⃣ 조인 검증 쿼리
------------------------------------------------------------

SELECT
    c.customer_id,
    c.customer_name,
    SUM(o.order_amount) AS total_spent
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC;

------------------------------------------------------------
-- 8️⃣ 설계 요약
------------------------------------------------------------

/*
PK: 엔티티 식별자
FK: 엔티티 관계 무결성 보장

관계형 모델에서 가장 중요한 3가지:

1) Entity Integrity (PK는 NULL 불가)
2) Referential Integrity (FK는 반드시 존재하는 PK 참조)
3) Domain Integrity (CHECK / 타입 / 범위 제약)

이 파일은 그 중 1, 2를 구현한다.
*/