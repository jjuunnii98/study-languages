/*
Day 17: SQL Recursive CTE — WITH RECURSIVE

Recursive CTE는 "자기 자신을 참조"하여 계층/트리/그래프 구조를 펼치거나,
시퀀스/기간 생성 같은 반복 구조를 SQL 안에서 처리할 수 있게 해준다.

대표 활용:
- 조직도(상사-부하), 카테고리 트리(부모-자식)
- BOM(부품 구조) 전개
- 숫자/날짜 시퀀스 생성 (캘린더 테이블 대체)
- 그래프 경로 탐색(간단한 형태)

핵심 문법 (PostgreSQL 기준):
WITH RECURSIVE cte_name AS (
  -- Anchor member (시작점)
  SELECT ...

  UNION ALL

  -- Recursive member (반복)
  SELECT ...
  FROM cte_name
  JOIN ...
)
SELECT * FROM cte_name;

주의:
- 무한 루프 가능 → 종료 조건이 반드시 필요
- 사이클(순환 참조) 발생 가능 → path 누적/visited 체크 등 방지 로직 필요
*/


/* ------------------------------------------------------------
[Example 1] 조직도/계층 구조 펼치기 (Adjacency List)
테이블 가정: employees
- employee_id (PK)
- name
- manager_id (상사 employee_id, 최상위는 NULL)

목표:
- 특정 매니저(예: 100) 아래의 모든 부하 직원을 depth(깊이)와 함께 조회
------------------------------------------------------------ */

-- Anchor: 시작 매니저(루트) 설정
-- Recursive: manager_id를 따라 내려가며 트리 전개
WITH RECURSIVE org AS (
  SELECT
    e.employee_id,
    e.name,
    e.manager_id,
    0 AS depth
  FROM employees e
  WHERE e.employee_id = 100

  UNION ALL

  SELECT
    child.employee_id,
    child.name,
    child.manager_id,
    org.depth + 1 AS depth
  FROM employees child
  JOIN org
    ON child.manager_id = org.employee_id
)
SELECT
  employee_id,
  name,
  manager_id,
  depth
FROM org
ORDER BY depth, employee_id;


/* ------------------------------------------------------------
[Example 2] path(경로) 누적 + 사이클 방지(기본 아이디어)
- 순환 참조가 가능한 데이터(잘못된 입력 등)가 있다면,
  단순 재귀는 무한 루프가 날 수 있다.
- 이를 방지하려면 "지나온 노드 목록(path)"를 누적하고,
  다음 노드가 이미 path에 있으면 확장하지 않는다.

PostgreSQL에서는 배열/문자열로 path를 관리하는 패턴이 흔하다.
------------------------------------------------------------ */

WITH RECURSIVE org_path AS (
  SELECT
    e.employee_id,
    e.name,
    e.manager_id,
    0 AS depth,
    CAST(e.employee_id AS TEXT) AS path  -- 시작 경로
  FROM employees e
  WHERE e.employee_id = 100

  UNION ALL

  SELECT
    child.employee_id,
    child.name,
    child.manager_id,
    op.depth + 1 AS depth,
    op.path || ' -> ' || CAST(child.employee_id AS TEXT) AS path
  FROM employees child
  JOIN org_path op
    ON child.manager_id = op.employee_id
  -- 사이클 방지: path 문자열에 이미 child id가 포함되면 제외
  -- (정교하게 하려면 delimiter 처리/배열 사용 권장)
  WHERE op.path NOT LIKE '%' || CAST(child.employee_id AS TEXT) || '%'
)
SELECT
  employee_id,
  name,
  manager_id,
  depth,
  path
FROM org_path
ORDER BY depth, employee_id;


/* ------------------------------------------------------------
[Example 3] 숫자 시퀀스 생성 (1..N)
- 캘린더 테이블, 배치 처리, 샘플 데이터 생성 등에 유용
------------------------------------------------------------ */

WITH RECURSIVE seq AS (
  SELECT 1 AS n
  UNION ALL
  SELECT n + 1
  FROM seq
  WHERE n < 10   -- 종료 조건 (N=10)
)
SELECT n
FROM seq;


/* ------------------------------------------------------------
[Example 4] 날짜 시퀀스 생성 (기간 생성)
- start_date ~ end_date 날짜를 하루 단위로 생성
- 분석에서 "날짜 테이블"이 없을 때 매우 유용한 패턴
------------------------------------------------------------ */

WITH RECURSIVE calendar AS (
  SELECT DATE '2026-01-01' AS dt
  UNION ALL
  SELECT dt + INTERVAL '1 day'
  FROM calendar
  WHERE dt < DATE '2026-01-10'
)
SELECT
  dt::date AS dt
FROM calendar;


/* ------------------------------------------------------------
[Example 5] 계층 구조에 대한 집계/표현 (응용 아이디어)
- depth별 인원 수, 특정 depth 이하만 보기 등
------------------------------------------------------------ */

WITH RECURSIVE org AS (
  SELECT
    e.employee_id,
    e.name,
    e.manager_id,
    0 AS depth
  FROM employees e
  WHERE e.employee_id = 100

  UNION ALL

  SELECT
    child.employee_id,
    child.name,
    child.manager_id,
    org.depth + 1 AS depth
  FROM employees child
  JOIN org
    ON child.manager_id = org.employee_id
)
SELECT
  depth,
  COUNT(*) AS cnt
FROM org
GROUP BY depth
ORDER BY depth;


/*
요약
- Recursive CTE는 계층/트리/그래프/시퀀스 문제를 SQL로 해결한다.
- Anchor(시작점) + Recursive(반복) + 종료 조건(필수) 구조를 반드시 이해하자.
- 실무에서는 사이클 방지(path/visited)와 성능(인덱스, 종료 조건)이 중요하다.
*/