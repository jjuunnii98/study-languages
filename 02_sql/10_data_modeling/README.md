# 🏗 SQL Data Modeling — 10_data_modeling

This directory implements **production-oriented relational data modeling**
for analytics and data warehousing systems.

It goes beyond table creation and focuses on:

- Structural integrity
- Analytical scalability
- Query predictability
- Referential stability
- Performance-aware schema design

본 디렉토리는 분석 및 데이터웨어하우스 환경에서 필요한  
**실무형 SQL 데이터 모델링 아키텍처**를 단계적으로 구현합니다.

단순 테이블 생성이 아니라,

- 무결성 보장
- 분석 친화적 구조 설계
- 성능 최적화 고려
- 재현 가능한 DDL 설계
- 실행 계획 기반 검증

까지 포함합니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Design Fact and Dimension tables properly
- Implement Star and Snowflake schemas
- Apply surrogate key strategies
- Enforce referential integrity using PK/FK
- Design composite and normalized dimensions
- Apply index strategies based on workload patterns
- Validate modeling decisions using analytical queries

본 모듈 완료 후 다음을 수행할 수 있습니다:

- Fact/Dimension 구조를 정확히 설계
- Star / Snowflake 스키마 구현
- 대리키 기반 안정적 모델링
- PK/FK로 참조 무결성 보장
- 정규화된 차원 설계
- 쿼리 기반 인덱스 전략 적용
- 분석 쿼리로 모델 검증

---

# 📂 Module Structure

---

## 01️⃣ Fact & Dimension Modeling  
`01_fact_dimension`

**Focus: Dimensional Modeling Fundamentals**

- Fact table design (measures, additive logic)
- Dimension table design (attributes, hierarchy)
- Surrogate key introduction
- Foreign key enforcement
- Basic indexing for joins

👉 목표: Star Schema의 기초 구조 확립

---

## 02️⃣ Star Schema  
`02_star_schema`

**Focus: Analytical Warehouse Structure**

- Central fact table
- Denormalized dimensions
- Optimized for read-heavy workloads
- Simple join patterns
- Aggregation-friendly design
- Analytical query examples

👉 목표: OLAP 중심 분석 구조 완성

---

## 03️⃣ Snowflake Schema  
`03_snowflake_schema`

**Focus: Normalized Dimension Architecture**

- Dimension normalization (3NF-style)
- Sub-dimension decomposition
- Reduced redundancy
- Stronger governance
- Surrogate key mapping
- ETL-ready dimension loading patterns

👉 목표: 정규화 기반 고급 모델링 구조 이해

---

## 04️⃣ Keys & Indexes  
`04_keys_indexes`

**Focus: Integrity & Performance Layer**

- Primary Key (Entity Integrity)
- Foreign Key (Referential Integrity)
- ON DELETE / ON UPDATE 전략
- Composite index design
- Workload-based index strategy
- Execution plan validation (`EXPLAIN`)
- Query-driven optimization

👉 목표: 무결성과 성능을 동시에 확보하는 설계 능력

---

# 🧠 Architectural Progression

```text
Fact/Dimension Fundamentals
        ↓
Star Schema (Denormalized Dimensions)
        ↓
Snowflake Schema (Normalized Dimensions)
        ↓
Keys & Indexes (Integrity + Performance)
        ↓
Execution Plan Validation
        ↓
Production-Grade Analytical Modeling
```

---

## ⚙️ Modeling Principles Demonstrated

1️⃣ Entity Integrity
	•	Every entity has a stable primary key

2️⃣ Referential Integrity
	•	Foreign keys enforce relationship correctness

3️⃣ Analytical Design
	•	Fact = measurable events
	•	Dimension = analytical context

4️⃣ Performance Awareness
	•	Indexes based on real query workload
	•	Composite index ordering rules
	•	Execution plan inspection

5️⃣ Reproducibility
	•	Idempotent DDL (DROP IF EXISTS)
	•	Structured test queries
	•	Deterministic modeling decisions

---

## 🚀 Current Status

Data Modeling Core Completed

This module now demonstrates:
	•	Full Star Schema design
	•	Snowflake Schema normalization
	•	Referential integrity enforcement
	•	Workload-based index design
	•	Analytical query validation

---

## 🔜 Future Expansion (Optional)
	•	Slowly Changing Dimensions (SCD)
	•	Partitioning strategy
	•	Materialized views
	•	Bridge tables (many-to-many modeling)
	•	Performance benchmarking experiments
	•	Locking & transaction isolation basics

---

# 🏁 Summary

This directory represents a transition from:

“Writing SQL tables”

to

“Designing production-grade analytical systems.”

It demonstrates architectural thinking,
integrity discipline,
and performance-aware modeling strategy. 