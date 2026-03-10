/*
Day 49 — Categorical Encoding for ML
File: 02_sql/11_sql_for_ml/01_feature_engineering/02_categorical_encoding.sql

목표
- 범주형(categorical) 데이터를 머신러닝 입력용 feature로 변환하는 SQL 패턴 학습
- Python 이전 단계에서 SQL로 처리 가능한 categorical feature engineering 구조 정리

대표적인 categorical encoding 방식
1) Label Encoding
2) One-Hot Encoding
3) Frequency Encoding
4) Binary Flag Encoding
5) Rare Category Grouping

실무 포인트
- SQL에서는 "모델 최종 입력 직전의 feature table"을 만들기 위해
  categorical encoding을 미리 처리하는 경우가 많다.
- 특히 데이터웨어하우스 / feature mart 환경에서는
  SQL 기반 categorical encoding이 재현성과 운영성을 높여준다.

주의
- label encoding은 "숫자 크기 의미"가 생길 수 있으므로
  선형 모델에서는 주의 필요
- one-hot은 category 수가 많아지면 컬럼 폭발 위험
- high-cardinality category는 frequency encoding이나 rare grouping 고려
*/


/* ============================================================
1️⃣ Example Base Table
============================================================ */

/*
고객 거래 데이터 예시
- region, channel, membership_tier 같은 범주형 컬럼 포함
*/

CREATE TABLE IF NOT EXISTS customer_profiles (
    customer_id INT PRIMARY KEY,
    region VARCHAR(50),
    channel VARCHAR(50),
    membership_tier VARCHAR(50),
    signup_source VARCHAR(50)
);


/* ============================================================
2️⃣ Label Encoding
============================================================ */

/*
Label encoding:
범주를 정수 코드로 변환

예:
region
seoul -> 1
busan -> 2
daegu -> 3
etc   -> 4

주의:
이 숫자는 순서를 의미하지 않지만,
모델은 순서를 있다고 해석할 수도 있다.
따라서 tree 계열 모델에서 더 안전하고,
선형 모델에서는 주의가 필요하다.
*/

SELECT
    customer_id,
    region,

    CASE
        WHEN region = 'seoul' THEN 1
        WHEN region = 'busan' THEN 2
        WHEN region = 'daegu' THEN 3
        ELSE 4
    END AS region_label_encoded

FROM customer_profiles;


/* ============================================================
3️⃣ One-Hot Encoding
============================================================ */

/*
One-Hot Encoding:
각 category를 0/1 컬럼으로 변환

예:
channel = 'web'
→ channel_web = 1
→ channel_app = 0
*/

SELECT
    customer_id,
    channel,

    CASE WHEN channel = 'web' THEN 1 ELSE 0 END AS channel_web,
    CASE WHEN channel = 'app' THEN 1 ELSE 0 END AS channel_app,
    CASE WHEN channel = 'offline' THEN 1 ELSE 0 END AS channel_offline

FROM customer_profiles;


/*
한국어 설명

One-hot encoding은 가장 직관적인 categorical encoding 방식이다.
특히 category 수가 적을 때 매우 유용하다.

하지만 category 종류가 많아지면
컬럼 수가 급격히 증가할 수 있다.
*/


/* ============================================================
4️⃣ Frequency Encoding
============================================================ */

/*
Frequency Encoding:
각 category가 데이터에서 얼마나 자주 등장하는지를 feature로 사용

예:
region = 'seoul'
전체 customer 중 seoul 비율 = 0.42
→ region_freq = 0.42
*/

WITH region_freq AS (
    SELECT
        region,
        COUNT(*) AS region_count,
        COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS region_ratio
    FROM customer_profiles
    GROUP BY region
)

SELECT
    c.customer_id,
    c.region,
    r.region_count,
    r.region_ratio
FROM customer_profiles c
JOIN region_freq r
    ON c.region = r.region;


/*
Frequency encoding 장점
- category 수가 많아도 컬럼 폭발 없음
- high-cardinality feature에 유리
- tree 모델이나 boosting 계열에서 baseline으로 자주 사용
*/


