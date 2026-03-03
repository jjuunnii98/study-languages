# 🔑 Keys & Indexes (SQL) — 04_keys_indexes

This module covers **production-grade key design and index strategy**
for relational modeling and analytical workloads.

Keys are not just constraints.
They define:

- data integrity
- relationship correctness
- join stability
- aggregation reliability
- query performance

본 디렉토리는 분석 및 데이터 모델링 환경에서 필수적인  
**Primary Key / Foreign Key 설계와 인덱스 전략**을 실무 수준으로 정리합니다.

단순 문법 학습이 아니라,

- 무결성(Integrity)
- 관계 안정성(Relational Stability)
- 워크로드 기반 인덱스 설계
- 실행 계획 기반 성능 검증

까지 포함합니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain why Primary Keys are mandatory
- Enforce referential integrity using Foreign Keys
- Choose correct `ON DELETE / ON UPDATE` strategies
- Prevent orphan rows and silent join bugs
- Design indexes based on query patterns
- Apply composite index ordering rules
- Validate execution plans using `EXPLAIN`

본 모듈 완료 후 다음을 수행할 수 있습니다:

- PK가 모델 안정성의 기준점임을 설명
- FK로 참조 무결성 구현
- 삭제/수정 정책 전략적으로 선택
- 고아 레코드 및 조인 왜곡 사전 차단
- 쿼리 패턴 기반 인덱스 설계
- 복합 인덱스 컬럼 순서 원리 이해
- 실행 계획 기반 성능 검증

---

# 📂 Files & Progress

---

## ✅ Day 44 — Primary & Foreign Keys  
`01_primary_foreign_keys.sql`

### What It Implements

- Parent table (`customers`) with `PRIMARY KEY`
- Child table (`orders`) with `FOREIGN KEY`
- Referential integrity enforcement:
  - `ON DELETE RESTRICT`
  - `ON UPDATE CASCADE`
- Foreign key index creation
- Integrity violation test cases
- Join validation query (aggregation example)

---

### 🧠 Day 44 핵심 개념

#### 1️⃣ Primary Key = Entity Integrity

PK는:

- 고유성 보장
- NULL 불가
- 엔티티 식별 기준

PK가 없으면:

- 중복 발생
- 조인 결과 왜곡
- 집계 신뢰도 하락

---

#### 2️⃣ Foreign Key = Referential Integrity

FK는:

- 존재하는 PK만 참조 허용
- 고아 레코드 방지
- 관계 안정성 보장

FK가 없으면:

- 잘못된 ID 삽입 가능
- 조인 시 NULL 누락 발생
- 장기적으로 데이터 품질 붕괴

---

#### 3️⃣ ON DELETE 전략 비교

| Strategy | 설명 | 권장 상황 |
|----------|------|------------|
| RESTRICT | 자식 존재 시 삭제 금지 | 기본 안전값 |
| CASCADE  | 자식 자동 삭제 | 강한 종속 관계 |
| SET NULL | 참조 제거 | 약한 관계 |

Analytics 환경에서는 보통 `RESTRICT`가 안전합니다.

---

## ✅ Day 45 — Index Design Strategy  
`02_index_design.sql`

### What It Implements

- FK join index
- WHERE filtering index
- Date range index
- Composite index `(customer_id, order_date)`
- GROUP BY scenario discussion
- Selectivity analysis
- Execution plan validation (`EXPLAIN`)

---

## 🧠 Day 45 핵심 개념

### 1️⃣ 인덱스는 읽기 최적화 장치

- SELECT 성능 향상
- 쓰기 성능 저하
- 무분별한 생성 금지

---

### 2️⃣ 워크로드 기반 설계

인덱스는 쿼리에서 시작한다:

- WHERE
- JOIN
- ORDER BY
- GROUP BY

---

### 3️⃣ 복합 인덱스 설계 원칙

예:

```sql
WHERE customer_id = ?
  AND order_date BETWEEN ...
```  

권장 인덱스:

```
(customer_id, order_date)
```

규칙:
	•	동등조건(=) 컬럼을 앞에
	•	범위조건(BETWEEN, >, <) 컬럼을 뒤에

### 4️⃣ 선택도(Selectivity) 고려
	•	값 종류가 적으면 인덱스 효과 제한적
	•	데이터 분포가 편향되면 효과 증가
	•	항상 EXPLAIN 기반 검증 필요

---

### 5️⃣ 인덱스 설계 체크리스트
	1.	자주 실행되는 쿼리 분석
	2.	WHERE/JOIN 컬럼 우선 적용
	3.	복합 인덱스 순서 결정
	4.	ORDER BY 일관성 고려
	5.	EXPLAIN 실행 계획 확인
	6.	쓰기 부하 고려

---

### 🧠 Integrated Architecture

```
Primary Key (Entity Integrity)
        ↓
Foreign Key (Referential Integrity)
        ↓
Join Stability
        ↓
Index Optimization
        ↓
Execution Plan Validation
        ↓
Reliable Analytical Queries
```

무결성 없는 인덱스는 위험하고,
인덱스 없는 무결성은 느립니다.

두 요소는 함께 설계되어야 합니다.

---

## 🚀 Current Status

Day 44–45 Completed

This module demonstrates:
	•	Integrity-safe relational modeling
	•	Constraint-driven data validation
	•	Query-driven index design
	•	Composite index reasoning
	•	Execution-plan-based performance validation
	•	Production-aware SQL architecture mindset

---

## 🔜 Next Expansion
	•	UNIQUE / CHECK constraints
	•	Composite keys & bridge tables
	•	Covering index strategies
	•	Partial index patterns
	•	Index anti-patterns
	•	Locking & concurrency basics
