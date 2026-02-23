/*
Day 40 (SQL) — Star Schema Design

목표:
- 스타 스키마(Star Schema) 모델을 SQL DDL로 재현 가능하게 설계한다.
- 분석(OLAP) 관점에서 Fact(사실)와 Dimension(차원)을 분리한다.
- Surrogate Key(대리키) 기반 모델링으로 안정적인 조인/집계를 지원한다.

설계 철학:
- Fact 테이블은 "측정값(measures)" 중심: 매출, 수량, 금액 등
- Dimension 테이블은 "맥락(context)" 중심: 날짜, 고객, 상품, 매장 등
- Fact는 여러 Dimension을 FK로 참조하여 분석 축을 제공한다.
*/


/* =========================================================
0) (선택) 스키마 초기화 전략
- 실습/포트폴리오에서는 idempotent하게 만들기 위해 DROP IF EXISTS 사용
- 단, 실제 운영 환경에서는 마이그레이션 도구(Flyway/Liquibase 등) 권장
========================================================= */

-- SQLite 기준: 외래키 제약 활성화 (DB에 따라 필요)
PRAGMA foreign_keys = ON;


/* =========================================================
1) Dimension Tables (차원 테이블)
- 분석 기준(속성)을 저장하는 테이블
- 각 차원은 Surrogate Key를 PK로 가진다.
========================================================= */

-- 1-1) 날짜 차원: 분석에서 가장 많이 쓰는 축 (일/월/분기/요일 등)
DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date (
  date_key        INTEGER PRIMARY KEY,          -- 대리키(예: 20250101 같은 정수)
  date_value      DATE    NOT NULL UNIQUE,      -- 실제 날짜 값
  year            INTEGER NOT NULL,
  quarter         INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
  month           INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
  day             INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
  day_of_week     INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6), -- 0=Sun 같은 정책
  is_weekend      INTEGER NOT NULL CHECK (is_weekend IN (0,1))
);

-- 1-2) 고객 차원
DROP TABLE IF EXISTS dim_customer;
CREATE TABLE dim_customer (
  customer_key    INTEGER PRIMARY KEY AUTOINCREMENT, -- 대리키
  customer_id     TEXT    NOT NULL UNIQUE,           -- 자연키(업무 식별자)
  customer_name   TEXT,
  gender          TEXT,                               -- 'M','F' 등 (정책에 맞게)
  age_band        TEXT,                               -- 예: '20-29'
  country         TEXT,
  signup_date     DATE
);

-- 1-3) 상품 차원
DROP TABLE IF EXISTS dim_product;
CREATE TABLE dim_product (
  product_key     INTEGER PRIMARY KEY AUTOINCREMENT, -- 대리키
  product_id      TEXT    NOT NULL UNIQUE,           -- 자연키
  product_name    TEXT    NOT NULL,
  category        TEXT,
  brand           TEXT,
  list_price      REAL,                               -- 정가(참고용)
  is_active       INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1))
);

-- 1-4) 매장/채널 차원 (오프라인/온라인, 지점 등)
DROP TABLE IF EXISTS dim_store;
CREATE TABLE dim_store (
  store_key       INTEGER PRIMARY KEY AUTOINCREMENT, -- 대리키
  store_id        TEXT    NOT NULL UNIQUE,           -- 자연키
  store_name      TEXT,
  region          TEXT,
  channel         TEXT                                -- 예: 'offline', 'online'
);


/* =========================================================
2) Fact Table (사실 테이블)
- 측정 대상 이벤트(판매/거래 등)를 저장
- Dimension들의 FK를 통해 분석 축을 제공
- Measures는 집계 가능한 수치값 중심
========================================================= */

DROP TABLE IF EXISTS fact_sales;
CREATE TABLE fact_sales (
  sales_key       INTEGER PRIMARY KEY AUTOINCREMENT, -- Fact 대리키(행 고유 식별)
  
  -- 분석 축(차원키)
  date_key        INTEGER NOT NULL,
  customer_key    INTEGER NOT NULL,
  product_key     INTEGER NOT NULL,
  store_key       INTEGER NOT NULL,

  -- 측정값(집계 대상)
  quantity_sold   INTEGER NOT NULL CHECK (quantity_sold >= 0),
  unit_price      REAL    NOT NULL CHECK (unit_price >= 0),

  -- 파생 측정값(계산 컬럼): DB에 따라 generated column 지원이 다름
  -- SQLite는 generated column 지원 버전에 따라 동작하므로,
  -- 여기서는 "저장 컬럼"으로 두고 ETL에서 채우거나 VIEW로 계산하는 방식을 권장.
  total_amount    REAL    NOT NULL CHECK (total_amount >= 0),

  -- 무결성 제약: Fact는 Dimension을 참조
  CONSTRAINT fk_sales_date     FOREIGN KEY (date_key)     REFERENCES dim_date(date_key),
  CONSTRAINT fk_sales_customer FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
  CONSTRAINT fk_sales_product  FOREIGN KEY (product_key)  REFERENCES dim_product(product_key),
  CONSTRAINT fk_sales_store    FOREIGN KEY (store_key)    REFERENCES dim_store(store_key)
);

-- 분석 성능을 위한 인덱스
-- 원칙: Fact의 FK 컬럼은 조인/집계에서 매우 자주 쓰이므로 인덱스를 두는 것이 일반적
CREATE INDEX IF NOT EXISTS idx_fact_sales_date     ON fact_sales(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer ON fact_sales(customer_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product  ON fact_sales(product_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_store    ON fact_sales(store_key);


/* =========================================================
3) Star Schema Quick Check (검증용 샘플 쿼리)
- 실제 데이터가 있어야 동작하지만, 설계 의도를 보여주기 위해 포함
========================================================= */

-- 예: 월별 매출(총액) 집계
-- SELECT d.year, d.month, SUM(f.total_amount) AS revenue
-- FROM fact_sales f
-- JOIN dim_date d ON f.date_key = d.date_key
-- GROUP BY d.year, d.month
-- ORDER BY d.year, d.month;

-- 예: 카테고리별 매출 TOP
-- SELECT p.category, SUM(f.total_amount) AS revenue
-- FROM fact_sales f
-- JOIN dim_product p ON f.product_key = p.product_key
-- GROUP BY p.category
-- ORDER BY revenue DESC;