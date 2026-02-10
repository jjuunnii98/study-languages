/*
Day 32: Time Bucket Aggregation (Time Series Analysis)

[EN]
This script demonstrates how to aggregate event data into time buckets
(day/week/month) for time-series analytics:
- Daily/weekly/monthly buckets using DATE_TRUNC
- Handling time zones safely
- Generating a continuous date series (fill missing buckets with 0)
- Producing a clean, reusable time-series metric table

[KR]
이 SQL은 시계열 분석의 기본인 "시간 버킷(time bucket) 집계"를 다룬다.
단순 GROUP BY가 아니라,
- 일/주/월 단위 버킷 생성
- 타임존 처리(UTC 기준 권장)
- 누락 구간(빈 날짜/주)을 채워 0으로 만드는 방식
- 이후 rolling/누적 집계에 바로 쓸 수 있는 테이블 형태 출력
까지 포함한다.

DB: PostgreSQL 기준 (DATE_TRUNC, generate_series 사용)
*/

-- ============================================================
-- 0) Example schema (assumed)
-- ============================================================
-- events (
--   event_id        BIGINT,
--   user_id         BIGINT,
--   event_type      TEXT,          -- e.g., 'signup', 'purchase', 'login'
--   event_ts        TIMESTAMPTZ,    -- timestamp with timezone (recommended)
--   revenue         NUMERIC         -- nullable, only for purchase events
-- )

-- ============================================================
-- 1) Define analysis window
-- ============================================================
-- [KR] 분석 구간을 명시적으로 잡는 습관은 매우 중요하다.
--      (대시보드/리포트는 항상 "기간"을 갖는다)
WITH params AS (
  SELECT
    -- ✅ 분석 시작/종료일 (UTC 기준 권장)
    DATE '2026-01-01' AS start_date,
    DATE '2026-01-31' AS end_date
),

-- ============================================================
-- 2) Normalize timestamps to UTC and filter window
-- ============================================================
base_events AS (
  SELECT
    e.event_id,
    e.user_id,
    e.event_type,
    -- ✅ 타임존 통일: event_ts를 UTC로 정규화한 뒤 date_trunc에 사용
    (e.event_ts AT TIME ZONE 'UTC') AS event_ts_utc,
    e.revenue
  FROM events e
  CROSS JOIN params p
  WHERE (e.event_ts AT TIME ZONE 'UTC') >= p.start_date
    AND (e.event_ts AT TIME ZONE 'UTC') <  (p.end_date + INTERVAL '1 day')
),

-- ============================================================
-- 3) Daily bucket aggregation (core example)
-- ============================================================
daily_agg AS (
  SELECT
    DATE_TRUNC('day', event_ts_utc)::date AS bucket_date,
    COUNT(*) AS event_count,
    COUNT(DISTINCT user_id) AS active_users,
    -- [KR] 매출은 purchase 이벤트만 합산하는 식으로 "비즈니스 로직 분리" 권장
    SUM(CASE WHEN event_type = 'purchase' THEN COALESCE(revenue, 0) ELSE 0 END) AS revenue_sum,
    SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchase_count
  FROM base_events
  GROUP BY 1
),

-- ============================================================
-- 4) Create continuous date series (fill missing days)
-- ============================================================
date_spine AS (
  SELECT
    gs::date AS bucket_date
  FROM params p
  CROSS JOIN generate_series(p.start_date, p.end_date, INTERVAL '1 day') AS gs
),

-- ============================================================
-- 5) Final daily time series with zero-filled missing days
-- ============================================================
daily_filled AS (
  SELECT
    s.bucket_date,
    COALESCE(d.event_count, 0) AS event_count,
    COALESCE(d.active_users, 0) AS active_users,
    COALESCE(d.revenue_sum, 0) AS revenue_sum,
    COALESCE(d.purchase_count, 0) AS purchase_count
  FROM date_spine s
  LEFT JOIN daily_agg d
    ON s.bucket_date = d.bucket_date
)

-- ============================================================
-- 6) Output: daily metrics table (ready for BI / next steps)
-- ============================================================
SELECT
  bucket_date,
  event_count,
  active_users,
  revenue_sum,
  purchase_count,
  CASE
    WHEN purchase_count = 0 THEN 0
    ELSE revenue_sum / purchase_count
  END AS avg_revenue_per_purchase
FROM daily_filled
ORDER BY bucket_date;


-- ============================================================
-- (Optional) Weekly / Monthly bucket examples
-- ============================================================
-- [KR] 주/월 집계는 동일한 패턴으로 date_trunc 단위를 바꾸면 된다.
--      단, "주 시작 요일(월요일 vs 일요일)"은 조직/국가/BI툴 규칙에 맞춰 명시해야 한다.

-- Weekly (ISO week start is Monday in Postgres with date_trunc('week', ...))
-- SELECT
--   DATE_TRUNC('week', event_ts_utc)::date AS week_start,
--   COUNT(*) AS event_count,
--   COUNT(DISTINCT user_id) AS active_users
-- FROM base_events
-- GROUP BY 1
-- ORDER BY 1;

-- Monthly
-- SELECT
--   DATE_TRUNC('month', event_ts_utc)::date AS month_start,
--   COUNT(*) AS event_count,
--   COUNT(DISTINCT user_id) AS active_users
-- FROM base_events
-- GROUP BY 1
-- ORDER BY 1;