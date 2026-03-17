/*
Day 52 — Random Train/Test Split
File: 02_sql/11_sql_for_ml/03_train_test_split/01_random_split.sql

목표
- 머신러닝 학습용 데이터셋을 SQL에서 train / test로 무작위 분할한다.
- split_flag 또는 dataset_type 컬럼을 생성하여
  각 row가 train인지 test인지 구분할 수 있게 한다.
- random split의 기본 개념과 주의점을 이해한다.

핵심 개념
1) Train Set
   - 모델 학습에 사용하는 데이터

2) Test Set
   - 학습이 끝난 후 모델 성능을 평가하는 데이터

3) Random Split
   - 전체 데이터를 무작위로 섞어서 일정 비율로 분할
   - 예: 80% train / 20% test

4) 재현성(Reproducibility) 주의
   - DB마다 random 함수가 실행 시점마다 달라질 수 있음
   - 완전한 재현이 필요하면 해시 기반 분할 또는 seed 지원 방식 고려

5) 한계
   - random split은 기본 패턴이지만
     class imbalance, time series, leakage 위험이 있으면
     stratified split / time-based split이 더 적절할 수 있다.

예시 시나리오
- feature + label이 준비된 customer_ml_dataset 테이블이 있다.
- 각 row를 무작위로 train / test에 배정한다.
*/


/* ============================================================
1️⃣ Example Source Table
============================================================ */

/*
예시 테이블
- 이미 feature engineering과 label generation이 끝난 상태라고 가정
*/

CREATE TABLE IF NOT EXISTS customer_ml_dataset (
    customer_id INT PRIMARY KEY,
    feature_1 DECIMAL(10, 4),
    feature_2 DECIMAL(10, 4),
    feature_3 INT,
    label INT
);


/* ============================================================
2️⃣ Basic Random Split Logic
============================================================ */

/*
핵심 아이디어
- 각 row마다 random 값을 생성
- 0.8 미만이면 train
- 0.8 이상이면 test

주의:
- RANDOM() 함수는 DBMS마다 이름/동작이 다를 수 있다.
- PostgreSQL: RANDOM()
- MySQL: RAND()
- BigQuery: RAND()

아래 예시는 PostgreSQL 스타일로 작성
*/

SELECT
    customer_id,
    feature_1,
    feature_2,
    feature_3,
    label,

    RANDOM() AS random_score,

    CASE
        WHEN RANDOM() < 0.8 THEN 'train'
        ELSE 'test'
    END AS dataset_type

FROM customer_ml_dataset;


/* ============================================================
3️⃣ Better Pattern — Use One Random Value Per Row
============================================================ */

/*
중요:
아래처럼 RANDOM()를 여러 번 호출하면
같은 row에서 값이 달라질 수 있다.

잘못된 예시:
    RANDOM() AS random_score
    CASE WHEN RANDOM() < 0.8 THEN ...

이 경우 random_score와 dataset_type 기준 값이 다를 수 있음

따라서 CTE 또는 subquery에서
"한 번 생성한 random value"를 재사용하는 것이 더 안전하다.
*/

WITH randomized AS (
    SELECT
        customer_id,
        feature_1,
        feature_2,
        feature_3,
        label,
        RANDOM() AS random_score
    FROM customer_ml_dataset
)
SELECT
    customer_id,
    feature_1,
    feature_2,
    feature_3,
    label,
    random_score,

    CASE
        WHEN random_score < 0.8 THEN 'train'
        ELSE 'test'
    END AS dataset_type

FROM randomized;


/* ============================================================
4️⃣ Create Split Table
============================================================ */

/*
실무에서는 split 결과를 별도 테이블로 저장하는 경우가 많다.
이후 Python / R / ML pipeline에서 바로 사용 가능
*/

CREATE TABLE IF NOT EXISTS customer_ml_random_split AS
WITH randomized AS (
    SELECT
        customer_id,
        feature_1,
        feature_2,
        feature_3,
        label,
        RANDOM() AS random_score
    FROM customer_ml_dataset
)
SELECT
    customer_id,
    feature_1,
    feature_2,
    feature_3,
    label,
    random_score,

    CASE
        WHEN random_score < 0.8 THEN 'train'
        ELSE 'test'
    END AS dataset_type

FROM randomized;


/* ============================================================
5️⃣ Split Ratio Check
============================================================ */

/*
split 비율이 의도한 대로 생성되었는지 확인
*/

SELECT
    dataset_type,
    COUNT(*) AS row_count,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS ratio
FROM customer_ml_random_split
GROUP BY dataset_type;


/* ============================================================
6️⃣ Label Distribution Check
============================================================ */

/*
train / test 간 label 분포 차이 확인

한국어 설명
- random split을 했더라도
  label 비율이 train/test에서 많이 달라질 수 있다.
- 특히 불균형 데이터에서는 stratified split이 더 적절할 수 있다.
*/

SELECT
    dataset_type,
    label,
    COUNT(*) AS row_count,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER(PARTITION BY dataset_type) AS within_dataset_ratio
FROM customer_ml_random_split
GROUP BY
    dataset_type,
    label
ORDER BY
    dataset_type,
    label;


/* ============================================================
7️⃣ Example: Train/Test Separate Views
============================================================ */

/*
실무에서는 view 또는 downstream query로 분리해서 사용 가능
*/

CREATE OR REPLACE VIEW customer_ml_train AS
SELECT *
FROM customer_ml_random_split
WHERE dataset_type = 'train';


CREATE OR REPLACE VIEW customer_ml_test AS
SELECT *
FROM customer_ml_random_split
WHERE dataset_type = 'test';


/* ============================================================
8️⃣ Hash-Based Reproducible Alternative (Concept)
============================================================ */

/*
완전한 재현성이 중요하면 random 대신 hash 기반 분할을 고려할 수 있다.

예시 개념:
- customer_id를 해시
- 해시값의 특정 범위를 train / test로 매핑

장점:
- 같은 row는 항상 같은 split으로 감
- 재실행해도 결과가 동일

DBMS마다 해시 함수가 다르므로 실제 구현은 환경별로 조정 필요
*/


/* ============================================================
9️⃣ Leakage Notes
============================================================ */

/*
중요:
split은 feature/label 생성이 끝난 뒤에 해야 한다.

또한 아래 상황은 주의:
- 같은 고객이 여러 row로 존재
- 같은 이벤트 시퀀스가 train/test에 동시에 들어감
- 시계열 데이터에서 미래 정보가 섞임

이 경우 random split만으로는 부족할 수 있다.

예:
- 고객 단위 split 필요
- 시간 기준 split 필요
- stratified split 필요
*/


/* ============================================================
🔟 Summary
============================================================ */

/*
정리

1) random split은 SQL에서 가장 기본적인 train/test 분할 방식이다.
2) random value는 row마다 한 번만 생성해서 재사용하는 것이 안전하다.
3) split 비율과 label 분포를 반드시 검증해야 한다.
4) 불균형 데이터나 시계열 데이터에서는 다른 split 전략이 필요할 수 있다.

즉,
random split은 시작점이지만
문제 구조에 따라 더 정교한 split이 필요하다.
*/