/* ============================================================
5️⃣ Rare Category Grouping
============================================================ */

/*
희귀 카테고리(rare category)를 하나로 묶는 패턴

예:
signup_source 중 매우 적게 등장하는 값은 'other'로 통합
*/

WITH source_counts AS (
    SELECT
        signup_source,
        COUNT(*) AS cnt
    FROM customer_profiles
    GROUP BY signup_source
)

SELECT
    c.customer_id,
    c.signup_source,

    CASE
        WHEN s.cnt < 5 THEN 'other'
        ELSE c.signup_source
    END AS signup_source_grouped

FROM customer_profiles c
JOIN source_counts s
    ON c.signup_source = s.signup_source;


/*
한국어 설명

rare category는
- overfitting 위험
- 불안정한 feature
- sparse 문제

를 만들 수 있다.

그래서 일정 빈도 이하 category는
other로 묶는 것이 일반적이다.
*/


/* ============================================================
6️⃣ Binary Flag Encoding
============================================================ */

/*
특정 category 여부를 flag로 만드는 방식

예:
membership_tier = premium 인가?
*/

SELECT
    customer_id,
    membership_tier,

    CASE
        WHEN membership_tier = 'premium' THEN 1
        ELSE 0
    END AS is_premium,

    CASE
        WHEN membership_tier = 'vip' THEN 1
        ELSE 0
    END AS is_vip

FROM customer_profiles;


/*
이 방식은
"특정 중요 category만 분리해서 보고 싶을 때"
매우 자주 사용한다.

예:
is_fraud_country
is_high_value_customer
is_premium_member
*/


/* ============================================================
7️⃣ Combined Feature Table for ML
============================================================ */

/*
실무에서는 categorical encoding 결과를
하나의 feature table로 만드는 경우가 많다.
*/

CREATE TABLE IF NOT EXISTS customer_categorical_features AS

WITH region_freq AS (
    SELECT
        region,
        COUNT(*) AS region_count,
        COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS region_ratio
    FROM customer_profiles
    GROUP BY region
),
source_counts AS (
    SELECT
        signup_source,
        COUNT(*) AS cnt
    FROM customer_profiles
    GROUP BY signup_source
)

SELECT
    c.customer_id,

    /* Label Encoding */
    CASE
        WHEN c.region = 'seoul' THEN 1
        WHEN c.region = 'busan' THEN 2
        WHEN c.region = 'daegu' THEN 3
        ELSE 4
    END AS region_label_encoded,

    /* One-Hot Encoding */
    CASE WHEN c.channel = 'web' THEN 1 ELSE 0 END AS channel_web,
    CASE WHEN c.channel = 'app' THEN 1 ELSE 0 END AS channel_app,
    CASE WHEN c.channel = 'offline' THEN 1 ELSE 0 END AS channel_offline,

    /* Frequency Encoding */
    r.region_ratio AS region_frequency_ratio,

    /* Rare Category Grouping */
    CASE
        WHEN s.cnt < 5 THEN 'other'
        ELSE c.signup_source
    END AS signup_source_grouped,

    /* Binary Flag */
    CASE WHEN c.membership_tier = 'premium' THEN 1 ELSE 0 END AS is_premium,
    CASE WHEN c.membership_tier = 'vip' THEN 1 ELSE 0 END AS is_vip

FROM customer_profiles c
LEFT JOIN region_freq r
    ON c.region = r.region
LEFT JOIN source_counts s
    ON c.signup_source = s.signup_source;


/* ============================================================
8️⃣ Final Notes
============================================================ */

/*
정리

1) Label Encoding
- 간단하지만 순서 의미 주의

2) One-Hot Encoding
- category 수가 적을 때 강력

3) Frequency Encoding
- high-cardinality feature에 유리

4) Rare Category Grouping
- sparse / overfitting 완화

5) Binary Flag
- 중요한 category를 직접 강조 가능

즉,
categorical encoding은
"데이터 분포 + 모델 특성 + 운영 구조"
를 함께 고려해서 선택해야 한다.
*/