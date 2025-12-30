/*
Day 5: SQL INNER JOIN

이 파일에서는 여러 테이블을 결합하는 JOIN의 가장 기본인
INNER JOIN을 다룬다.

INNER JOIN은 두 테이블에서
'조인 조건을 만족하는 행만' 결과로 반환한다.

핵심 포인트:
- JOIN 기본 구조
- ON 절을 통한 조인 조건
- 컬럼 충돌 방지(alias)
- WHERE vs JOIN 조건 차이
- 실전 분석 예제
*/

-- =========================================
-- 1. INNER JOIN 기본 구조
-- =========================================
-- 직원 테이블과 부서 테이블을 결합

SELECT *
FROM employees e
INNER JOIN departments d
    ON e.department_id = d.department_id;


-- =========================================
-- 2. 필요한 컬럼만 선택하기
-- =========================================
-- 실무에서는 SELECT * 지양

SELECT
    e.employee_id,
    e.name,
    d.department_name
FROM employees e
INNER JOIN departments d
    ON e.department_id = d.department_id;


-- =========================================
-- 3. 테이블 별칭(alias) 사용
-- =========================================
-- 가독성과 쿼리 길이 단축에 매우 중요

SELECT
    e.name AS employee_name,
    d.department_name
FROM employees AS e
INNER JOIN departments AS d
    ON e.department_id = d.department_id;


-- =========================================
-- 4. WHERE 절과 함께 사용
-- =========================================
-- JOIN으로 테이블 결합 후 조건 필터링

SELECT
    e.name,
    d.department_name,
    e.salary
FROM employees e
INNER JOIN departments d
    ON e.department_id = d.department_id
WHERE e.salary >= 50000;


-- =========================================
-- 5. JOIN 조건 vs WHERE 조건 (중요)
-- =========================================
-- JOIN 조건: 테이블을 어떻게 연결할 것인가
-- WHERE 조건: 결과에서 무엇을 필터링할 것인가

SELECT
    e.name,
    d.department_name
FROM employees e
INNER JOIN departments d
    ON e.department_id = d.department_id   -- 조인 조건
WHERE d.department_name = 'IT';            -- 필터 조건


-- =========================================
-- 6. 세 테이블 INNER JOIN
-- =========================================
-- employees + departments + locations

SELECT
    e.name,
    d.department_name,
    l.city
FROM employees e
INNER JOIN departments d
    ON e.department_id = d.department_id
INNER JOIN locations l
    ON d.location_id = l.location_id;


-- =========================================
-- 7. 실전 분석 예제
-- =========================================
-- IT 부서 직원 중 연봉 상위 5명

SELECT
    e.name,
    e.salary,
    d.department_name
FROM employees e
INNER JOIN departments d
    ON e.department_id = d.department_id
WHERE d.department_name = 'IT'
ORDER BY e.salary DESC
LIMIT 5;


/*
Day 5 요약
- INNER JOIN은 조인 조건을 만족하는 행만 반환한다
- 테이블 별칭(alias)은 JOIN에서 필수다
- JOIN 조건과 WHERE 조건의 역할을 명확히 구분해야 한다
- 다중 INNER JOIN으로 여러 테이블을 결합할 수 있다
- 분석 쿼리의 대부분은 JOIN + WHERE + ORDER BY + LIMIT 조합이다
*/