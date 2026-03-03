/*
Day 45 — Index Design (SQL) | 04_keys_indexes/02_index_design.sql

[목표]
- 인덱스가 "왜/언제" 필요한지, 어떤 형태가 있는지 실무 관점으로 정리
- 쿼리 패턴(WHERE/JOIN/ORDER BY/GROUP BY)에 맞춘 인덱스 설계
- 단일 인덱스 vs 복합 인덱스의 선택 기준 이해
- (가능한 경우) 커버링(covering) 효과를 위한 컬럼 포함 전략 이해

[주의]
- DBMS마다 지원 기능이 다름 (예: INCLUDE, partial index, function index 등)
- 본 스크립트는 SQLite/PostgreSQL/MySQL 계열에서 최대한 무난하게 동작하도록 작성
- EXPLAIN 결과는 DBMS별 출력이 다를 수 있음

[핵심 원칙]
1) 인덱스는 읽기(SELECT)를 빠르게 하지만, 쓰기(INSERT/UPDATE/DELETE)는 느리게 만든다.
2) 가장 중요한 것은 "자주 실행되는 쿼리의 WHERE/JOIN/ORDER BY" 조건을 먼저 잡는 것.
3) 인덱스는 많을수록 좋은 게 아니라, '워크로드 기반'으로 최소한으로 설계해야 한다.
*/

-- ============================================================
-- 0) 테이블 준비 (Day 44의 customers/orders가 있다면 그대로 사용 가능)
--    없으면 아래 DDL로 재현 가능하게 생성
-- ============================================================

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY,
  customer_name TEXT NOT NULL,
  email TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  order_date TEXT NOT NULL,
  status TEXT NOT NULL,         -- 예: 'paid', 'pending', 'canceled'
  amount NUMERIC NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

-- ============================================================
-- 1) 샘플 데이터 생성
--    (학습/테스트용: 작은 데이터로도 인덱스 구조를 이해하는 데 충분)
-- ============================================================

INSERT INTO customers (customer_id, customer_name, email, created_at) VALUES
(1, 'Alice', 'alice@example.com', '2026-01-01'),
(2, 'Bob',   'bob@example.com',   '2026-01-02'),
(3, 'Cara',  'cara@example.com',  '2026-01-03'),
(4, 'Dan',   'dan@example.com',   '2026-01-04');

INSERT INTO orders (order_id, customer_id, order_date, status, amount) VALUES
(101, 1, '2026-01-10', 'paid',    120.50),
(102, 1, '2026-01-12', 'paid',     80.00),
(103, 1, '2026-02-01', 'pending',  35.00),
(104, 2, '2026-01-11', 'paid',     15.00),
(105, 2, '2026-02-05', 'canceled', 55.00),
(106, 3, '2026-02-10', 'paid',    210.00),
(107, 3, '2026-03-01', 'paid',     75.00),
(108, 4, '2026-03-02', 'pending',  60.00);

-- ============================================================
-- 2) 인덱스가 필요한 대표 패턴
-- ============================================================

/*
[패턴 A] FK 조인(Join)
- orders.customer_id로 customers를 조인하는 경우가 많다.
- FK는 무결성을 보장하지만, 성능은 별개다.
- 따라서 '자식 테이블의 FK 컬럼'에 인덱스를 거는 것이 거의 표준.

예: 고객별 주문 합계
*/
SELECT
  c.customer_id,
  c.customer_name,
  SUM(o.amount) AS total_amount
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_amount DESC;

-- FK 인덱스 생성 (JOIN 성능 개선)
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);

-- ============================================================
-- 3) WHERE 조건 최적화 (필터링)
-- ============================================================

/*
[패턴 B] 상태(status)로 필터링
- 예: paid 주문만 자주 조회
- status는 카디널리티가 낮을 수 있음(paid/pending/canceled).
- 단독 인덱스가 항상 이득은 아니지만, "대규모 테이블 + 자주 필터링"이면 가치가 생긴다.
*/
SELECT * FROM orders
WHERE status = 'paid';

CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

-- ============================================================
-- 4) 날짜 범위 조건 + 정렬 (range + order by)
-- ============================================================

/*
[패턴 C] 날짜 범위 조회 + 최신순 정렬
- WHERE order_date BETWEEN ... AND ...
- ORDER BY order_date DESC
- 이런 경우 order_date 인덱스가 유리.
*/
SELECT order_id, customer_id, order_date, status, amount
FROM orders
WHERE order_date >= '2026-02-01'
  AND order_date <  '2026-04-01'
ORDER BY order_date DESC;

CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date);

-- ============================================================
-- 5) 복합 인덱스(Composite Index): 실제로 가장 실무적인 형태
-- ============================================================

/*
[패턴 D] (customer_id, order_date) 조합이 자주 등장
- 예: 특정 고객의 기간별 주문 조회
- WHERE customer_id = ? AND order_date BETWEEN ...
- 이 경우 (customer_id, order_date) 복합 인덱스가 유리

[중요] 복합 인덱스의 컬럼 순서
- 일반적으로 "동등조건(=)" 컬럼을 앞에, "범위조건(BETWEEN, >, <)" 컬럼을 뒤에 둔다.
- 그래서 (customer_id, order_date)가 많이 쓰인다.
*/
SELECT order_id, order_date, status, amount
FROM orders
WHERE customer_id = 1
  AND order_date >= '2026-01-01'
  AND order_date <  '2026-03-01'
ORDER BY order_date;

CREATE INDEX IF NOT EXISTS idx_orders_customer_date ON orders(customer_id, order_date);

-- ============================================================
-- 6) GROUP BY 최적화: 집계 워크로드
-- ============================================================

/*
[패턴 E] status별 매출(금액) 집계
- GROUP BY status
- 대용량일수록 인덱스가 도움될 수 있으나,
  집계는 종종 "테이블 스캔 + 해시집계"가 더 효율적일 수도 있다.
- 따라서 성능은 EXPLAIN/실측 기반으로 판단하는 습관이 중요.
*/
SELECT status, COUNT(*) AS cnt, SUM(amount) AS sum_amount
FROM orders
GROUP BY status
ORDER BY sum_amount DESC;

-- ============================================================
-- 7) 선택도(Selectivity)와 인덱스 남발 방지
-- ============================================================

/*
[실무 팁]
- status 같이 값 종류가 적은 컬럼은 "선택도(selectivity)"가 낮아
  인덱스 효과가 제한적일 수 있다.
- 하지만 "paid만 5%이고 나머지가 95%" 같은 편향이 있으면
  인덱스가 큰 효과를 낼 수 있다.
- 결론: 인덱스는 데이터 분포와 쿼리 빈도를 같이 봐야 한다.
*/

-- ============================================================
-- 8) EXPLAIN으로 계획 확인 (DBMS별 출력 상이)
-- ============================================================

/*
SQLite: EXPLAIN QUERY PLAN ...
PostgreSQL: EXPLAIN (ANALYZE, BUFFERS) ...
MySQL: EXPLAIN ...
*/
EXPLAIN QUERY PLAN
SELECT order_id, order_date, status, amount
FROM orders
WHERE customer_id = 1
  AND order_date >= '2026-01-01'
  AND order_date <  '2026-03-01'
ORDER BY order_date;

-- ============================================================
-- 9) 인덱스 설계 체크리스트 (요약)
-- ============================================================

/*
1) 가장 자주 실행되는 TOP 쿼리부터 잡기
2) WHERE/JOIN 조건 컬럼에 우선 적용
3) 복합 인덱스는 (동등조건 → 범위조건) 순으로
4) ORDER BY와 동일한 방향/컬럼 조합을 고려
5) 인덱스 추가 후 EXPLAIN + 실제 실행시간으로 검증
6) 쓰기 부하가 큰 테이블은 인덱스 최소화
*/