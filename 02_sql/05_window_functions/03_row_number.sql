/*
Day 15: SQL Window Functions — ROW_NUMBER()

ROW_NUMBER()는 윈도우 함수 중 가장 자주 쓰이는 함수 중 하나다.
- 그룹(파티션) 내에서 정렬 기준에 따라 1,2,3... 순번을 부여한다.
- RANK/DENSE_RANK와 달리 "동점(tie)"이 있어도 무조건 고유한 순번을 부여한다.

실무에서 ROW_NUMBER()가 많이 쓰이는 이유:
1) 그룹별 Top-N 추출 (예: 고객별 최근 구매 1건)
2) 중복 제거(dedup) (예: 동일 키에서 최신 레코드만 남기기)
3) 페이징/샘플링/순차 처리용 ID 생성

아래 예제들은 PostgreSQL/MySQL 8+/SQL Server/BigQuery 등에서
개념적으로 동일하게 적용된다. (세부 문법은 DBMS마다 일부 차이 가능)
*/


/* ------------------------------------------------------------
[Example 0] 기본 문법 구조
------------------------------------------------------------ */

-- SELECT
--   ...,
--   ROW_NUMBER() OVER (PARTITION BY <group_cols> ORDER BY <sort_cols>) AS rn
-- FROM <table>;


/* ------------------------------------------------------------
[Example 1] 고객별 구매 내역에 순번 부여
- customer_id 별로 purchase_at 최신순 정렬 → rn=1이 "가장 최근 구매"
------------------------------------------------------------ */

SELECT
  customer_id,
  order_id,
  purchase_at,
  amount,
  ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY purchase_at DESC
  ) AS rn
FROM orders;


/* ------------------------------------------------------------
[Example 2] 고객별 "최근 구매 1건"만 가져오기 (Top-1)
- 위 Example 1을 서브쿼리(또는 CTE)로 감싼 후 rn=1 필터
------------------------------------------------------------ */

WITH ranked_orders AS (
  SELECT
    customer_id,
    order_id,
    purchase_at,
    amount,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id
      ORDER BY purchase_at DESC
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
[Example 3] 고객별 "최근 N건" 가져오기 (Top-N)
- rn <= 3 이면 최근 3건
------------------------------------------------------------ */

WITH ranked_orders AS (
  SELECT
    customer_id,
    order_id,
    purchase_at,
    amount,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id
      ORDER BY purchase_at DESC
    ) AS rn
  FROM orders
)
SELECT
  customer_id,
  order_id,
  purchase_at,
  amount,
  rn
FROM ranked_orders
WHERE rn <= 3
ORDER BY customer_id, rn;


/* ------------------------------------------------------------
[Example 4] 중복 제거(Dedup): 동일 email에서 최신 사용자만 남기기
- user_updates 테이블에 같은 email이 여러 번 들어오는 상황
- updated_at 최신 1건만 남기려면 rn=1만 선택

포인트:
- PARTITION BY: 중복 기준(여기서는 email)
- ORDER BY: 최신 기준(여기서는 updated_at DESC)
------------------------------------------------------------ */

WITH dedup AS (
  SELECT
    user_id,
    email,
    name,
    updated_at,
    ROW_NUMBER() OVER (
      PARTITION BY email
      ORDER BY updated_at DESC
    ) AS rn
  FROM user_updates
)
SELECT
  user_id,
  email,
  name,
  updated_at
FROM dedup
WHERE rn = 1;


/* ------------------------------------------------------------
[Example 5] "최신 + 타이브레이커" 설계
- updated_at이 동일한 레코드(동점)일 수 있다.
- 이 경우 ORDER BY에 추가 기준을 넣어 "결정 규칙"을 명확히 해야 한다.
  예: updated_at DESC, user_id DESC

이렇게 해야 결과가 매번 동일(재현 가능)해진다.
------------------------------------------------------------ */

WITH dedup AS (
  SELECT
    user_id,
    email,
    name,
    updated_at,
    ROW_NUMBER() OVER (
      PARTITION BY email
      ORDER BY updated_at DESC, user_id DESC
    ) AS rn
  FROM user_updates
)
SELECT
  user_id,
  email,
  name,
  updated_at
FROM dedup
WHERE rn = 1;


/* ------------------------------------------------------------
[Example 6] ROW_NUMBER vs RANK vs DENSE_RANK 차이 (개념 정리)
- 동점이 있을 때:
  ROW_NUMBER(): 1,2,3... (무조건 고유 순번)
  RANK():       1,1,3... (동점 다음 순번이 건너뜀)
  DENSE_RANK(): 1,1,2... (동점 다음 순번이 연속)

즉, "정확히 N개만" 뽑고 싶으면 ROW_NUMBER가 더 예측 가능하다.
------------------------------------------------------------ */

SELECT
  department,
  employee_id,
  salary,
  ROW_NUMBER()  OVER (PARTITION BY department ORDER BY salary DESC) AS rn,
  RANK()        OVER (PARTITION BY department ORDER BY salary DESC) AS rnk,
  DENSE_RANK()  OVER (PARTITION BY department ORDER BY salary DESC) AS drnk
FROM employees;


/* ------------------------------------------------------------
[Example 7] 페이징/배치 처리에 활용
- 전체 데이터를 정렬 기준으로 순번 매긴 후
- rn 범위로 원하는 구간만 가져올 수 있다.
(대규모 데이터에서는 OFFSET보다 성능이 나을 때가 많다)

주의:
- DBMS에 따라 최적화 방식이 다르며, 인덱스 설계가 중요하다.
------------------------------------------------------------ */

WITH numbered AS (
  SELECT
    order_id,
    purchase_at,
    amount,
    ROW_NUMBER() OVER (ORDER BY purchase_at DESC, order_id DESC) AS rn
  FROM orders
)
SELECT
  order_id,
  purchase_at,
  amount
FROM numbered
WHERE rn BETWEEN 101 AND 200
ORDER BY rn;


/*
요약
- ROW_NUMBER()는 그룹 내 "고유 순번"을 만드는 함수
- Top-N, dedup(최신 1건), 페이징/배치 처리에서 매우 자주 쓰인다
- ORDER BY에 타이브레이커를 넣어 결과의 재현성을 확보하자
*/