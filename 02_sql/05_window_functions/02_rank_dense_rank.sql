/*
Day 14: SQL Window Functions — RANK() vs DENSE_RANK()

This file demonstrates professional usage of ranking window functions:
- RANK() vs DENSE_RANK() tie-handling
- Partitioned ranking (rank within groups)
- Top-N per group patterns
- Deterministic ordering (avoid ambiguous ties)
- Practical analytics examples

본 파일은 실무에서 자주 쓰는 순위 윈도우 함수를 다룬다:
- 동점(tie) 처리 방식에 따른 RANK vs DENSE_RANK 차이
- PARTITION BY로 그룹별 순위 계산
- 그룹별 Top-N 추출 패턴
- ORDER BY 정렬 기준을 명확히 하여 재현성 있는 결과 만들기
*/

/* =========================================================
0) Example Schema (for context)
------------------------------------------------------------
Assume we have a table like:

sales(
  order_id     INT,
  customer_id  INT,
  category     VARCHAR,
  amount       DECIMAL(12,2),
  order_date   DATE
)

※ 아래 쿼리는 분석 목적 예제이며,
   실제 DB에서는 테이블/컬럼명을 상황에 맞게 바꾸면 된다.
========================================================= */


/* =========================================================
1) Global Ranking (전체 순위): RANK vs DENSE_RANK
------------------------------------------------------------
- RANK(): 동점이 있으면 다음 순위가 "건너뛴다" (1,1,3,...)
- DENSE_RANK(): 동점이 있어도 다음 순위를 "연속"으로 매긴다 (1,1,2,...)

실무 포인트:
- "순위 번호 자체가 의미"일 때(예: Top 3 레벨링) DENSE_RANK가 자연스러움
- "경쟁 순위"처럼 동점 처리 후 번호를 건너뛰는 개념이 필요하면 RANK
========================================================= */

SELECT
  customer_id,
  amount,
  RANK() OVER (ORDER BY amount DESC)        AS rank_competition,
  DENSE_RANK() OVER (ORDER BY amount DESC)  AS rank_dense
FROM sales;


/* =========================================================
2) Deterministic Ranking (재현성 있는 정렬)
------------------------------------------------------------
동일 amount가 많으면 ORDER BY amount만으로는 "결과가 흔들릴 수" 있다.
(특히 DB 엔진/실행 계획에 따라 동점 레코드의 순서가 바뀔 수 있음)

실무에서는 ORDER BY에 "tie-breaker"를 추가한다.
예: amount DESC, order_date DESC, order_id ASC
========================================================= */

SELECT
  order_id,
  customer_id,
  amount,
  order_date,
  RANK() OVER (
    ORDER BY amount DESC, order_date DESC, order_id ASC
  ) AS rank_stable
FROM sales;


/* =========================================================
3) Partitioned Ranking (그룹별 순위)
------------------------------------------------------------
PARTITION BY를 사용하면 "카테고리별", "지역별", "상품별" 등
그룹 내부에서만 순위를 매길 수 있다.

예: category별 매출(amount) 순위
========================================================= */

SELECT
  category,
  customer_id,
  amount,
  RANK() OVER (
    PARTITION BY category
    ORDER BY amount DESC
  ) AS rank_in_category,
  DENSE_RANK() OVER (
    PARTITION BY category
    ORDER BY amount DESC
  ) AS dense_rank_in_category
FROM sales;


/* =========================================================
4) Top-N Per Group Pattern (그룹별 Top-N 추출)
------------------------------------------------------------
윈도우 함수는 "필터"가 아니라 "계산"이기 때문에,
TOP-N을 뽑으려면 보통 서브쿼리/CTE로 한 번 감싼다.

예: category별 Top 3 매출 레코드
- 동점이 있으면 RANK/DENSE_RANK에 따라 결과가 달라진다.
========================================================= */

WITH ranked AS (
  SELECT
    category,
    order_id,
    customer_id,
    amount,
    RANK() OVER (
      PARTITION BY category
      ORDER BY amount DESC
    ) AS rnk
  FROM sales
)
SELECT
  category,
  order_id,
  customer_id,
  amount,
  rnk
FROM ranked
WHERE rnk <= 3
ORDER BY category, rnk, amount DESC;


/* =========================================================
5) Business Use Case Example: "Customer Tiering"
------------------------------------------------------------
예: 고객을 매출 기준으로 등급화한다.
- DENSE_RANK로 등급 번호를 연속적으로 매기면 "티어"가 깔끔해진다.
- 상위 5등급까지 관리하는 경우 등에 적합.

※ 실제로는 amount를 고객 단위로 집계한 뒤 랭킹을 매긴다.
========================================================= */

WITH customer_sales AS (
  SELECT
    customer_id,
    SUM(amount) AS total_amount
  FROM sales
  GROUP BY customer_id
),
tiered AS (
  SELECT
    customer_id,
    total_amount,
    DENSE_RANK() OVER (ORDER BY total_amount DESC) AS tier
  FROM customer_sales
)
SELECT
  customer_id,
  total_amount,
  tier
FROM tiered
WHERE tier <= 5
ORDER BY tier, total_amount DESC;


/* =========================================================
6) Quick Summary
------------------------------------------------------------
- RANK(): 동점 후 순위 건너뜀 (competition ranking)
- DENSE_RANK(): 동점 후 순위 연속 (dense ranking)
- PARTITION BY: 그룹별 순위 계산
- Top-N per group: CTE/서브쿼리 + WHERE rank <= N
- 안정적 결과를 위해 ORDER BY tie-breaker 추가 권장
========================================================= */