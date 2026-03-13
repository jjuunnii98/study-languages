/*
Day 51 — Time-to-Event Label Generation
File: 02_sql/11_sql_for_ml/02_label_generation/02_time_to_event_label.sql

목표
- time-to-event 분석을 위한 라벨을 SQL로 생성한다.
- 각 개체(entity)에 대해:
  1) event 발생 여부
  2) event까지 걸린 시간
  3) censoring 여부
  를 함께 정의한다.

핵심 개념
1) Time-to-Event
   - 특정 기준일(anchor_date) 이후 이벤트가 발생할 때까지 걸린 시간
   - 예: 재입원까지 일수, 이탈까지 일수, 연체 발생까지 일수

2) Event Indicator
   - event 발생: 1
   - censoring(관찰 종료 시점까지 event 없음): 0

3) Censoring
   - 관찰 종료일까지 이벤트가 발생하지 않은 경우
   - "발생 안 함"이 아니라 "관찰 구간 안에서 확인되지 않음"으로 해석

4) Anchor Date
   - 예측/관찰 시작 기준일
   - feature는 이 시점 이전 정보만 사용해야 함

5) Leakage 주의
   - anchor_date 이후 미래 정보는 label 계산에만 사용
   - feature 생성에는 사용하면 안 됨

예시 시나리오
- 고객마다 anchor_date가 있다.
- anchor_date 이후 첫 구매일까지의 일수를 구한다.
- 단, 90일 관찰 구간 안에 구매가 없으면 censoring 처리한다.
*/


/* ============================================================
1️⃣ Example Base Tables
============================================================ */

/*
customers:
- 고객 기준 테이블
- anchor_date: 관찰 시작일
*/

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    anchor_date DATE
);


/*
orders:
- 고객 이벤트 테이블
- 여기서는 "구매 발생"을 event로 가정
*/

CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    order_amount DECIMAL(10,2)
);


/* ============================================================
2️⃣ Business Question
============================================================ */

/*
문제 정의 예시

"고객이 anchor_date 이후 첫 구매를 하기까지 걸린 시간은 얼마인가?"

관찰 규칙:
- observation horizon = 90일
- 90일 안에 구매 발생 → event=1
- 90일 안에 구매 없음 → event=0 (censored)
- event_time_days:
    - event 발생 시: 첫 구매일까지의 일수
    - censoring 시: 90일
*/


/* ============================================================
3️⃣ First Event After Anchor Date
============================================================ */

/*
핵심 로직
- 각 customer_id에 대해
- anchor_date 이후 첫 order_date를 찾는다
- 단, 90일 이내 이벤트만 고려
*/

WITH first_event AS (
    SELECT
        c.customer_id,
        c.anchor_date,
        MIN(o.order_date) AS first_order_date
    FROM customers c
    LEFT JOIN orders o
        ON o.customer_id = c.customer_id
       AND o.order_date > c.anchor_date
       AND o.order_date <= c.anchor_date + INTERVAL '90 day'
    GROUP BY
        c.customer_id,
        c.anchor_date
)

SELECT
    customer_id,
    anchor_date,
    first_order_date
FROM first_event;


/* ============================================================
4️⃣ Time-to-Event Label Generation
============================================================ */

/*
생존분석/시간-이벤트 라벨 생성

출력 컬럼
- event_indicator: 1=이벤트 발생, 0=검열(censored)
- event_time_days: 이벤트까지 일수 또는 censoring 일수
*/

WITH first_event AS (
    SELECT
        c.customer_id,
        c.anchor_date,
        MIN(o.order_date) AS first_order_date
    FROM customers c
    LEFT JOIN orders o
        ON o.customer_id = c.customer_id
       AND o.order_date > c.anchor_date
       AND o.order_date <= c.anchor_date + INTERVAL '90 day'
    GROUP BY
        c.customer_id,
        c.anchor_date
)

SELECT
    customer_id,
    anchor_date,
    first_order_date,

    CASE
        WHEN first_order_date IS NOT NULL THEN 1
        ELSE 0
    END AS event_indicator,

    CASE
        WHEN first_order_date IS NOT NULL
            THEN first_order_date - anchor_date
        ELSE 90
    END AS event_time_days

