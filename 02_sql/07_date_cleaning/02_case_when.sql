/*
Day 19: SQL Data Cleaning — CASE WHEN

CASE WHEN은 SQL에서 "비즈니스 규칙"과 "파생 변수(derived feature)"를 만드는 핵심 도구다.
실무 데이터에서는 숫자/문자 값 자체보다, 이를 해석한 카테고리/구간/상태 변수가 더 중요하다.

핵심 포인트:
- CASE WHEN으로 결측/이상값을 안전하게 처리한다.
- 조건 기반 라벨링(분류), 구간화(bucketing), 상태 플래그(flag) 생성에 사용한다.
- 가능한 경우 ELSE를 명시하여 예외 케이스를 놓치지 않는다.
*/


/* ------------------------------------------------------------
[Example 1] CASE 기본 문법: 조건 분기
------------------------------------------------------------ */

SELECT
  customer_id,
  age,
  CASE
    WHEN age IS NULL THEN 'unknown'
    WHEN age < 18 THEN 'minor'
    WHEN age BETWEEN 18 AND 34 THEN 'young_adult'
    WHEN age BETWEEN 35 AND 54 THEN 'adult'
    ELSE 'senior'
  END AS age_group
FROM customers;


/*
설명:
- age가 NULL이면 unknown으로 처리
- 범위 기반 bucket 생성 (분석/리포팅/모델 입력에 자주 사용)
- ELSE를 둬서 55 이상은 senior로 통일
*/


/* ------------------------------------------------------------
[Example 2] 결측/이상값 정제 + 표준화
------------------------------------------------------------ */

SELECT
  user_id,
  COALESCE(NULLIF(TRIM(city), ''), 'unknown') AS cleaned_city,
  CASE
    WHEN city IS NULL OR TRIM(city) = '' THEN 1
    ELSE 0
  END AS is_city_missing
FROM users;


/*
설명:
- city: NULL 또는 빈 문자열을 'unknown'으로 표준화
- is_city_missing: 결측 여부를 flag로 남김 (품질 모니터링 / 모델 피처로 유용)
*/


/* ------------------------------------------------------------
[Example 3] 금액 기반 리스크/등급 라벨링 (실무 패턴)
------------------------------------------------------------ */

SELECT
  order_id,
  amount,
  CASE
    WHEN amount IS NULL THEN 'unknown'
    WHEN amount < 0 THEN 'invalid'
    WHEN amount = 0 THEN 'free'
    WHEN amount < 50 THEN 'low'
    WHEN amount < 200 THEN 'mid'
    ELSE 'high'
  END AS amount_bucket
FROM orders;


/*
설명:
- 음수 금액은 비정상(invalid)으로 구분해 추후 원인 추적 가능
- 구간 라벨은 리포트/대시보드/세그먼트 분석에 매우 자주 사용
*/


/* ------------------------------------------------------------
[Example 4] 상태(state) 파생: 조건 조합
------------------------------------------------------------ */

SELECT
  account_id,
  last_login_at,
  status,
  CASE
    WHEN status = 'banned' THEN 'blocked'
    WHEN last_login_at IS NULL THEN 'inactive'
    WHEN last_login_at >= CURRENT_DATE - INTERVAL '30 day' THEN 'active_30d'
    ELSE 'dormant'
  END AS activity_state
FROM accounts;


/*
설명:
- 상태와 행동 로그를 결합해 더 의미 있는 상태(activity_state)를 만든다.
- "최근 30일 활동" 같은 규칙은 CRM/마케팅/리텐션 분석에서 표준
주의:
- INTERVAL 문법은 DBMS(PostgreSQL 등)에 따라 다를 수 있음
*/


/* ------------------------------------------------------------
[Example 5] 집계 전에 CASE로 파생변수 만든 후 GROUP BY (실무 중요)
------------------------------------------------------------ */

SELECT
  CASE
    WHEN amount IS NULL OR amount <= 0 THEN 'non_revenue'
    WHEN amount < 50 THEN 'low'
    WHEN amount < 200 THEN 'mid'
    ELSE 'high'
  END AS revenue_segment,
  COUNT(*) AS order_count,
  SUM(COALESCE(amount, 0)) AS total_amount
FROM orders
GROUP BY 1
ORDER BY order_count DESC;


/*
설명:
- CASE 결과를 GROUP BY에 바로 사용 가능
- GROUP BY 1: 첫 번째 컬럼(revenue_segment) 기준 그룹화
- NULL/비정상(amount<=0) 처리를 미리 정의하면 집계가 안정적
*/


/* ------------------------------------------------------------
[Example 6] 조건 기반 "우선순위" 분기 (중요: WHEN 순서가 의미를 가짐)
------------------------------------------------------------ */

SELECT
  ticket_id,
  priority,
  created_at,
  CASE
    WHEN priority = 'P0' THEN 'urgent'
    WHEN priority = 'P1' THEN 'high'
    WHEN priority IN ('P2', 'P3') THEN 'normal'
    ELSE 'low'
  END AS normalized_priority
FROM support_tickets;


/*
설명:
- CASE는 위에서부터 조건을 평가하므로 "우선순위 규칙"은 WHEN 순서가 중요
- ELSE가 없으면 NULL이 될 수 있으므로, 실무에서는 ELSE를 두는 것을 권장
*/


/* ------------------------------------------------------------
[Example 7] (선택) CASE + NULLIF/COALESCE 조합: 가장 실무적인 형태
------------------------------------------------------------ */

SELECT
  user_id,
  CASE
    WHEN COALESCE(NULLIF(TRIM(email), ''), '') = '' THEN 'missing_email'
    WHEN POSITION('@' IN email) = 0 THEN 'invalid_email'
    ELSE 'valid_email'
  END AS email_quality
FROM users;


/*
설명:
- email이 NULL/빈값이면 missing
- '@'가 없으면 invalid (아주 단순한 규칙이지만 품질 점검에 유용)
- 그 외 valid
주의:
- POSITION 함수 역시 DBMS별로 다를 수 있음
*/


/*
Day 19 요약
- CASE WHEN은 비즈니스 규칙을 SQL로 표현하는 핵심 도구
- 구간화(bucketing), 상태(state), 결측 flag, 정규화 라벨 생성에 사용
- ELSE를 명시해 예외 케이스를 관리하자
- 집계 전 파생변수를 만들면 분석이 훨씬 안정적이다
*/