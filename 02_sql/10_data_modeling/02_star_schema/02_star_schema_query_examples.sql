/*
Day 41 — Star Schema Query Examples

목표:
- Star Schema 구조가 실제 분석 쿼리에서 어떻게 활용되는지 보여준다.
- 집계, 그룹화, Top-N, 세그먼트 분석 패턴을 예시로 작성한다.
- Fact + Dimension 조인이 단순하고 예측 가능하다는 것을 증명한다.
*/


/* =========================================================
1️⃣ 월별 매출 집계 (Time-based Aggregation)
- 날짜 차원을 활용한 월 단위 집계
========================================================= */

-- 월별 총 매출
SELECT
  d.year,
  d.month,
  SUM(f.total_amount) AS monthly_revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


/* =========================================================
2️⃣ 카테고리별 매출 분석 (Product Dimension 활용)
========================================================= */

-- 상품 카테고리별 총 매출
SELECT
  p.category,
  SUM(f.total_amount) AS category_revenue,
  SUM(f.quantity_sold) AS total_units
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY category_revenue DESC;


/* =========================================================
3️⃣ 고객 세그먼트 분석 (Customer Dimension 활용)
========================================================= */

-- 연령대별 매출
SELECT
  c.age_band,
  COUNT(DISTINCT c.customer_key) AS unique_customers,
  SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.age_band
ORDER BY revenue DESC;


/* =========================================================
4️⃣ 지역별 매출 분석 (Store Dimension 활용)
========================================================= */

-- 지역 + 채널별 매출
SELECT
  s.region,
  s.channel,
  SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_store s ON f.store_key = s.store_key
GROUP BY s.region, s.channel
ORDER BY revenue DESC;


/* =========================================================
5️⃣ Top-N 상품 분석
========================================================= */

-- 매출 상위 5개 상품
SELECT
  p.product_name,
  SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 5;


/* =========================================================
6️⃣ 고객 생애가치(LTV) 단순 계산 예시
========================================================= */

-- 고객별 누적 매출
SELECT
  c.customer_id,
  SUM(f.total_amount) AS lifetime_value
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.customer_id
ORDER BY lifetime_value DESC;


/* =========================================================
7️⃣ 다차원 집계 예시 (Year + Category)
========================================================= */

-- 연도별 + 카테고리별 매출
SELECT
  d.year,
  p.category,
  SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY d.year, p.category
ORDER BY d.year, revenue DESC;