FROM first_event;


/* ============================================================
5️⃣ Create Label Table
============================================================ */

/*
실무에서는 별도 label table로 저장하는 경우가 많다.
이후 feature table과 join하여 survival / time-to-event dataset 구성
*/

CREATE TABLE IF NOT EXISTS customer_time_to_event_labels AS
WITH first_event AS (
    SELECT
        c.customer_id,
        c.anchor_date,
        MIN(o.order_date) AS first_order_date
    FROM customers c
    LEFT JOIN orders o
        ON o.customer_id = c.customer_id
       AND o.order_date > c.anchor_date
       AND o.order_date <= c.anchor_date + INTERVAL '90 day'
    GROUP BY
        c.customer_id,
        c.anchor_date
)
SELECT
    customer_id,
    anchor_date,
    first_order_date,

    CASE
        WHEN first_order_date IS NOT NULL THEN 1
        ELSE 0
    END AS event_indicator,

    CASE
        WHEN first_order_date IS NOT NULL
            THEN first_order_date - anchor_date
        ELSE 90
    END AS event_time_days

FROM first_event;


/* ============================================================
6️⃣ Distribution Check
============================================================ */

/*
event 발생률 확인
- censoring 비율이 너무 높거나 너무 낮지 않은지 점검
*/

SELECT
    event_indicator,
    COUNT(*) AS cnt,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS ratio
FROM customer_time_to_event_labels
GROUP BY event_indicator;


/*
event_time 분포 확인
- 발생한 경우(event=1) event까지 걸린 시간 분포 점검
*/

SELECT
    MIN(event_time_days) AS min_days,
    AVG(event_time_days * 1.0) AS avg_days,
    MAX(event_time_days) AS max_days
FROM customer_time_to_event_labels
WHERE event_indicator = 1;


/* ============================================================
7️⃣ Anchor-Date Level Monitoring
============================================================ */

/*
anchor_date별 event rate 확인
- 특정 시점에 label 분포가 왜곡되었는지 확인 가능
*/

SELECT
    anchor_date,
    COUNT(*) AS total_customers,
    SUM(event_indicator) AS events,
    AVG(event_indicator * 1.0) AS event_rate,
    AVG(event_time_days * 1.0) AS avg_event_time_days
FROM customer_time_to_event_labels
GROUP BY anchor_date
ORDER BY anchor_date;


/* ============================================================
8️⃣ Censoring Notes
============================================================ */

/*
중요한 해석

event_indicator = 0
→ "이벤트가 절대 발생하지 않음"이 아님
→ "관찰 구간(90일) 안에서는 event가 관측되지 않음"

즉 censoring은
"정보가 불완전한 상태"
를 의미한다.
*/


/* ============================================================
9️⃣ Leakage Awareness
============================================================ */

/*
feature 생성 시 금지되는 예시

- anchor_date 이후 구매 횟수
- anchor_date 이후 총 결제금액
- anchor_date 이후 마지막 주문일
- anchor_date 이후 첫 이벤트 정보 자체

이런 값은 label 생성에는 사용 가능하지만
feature에 포함되면 미래 정보 유출(data leakage)이 된다.
*/


/* ============================================================
🔟 Alternative: Event Horizon Parameterization
============================================================ */

/*
관찰 기간을 90일이 아니라 30일 / 60일 / 180일 등으로 바꿀 수도 있다.
실무에서는 business question에 따라 horizon을 조정한다.

예:
- churn 30d
- purchase 60d
- readmission 180d
*/


/* ============================================================
1️⃣1️⃣ Summary
============================================================ */

/*
정리

1) time-to-event label은
   - event 발생 여부
   - event까지 걸린 시간
   - censoring
   을 함께 정의한다.

2) anchor_date 이전 정보는 feature,
   anchor_date 이후 정보는 label 계산에만 사용한다.

3) 관찰 기간(horizon)을 명확히 정의해야 한다.

4) censoring은 "negative"가 아니라
   "관찰 구간 내 event 미관측"이다.

즉,
time-to-event label generation은
생존분석 / 리스크 모델링의 출발점이다.
*/