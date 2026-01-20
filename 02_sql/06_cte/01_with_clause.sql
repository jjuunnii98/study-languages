/*
Day 16: SQL CTE — WITH clause (Common Table Expression)

CTE(Common Table Expression)는 "임시 결과를 이름 붙여" 쿼리 안에서 재사용하는 구조다.
- 복잡한 쿼리를 단계별로 쪼개서 가독성을 높인다.
- 동일한 서브쿼리를 여러 번 반복하지 않아도 된다.
- 분석/ETL 파이프라인에서 매우 자주 사용된다.

핵심 문법:
WITH cte_name AS (
  SELECT ...
)
SELECT ...
FROM cte_name;

주의:
- DBMS에 따라 최적화 방식이 다를 수 있다.
- 일부 DB에서는 CTE가 materialize(임시 테이블처럼) 될 수 있어 성능에 영향이 있을 수 있다.
  (PostgreSQL은 버전에 따라 최적화 정책이 달라짐)
*/


/* ------------------------------------------------------------
[Example 1] 가장 기본적인 CTE: 가독성 개선
- orders에서 최근 30일 주문만 먼저 뽑고
- 그 결과에서 고객별 매출 합계를 계산
------------------------------------------------------------ */

WITH recent_orders AS (
  SELECT
    order_id,
    customer_id,
    purchase_at,
    amount
  FROM orders
  WHERE purchase_at >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT
  customer_id,
  COUNT(*) AS order_count,
  SUM(amount) AS total_amount,
  AVG(amount) AS avg_amount
FROM recent_orders
GROUP BY customer_id
ORDER BY total_amount DESC;


/* ------------------------------------------------------------
[Example 2] "단계적 변환" (step-by-step pipeline)
- raw_users: 원본
- cleaned_users: 표준화/전처리 결과
- final: 최종 출력

실무에서 CTE는 이렇게 '파이프라인'처럼 쓰는 경우가 많다.
------------------------------------------------------------ */

WITH raw_users AS (
  SELECT
    user_id,
    email,
    name,
    created_at
  FROM users
),
cleaned_users AS (
  SELECT
    user_id,
    LOWER(TRIM(email)) AS email_norm,   -- 이메일 표준화
    NULLIF(TRIM(name), '') AS name,     -- 빈 문자열 -> NULL
    created_at
  FROM raw_users
),
final AS (
  SELECT
    user_id,
    email_norm,
    COALESCE(name, 'unknown') AS name,
    created_at
  FROM cleaned_users
)
SELECT *
FROM final
ORDER BY created_at DESC;


/* ------------------------------------------------------------
[Example 3] CTE + Window Function: 그룹별 Top-1 (최신 레코드)
- 고객별 가장 최근 주문 1건 가져오기
------------------------------------------------------------ */

WITH ranked_orders AS (
  SELECT
    customer_id,
    order_id,
    purchase_at,
    amount,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id
      ORDER BY purchase_at DESC, order_id DESC   -- tie-breaker로 재현성 확보
    ) AS rn
  FROM orders
)
SELECT
  customer_id,
  order_id,
  purchase_at,
  amount
FROM ranked_orders
WHERE rn = 1
ORDER BY customer_id;


/* ------------------------------------------------------------
[Example 4] 집계 결과를 재사용: 전체 평균보다 큰 고객만 선택
- 고객별 총매출을 구하고
- 전체 평균 총매출보다 큰 고객만 필터링

포인트:
- CTE로 집계를 한 번만 수행 → 다른 단계에서 쉽게 재사용 가능
------------------------------------------------------------ */

WITH customer_revenue AS (
  SELECT
    customer_id,
    SUM(amount) AS total_amount
  FROM orders
  GROUP BY customer_id
),
avg_revenue AS (
  SELECT
    AVG(total_amount) AS avg_total_amount
  FROM customer_revenue
)
SELECT
  cr.customer_id,
  cr.total_amount
FROM customer_revenue cr
CROSS JOIN avg_revenue ar
WHERE cr.total_amount > ar.avg_total_amount
ORDER BY cr.total_amount DESC;


/* ------------------------------------------------------------
[Example 5] CTE를 이용한 "디버깅/검증" 관점
- 각 단계 결과를 SELECT로 확인하면서 쿼리를 점진적으로 완성할 수 있다.

실무 팁:
- 복잡한 쿼리는 CTE로 쪼개고,
- 중간 단계별 row 수 / NULL 비율 / 샘플을 확인하면 실수가 줄어든다.
------------------------------------------------------------ */

WITH base AS (
  SELECT
    order_id,
    customer_id,
    amount
  FROM orders
),
flagged AS (
  SELECT
    *,
    CASE WHEN amount >= 1000 THEN 1 ELSE 0 END AS is_high_value
  FROM base
)
SELECT
  is_high_value,
  COUNT(*) AS cnt,
  AVG(amount) AS avg_amount
FROM flagged
GROUP BY is_high_value
ORDER BY is_high_value DESC;


/*
요약
- CTE(WITH)는 복잡한 SQL을 "읽기 쉬운 단계"로 분해한다.
- 동일한 서브쿼리 반복을 줄이고 재사용성을 높인다.
- Window Function과 결합하면 Top-N, dedup, 최신 레코드 선택이 매우 깔끔해진다.
*/