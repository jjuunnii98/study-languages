# 🔑 Keys & Indexes (SQL) — 04_keys_indexes

This directory covers **production-grade key design and indexing fundamentals**
for analytics and data modeling.

Keys are not “just constraints.”
They define **data integrity**, **join correctness**, and **query performance**.

본 디렉토리는 분석/데이터모델링 관점에서 핵심이 되는  
**Key 설계(PK/FK) 및 인덱싱 기본 원리**를 실무 수준으로 정리합니다.

---

## 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain why primary keys are mandatory for stable modeling
- Enforce referential integrity using foreign keys
- Choose correct `ON DELETE / ON UPDATE` strategies
- Prevent orphan rows and silent join bugs
- Apply indexing to foreign key columns for join performance
- Validate integrity using negative test cases (expected failures)

본 모듈 완료 후 다음을 수행할 수 있습니다:

- PK가 왜 모델 안정성의 필수 조건인지 설명
- FK로 참조 무결성(Referential Integrity) 구현
- `ON DELETE / ON UPDATE` 전략을 상황에 맞게 선택
- 고아 레코드(Orphan Row) 및 조인 오류를 사전에 차단
- FK 인덱싱으로 조인 성능 최적화
- 무결성 위반 테스트(실패 케이스)로 설계 검증

---

## 📂 Files & Progress

### ✅ Day 44 — Primary & Foreign Keys  
`01_primary_foreign_keys.sql`

#### Core Coverage (English)

- Creates a **parent table** (`customers`) with a `PRIMARY KEY`
- Creates a **child table** (`orders`) with a `FOREIGN KEY`
- Enforces referential integrity using:
  - `ON DELETE RESTRICT` (prevent deleting parent rows referenced by children)
  - `ON UPDATE CASCADE` (propagate PK updates safely)
- Adds an index on the FK column (`orders.customer_id`) for join performance
- Includes integrity test queries:
  - FK violation insert (expected to fail)
  - Restrict delete test (expected to fail)
- Provides a join-based validation query for analytics (e.g., total_spent)

#### 핵심 요약 (한국어)

- **부모 테이블(customers)** 에 PK를 정의하여 엔티티 식별 안정성 확보
- **자식 테이블(orders)** 에 FK를 정의하여 참조 무결성 보장
- 실무형 삭제/수정 정책 예시:
  - `ON DELETE RESTRICT` → 자식 존재 시 부모 삭제 금지(기본 안전값)
  - `ON UPDATE CASCADE` → 부모 PK 변경 시 자식 FK 자동 반영
- FK 컬럼 인덱스 생성으로 조인/집계 성능 최적화
- “정상 케이스 + 실패 케이스” 테스트로 설계 검증까지 포함

---

## 🧠 Practical Notes (실무 포인트)

### 1) PK는 모델의 “기준점(Anchor)”
PK가 없거나 불안정하면:

- 중복 데이터 발생
- 조인 결과가 폭발(duplication)
- 집계값 왜곡
- 데이터 품질/검증 비용 증가

PK는 단순 제약조건이 아니라 **모델의 신뢰성 기반**입니다.

---

### 2) FK는 “조인 정확성”을 강제하는 장치
FK가 없으면:

- 존재하지 않는 ID로 데이터가 들어올 수 있음
- 조인에서 누락/NULL이 발생하고도 조용히 넘어감(“silent bug”)
- 데이터 파이프라인 품질이 장기적으로 붕괴

FK는 **분석 결과의 정확성을 보장**합니다.

---

### 3) ON DELETE 전략 선택 가이드

| Strategy | Meaning | When to use |
|---------|---------|-------------|
| `RESTRICT` | prevent delete if referenced | safest default (analytics/fact-like) |
| `CASCADE` | delete children automatically | strong dependency (true ownership) |
| `SET NULL` | nullify reference | optional relationships / soft links |

실무 기본값은 보통 `RESTRICT`가 안전합니다.  
(특히 Fact → Dimension 관계에서 “자동 삭제”는 리스크가 큼)

---

### 4) FK 컬럼 인덱스는 “거의 필수”
FK는 무결성만 보장하고, 성능을 보장하지는 않습니다.  
대부분의 DB에서 FK 인덱스는 자동 생성되지 않으므로:

- 자식 테이블의 FK 컬럼 인덱스 생성 권장
- 조인/집계 성능에 매우 큰 영향을 줌

---

## ✅ Status

**Day 44 Completed**

This module currently establishes a clean foundation for:

- integrity-safe modeling
- predictable joins
- scalable analytics queries

Next planned topics:

- `UNIQUE` / `CHECK` constraints (domain integrity)
- composite keys & bridge tables
- index strategy patterns (covering index, partial index, etc.)

---