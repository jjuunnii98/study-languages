/*
Day 46 — Slowly Changing Dimensions Type 1
파일: 05_slowly_changing_dimensions/01_scd_type1.sql

목표
- SCD Type 1(이력 미보존, 최신값 덮어쓰기) 패턴 구현
- 차원 테이블(dim_customer)의 속성이 변경되면 기존 값을 overwrite
- 분석/리포팅에서 "현재 최신 상태"만 유지하는 설계 이해

SCD Type 1 핵심
- 과거 이력(history)을 저장하지 않음
- 변경 발생 시 기존 row를 UPDATE
- 단순하고 저장 비용이 낮음
- 하지만 "예전 값"은 복구 불가

적합한 예시
- 고객 이메일 오타 수정
- 이름 표기 정정
- 잘못 입력된 속성 수정
- 최신 상태만 중요하고 과거 이력이 필요 없는 경우

주의
- 아래 SQL은 범용적인 UPDATE + INSERT 패턴으로 작성
- DBMS마다 MERGE 문법이 다르므로, 학습용/이식성 관점에서
  staging 테이블 + update/insert 2단계 방식 사용
*/

------------------------------------------------------------
-- 0️⃣ 기존 테이블 제거 (재실행 가능)
------------------------------------------------------------

DROP TABLE IF EXISTS stg_customer;
DROP TABLE IF EXISTS dim_customer;

------------------------------------------------------------
-- 1️⃣ Dimension Table 생성
------------------------------------------------------------

/*
dim_customer:
- customer_key: surrogate key
- customer_id : business key (업무 식별자)
- customer_name, city, email: 속성 컬럼
- updated_at: 마지막 갱신 시각
*/
CREATE TABLE dim_customer (
    customer_key   INTEGER PRIMARY KEY,
    customer_id    VARCHAR(20) NOT NULL UNIQUE,
    customer_name  VARCHAR(100) NOT NULL,
    city           VARCHAR(100),
    email          VARCHAR(150),
    updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

------------------------------------------------------------
-- 2️⃣ 초기 데이터 적재
------------------------------------------------------------

INSERT INTO dim_customer (customer_key, customer_id, customer_name, city, email)
VALUES
    (1, 'C001', 'Alice Kim', 'Seoul', 'alice@example.com'),
    (2, 'C002', 'Bob Lee',   'Busan', 'bob@example.com'),
    (3, 'C003', 'Cara Park', 'Daegu', 'cara@example.com');

------------------------------------------------------------
-- 3️⃣ Staging Table 생성
------------------------------------------------------------

/*
stg_customer:
- 외부 소스/ETL에서 들어온 최신 데이터라고 가정
- 여기서 customer_id가 business key 역할
*/
CREATE TABLE stg_customer (
    customer_id    VARCHAR(20) NOT NULL,
    customer_name  VARCHAR(100) NOT NULL,
    city           VARCHAR(100),
    email          VARCHAR(150)
);

------------------------------------------------------------
-- 4️⃣ 변경 데이터 적재 (예시)
------------------------------------------------------------

/*
예시 시나리오
- C001: city, email 변경
- C002: name 변경
- C004: 신규 고객
*/
INSERT INTO stg_customer (customer_id, customer_name, city, email)
VALUES
    ('C001', 'Alice Kim',      'Incheon', 'alice_new@example.com'),
    ('C002', 'Bob Lee Jr.',    'Busan',   'bob@example.com'),
    ('C004', 'David Choi',     'Seoul',   'david@example.com');

------------------------------------------------------------
-- 5️⃣ SCD Type 1 UPDATE
------------------------------------------------------------

/*
기존 business key가 이미 존재하면
속성값을 staging 기준으로 덮어쓴다.

중요:
- 이력 테이블 없음
- 이전 city/email/name 값은 사라짐
- 최신 상태만 유지
*/
UPDATE dim_customer
SET
    customer_name = (
        SELECT s.customer_name
        FROM stg_customer s
        WHERE s.customer_id = dim_customer.customer_id
    ),
    city = (
        SELECT s.city
        FROM stg_customer s
        WHERE s.customer_id = dim_customer.customer_id
    ),
    email = (
        SELECT s.email
        FROM stg_customer s
        WHERE s.customer_id = dim_customer.customer_id
    ),
    updated_at = CURRENT_TIMESTAMP
WHERE customer_id IN (
    SELECT s.customer_id
    FROM stg_customer s
);

------------------------------------------------------------
-- 6️⃣ 신규 데이터 INSERT
------------------------------------------------------------

/*
staging에는 있지만 dim에는 없는 customer_id는 신규 row로 적재
surrogate key는 기존 max(customer_key)+row_number 방식으로 생성
실무에서는 sequence/identity 사용 권장
*/
INSERT INTO dim_customer (
    customer_key,
    customer_id,
    customer_name,
    city,
    email,
    updated_at
)
SELECT
    (SELECT COALESCE(MAX(customer_key), 0) FROM dim_customer)
    + ROW_NUMBER() OVER (ORDER BY s.customer_id) AS customer_key,
    s.customer_id,
    s.customer_name,
    s.city,
    s.email,
    CURRENT_TIMESTAMP
FROM stg_customer s
LEFT JOIN dim_customer d
    ON s.customer_id = d.customer_id
WHERE d.customer_id IS NULL;

------------------------------------------------------------
-- 7️⃣ 결과 확인
------------------------------------------------------------

/*
기대 결과
- C001: city/email 최신값으로 변경
- C002: customer_name 최신값으로 변경
- C003: 그대로 유지
- C004: 신규 insert
*/
SELECT
    customer_key,
    customer_id,
    customer_name,
    city,
    email,
    updated_at
FROM dim_customer
ORDER BY customer_key;

------------------------------------------------------------
-- 8️⃣ SCD Type 1 요약
------------------------------------------------------------

/*
장점
- 구현 단순
- 조회 성능 단순
- 저장 공간 절약

단점
- 과거 이력 손실
- "언제 무엇이 바뀌었는지" 분석 불가

즉,
SCD Type 1은 "현재 상태(current state)"만 중요할 때 사용한다.
*/