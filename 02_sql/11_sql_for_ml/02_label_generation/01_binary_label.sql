/*
Day 50 — Binary Label Generation
File: 02_sql/11_sql_for_ml/02_label_generation/01_binary_label.sql

목표
- 머신러닝 분류 문제를 위한 binary label(0/1 타깃)을 SQL로 생성한다.
- "무엇을 positive event로 볼 것인가?"를 명확히 정의한다.
- label generation 시점과 관측 구간을 분리하는 사고를 익힌다.

핵심 개념
1) Binary Label
   - 0 또는 1로 표현되는 타깃 변수
   - 예: churn 여부, 구매 여부, 재입원 여부, 연체 여부

2) Event Definition
   - positive class(1)가 무엇인지 명확히 정의해야 한다.
   - 정의가 불명확하면 모델 목표도 불명확해진다.

3) Observation Window vs Prediction Window
   - observation window: feature를 수집하는 기간
   - prediction window: 미래 event를 관측하는 기간

4) Leakage 주의
   - label을 정의할 때 future 정보가 feature에 섞이면 안 된다.

예시 시나리오
- 고객이 기준일(anchor_date) 이후 30일 내 구매하면 label=1
- 그렇지 않으면 label=0
*/


/* ============================================================
1️⃣ Example Base Tables
============================================================ */

/*
customers:
- 고객 기준 테이블
- anchor_date: 예측 기준일
*/

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    anchor_date DATE
);


/*
orders:
- 고객 주문 이력 테이블
- order_date를 기준으로 미래 구매 여부를 판단
*/

CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    order_amount DECIMAL(10,2)
);


/* ============================================================
2️⃣ Example Business Question
============================================================ */

/*
문제 정의 예시

"기준일(anchor_date) 이후 30일 안에 구매한 고객을 예측하라."

즉:
- 미래 30일 이내 구매 발생 → label = 1
- 미래 30일 이내 구매 없음 → label = 0
*/


/* ============================================================
3️⃣ Binary Label Generation
============================================================ */

/*
핵심 로직
- 각 고객에 대해
- anchor_date 이후 30일 이내 주문이 존재하면 1
- 없으면 0

중요:
- order_date > anchor_date
- order_date <= anchor_date + 30일

즉 "미래" 이벤트만 label로 사용
*/

SELECT
    c.customer_id,
    c.anchor_date,

    CASE
        WHEN EXISTS (
            SELECT 1
            FROM orders o
            WHERE o.customer_id = c.customer_id
              AND o.order_date > c.anchor_date
              AND o.order_date <= c.anchor_date + INTERVAL '30 day'
        ) THEN 1
        ELSE 0
    END AS purchase_30d_label

FROM customers c;


/* ============================================================
4️⃣ Label Table Creation
============================================================ */

/*
실무에서는 label을 별도 테이블로 저장하는 경우가 많다.
이후 feature table과 join하여 학습 데이터셋을 만든다.
*/

CREATE TABLE IF NOT EXISTS customer_binary_labels AS
SELECT
    c.customer_id,
    c.anchor_date,

    CASE
        WHEN EXISTS (
            SELECT 1
            FROM orders o
            WHERE o.customer_id = c.customer_id
              AND o.order_date > c.anchor_date
              AND o.order_date <= c.anchor_date + INTERVAL '30 day'
        ) THEN 1
        ELSE 0
    END AS purchase_30d_label

FROM customers c;


/* ============================================================
5️⃣ Label Distribution Check
============================================================ */

/*
라벨 생성 후 반드시 클래스 분포를 확인해야 한다.

이유:
- positive 비율이 너무 낮으면 class imbalance 문제
- label 정의가 너무 엄격하거나 느슨할 수 있음
*/

SELECT
    purchase_30d_label,
    COUNT(*) AS cnt,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS ratio
FROM customer_binary_labels
GROUP BY purchase_30d_label;


/* ============================================================
6️⃣ Positive Event Count by Anchor Date
============================================================ */

/*
anchor_date별 positive event 비율 확인
- 특정 시점에 label 분포가 치우치지 않았는지 확인 가능
*/

SELECT
    anchor_date,
    COUNT(*) AS total_customers,
    SUM(purchase_30d_label) AS positive_customers,
    AVG(purchase_30d_label * 1.0) AS positive_rate
FROM customer_binary_labels
GROUP BY anchor_date
ORDER BY anchor_date;


/* ============================================================
7️⃣ Leakage Awareness Notes
============================================================ */

/*
중요한 실무 포인트

feature 생성 시 아래 정보는 절대 포함되면 안 된다.

금지 예시:
- anchor_date 이후의 구매 횟수
- anchor_date 이후의 총 결제금액
- anchor_date 이후의 마지막 활동일

이런 정보는 이미 미래를 알고 있는 것이므로
label leakage를 발생시킨다.
*/


/* ============================================================
8️⃣ Alternative Pattern: Join + Aggregate
============================================================ */

/*
EXISTS 대신 LEFT JOIN + aggregate로도 구현 가능
*/

SELECT
    c.customer_id,
    c.anchor_date,

    CASE
        WHEN COUNT(o.order_id) > 0 THEN 1
        ELSE 0
    END AS purchase_30d_label

FROM customers c
LEFT JOIN orders o
    ON o.customer_id = c.customer_id
   AND o.order_date > c.anchor_date
   AND o.order_date <= c.anchor_date + INTERVAL '30 day'
GROUP BY
    c.customer_id,
    c.anchor_date;


/* ============================================================
9️⃣ Summary
============================================================ */

/*
정리

1) Binary Label은 classification 문제의 타깃이다.
2) Event 정의가 명확해야 한다.
3) anchor_date 이후 미래 event만 label에 포함해야 한다.
4) feature와 label의 시간 경계를 명확히 구분해야 한다.
5) label 생성 후 class balance를 반드시 확인해야 한다.

즉,
label generation은 단순 SQL이 아니라
"예측 문제 정의" 그 자체다.
*/