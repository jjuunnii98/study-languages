/*
Day 53 — Stratified Train/Test Split
File: 02_sql/11_sql_for_ml/03_train_test_split/02_stratified_split.sql

목표
- 머신러닝 데이터셋을 label 비율을 유지한 채 train / test로 분할한다.
- stratified split의 기본 원리를 SQL로 구현한다.
- 특히 class imbalance가 있는 데이터에서
  train/test label 분포를 안정적으로 유지하는 방법을 익힌다.

핵심 개념
1) Stratified Split
   - label 값별로 데이터를 나눈 뒤
   - 각 label 내부에서 동일한 비율로 train/test를 분할하는 방식

2) 왜 필요한가?
   - random split은 전체적으로는 80/20이 되어도
     train/test 내부 label 비율이 많이 흔들릴 수 있다.
   - 불균형 데이터에서는 이 문제가 더 커진다.

3) 예시
   - 전체 label=1 비율이 10%라면
   - train도 대략 10%, test도 대략 10%로 유지되도록 분할

4) 구현 방식
   - label별로 random score 생성
   - label별 row_number / count 계산
   - 각 label 그룹 안에서 일정 비율까지는 train, 나머지는 test

주의
- DBMS마다 RANDOM() / RAND() 함수 차이가 있다.
- 아래 예시는 PostgreSQL 스타일 기준
*/


/* ============================================================
1️⃣ Example Source Table
============================================================ */

/*
이미 feature와 label이 준비된 상태라고 가정
*/

CREATE TABLE IF NOT EXISTS customer_ml_dataset (
    customer_id INT PRIMARY KEY,
    feature_1 DECIMAL(10, 4),
    feature_2 DECIMAL(10, 4),
    feature_3 INT,
    label INT
);


/* ============================================================
2️⃣ Why Not Pure Random Only?
============================================================ */

/*
예를 들어 label=1 비율이 매우 낮은 경우
random split만 하면 test에 positive class가 너무 적게 들어갈 수 있다.

stratified split은
각 label 그룹 안에서 따로 분할하기 때문에
train/test의 클래스 분포를 더 안정적으로 유지할 수 있다.
*/


/* ============================================================
3️⃣ Stratified Split Logic
============================================================ */

/*
핵심 구현 아이디어

1. label별로 데이터를 분리
2. 각 label 그룹 안에서 random order 부여
3. 각 label 그룹 row 수 계산
4. 그룹 내부 상위 80%는 train
5. 나머지 20%는 test

즉,
label=0 안에서도 80/20
label=1 안에서도 80/20
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
),
ranked AS (
    SELECT
        customer_id,
        feature_1,
        feature_2,
        feature_3,
        label,
        random_score,

        ROW_NUMBER() OVER (
            PARTITION BY label
            ORDER BY random_score
        ) AS label_row_num,

        COUNT(*) OVER (
            PARTITION BY label
        ) AS label_total_count
    FROM randomized
)
SELECT
    customer_id,
    feature_1,
    feature_2,
    feature_3,
    label,
    random_score,
    label_row_num,
    label_total_count,

    CASE
        WHEN label_row_num <= label_total_count * 0.8 THEN 'train'
        ELSE 'test'
    END AS dataset_type

FROM ranked
ORDER BY
    label,
    label_row_num;


/* ============================================================
4️⃣ Create Stratified Split Table
============================================================ */

/*
실무에서는 stratified split 결과를 별도 테이블로 저장하는 경우가 많다.
*/

CREATE TABLE IF NOT EXISTS customer_ml_stratified_split AS
WITH randomized AS (
    SELECT
        customer_id,
        feature_1,
        feature_2,
        feature_3,
        label,
        RANDOM() AS random_score
    FROM customer_ml_dataset
),
ranked AS (
    SELECT
        customer_id,
        feature_1,
        feature_2,
        feature_3,
        label,
        random_score,

        ROW_NUMBER() OVER (
            PARTITION BY label
            ORDER BY random_score
        ) AS label_row_num,

        COUNT(*) OVER (
            PARTITION BY label
        ) AS label_total_count
    FROM randomized
)
SELECT
    customer_id,
    feature_1,
    feature_2,
    feature_3,
    label,
    random_score,
    label_row_num,
    label_total_count,

    CASE
        WHEN label_row_num <= label_total_count * 0.8 THEN 'train'
        ELSE 'test'
    END AS dataset_type

FROM ranked;


/* ============================================================
5️⃣ Train/Test Ratio Check
============================================================ */

/*
전체 train/test 비율 확인
*/

SELECT
    dataset_type,
    COUNT(*) AS row_count,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS ratio
FROM customer_ml_stratified_split
GROUP BY dataset_type;


/* ============================================================
6️⃣ Label Distribution Check
============================================================ */

/*
stratified split의 핵심 검증
- train/test 각각에서 label 분포가 비슷한지 확인
*/

SELECT
    dataset_type,
    label,
    COUNT(*) AS row_count,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (PARTITION BY dataset_type) AS within_dataset_ratio
FROM customer_ml_stratified_split
GROUP BY
    dataset_type,
    label
ORDER BY
    dataset_type,
    label;


/* ============================================================
7️⃣ Compare With Overall Label Distribution
============================================================ */

/*
전체 원본 데이터의 label 분포와 비교
*/

SELECT
    label,
    COUNT(*) AS row_count,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS overall_ratio
FROM customer_ml_dataset
GROUP BY label
ORDER BY label;


/* ============================================================
8️⃣ Separate Views
============================================================ */

/*
train/test를 뷰로 분리
*/

CREATE OR REPLACE VIEW customer_ml_train AS
SELECT *
FROM customer_ml_stratified_split
WHERE dataset_type = 'train';


CREATE OR REPLACE VIEW customer_ml_test AS
SELECT *
FROM customer_ml_stratified_split
WHERE dataset_type = 'test';


/* ============================================================
9️⃣ Practical Notes
============================================================ */

/*
실무 포인트

1) stratified split은 classification에서 매우 자주 사용
2) 특히 positive class 비율이 낮을 때 중요
3) random split보다 label 분포 안정성이 높음
4) 다만 time series 데이터에는 적절하지 않을 수 있음
5) 고객 단위 leakage나 그룹 단위 leakage가 있으면
   group-based split이 더 적절할 수 있다.
*/


/* ============================================================
🔟 Reproducibility Note
============================================================ */

/*
RANDOM() 기반 방식은 실행마다 결과가 달라질 수 있다.

완전한 재현성이 필요하면:
- hash(customer_id) 기반 split
- seed 지원 함수
- split 결과 테이블 저장
등의 방법을 고려한다.

실무에서는 보통
"한 번 생성한 split 테이블을 저장"
하는 방식이 많이 쓰인다.
*/


/* ============================================================
1️⃣1️⃣ Summary
============================================================ */

/*
정리

1) stratified split은 label 비율을 유지하는 train/test 분할 방식이다.
2) label 그룹별로 따로 분할하기 때문에
   train/test 클래스 분포가 더 안정적이다.
3) 불균형 classification 문제에서 특히 중요하다.
4) split 후에는 반드시 train/test label 분포를 검증해야 한다.

즉,
stratified split은
"random split의 실무형 개선 버전"이라고 볼 수 있다.
*/