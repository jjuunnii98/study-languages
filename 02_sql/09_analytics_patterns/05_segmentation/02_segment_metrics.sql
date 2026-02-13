/*
Day 36 — Segmentation: Segment Metrics (SQL)

Goal:
- Compute segment-level KPIs for reporting and decision-making.
- Provide metrics such as:
  - users in segment
  - active users (last 30d)
  - purchasers (last 90d)
  - revenue (last 90d)
  - ARPU / ARPPU
  - purchase rate
  - average recency

한국어 요약:
- Day 35에서 만든 세그먼트를 "의사결정용 KPI"로 변환하는 단계
- 세그먼트별 규모/활동/구매/매출을 함께 산출하여
  캠페인/제품/리스크 판단에 바로 사용할 수 있게 만든다.

Assumptions:
- user_segments(user_id, segment, as_of_date, recency_days, frequency_90d, monetary_90d)
- events(user_id, event_time, event_name, revenue)
*/

WITH params AS (
  SELECT
    CURRENT_DATE AS as_of_date,
    (CURRENT_DATE - INTERVAL '30 day') AS start_30d,
    (CURRENT_DATE - INTERVAL '90 day') AS start_90d
),

/* 1) 오늘 기준(스냅샷) 세그먼트 */
seg AS (
  SELECT
    us.user_id,
    us.segment,
    us.as_of_date,
    us.recency_days
  FROM user_segments us
  JOIN params p
    ON us.as_of_date = p.as_of_date
),

/* 2) 최근 30일: 활동 유저 */
activity_30d AS (
  SELECT
    e.user_id,
    1 AS is_active_30d
  FROM events e
  CROSS JOIN params p
  WHERE e.event_time >= p.start_30d
    AND e.event_name IN ('login', 'view_item', 'add_to_cart', 'purchase')
  GROUP BY e.user_id
),

/* 3) 최근 90일: 구매 유저 + 구매/매출 */
purchase_90d AS (
  SELECT
    e.user_id,
    COUNT(*) AS purchase_cnt_90d,
    COALESCE(SUM(e.revenue), 0) AS revenue_90d
  FROM events e
  CROSS JOIN params p
  WHERE e.event_time >= p.start_90d
    AND e.event_name = 'purchase'
  GROUP BY e.user_id
),

/* 4) 유저 레벨 지표 결합 */
user_kpis AS (
  SELECT
    s.user_id,
    s.segment,
    s.recency_days,
    COALESCE(a.is_active_30d, 0) AS is_active_30d,
    COALESCE(p.purchase_cnt_90d, 0) AS purchase_cnt_90d,
    COALESCE(p.revenue_90d, 0) AS revenue_90d,
    CASE WHEN COALESCE(p.purchase_cnt_90d, 0) > 0 THEN 1 ELSE 0 END AS is_purchaser_90d
  FROM seg s
  LEFT JOIN activity_30d a ON s.user_id = a.user_id
  LEFT JOIN purchase_90d p ON s.user_id = p.user_id
),

/* 5) 세그먼트 집계 KPI */
segment_metrics AS (
  SELECT
    segment,

    COUNT(*) AS users,
    SUM(is_active_30d) AS active_users_30d,
    SUM(is_purchaser_90d) AS purchasers_90d,

    SUM(purchase_cnt_90d) AS purchases_90d,
    SUM(revenue_90d) AS revenue_90d,

    ROUND(AVG(recency_days)::numeric, 2) AS avg_recency_days,

    /* Purchase Rate: 구매자 / 전체 */
    ROUND(
      (SUM(is_purchaser_90d)::numeric / NULLIF(COUNT(*), 0)) * 100,
      2
    ) AS purchase_rate_pct,

    /* ARPU: 유저당 매출 */
    ROUND(
      (SUM(revenue_90d)::numeric / NULLIF(COUNT(*), 0)),
      2
    ) AS arpu_90d,

    /* ARPPU: 구매자당 매출 */
    ROUND(
      (SUM(revenue_90d)::numeric / NULLIF(SUM(is_purchaser_90d), 0)),
      2
    ) AS arppu_90d

  FROM user_kpis
  GROUP BY segment
)

SELECT *
FROM segment_metrics
ORDER BY revenue_90d DESC, users DESC;