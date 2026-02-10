/*
Day 34: Period-over-Period (PoP) Analysis (Time Series Analysis)

[EN]
This script calculates period-over-period changes using SQL window functions:
- WoW (week-over-week) or MoM (month-over-month) style comparisons
- Absolute change and percentage change
- Safe handling of NULLs and division-by-zero
- Designed to be BI-ready and extendable

[KR]
이 SQL은 시계열 분석에서 가장 중요한 패턴 중 하나인
기간 대비 변화(Period-over-Period: WoW/MoM/YoY)를 계산한다.

핵심 포인트:
- LAG()로 이전 기간 값을 가져오기
- 절대 변화량(diff) + 성장률(pct_change) 동시 제공
- 0/NULL 분모 처리(division-by-zero 방지)
- 일 단위 뿐 아니라 주/월 단위로 쉽게 확장 가능
- (권장) 연속 날짜(date spine) 기반 지표 테이블에서 계산

DB: PostgreSQL 기준
*/

-- ============================================================
-- 0) Assumptions
-- ============================================================
-- Day 32에서 만든 일별 지표 테이블/뷰(연속 날짜 + 0-filled)를 사용한다고 가정한다.
-- 예: daily_filled(bucket_date, active_users, revenue_sum, ...)
--
-- 아래 CTE daily_metrics는 예시이며, 실제 환경에서는 테이블/뷰로 대체하면 된다.

WITH daily_metrics AS (
  SELECT
    bucket_date,
    active_users AS dau,
    revenue_sum AS revenue
  FROM daily_filled
),

-- ============================================================
-- 1) Add previous period values using LAG
-- ============================================================
pop AS (
  SELECT
    bucket_date,
    dau,
    revenue,

    -- --------------------------------------------------------
    -- (A) Previous day (DoD: day-over-day)
    -- --------------------------------------------------------
    LAG(dau, 1) OVER (ORDER BY bucket_date) AS dau_prev_day,
    LAG(revenue, 1) OVER (ORDER BY bucket_date) AS rev_prev_day,

    -- --------------------------------------------------------
    -- (B) Previous week (WoW: 7 days ago) - for daily series
    -- --------------------------------------------------------
    LAG(dau, 7) OVER (ORDER BY bucket_date) AS dau_prev_week,
    LAG(revenue, 7) OVER (ORDER BY bucket_date) AS rev_prev_week

    -- [KR] MoM이 필요하면 LAG(..., 28~31)처럼 고정일로 하지 말고,
    --      월 단위 버킷(month_start)로 집계한 뒤 LAG(..., 1)을 쓰는 것을 권장.
  FROM daily_metrics
),

-- ============================================================
-- 2) Compute changes (absolute + percent) with safety guards
-- ============================================================
final AS (
  SELECT
    bucket_date,
    dau,
    revenue,

    -- -------------------------
    -- DoD (vs previous day)
    -- -------------------------
    dau_prev_day,
    (dau - dau_prev_day) AS dau_dod_diff,
    CASE
      WHEN dau_prev_day IS NULL OR dau_prev_day = 0 THEN NULL
      ELSE ROUND(((dau - dau_prev_day)::numeric / dau_prev_day) * 100, 2)
    END AS dau_dod_pct,

    rev_prev_day,
    (revenue - rev_prev_day) AS revenue_dod_diff,
    CASE
      WHEN rev_prev_day IS NULL OR rev_prev_day = 0 THEN NULL
      ELSE ROUND(((revenue - rev_prev_day)::numeric / rev_prev_day) * 100, 2)
    END AS revenue_dod_pct,

    -- -------------------------
    -- WoW (vs 7 days ago)
    -- -------------------------
    dau_prev_week,
    (dau - dau_prev_week) AS dau_wow_diff,
    CASE
      WHEN dau_prev_week IS NULL OR dau_prev_week = 0 THEN NULL
      ELSE ROUND(((dau - dau_prev_week)::numeric / dau_prev_week) * 100, 2)
    END AS dau_wow_pct,

    rev_prev_week,
    (revenue - rev_prev_week) AS revenue_wow_diff,
    CASE
      WHEN rev_prev_week IS NULL OR rev_prev_week = 0 THEN NULL
      ELSE ROUND(((revenue - rev_prev_week)::numeric / rev_prev_week) * 100, 2)
    END AS revenue_wow_pct

  FROM pop
)

-- ============================================================
-- 3) Output (BI-friendly)
-- ============================================================
SELECT
  bucket_date,

  -- current metrics
  dau,
  revenue,

  -- day-over-day
  dau_prev_day,
  dau_dod_diff,
  dau_dod_pct,
  rev_prev_day,
  revenue_dod_diff,
  revenue_dod_pct,

  -- week-over-week
  dau_prev_week,
  dau_wow_diff,
  dau_wow_pct,
  rev_prev_week,
  revenue_wow_diff,
  revenue_wow_pct

FROM final
ORDER BY bucket_date;