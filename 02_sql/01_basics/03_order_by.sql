/*
Day 3: SQL ORDER BY Clause

이 파일에서는 결과를 정렬하는 ORDER BY 절을 다룬다.
ORDER BY는 분석 결과를 해석 가능하게 만드는 핵심 요소다.

핵심 내용:
- 오름차순(ASC), 내림차순(DESC)
- 여러 컬럼 기준 정렬
- 숫자, 문자열, 날짜 정렬
- WHERE와 함께 사용
*/

-- =========================================
-- 1. 기본 ORDER BY (오름차순)
-- =========================================
-- 기본값은 ASC (오름차순)

SELECT name, salary
FROM employees
ORDER BY salary;


-- =========================================
-- 2. 내림차순 정렬 (DESC)
-- =========================================

SELECT name, salary
FROM employees
ORDER BY salary DESC;


-- =========================================
-- 3. 문자열 정렬
-- =========================================
-- 알파벳 순서로 정렬

SELECT name, department
FROM employees
ORDER BY name ASC;


-- =========================================
-- 4. 여러 컬럼 기준 정렬
-- =========================================
-- 첫 번째 기준 → 두 번째 기준

SELECT department, salary, name
FROM employees
ORDER BY department ASC, salary DESC;


-- =========================================
-- 5. WHERE + ORDER BY
-- =========================================
-- 조건 필터링 후 정렬

SELECT name, salary
FROM employees
WHERE department = 'IT'
ORDER BY salary DESC;


-- =========================================
-- 6. 날짜 정렬
-- =========================================
-- 최신 데이터 우선 조회

SELECT name, hire_date
FROM employees
ORDER BY hire_date DESC;


-- =========================================
-- 7. 컬럼 위치 기반 정렬 (비추천)
-- =========================================
-- SELECT 절의 컬럼 순서를 기준으로 정렬
-- 가독성이 떨어지므로 실무에서는 권장하지 않음

SELECT name, salary, department
FROM employees
ORDER BY 2 DESC;


-- =========================================
-- 8. 실전 예제
-- =========================================
-- IT 부서 직원 중
-- 연봉 높은 순 → 이름 오름차순

SELECT name, salary
FROM employees
WHERE department = 'IT'
ORDER BY salary DESC, name ASC;


/*
Day 3 요약
- ORDER BY는 결과의 해석을 좌우한다
- ASC(기본), DESC 명확히 구분
- 여러 컬럼으로 우선순위 정렬 가능
- WHERE 이후 ORDER BY 실행
*/