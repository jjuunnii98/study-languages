/*
Day 42 — Snowflake Schema Design (SQL)

목표:
- Star Schema(비정규화된 차원)에서 한 단계 더 나아가
  Dimension을 정규화하여 Snowflake Schema를 구성한다.
- 분석 관점에서 "차원 확장/중복 감소/무결성 강화"를 목표로 한다.

핵심 포인트:
- Snowflake Schema = Fact는 동일하되, Dimension을 하위 Dimension(서브차원)으로 분해(정규화)
- 장점: 중복 감소, 차원 속성 관리 용이, 무결성 강화
- 단점: JOIN depth 증가 → 쿼리 복잡도/성능 리스크 증가 (인덱스 전략 중요)
*/

-- =========================================
-- 0) 안전한 재실행을 위한 DROP 순서
--    (FK 의존성 때문에 "하위 → 상위" 순서로 삭제)
-- =========================================
DROP TABLE IF EXISTS fact_sales;

DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_store;
DROP TABLE IF EXISTS dim_date;

-- Snowflake로 분해된 서브 차원들(정규화 Dimension)
DROP TABLE IF EXISTS dim_category;
DROP TABLE IF EXISTS dim_brand;

DROP TABLE IF EXISTS dim_region;
DROP TABLE IF EXISTS dim_channel;

DROP TABLE IF EXISTS dim_age_band;

-- =========================================
-- 1) Snowflake Sub-Dimensions (정규화된 서브 차원)
-- =========================================

/*
1-1) Product dimension을 정규화:
- dim_product 내에 category_name, brand_name 등을 직접 넣지 않고
  dim_category, dim_brand로 분리
*/

CREATE TABLE dim_category (
  category_key   INTEGER PRIMARY KEY,
  category_name  TEXT NOT NULL UNIQUE
);

CREATE TABLE dim_brand (
  brand_key      INTEGER PRIMARY KEY,
  brand_name     TEXT NOT NULL UNIQUE
);

/*
1-2) Store dimension을 정규화:
- 지역(region), 판매채널(channel)을 분리
*/

CREATE TABLE dim_region (
  region_key     INTEGER PRIMARY KEY,
  region_name    TEXT NOT NULL UNIQUE
);

CREATE TABLE dim_channel (
  channel_key    INTEGER PRIMARY KEY,
  channel_name   TEXT NOT NULL UNIQUE
);

/*
1-3) Customer dimension을 정규화:
- 나이대(age_band)를 분리하여 고객 속성의 중복을 줄임
*/

CREATE TABLE dim_age_band (
  age_band_key   INTEGER PRIMARY KEY,
  age_band_label TEXT NOT NULL UNIQUE
);

-- =========================================
-- 2) Core Dimensions (Snowflake의 "상위 차원")
-- =========================================

/*
2-1) Date dimension (Star/Snowflake 모두에서 일반적으로 독립 차원)
- 날짜 계층(year/month/day)은 분석에서 핵심 축이라 그대로 유지
*/
CREATE TABLE dim_date (
  date_key       INTEGER PRIMARY KEY,   -- surrogate key(예: 20250101)
  date_value     TEXT NOT NULL,          -- 'YYYY-MM-DD'
  year           INTEGER NOT NULL,
  month          INTEGER NOT NULL,
  day            INTEGER NOT NULL,
  week_of_year   INTEGER,
  day_of_week    INTEGER
);

/*
2-2) Product dimension (정규화된 category/brand와 연결)
*/
CREATE TABLE dim_product (
  product_key    INTEGER PRIMARY KEY,
  product_name   TEXT NOT NULL,
  category_key   INTEGER NOT NULL,
  brand_key      INTEGER NOT NULL,

  -- Snowflake 핵심: 상위 dim_product가 하위 dim_category/dim_brand를 참조
  FOREIGN KEY (category_key) REFERENCES dim_category(category_key),
  FOREIGN KEY (brand_key)    REFERENCES dim_brand(brand_key)
);

