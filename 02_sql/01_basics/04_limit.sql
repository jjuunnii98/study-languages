/*
Day 4: SQL LIMIT Clause

이 파일에서는 조회 결과의 개수를 제한하는 LIMIT 절을 다룬다.
LIMIT는 데이터 탐색(EDA)과 대용량 테이블 분석에서 필수적인 도구다.

핵심 내용:
- LIMIT 기본 사용법
- ORDER BY + LIMIT 조합
- OFFSET과 함께 사용
- 실전 분석 패턴 (Top-N, 샘플링)
*/

-- =========================================
-- 1. LIMIT 기본 사용법
-- =========================================
-- 결과 상위 N개만 조회

SELECT *
FROM employees
LIMIT 5;


-- =========================================
-- 2. ORDER BY + LIMIT (가장 중요)
-- =========================================
-- 연봉이 높은 상위 3명 조회

SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 3;


-- =========================================
-- 3. WHERE + ORDER BY + LIMIT
-- =========================================
-- IT 부서 직원 중 연봉 상위 2명

SELECT name, salary
FROM employees
WHERE department = 'IT'
ORDER BY salary DESC
LIMIT 2;


-- =========================================
-- 4. OFFSET과 함께 사용
-- =========================================
-- OFFSET은 앞의 N개를 건너뛴다
-- (페이지네이션, 배치 분석에서 사용)

-- 예: 연봉 순으로 정렬 후 4~6번째 데이터 조회
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 3 OFFSET 3;


-- =========================================
-- 5. LIMIT + OFFSET 축약 문법 (MySQL, PostgreSQL)
-- =========================================
-- LIMIT offset, count 형식
-- (DB 종류에 따라 지원 여부 다름)

SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 3, 3;


-- =========================================
-- 6. 실전 분석 패턴: Top-N 분석
-- =========================================
-- 부서별 최고 연봉자 예시 (단순 예제)

SELECT department, name, salary
FROM employees
ORDER BY salary DESC
LIMIT 10;


-- =========================================
-- 7. EDA에서 LIMIT 사용 예시
-- =========================================
-- 대용량 테이블에서 구조 파악용 샘플링

SELECT *
FROM transactions
LIMIT 20;


/*
Day 4 요약
- LIMIT는 결과 개수를 제한한다
- ORDER BY 없이 LIMIT만 쓰면 의미가 약해질 수 있다
- ORDER BY + LIMIT는 Top-N 분석의 핵심 패턴
- OFFSET은 페이지네이션과 배치 분석에서 자주 사용된다
- EDA 초기 단계에서 LIMIT는 필수 도구다
*/