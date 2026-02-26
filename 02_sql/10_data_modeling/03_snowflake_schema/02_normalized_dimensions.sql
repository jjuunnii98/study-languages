/* 
Day 43 — Normalized Dimensions (Snowflake Schema)

목표:
- Snowflake Schema에서 "정규화된 차원 테이블"들을 안정적으로 적재(ETL/ELT)하는 패턴을 제공
- dim_category, dim_brand, dim_region, dim_channel, dim_age_band 같은 서브 차원을 먼저 구축
- 이후 dim_product, dim_store, dim_customer를 서브 차원 키로 연결하여 적재
- 마지막으로 fact_sales가 안정적으로 FK를 참조할 수 있는 형태를 완성

주의:
- 아래 SQL은 "테이블이 이미 생성되어 있다"는 전제(= Day 42의 01_snowflake_schema_design.sql 실행 완료)에서 동작
- DBMS별 문법 차이를 최소화하기 위해 "INSERT ... SELECT + NOT EXISTS" 패턴 위주로 구성
- (Postgres라면 ON CONFLICT, MySQL이라면 INSERT IGNORE/ON DUPLICATE KEY 같은 업서트로 확장 가능)
*/


/* =========================================================
  0) 샘플 Staging 데이터 (데모용)
  - 실제 환경에서는 raw/staging 테이블에서 읽는 구조
  - 여기서는 Day 43 파일 단독 실행 테스트를 위해 CTE로 가정
========================================================= */

-- ✅ 예시 입력(원천) 데이터: 제품/매장/고객 차원에서 필요한 속성들을 staging으로 가정
WITH
stg_product AS (
  SELECT 'P001' AS product_code, 'iPhone 15' AS product_name, 'PHONE' AS category_name, 'APPLE' AS brand_name UNION ALL
  SELECT 'P002', 'Galaxy S24', 'PHONE', 'SAMSUNG' UNION ALL
  SELECT 'P003', 'MacBook Air', 'LAPTOP', 'APPLE'
),
stg_store AS (
  SELECT 'S001' AS store_code, 'Gangnam' AS store_name, 'SEOUL' AS region_name, 'OFFLINE' AS channel_name UNION ALL
  SELECT 'S002', 'Hongdae', 'SEOUL', 'OFFLINE' UNION ALL
  SELECT 'S003', 'OnlineMall', 'KOREA', 'ONLINE'
),
stg_customer AS (
  SELECT 'C001' AS customer_code, 'F' AS gender, 26 AS age UNION ALL
  SELECT 'C002', 'M', 34 UNION ALL
  SELECT 'C003', 'F', 47
)
SELECT 1;


/* =========================================================
  1) 서브 차원(정규화 테이블) 적재
  - Snowflake에서 핵심은 "중복 제거된 기준 테이블"을 먼저 구축하는 것
  - NOT EXISTS를 사용해 멱등적(idempotent) INSERT 구현
========================================================= */

-- 1-1) dim_category 적재
INSERT INTO dim_category (category_name)
SELECT DISTINCT p.category_name
FROM (
  SELECT 'PHONE' AS category_name UNION ALL
  SELECT 'LAPTOP'
) p
WHERE NOT EXISTS (
  SELECT 1
  FROM dim_category d
  WHERE d.category_name = p.category_name
);

-- 1-2) dim_brand 적재
INSERT INTO dim_brand (brand_name)
SELECT DISTINCT b.brand_name
FROM (
  SELECT 'APPLE' AS brand_name UNION ALL
  SELECT 'SAMSUNG'
) b
WHERE NOT EXISTS (
  SELECT 1
  FROM dim_brand d
  WHERE d.brand_name = b.brand_name
);

-- 1-3) dim_region 적재
INSERT INTO dim_region (region_name)
SELECT DISTINCT r.region_name
FROM (
  SELECT 'SEOUL' AS region_name UNION ALL
  SELECT 'KOREA'
) r
WHERE NOT EXISTS (
  SELECT 1
  FROM dim_region d
  WHERE d.region_name = r.region_name
);

-- 1-4) dim_channel 적재
INSERT INTO dim_channel (channel_name)
SELECT DISTINCT c.channel_name
FROM (
  SELECT 'OFFLINE' AS channel_name UNION ALL
  SELECT 'ONLINE'
) c
WHERE NOT EXISTS (
  SELECT 1
  FROM dim_channel d
  WHERE d.channel_name = c.channel_name
);