/*
2-3) Store dimension (정규화된 region/channel과 연결)
*/
CREATE TABLE dim_store (
  store_key      INTEGER PRIMARY KEY,
  store_name     TEXT NOT NULL,
  region_key     INTEGER NOT NULL,
  channel_key    INTEGER NOT NULL,

  FOREIGN KEY (region_key)  REFERENCES dim_region(region_key),
  FOREIGN KEY (channel_key) REFERENCES dim_channel(channel_key)
);

/*
2-4) Customer dimension (정규화된 age_band와 연결)
*/
CREATE TABLE dim_customer (
  customer_key   INTEGER PRIMARY KEY,
  customer_name  TEXT,
  age            INTEGER,
  age_band_key   INTEGER NOT NULL,

  FOREIGN KEY (age_band_key) REFERENCES dim_age_band(age_band_key)
);

-- =========================================
-- 3) Fact Table (사실 테이블)
-- =========================================

/*
Fact table은 이벤트(거래/행동)를 담고
각 Dimension의 surrogate key를 FK로 연결한다.

여기서는 sales를 예시로:
- quantity_sold, unit_price 같은 additive measure 포함
- total_amount 같은 파생 measure 포함(일부 DB는 GENERATED 컬럼 지원)
*/

CREATE TABLE fact_sales (
  sales_key      INTEGER PRIMARY KEY,
  date_key       INTEGER NOT NULL,
  product_key    INTEGER NOT NULL,
  customer_key   INTEGER NOT NULL,
  store_key      INTEGER NOT NULL,

  quantity_sold  INTEGER NOT NULL CHECK (quantity_sold >= 0),
  unit_price     REAL    NOT NULL CHECK (unit_price >= 0),

  -- DB별로 GENERATED 컬럼 지원이 다르므로, 범용성을 위해 일반 컬럼 + 주석 처리
  total_amount   REAL    NOT NULL,

  FOREIGN KEY (date_key)     REFERENCES dim_date(date_key),
  FOREIGN KEY (product_key)  REFERENCES dim_product(product_key),
  FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
  FOREIGN KEY (store_key)    REFERENCES dim_store(store_key)
);

-- =========================================
-- 4) Index 전략 (JOIN depth 증가 대응)
-- =========================================

/*
Snowflake는 join depth가 증가하므로,
Fact의 FK 인덱스는 기본 중의 기본.

또한 정규화된 서브 차원과의 JOIN을 고려해
dim_product.category_key, dim_product.brand_key 등에도 인덱스를 주는 것이 일반적
*/

-- Fact FK indexes
CREATE INDEX idx_fact_sales_date     ON fact_sales(date_key);
CREATE INDEX idx_fact_sales_product  ON fact_sales(product_key);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_key);
CREATE INDEX idx_fact_sales_store    ON fact_sales(store_key);

-- Dimension linkage indexes (snowflake join path)
CREATE INDEX idx_dim_product_category ON dim_product(category_key);
CREATE INDEX idx_dim_product_brand    ON dim_product(brand_key);

CREATE INDEX idx_dim_store_region     ON dim_store(region_key);
CREATE INDEX idx_dim_store_channel    ON dim_store(channel_key);

CREATE INDEX idx_dim_customer_ageband ON dim_customer(age_band_key);

-- =========================================
-- 5) (선택) Snowflake join path 예시 쿼리
-- =========================================

/*
예: 월별/카테고리별 매출 집계

Star Schema였다면:
fact_sales -> dim_date / dim_product(카테고리 포함) 로 끝났겠지만,
Snowflake에서는:
fact_sales -> dim_product -> dim_category
처럼 한 단계 더 JOIN이 필요하다.
*/

-- SELECT
--   d.year,
--   d.month,
--   c.category_name,
--   SUM(f.total_amount) AS revenue
-- FROM fact_sales f
-- JOIN dim_date d        ON f.date_key = d.date_key
-- JOIN dim_product p     ON f.product_key = p.product_key
-- JOIN dim_category c    ON p.category_key = c.category_key
-- GROUP BY d.year, d.month, c.category_name
-- ORDER BY d.year, d.month, c.category_name;