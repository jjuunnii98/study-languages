/*
Day 48 — Numerical Feature Engineering
File: 02_sql/11_sql_for_ml/01_feature_engineering/01_numerical_features.sql

목표
- 머신러닝 모델에서 사용할 수 있는 수치형 feature를 SQL에서 생성한다.
- Raw 데이터에서 의미 있는 파생 변수(feature)를 만든다.

대표적인 수치형 Feature Engineering:

1) Scaling / Normalization
2) Ratio Features
3) Difference Features
4) Log Transform
5) Aggregation-based Features
6) Window Function Features

실무 포인트
- Feature engineering은 Python 이전 단계에서 SQL로 상당 부분 처리 가능하다.
- 데이터웨어하우스에서 feature를 생성하면 파이프라인 재현성이 좋아진다.
*/


/* ============================================================
1️⃣ Example Base Table
============================================================ */

-- 고객 구매 데이터 예시 테이블

CREATE TABLE IF NOT EXISTS customer_transactions (
    transaction_id INT PRIMARY KEY,
    customer_id INT,
    purchase_amount DECIMAL(10,2),
    purchase_count INT,
    account_age_days INT,
    transaction_date DATE
);


/* ============================================================
2️⃣ Basic Numerical Feature Creation
============================================================ */

-- 기본 파생 feature 생성

SELECT
    customer_id,

    -- 총 구매금액
    SUM(purchase_amount) AS total_purchase,

    -- 평균 구매금액
    AVG(purchase_amount) AS avg_purchase,

    -- 총 구매 횟수
    SUM(purchase_count) AS total_transactions,

    -- 최대 구매금액
    MAX(purchase_amount) AS max_purchase,

    -- 최소 구매금액
    MIN(purchase_amount) AS min_purchase

FROM customer_transactions
GROUP BY customer_id;


/*
한국어 설명

ML에서는 raw transaction 데이터를 그대로 사용하지 않고
고객 단위로 aggregation을 수행하여 feature를 만든다.

예:

total_purchase
avg_purchase
max_purchase
transaction_count
*/


/* ============================================================
3️⃣ Ratio Feature
============================================================ */

-- 구매당 평균 금액

SELECT
    customer_id,
    SUM(purchase_amount) / NULLIF(SUM(purchase_count),0) AS avg_amount_per_purchase
FROM customer_transactions
GROUP BY customer_id;


/*
Ratio Feature

비율 변수는 ML에서 매우 중요한 feature다.

예:
구매금액 / 구매횟수
사용시간 / 로그인횟수
매출 / 직원수
*/


/* ============================================================
4️⃣ Difference Feature
============================================================ */

-- 최근 거래와 이전 거래 간 금액 차이

SELECT
    customer_id,
    transaction_id,
    purchase_amount,

    purchase_amount -
    LAG(purchase_amount) OVER(
        PARTITION BY customer_id
        ORDER BY transaction_date
    ) AS purchase_diff

FROM customer_transactions;


/*
Difference Feature

시간 순서 데이터에서는 변화량이 중요한 feature가 된다.

예:
현재 매출 - 이전 매출
현재 가격 - 이전 가격
현재 활동 - 이전 활동
*/


/* ============================================================
5️⃣ Log Transformation
============================================================ */

-- 로그 변환 feature

SELECT
    customer_id,
    purchase_amount,

    LOG(purchase_amount + 1) AS log_purchase_amount

FROM customer_transactions;


/*
Log Transform

금액 데이터는 종종 heavy-tail 분포를 가진다.

log 변환을 통해

- 분포 안정화
- extreme value 완화
- 모델 학습 안정성 개선

효과를 얻을 수 있다.
*/


/* ============================================================
6️⃣ Window Aggregation Feature
============================================================ */

-- 고객별 누적 구매 금액

SELECT
    customer_id,
    transaction_date,
    purchase_amount,

    SUM(purchase_amount) OVER(
        PARTITION BY customer_id
        ORDER BY transaction_date
    ) AS cumulative_purchase

FROM customer_transactions;


/*
Window Feature

누적 합계 / 평균 / 카운트는
고객 행동 패턴을 설명하는 중요한 feature다.

예:

cumulative_purchase
rolling_avg
rolling_sum
*/


/* ============================================================
7️⃣ Rolling Feature
============================================================ */

-- 최근 3회 거래 평균

SELECT
    customer_id,
    transaction_date,
    purchase_amount,

    AVG(purchase_amount) OVER(
        PARTITION BY customer_id
        ORDER BY transaction_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS rolling_avg_3

FROM customer_transactions;


/*
Rolling Feature

최근 행동 패턴을 반영하는 feature

예:

최근 7일 구매
최근 3회 거래 평균
최근 30일 로그인 횟수
*/


/* ============================================================
8️⃣ Feature Table for ML
============================================================ */

-- ML 모델 입력용 Feature Table 생성

CREATE TABLE IF NOT EXISTS customer_features AS

SELECT
    customer_id,

    SUM(purchase_amount) AS total_purchase,
    AVG(purchase_amount) AS avg_purchase,
    MAX(purchase_amount) AS max_purchase,

    SUM(purchase_count) AS total_transactions,

    SUM(purchase_amount) /
    NULLIF(SUM(purchase_count),0) AS avg_amount_per_purchase,

    LOG(SUM(purchase_amount) + 1) AS log_total_purchase

FROM customer_transactions
GROUP BY customer_id;


/*
Feature Table

실무에서는

Raw Table
↓
Feature Table
↓
ML Dataset

구조를 사용한다.
*/