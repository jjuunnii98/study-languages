/*
Day 2: SQL WHERE Clause

이 파일에서는 SQL의 핵심 조건절인 WHERE를 다룬다. 
WHERE는 데이터 분석과 퀴리 최적화의 출발점이다. 

핵심 내용: 
- 기본 조건 비교(=, !=, >, <, >=, <=) 
- AND / OR / NOT
- BETWEEN 
- IN
- LIKE
- NULL 처리 (IS NULL / IS NOT NULL) 
*/ 

-- =========================================
-- 1. 기본 WHERE 조건
-- =========================================
-- 특정 조건에 맞는 행(row)만 선택

SELECT * 
FROM employees
WHERE department = 'Sales'; 

-- =========================================
-- 2. 비교 연산자 사용
-- =========================================

SELECT name, salary
FROM employees
WHERE salary >= 50000; 

-- =========================================
-- 3. AND / OR / NOT
-- =========================================
-- 여러 조건을 결합할 때 사용

SELECT * 
FROM employees
WHERE department = 'HR' 
    OR department = 'Finance';

SELECT * 
FROM employees
WHERE NOT department = 'Sales';


-- =========================================
-- 4. BETWEEN
-- =========================================
-- 특정 범위의 값 선택 (이상, 이하 포함)

SELECT name, salary
FROM employees
WHERE salary BETWEEN 40000 AND 70000;


-- =========================================
-- 5. IN
-- =========================================
-- 여러 값 중 하나라도 해당하는 경우


SELECT *
FROM employees
WHERE department IN ('IT', 'Finance', 'HR');


-- =========================================
-- 6. LIKE (문자열 패턴 검색)
-- =========================================
-- % : 임의의 문자열
-- _ : 임의의 한 글자

SELECT *
FROM employees
WHERE name LIKE 'J%';     -- J로 시작

SELECT *
FROM employees
WHERE email LIKE '%@gmail.com';  -- gmail 계정

SELECT *
FROM employees
WHERE name LIKE '_im';   -- 세 글자 이름, 가운데 im

-- =========================================
-- 7. NULL 처리
-- =========================================
-- NULL은 = 로 비교할 수 없다

SELECT *
FROM employees
WHERE manager_id IS NULL;

SELECT *
FROM employees
WHERE manager_id IS NOT NULL;


-- =========================================
-- 8. 실전 예제: 조건 조합
-- =========================================
-- IT 부서이면서 연봉이 50,000 이상이고
-- 이메일이 gmail 계정인 직원

SELECT name, department, salary, email
FROM employees
WHERE department = 'IT'
  AND salary >= 50000
  AND email LIKE '%@gmail.com';


/*
Day 2 요약
- WHERE는 행(row)을 필터링하는 핵심 절
- AND / OR / NOT으로 조건 조합
- BETWEEN, IN으로 가독성 향상
- NULL은 반드시 IS NULL / IS NOT NULL 사용
*/