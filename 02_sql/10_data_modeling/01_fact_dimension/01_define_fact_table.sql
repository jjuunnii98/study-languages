/*
===============================================================
 Day 38 — Fact Table 정의 (Star Schema 기반)
 Module: 10_data_modeling / 01_fact_dimension
===============================================================

📌 목적:
- 트랜잭션 기반 Fact 테이블 정의
- Star Schema 설계 원칙 적용
- Surrogate Key + Foreign Key 구조
- 집계 성능을 고려한 Index 설계

📌 핵심 개념:
Fact Table = "측정값(Measure)을 저장하는 중심 테이블"
Dimension Table = "분석 기준 속성(Attribute)을 저장하는 테이블"

이 파일은 데이터 웨어하우스 모델링 역량을 증명하기 위한 DDL 예제이다.
*/


-- ============================================================
-- 1️⃣ 기존 테이블 제거 (Idempotent 설계)
--    반복 실행해도 오류가 발생하지 않도록 처리
-- ============================================================

DROP TABLE IF EXISTS fact_sales;


-- ============================================================
-- 2️⃣ Fact 테이블 생성
-- ============================================================

CREATE TABLE fact_sales (

    -- --------------------------------------------------------
    -- Surrogate Key (대리키)
    -- 자연키 대신 시스템 생성 키 사용
    -- ETL 안정성 및 SCD 대응을 위해 권장
    -- --------------------------------------------------------
    sales_key BIGSERIAL PRIMARY KEY,

    -- --------------------------------------------------------
    -- Foreign Keys (차원 테이블 참조 키)
    -- Fact는 Dimension의 Key만 보유
    -- --------------------------------------------------------
    date_key      INT NOT NULL,   -- 날짜 차원
    product_key   INT NOT NULL,   -- 상품 차원
    customer_key  INT NOT NULL,   -- 고객 차원
    store_key     INT NOT NULL,   -- 매장 차원

    -- --------------------------------------------------------
    -- Measures (집계 대상 수치)
    -- BI / 분석 / KPI 계산에 사용됨
    -- --------------------------------------------------------
    quantity_sold INT NOT NULL,          -- 판매 수량
    unit_price    NUMERIC(12,2) NOT NULL,-- 단가

    -- 파생 측정값 (계산 컬럼)
    -- 데이터 정합성 유지를 위해 DB 레벨에서 계산
    total_amount  NUMERIC(14,2)
        GENERATED ALWAYS AS (quantity_sold * unit_price) STORED,

    -- --------------------------------------------------------
    -- 메타 정보
    -- --------------------------------------------------------
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 3️⃣ Foreign Key 제약조건 설정
--    참조 무결성 보장
-- ============================================================

ALTER TABLE fact_sales
ADD CONSTRAINT fk_fact_date
FOREIGN KEY (date_key)
REFERENCES dim_date(date_key);

ALTER TABLE fact_sales
ADD CONSTRAINT fk_fact_product
FOREIGN KEY (product_key)
REFERENCES dim_product(product_key);

ALTER TABLE fact_sales
ADD CONSTRAINT fk_fact_customer
FOREIGN KEY (customer_key)
REFERENCES dim_customer(customer_key);

ALTER TABLE fact_sales
ADD CONSTRAINT fk_fact_store
FOREIGN KEY (store_key)
REFERENCES dim_store(store_key);


-- ============================================================
-- 4️⃣ 성능 최적화를 위한 Index 생성
--    Fact 테이블은 대용량이 되므로
--    FK 컬럼 인덱스는 필수
-- ============================================================

CREATE INDEX idx_fact_sales_date_key
ON fact_sales(date_key);

CREATE INDEX idx_fact_sales_product_key
ON fact_sales(product_key);

CREATE INDEX idx_fact_sales_customer_key
ON fact_sales(customer_key);

CREATE INDEX idx_fact_sales_store_key
ON fact_sales(store_key);


/*
===============================================================
📊 설계 요약

✔ Fact 테이블은 수치 중심
✔ Dimension은 분석 기준 속성 중심
✔ Surrogate Key 사용
✔ Foreign Key로 Star Schema 구성
✔ FK 컬럼에 인덱스 생성
✔ 계산 컬럼을 DB 레벨에서 처리하여 일관성 유지

이 구조는 BI, OLAP, 집계 쿼리, KPI 분석에 최적화된 모델이다.
===============================================================
*/