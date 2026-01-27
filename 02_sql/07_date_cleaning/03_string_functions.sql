/*
Day 20: SQL String Functions for Data Cleaning

This file covers essential SQL string functions used in data cleaning
and preprocessing tasks.

Focus:
- Standardizing text
- Cleaning noisy string fields
- Extracting meaningful substrings
- Handling inconsistent formatting

실무 데이터에서 문자열 정리는
JOIN, GROUP BY, 분석 품질을 좌우하는 핵심 단계다.
*/


-- ------------------------------------------------------------
-- 1) LOWER / UPPER / INITCAP (대소문자 표준화)
-- ------------------------------------------------------------
-- 문자열 비교나 그룹화 전에 반드시 표준화가 필요하다.

SELECT
    'Seoul'              AS original,
    LOWER('Seoul')       AS lower_text,
    UPPER('Seoul')       AS upper_text;

-- INITCAP은 DB에 따라 지원 여부가 다름 (PostgreSQL, Oracle 등)
-- 첫 글자만 대문자로 변환
-- SELECT INITCAP('machine learning');


-- ------------------------------------------------------------
-- 2) TRIM / LTRIM / RTRIM (공백 제거)
-- ------------------------------------------------------------
-- 데이터 입력 과정에서 불필요한 공백은 매우 흔함

SELECT
    '  data science  '           AS original,
    TRIM('  data science  ')     AS trimmed,
    LTRIM('  data science  ')    AS left_trimmed,
    RTRIM('  data science  ')    AS right_trimmed;


-- ------------------------------------------------------------
-- 3) LENGTH / CHAR_LENGTH (문자 길이 확인)
-- ------------------------------------------------------------
-- 결측치 판별, 이상값 탐지에 활용

SELECT
    'SQL'                AS text,
    LENGTH('SQL')        AS length_bytes,
    CHAR_LENGTH('SQL')   AS length_chars;


-- ------------------------------------------------------------
-- 4) SUBSTRING / LEFT / RIGHT (부분 문자열 추출)
-- ------------------------------------------------------------
-- 코드, 날짜, 카테고리 분리 시 자주 사용

SELECT
    '2026-01-15'                     AS date_text,
    SUBSTRING('2026-01-15' FROM 1 FOR 4) AS year_part,
    SUBSTRING('2026-01-15' FROM 6 FOR 2) AS month_part,
    RIGHT('2026-01-15', 2)           AS day_part;


-- ------------------------------------------------------------
-- 5) REPLACE (문자열 치환)
-- ------------------------------------------------------------
-- 잘못된 구분자, 불필요한 기호 제거에 유용

SELECT
    'KR-SEOUL'                         AS original,
    REPLACE('KR-SEOUL', '-', '_')     AS replaced_text;


-- ------------------------------------------------------------
-- 6) CONCAT / CONCAT_WS (문자열 결합)
-- ------------------------------------------------------------
-- CONCAT_WS는 구분자를 자동 삽입 (실무에서 매우 유용)

SELECT
    CONCAT('Risk', 'AI')                      AS concat_basic,
    CONCAT_WS('_', 'Risk', 'AI', 'Model')    AS concat_with_separator;


-- ------------------------------------------------------------
-- 7) POSITION / STRPOS (문자 위치 탐색)
-- ------------------------------------------------------------
-- 특정 키워드 포함 여부 확인 가능

SELECT
    'junixion-risk-ai'            AS text,
    POSITION('-' IN 'junixion-risk-ai') AS dash_position;


-- ------------------------------------------------------------
-- 8) 문자열 기반 데이터 정제 예시 (실전 패턴)
-- ------------------------------------------------------------
-- 이메일 도메인 추출 예제

SELECT
    'user@junixion.ai'                                        AS email,
    SUBSTRING('user@junixion.ai' FROM POSITION('@' IN 'user@junixion.ai') + 1)
        AS domain;


-- ------------------------------------------------------------
-- 9) CASE + 문자열 함수 (정규화 패턴)
-- ------------------------------------------------------------
-- 문자열 상태를 기준으로 카테고리 분류

SELECT
    'Seoul' AS city,
    CASE
        WHEN LOWER('Seoul') IN ('seoul', 'busan', 'incheon')
            THEN 'KOREA'
        ELSE 'OTHER'
    END AS region_category;


-- ------------------------------------------------------------
-- Day 20 Summary
-- ------------------------------------------------------------
-- - 문자열은 반드시 표준화 후 분석해야 한다
-- - TRIM + LOWER 조합은 거의 필수 패턴
-- - SUBSTRING / POSITION은 코드·날짜 파싱에 매우 중요
-- - 문자열 정제는 분석 품질을 직접적으로 결정한다