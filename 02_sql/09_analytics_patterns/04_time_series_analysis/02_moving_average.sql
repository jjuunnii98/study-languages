/*
Day 33: Moving Average (Time Series Analysis)

[EN]
This script demonstrates moving average patterns using SQL window functions:
- Simple moving average (SMA) for smoothing daily metrics
- Rolling sums and rolling averages with explicit window frames
- Comparing raw vs smoothed trends (trend vs noise)
- Best practice: compute on a continuous date spine to avoid bias

[KR]
이 SQL은 시계열 분석에서 가장 많이 쓰이는 "이동평균(Moving Average)"을 다룬다.
이동평균은 단기 변동(노이즈)을 줄이고 추세(trend)를 보기 위한 대표적인 방법이다.

핵심 포인트:
- WINDOW frame을 명시적으로 지정 (ROWS BETWEEN ...)
- 결측 날짜를 0으로 채운 연속 날짜(date spine) 기반에서 계산
- raw 지표 vs smoothed 지표를 같이 출력하여 비교 가능하게 설계
- DAU/매출 등 다양한 지표에 동일 패턴 적용

DB: PostgreSQL 기준
*/

-- ============================================================
-- 0) Assumptions
-- ============================================================
-- Day 32에서 만든 daily time-series 테이블(또는 뷰)을 입력으로 사용한다고 가정한다.
-- 예: daily_metrics(bucket_date, event_count, active_users, revenue_sum, purchase_count, ...)
--
-- 만약 실제 테이블이 없다면 Day 32 쿼리의 최종 SELECT를
-- materialize(테이블/뷰로 저장)한 뒤 사용하는 것을 권장한다.

-- ============================================================
-- 1) Base daily metrics (replace with your actual table/view)
-- ============================================================
WITH daily_metrics AS (
  SELECT
    bucket_date,
    event_count,
    active_users,
    revenue_sum
  FROM daily_filled   -- ✅ Day 32 결과(연속 날짜 + 0-filled)가 있는 형태를 권장
),

-- ============================================================
-- 2) Moving average calculations
-- ============================================================
ma AS (
  SELECT
    bucket_date,
    event_count,
    active_users,
    revenue_sum,

    -- --------------------------------------------------------
    -- (A) 7-day moving average (including today)
    -- --------------------------------------------------------
    -- [KR] "오늘 포함 7일 평균" (t-6 ~ t)
    AVG(active_users) OVER (
      ORDER BY bucket_date
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS dau_ma7,

    AVG(revenue_sum) OVER (
      ORDER BY bucket_date
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS revenue_ma7,

    -- --------------------------------------------------------
    -- (B) 7-day rolling sum (including today)
    -- --------------------------------------------------------
    SUM(revenue_sum) OVER (
      ORDER BY bucket_date
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS revenue_roll7_sum,

    -- --------------------------------------------------------
    -- (C) 7-day moving average (excluding today)
    -- --------------------------------------------------------
    -- [KR] "오늘 제외 7일 평균" (t-7 ~ t-1)
    --      오늘 값이 급격히 튈 때, 비교/모니터링에 유용
    AVG(active_users) OVER (
      ORDER BY bucket_date
      ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
    ) AS dau_ma7_excl_today,

    -- --------------------------------------------------------
    -- (D) 28-day moving average (monthly-level smoothing)
    -- --------------------------------------------------------
    AVG(active_users) OVER (
      ORDER BY bucket_date
      ROWS BETWEEN 27 PRECEDING AND CURRENT ROW
    ) AS dau_ma28,

    AVG(revenue_sum) OVER (
      ORDER BY bucket_date
      ROWS BETWEEN 27 PRECEDING AND CURRENT ROW
    ) AS revenue_ma28

  FROM daily_metrics
)

-- ============================================================
-- 3) Output: raw + smoothed metrics
-- ============================================================
SELECT
  bucket_date,

  -- raw metrics
  active_users AS dau,
  revenue_sum AS revenue,

  -- smoothed metrics
  ROUND(dau_ma7::numeric, 2) AS dau_ma7,
  ROUND(dau_ma28::numeric, 2) AS dau_ma28,
  ROUND(revenue_ma7::numeric, 2) AS revenue_ma7,
  ROUND(revenue_ma28::numeric, 2) AS revenue_ma28,

  -- rolling sum
  ROUND(revenue_roll7_sum::numeric, 2) AS revenue_roll7_sum,

  -- useful comparison metric
  ROUND((active_users - dau_ma7)::numeric, 2) AS dau_minus_ma7,

  -- optional: trend direction (very simple)
  CASE
    WHEN active_users > dau_ma7 THEN 'above_trend'
    WHEN active_users < dau_ma7 THEN 'below_trend'
    ELSE 'on_trend'
  END AS dau_vs_trend

FROM ma
ORDER BY bucket_date;