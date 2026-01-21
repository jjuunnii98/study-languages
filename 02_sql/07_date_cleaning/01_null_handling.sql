/*
Day 18: SQL Data Cleaning — NULL Handling

NULL은 "값이 없음"을 의미하며,
실무 데이터 분석과 모델링에서 가장 많은 오류를 발생시키는 원인 중 하나다.

핵심 포인트:
- NULL은 0이나 빈 문자열('')과 다르다
- NULL과의 비교는 반드시 IS NULL / IS NOT NULL을 사용해야 한다
- 집계 함수, 조건문, 계산식에서 NULL 처리가 매우 중요하다
*/


/* ------------------------------------------------------------
[Example 1] NULL 값 확인: IS NULL / IS NOT NULL
------------------------------------------------------------ */

SELECT *
FROM customers
WHERE email IS NULL;

SELECT *
FROM customers
WHERE phone IS NOT NULL;


/*
주의:
- WHERE email = NULL ❌ (항상 FALSE)
- WHERE email IS NULL ✅
*/


/* ------------------------------------------------------------
[Example 2] COALESCE: NULL을 대체 값으로 변환
- 가장 많이 사용되는 NULL 처리 함수
------------------------------------------------------------ */

SELECT
  customer_id,
  COALESCE(name, 'unknown') AS customer_name,
  COALESCE(email, 'no_email') AS email
FROM customers;


/*
COALESCE(a, b, c)
→ a가 NULL이면 b
→ b도 NULL이면 c
*/


/* ------------------------------------------------------------
[Example 3] NULLIF: 특정 값을 NULL로 변환
- 데이터 정제 시 매우 유용
------------------------------------------------------------ */

SELECT
  user_id,
  NULLIF(TRIM(name), '') AS cleaned_name
FROM users;


/*
설명:
- 빈 문자열('')은 의미 없는 값인 경우가 많다
- NULLIF를 사용해 '' → NULL로 통일
*/


/* ------------------------------------------------------------
[Example 4] CASE WHEN을 이용한 조건부 NULL 처리
------------------------------------------------------------ */

SELECT
  order_id,
  amount,
  CASE
    WHEN amount IS NULL THEN 0
    ELSE amount
  END AS amount_filled
FROM orders;


/*
실무 팁:
- COALESCE로 가능한 경우가 많지만
- 조건이 복잡하면 CASE WHEN이 더 명확
*/


/* ------------------------------------------------------------
[Example 5] 집계 함수와 NULL
------------------------------------------------------------ */

SELECT
  COUNT(*) AS total_rows,
  COUNT(amount) AS non_null_amount_count,
  SUM(amount) AS total_amount,
  AVG(amount) AS avg_amount
FROM orders;


/*
설명:
- COUNT(*) : 전체 행 수 (NULL 포함)
- COUNT(column) : NULL 제외
- SUM / AVG : NULL 자동 제외
*/


/* ------------------------------------------------------------
[Example 6] 계산식에서 NULL 주의
------------------------------------------------------------ */

SELECT
  order_id,
  quantity,
  price,
  quantity * price AS total_price,              -- NULL 발생 가능
  COALESCE(quantity, 0) * COALESCE(price, 0) AS safe_total_price
FROM order_items;


/*
실무 포인트:
- 계산식에 NULL이 하나라도 있으면 결과는 NULL
- 분석/리포트에서는 COALESCE로 방어적 처리 필수
*/


/* ------------------------------------------------------------
[Example 7] WHERE 절에서 NULL 필터링 패턴
------------------------------------------------------------ */

-- 값이 존재하는 데이터만 사용
SELECT *
FROM users
WHERE last_login_at IS NOT NULL;

-- 값이 없거나 특정 값인 경우
SELECT *
FROM users
WHERE last_login_at IS NULL
   OR status = 'inactive';


/*
요약
- NULL은 모든 실무 데이터에서 반드시 다뤄야 한다
- IS NULL / IS NOT NULL을 정확히 사용
- COALESCE, NULLIF, CASE WHEN은 필수 도구
- 집계/계산/조건문에서 NULL을 방어적으로 처리하자
*/