-- 1-5) dim_age_band 적재
-- ✅ 나이 구간은 "분석용 버킷"이므로 규칙을 고정해서 넣는 것이 일반적
INSERT INTO dim_age_band (age_band)
SELECT x.age_band
FROM (
  SELECT '18-24' AS age_band UNION ALL
  SELECT '25-34' UNION ALL
  SELECT '35-44' UNION ALL
  SELECT '45-54' UNION ALL
  SELECT '55+'
) x
WHERE NOT EXISTS (
  SELECT 1
  FROM dim_age_band d
  WHERE d.age_band = x.age_band
);


/* =========================================================
  2) 메인 차원(dim_product / dim_store / dim_customer) 적재
  - 서브 차원의 surrogate key를 lookup해서 FK로 저장
  - 원천 natural key(product_code/store_code/customer_code)는 "업무키"로 별도 unique 관리 권장
========================================================= */

-- 2-1) dim_product 적재
-- ✅ 핵심: category_key, brand_key를 lookup해서 넣는다
INSERT INTO dim_product (product_code, product_name, category_key, brand_key)
SELECT
  p.product_code,
  p.product_name,
  dc.category_key,
  db.brand_key
FROM (
  SELECT 'P001' AS product_code, 'iPhone 15' AS product_name, 'PHONE' AS category_name, 'APPLE' AS brand_name UNION ALL
  SELECT 'P002', 'Galaxy S24', 'PHONE', 'SAMSUNG' UNION ALL
  SELECT 'P003', 'MacBook Air', 'LAPTOP', 'APPLE'
) p
JOIN dim_category dc
  ON dc.category_name = p.category_name
JOIN dim_brand db
  ON db.brand_name = p.brand_name
WHERE NOT EXISTS (
  SELECT 1
  FROM dim_product dp
  WHERE dp.product_code = p.product_code
);

-- 2-2) dim_store 적재
INSERT INTO dim_store (store_code, store_name, region_key, channel_key)
SELECT
  s.store_code,
  s.store_name,
  dr.region_key,
  dch.channel_key
FROM (
  SELECT 'S001' AS store_code, 'Gangnam' AS store_name, 'SEOUL' AS region_name, 'OFFLINE' AS channel_name UNION ALL
  SELECT 'S002', 'Hongdae', 'SEOUL', 'OFFLINE' UNION ALL
  SELECT 'S003', 'OnlineMall', 'KOREA', 'ONLINE'
) s
JOIN dim_region dr
  ON dr.region_name = s.region_name
JOIN dim_channel dch
  ON dch.channel_name = s.channel_name
WHERE NOT EXISTS (
  SELECT 1
  FROM dim_store ds
  WHERE ds.store_code = s.store_code
);

-- 2-3) dim_customer 적재
-- ✅ 고객은 age → age_band 로 변환 후 age_band_key를 lookup
INSERT INTO dim_customer (customer_code, gender, age, age_band_key)
SELECT
  c.customer_code,
  c.gender,
  c.age,
  dab.age_band_key
FROM (
  SELECT 'C001' AS customer_code, 'F' AS gender, 26 AS age UNION ALL
  SELECT 'C002', 'M', 34 UNION ALL
  SELECT 'C003', 'F', 47
) c
JOIN dim_age_band dab
  ON dab.age_band = CASE
    WHEN c.age BETWEEN 18 AND 24 THEN '18-24'
    WHEN c.age BETWEEN 25 AND 34 THEN '25-34'
    WHEN c.age BETWEEN 35 AND 44 THEN '35-44'
    WHEN c.age BETWEEN 45 AND 54 THEN '45-54'
    ELSE '55+'
  END
WHERE NOT EXISTS (
  SELECT 1
  FROM dim_customer dc
  WHERE dc.customer_code = c.customer_code
);


/* =========================================================
  3) 검증 쿼리(Validation)
  - Snowflake join path가 정상인지 확인
  - dim_product -> dim_category/brand, dim_store -> dim_region/channel, dim_customer -> dim_age_band
========================================================= */

-- ✅ 제품 차원 검증
SELECT
  dp.product_code,
  dp.product_name,
  dc.category_name,
  db.brand_name
FROM dim_product dp
JOIN dim_category dc ON dp.category_key = dc.category_key
JOIN dim_brand db ON dp.brand_key = db.brand_key
ORDER BY dp.product_code;

-- ✅ 매장 차원 검증
SELECT
  ds.store_code,
  ds.store_name,
  dr.region_name,
  dch.channel_name
FROM dim_store ds
JOIN dim_region dr ON ds.region_key = dr.region_key
JOIN dim_channel dch ON ds.channel_key = dch.channel_key
ORDER BY ds.store_code;

-- ✅ 고객 차원 검증
SELECT
  dc.customer_code,
  dc.gender,
  dc.age,
  dab.age_band
FROM dim_customer dc
JOIN dim_age_band dab ON dc.age_band_key = dab.age_band_key
ORDER BY dc.customer_code;