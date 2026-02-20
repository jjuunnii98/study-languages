/*
===============================================================
 Day 39 — Dimension Tables 정의 (Star Schema 기반)
 Module: 10_data_modeling / 01_fact_dimension
 File: 02_define_dimension_tables.sql
===============================================================

📌 목적:
- Fact 테이블(fact_sales)이 참조하는 Dimension 테이블 정의
- Star Schema의 “분석 기준 축”을 제공하는 테이블 설계
- Surrogate Key(대리키) + Natural Key(자연키) 분리
- 조회 성능을 고려한 Index 설계

📌 Dimension 설계 원칙(실무 기준):
1) PK는 surrogate key로 (INT/BIGINT) → ETL/SCD 안정성
2) Natural key는 UNIQUE로 보존 → 원천 시스템 식별성 유지
3) Attribute 컬럼은 분석을 위한 “설명 정보”
4) 자주 조인/필터되는 컬럼에 인덱스 고려

※ 이 파일은 Postgres 기준 DDL 예제이다.
*/


-- ============================================================
-- 0️⃣ 기존 테이블 제거 (의존성 고려: Fact 먼저 삭제/비활성 필요)
--     - 이미 Fact에서 FK를 걸어둔 경우, Dimension을 DROP하려면
--       Fact를 먼저 DROP 하거나 FK를 제거해야 한다.
--     - 학습/포트폴리오 목적이라면, Dimension을 먼저 정의하고
--       Fact에서 FK를 나중에 연결하는 순서가 안전하다.
-- ============================================================

DROP TABLE IF EXISTS dim_store;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_date;


-- ============================================================
-- 1️⃣ dim_date (날짜 차원)
--     - 날짜는 가장 흔한 분석 축
--     - date_key는 보통 YYYYMMDD 형태의 int를 사용하기도 함
-- ============================================================

CREATE TABLE dim_date (
    -- 분석에서 사용하기 좋은 정수형 날짜 키 (예: 20260115)
    date_key INT PRIMARY KEY,

    -- 실제 날짜 (원본)
    full_date DATE NOT NULL UNIQUE,

    -- 파생 속성들 (그룹핑/필터링에 매우 자주 사용)
    year       SMALLINT NOT NULL,
    quarter    SMALLINT NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    month      SMALLINT NOT NULL CHECK (month BETWEEN 1 AND 12),
    day        SMALLINT NOT NULL CHECK (day BETWEEN 1 AND 31),
    day_of_week SMALLINT NOT NULL CHECK (day_of_week BETWEEN 1 AND 7), -- 1=Mon~7=Sun (정책은 팀마다 다름)
    is_weekend BOOLEAN NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 자주 쓰는 축 인덱스 (필수는 아니지만, 실무에서는 충분히 가치 있음)
CREATE INDEX idx_dim_date_year_month
ON dim_date(year, month);



-- ============================================================
-- 2️⃣ dim_product (상품 차원)
--     - product_key: surrogate key
--     - product_code: 자연키(원천 시스템 ID) → UNIQUE로 보존
-- ============================================================

CREATE TABLE dim_product (
    product_key BIGSERIAL PRIMARY KEY,

    -- 자연키: 원천 시스템의 상품 코드/ID
    product_code TEXT NOT NULL UNIQUE,

    -- 분석용 속성들
    product_name TEXT NOT NULL,
    category     TEXT,
    subcategory  TEXT,
    brand        TEXT,

    -- 가격/상태 같은 속성은 변화 가능성 있음 (SCD에서 다루기도 함)
    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 분석/필터링 자주 쓰는 컬럼 인덱스 예시
CREATE INDEX idx_dim_product_category
ON dim_product(category);



-- ============================================================
-- 3️⃣ dim_customer (고객 차원)
--     - customer_key: surrogate key
--     - customer_id: 자연키(원천 시스템 ID)
-- ============================================================

CREATE TABLE dim_customer (
    customer_key BIGSERIAL PRIMARY KEY,

    -- 자연키: 원천 시스템 고객 ID
    customer_id TEXT NOT NULL UNIQUE,

    -- 분석용 속성들
    customer_name TEXT,
    gender        TEXT CHECK (gender IN ('M', 'F') OR gender IS NULL),
    birth_year    SMALLINT CHECK (birth_year BETWEEN 1900 AND 2100 OR birth_year IS NULL),

    -- 고객 세그먼트(마케팅/CRM 분석에서 자주 사용)
    segment       TEXT,

    -- 지역 기반 분석
    country       TEXT,
    city          TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dim_customer_segment
ON dim_customer(segment);

CREATE INDEX idx_dim_customer_country_city
ON dim_customer(country, city);



-- ============================================================
-- 4️⃣ dim_store (매장/채널 차원)
--     - store_key: surrogate key
--     - store_code: 자연키
-- ============================================================

CREATE TABLE dim_store (
    store_key BIGSERIAL PRIMARY KEY,

    -- 자연키: 원천 시스템의 매장 코드
    store_code TEXT NOT NULL UNIQUE,

    -- 분석용 속성들
    store_name TEXT NOT NULL,

    -- 오프라인/온라인 채널 구분 등
    channel    TEXT,    -- 예: 'offline', 'online', 'mobile'
    region     TEXT,    -- 예: 'Seoul', 'Busan'
    country    TEXT,

    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dim_store_channel
ON dim_store(channel);

CREATE INDEX idx_dim_store_region
ON dim_store(region);



/*
===============================================================
✅ Day 39 요약

- dim_date: 날짜 축(연/월/요일/주말 여부) 제공
- dim_product: 상품 속성(카테고리/브랜드 등) 제공
- dim_customer: 고객 속성(세그먼트/지역 등) 제공
- dim_store: 매장/채널/지역 축 제공

📌 다음 단계(권장):
- Fact 테이블(fact_sales)에서 FK 참조가 정상 동작하도록
  dim_* 테이블의 PK 구조와 fact의 key 컬럼 타입을 정합하게 맞춘다.
- 필요 시 SCD(Type 2)로 확장하여 “속성 변화 이력”을 모델링한다.
===============================================================
*/