/*
Day 47 — Slowly Changing Dimensions Type 2
파일: 05_slowly_changing_dimensions/02_scd_type2.sql

목표
- SCD Type 2 패턴 구현
- 변경 이력을 보존하는 차원 테이블 관리 방법 학습

SCD Type 2 핵심
- 변경 발생 시 기존 row를 수정하지 않는다
- 기존 row를 expire 처리
- 새로운 row를 insert
- 과거 이력(history)을 유지

즉:

변경 발생
↓
기존 row end_date 설정
↓
새로운 row insert
↓
history 유지

대표 사용 사례
- 고객 주소 변경
- 고객 등급 변경
- 상품 카테고리 변경
- 조직 구조 변경
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
SCD Type 2에서는 다음 컬럼이 필수이다.

start_date : row가 시작된 시점
end_date   : row 종료 시점
is_current : 현재 활성 row 여부

business key:
customer_id

surrogate key:
customer_key
*/

CREATE TABLE dim_customer (

    customer_key   INTEGER PRIMARY KEY,
    customer_id    VARCHAR(20) NOT NULL,

    customer_name  VARCHAR(100),
    city           VARCHAR(100),

    start_date     DATE NOT NULL,
    end_date       DATE,
    is_current     BOOLEAN NOT NULL

);

------------------------------------------------------------
-- 2️⃣ 초기 데이터 적재
------------------------------------------------------------

INSERT INTO dim_customer
(customer_key, customer_id, customer_name, city, start_date, end_date, is_current)
VALUES
(1,'C001','Alice Kim','Seoul','2024-01-01',NULL,TRUE),
(2,'C002','Bob Lee','Busan','2024-01-01',NULL,TRUE),
(3,'C003','Cara Park','Daegu','2024-01-01',NULL,TRUE);

------------------------------------------------------------
-- 3️⃣ Staging Table 생성
------------------------------------------------------------

CREATE TABLE stg_customer (

    customer_id   VARCHAR(20),
    customer_name VARCHAR(100),
    city          VARCHAR(100)

);

------------------------------------------------------------
-- 4️⃣ 변경 데이터 입력 (예시)
------------------------------------------------------------

/*
시나리오

C001
Seoul → Incheon (변경)

C002
변경 없음

C004
신규 고객
*/

INSERT INTO stg_customer
VALUES
('C001','Alice Kim','Incheon'),
('C002','Bob Lee','Busan'),
('C004','David Choi','Seoul');

------------------------------------------------------------
-- 5️⃣ 변경 감지 (Change Detection)
------------------------------------------------------------

/*
현재 활성 row와 staging 데이터를 비교

조건
city 또는 name 변경
*/

SELECT
d.customer_id,
d.customer_name AS old_name,
s.customer_name AS new_name,
d.city AS old_city,
s.city AS new_city
FROM dim_customer d
JOIN stg_customer s
ON d.customer_id = s.customer_id
WHERE d.is_current = TRUE
AND (
d.customer_name <> s.customer_name
OR
d.city <> s.city
);

------------------------------------------------------------
-- 6️⃣ 기존 row expire 처리
------------------------------------------------------------

/*
변경 발생한 경우
현재 row 종료 처리

end_date 설정
is_current FALSE
*/

UPDATE dim_customer
SET
end_date = CURRENT_DATE,
is_current = FALSE
WHERE customer_id IN (

SELECT s.customer_id
FROM stg_customer s
JOIN dim_customer d
ON s.customer_id = d.customer_id

WHERE d.is_current = TRUE
AND (
s.customer_name <> d.customer_name
OR
s.city <> d.city
)

);

------------------------------------------------------------
-- 7️⃣ 새로운 row insert
------------------------------------------------------------

/*
변경된 고객 또는 신규 고객을 insert

새로운 history row 생성
*/

INSERT INTO dim_customer
(
customer_key,
customer_id,
customer_name,
city,
start_date,
end_date,
is_current
)

SELECT
(SELECT COALESCE(MAX(customer_key),0) FROM dim_customer)
+ ROW_NUMBER() OVER(ORDER BY s.customer_id),

s.customer_id,
s.customer_name,
s.city,
CURRENT_DATE,
NULL,
TRUE

FROM stg_customer s
LEFT JOIN dim_customer d
ON s.customer_id = d.customer_id
AND d.is_current = TRUE

WHERE

d.customer_id IS NULL

OR

(
s.customer_name <> d.customer_name
OR
s.city <> d.city
);

------------------------------------------------------------
-- 8️⃣ 결과 확인
------------------------------------------------------------

SELECT
customer_key,
customer_id,
customer_name,
city,
start_date,
end_date,
is_current
FROM dim_customer
ORDER BY customer_id, start_date;

------------------------------------------------------------
-- 9️⃣ SCD Type 2 요약
------------------------------------------------------------

/*
장점
- 과거 이력 보존
- 시점 분석 가능 (point-in-time analysis)
- 데이터 변경 추적 가능

단점
- 저장 공간 증가
- 쿼리 복잡도 증가
- ETL 로직 복잡

Type 1 vs Type 2

Type 1
overwrite
history 없음

Type 2
insert new row
history 유지

데이터웨어하우스에서
가장 많이 사용하는 패턴이
SCD Type 2이다.
*/