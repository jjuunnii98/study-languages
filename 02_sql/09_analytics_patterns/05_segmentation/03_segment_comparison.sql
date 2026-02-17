/*
Day 37 — Segment Comparison (Segmentation)

Goal:
- Compare segments side-by-side with standardized KPIs
- Add "lift" vs overall average (relative performance)
- Provide rank + share for decision-making

목표:
- 세그먼트별 KPI를 한 화면에서 비교 가능하게 만든다.
- 전체 평균 대비 LIFT(상대 성과)를 계산한다.
- 비즈니스 의사결정용 Rank/Share를 함께 제공한다.

Assumed tables (example):
- users(user_id, signup_date, country, device_type, plan, ...)
- events(user_id, event_time, event_name, revenue, ...)
- user_segments(user_id, segment_key, segment_value)  -- from Day 35
*/

WITH
-- 1) Segment definition (Day 35 output)
segments AS (
  SELECT
    user_id,
    segment_key,
    segment_value
  FROM user_segments
),

-- 2) Build user-level activity metrics (can be adjusted per business)
--    실무에서는 "활성 기준", "구매 기준", "기간"을 명확히 정의하는 게 핵심이다.
user_activity AS (
  SELECT
    e.user_id,
    COUNT(*) FILTER (WHERE e.event_name = 'session') AS sessions,
    COUNT(*) FILTER (WHERE e.event_name = 'purchase') AS purchases,
    COALESCE(SUM(CASE WHEN e.event_name = 'purchase' THEN e.revenue ELSE 0 END), 0) AS revenue
  FROM events e
  -- 기간 조건 예시(필요 시 활성화):
  -- WHERE e.event_time >= DATE '2026-01-01' AND e.event_time < DATE '2026-02-01'
  GROUP BY e.user_id
),

-- 3) Segment metrics (Day 36 concept)
segment_metrics AS (
  SELECT
    s.segment_key,
    s.segment_value,
    COUNT(DISTINCT s.user_id) AS users,
    COUNT(DISTINCT CASE WHEN ua.sessions > 0 THEN s.user_id END) AS active_users,
    COALESCE(SUM(ua.purchases), 0) AS orders,
    COALESCE(SUM(ua.revenue), 0) AS revenue
  FROM segments s
  LEFT JOIN user_activity ua
    ON s.user_id = ua.user_id
  GROUP BY 1, 2
),

-- 4) Compute derived KPIs per segment
segment_kpis AS (
  SELECT
    segment_key,
    segment_value,
    users,
    active_users,
    orders,
    revenue,

    -- 활성률: active_users / users
    CASE WHEN users = 0 THEN 0
         ELSE active_users::numeric / users END AS active_rate,

    -- 구매 전환율: orders / active_users (정의는 상황에 따라 users 기준으로도 가능)
    CASE WHEN active_users = 0 THEN 0
         ELSE orders::numeric / active_users END AS purchase_rate,

    -- ARPU: revenue / users
    CASE WHEN users = 0 THEN 0
         ELSE revenue::numeric / users END AS arpu,

    -- AOV: revenue / orders
    CASE WHEN orders = 0 THEN 0
         ELSE revenue::numeric / orders END AS aov
  FROM segment_metrics
),

-- 5) Overall baseline (전체 평균/전체 KPI)
overall AS (
  SELECT
    segment_key,
    SUM(users) AS total_users,
    SUM(active_users) AS total_active_users,
    SUM(orders) AS total_orders,
    SUM(revenue) AS total_revenue,

    CASE WHEN SUM(users) = 0 THEN 0
         ELSE SUM(active_users)::numeric / SUM(users) END AS overall_active_rate,

    CASE WHEN SUM(active_users) = 0 THEN 0
         ELSE SUM(orders)::numeric / SUM(active_users) END AS overall_purchase_rate,

    CASE WHEN SUM(users) = 0 THEN 0
         ELSE SUM(revenue)::numeric / SUM(users) END AS overall_arpu,

    CASE WHEN SUM(orders) = 0 THEN 0
         ELSE SUM(revenue)::numeric / SUM(orders) END AS overall_aov
  FROM segment_kpis
  GROUP BY segment_key
),

-- 6) Join segment KPIs with baseline + compute lift and share
final AS (
  SELECT
    k.segment_key,
    k.segment_value,
    k.users,
    k.active_users,
    k.orders,
    k.revenue,

    k.active_rate,
    k.purchase_rate,
    k.arpu,
    k.aov,

    -- 전체 대비 사용자 비중(share)
    CASE WHEN o.total_users = 0 THEN 0
         ELSE k.users::numeric / o.total_users END AS user_share,

    -- LIFT (segment KPI / overall KPI)
    -- 1.0보다 크면 전체 대비 성과가 높음
    CASE WHEN o.overall_active_rate = 0 THEN NULL
         ELSE k.active_rate / o.overall_active_rate END AS active_rate_lift,

    CASE WHEN o.overall_purchase_rate = 0 THEN NULL
         ELSE k.purchase_rate / o.overall_purchase_rate END AS purchase_rate_lift,

    CASE WHEN o.overall_arpu = 0 THEN NULL
         ELSE k.arpu / o.overall_arpu END AS arpu_lift,

    CASE WHEN o.overall_aov = 0 THEN NULL
         ELSE k.aov / o.overall_aov END AS aov_lift
  FROM segment_kpis k
  JOIN overall o
    ON k.segment_key = o.segment_key
)

SELECT
  segment_key,
  segment_value,
  users,
  active_users,
  orders,
  revenue,

  ROUND(active_rate::numeric, 4) AS active_rate,
  ROUND(purchase_rate::numeric, 4) AS purchase_rate,
  ROUND(arpu::numeric, 2) AS arpu,
  ROUND(aov::numeric, 2) AS aov,

  ROUND(user_share::numeric, 4) AS user_share,
  ROUND(active_rate_lift::numeric, 4) AS active_rate_lift,
  ROUND(purchase_rate_lift::numeric, 4) AS purchase_rate_lift,
  ROUND(arpu_lift::numeric, 4) AS arpu_lift,
  ROUND(aov_lift::numeric, 4) AS aov_lift,

  -- KPI 기준 랭킹 (예: ARPU 기준)
  DENSE_RANK() OVER (PARTITION BY segment_key ORDER BY arpu DESC) AS arpu_rank
FROM final
ORDER BY segment_key, arpu_rank, users DESC;