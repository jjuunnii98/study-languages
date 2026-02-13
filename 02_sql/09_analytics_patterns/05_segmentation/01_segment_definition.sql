/* 
Day 35 — Segmentation: Segment Definition (SQL)

Goal:
- Define user segments in a consistent, reusable way.
- Build a segmentation table that can be joined to downstream analyses.

핵심:
- 세그먼트는 "설명 가능한 규칙"이어야 한다.
- 단순히 클러스터링 결과만 저장하는 것이 아니라,
  비즈니스 관점으로 재현 가능한 정의가 중요하다.

Assumed table:
- events(user_id, event_time, event_name, revenue)

Output:
- user_segments(user_id, segment, as_of_date, recency_days, frequency_90d, monetary_90d)
*/

WITH params AS (
  SELECT
    CURRENT_DATE AS as_of_date,
    (CURRENT_DATE - INTERVAL '90 day') AS start_90d
),

/* 1) 최근 90일 기준 구매/활동 지표 집계 */
user_metrics AS (
  SELECT
    e.user_id,
    MAX(CASE WHEN e.event_name IN ('purchase', 'login', 'view_item') THEN e.event_time END) AS last_activity_at,
    MAX(CASE WHEN e.event_name = 'purchase' THEN e.event_time END) AS last_purchase_at,
    COUNT(CASE WHEN e.event_name = 'purchase' THEN 1 END) AS purchase_cnt_90d,
    COALESCE(SUM(CASE WHEN e.event_name = 'purchase' THEN e.revenue END), 0) AS revenue_90d
  FROM events e
  CROSS JOIN params p
  WHERE e.event_time >= p.start_90d
  GROUP BY e.user_id
),

/* 2) Recency 계산 (마지막 구매/활동 기준) */
user_rfm AS (
  SELECT
    um.user_id,
    p.as_of_date,
    um.last_activity_at,
    um.last_purchase_at,
    um.purchase_cnt_90d,
    um.revenue_90d,

    /* Recency: 마지막 구매 기준이 더 강한 신호, 없으면 마지막 활동 기준 */
    CASE
      WHEN um.last_purchase_at IS NOT NULL
        THEN DATE_PART('day', p.as_of_date - um.last_purchase_at::date)
      WHEN um.last_activity_at IS NOT NULL
        THEN DATE_PART('day', p.as_of_date - um.last_activity_at::date)
      ELSE NULL
    END AS recency_days
  FROM user_metrics um
  CROSS JOIN params p
),

/* 3) 규칙 기반 세그먼트 정의 */
user_segments AS (
  SELECT
    user_id,
    as_of_date,
    recency_days,
    purchase_cnt_90d AS frequency_90d,
    revenue_90d AS monetary_90d,

    CASE
      /* 신규/활성: 최근 7일 이내 활동 + 구매는 아직 적음 */
      WHEN recency_days <= 7 AND purchase_cnt_90d BETWEEN 0 AND 1 THEN 'new_or_active'

      /* VIP: 최근 30일 이내 + 구매 빈도/매출이 높음 (threshold는 도메인별 조정) */
      WHEN recency_days <= 30 AND (purchase_cnt_90d >= 5 OR revenue_90d >= 300) THEN 'vip'

      /* 반복구매: 최근 45일 이내 + 구매 2회 이상 */
      WHEN recency_days <= 45 AND purchase_cnt_90d >= 2 THEN 'repeat_buyer'

      /* 잠재 이탈: 최근 46~90일 사이에만 활동/구매가 있음 */
      WHEN recency_days BETWEEN 46 AND 90 THEN 'at_risk'

      /* 휴면: 90일 내 활동 자체가 없음 (user_metrics에 없거나 recency NULL) */
      WHEN recency_days IS NULL THEN 'inactive'

      ELSE 'other'
    END AS segment
  FROM user_rfm
)

/* 최종 출력 */
SELECT
  user_id,
  segment,
  as_of_date,
  recency_days,
  frequency_90d,
  monetary_90d
FROM user_segments
ORDER BY segment, monetary_90d DESC, frequency_90d DESC;