# ❄️ Snowflake Schema Modeling (SQL) — 03_snowflake_schema

This module implements a **production-grade Snowflake Schema architecture**
for analytical and data warehousing systems.

Snowflake Schema is a **normalized extension of the Star Schema**.
It keeps the Fact table at the center while Dimensions are further
decomposed into sub-dimensions (normalized tables).

Instead of storing all descriptive attributes in a single wide dimension,
Snowflake separates reusable or redundant attributes into dedicated tables.

본 디렉토리는 Star Schema를 한 단계 확장한  
**Snowflake Schema(스노우플레이크 스키마)**를 SQL 기반으로 구현합니다.

핵심 개념:

- Fact 테이블은 이벤트/측정값(Measure)을 저장
- Dimension 테이블은 분석 축(Analytical Context)을 제공
- Snowflake는 Dimension을 **정규화(3NF 스타일)**하여
  중복을 줄이고 무결성을 강화합니다

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain the structural difference between **Star Schema** and **Snowflake Schema**
- Normalize dimensions into sub-dimensions
- Design surrogate key–based stable joins
- Enforce referential integrity via foreign keys
- Apply indexing strategies for deeper join paths
- Write idempotent DDL scripts
- Implement safe normalized-dimension loading patterns

본 모듈 완료 후 다음을 수행할 수 있습니다:

- Star vs Snowflake 구조 차이를 명확히 설명
- 차원 테이블을 서브 차원으로 정규화
- 대리키 기반 안정적 조인 설계
- FK 제약조건으로 무결성 확보
- JOIN depth 증가를 고려한 인덱스 설계
- 재현 가능한 DDL 작성
- 정규화된 차원 적재(ETL) 패턴 구현

---

# 🧠 Conceptual Architecture

## 🔷 Star Schema (Denormalized Dimensions)

```text
fact_sales
   |
dim_product (category_name, brand_name 포함)
```

## 🔷 Snowflake Schema (Normalized Dimensions)

```text
fact_sales
   |
dim_product
   | \
dim_category dim_brand
```

Snowflake는 차원 속성을 별도 테이블로 분리합니다.

---

# 🧊 Full Snowflake Conceptual Diagram

```text
                 dim_date
                    |
dim_product — fact_sales — dim_customer
     |                 |
dim_category        dim_age_band
     |
  dim_brand

dim_store
  |    \
dim_region dim_channel
```

---

# 📂 Files & Progress

## ✅ Day 42 — Snowflake Schema Design (DDL)

`01_snowflake_schema_design.sql`

### What It Implements

- Core Fact Table: `fact_sales`
- Core Dimensions:
  - `dim_date`
  - `dim_product`
  - `dim_store`
  - `dim_customer`
- Normalized Sub-Dimensions:
  - `dim_category`
  - `dim_brand`
  - `dim_region`
  - `dim_channel`
  - `dim_age_band`
- Surrogate key strategy
- Foreign key enforcement
- Fact FK indexing
- Dimension linkage indexing
- Idempotent DDL (`DROP IF EXISTS`)
- Example snowflake join query

### 핵심 의의

구조 설계 단계 — 정규화된 차원 모델 완성

---

## ✅ Day 43 — Normalized Dimension Loading

`02_normalized_dimensions.sql`

### What It Implements

- Sub-dimension loading first (deduplicated insert pattern)
- `NOT EXISTS` 기반 멱등적 INSERT
- Surrogate key lookup pattern
- Natural key → surrogate key mapping
- Age → age_band transformation example
- Validation queries for join path verification

### 핵심 의의

구조 설계 → 실제 적재 패턴까지 확장  
Snowflake Schema의 운영 가능성 구현

---

# 🔄 Star vs Snowflake — Practical Comparison

| Feature | Star Schema | Snowflake Schema |
|----------|--------------|------------------|
| Dimension structure | Denormalized | Normalized |
| Join depth | Shallow | Deeper |
| Query simplicity | High | Moderate |
| Redundancy | Higher | Lower |
| Governance | Moderate | Strong |
| Performance tuning need | Moderate | Higher |

---

# ⚙️ Performance Considerations

Snowflake introduces deeper join paths:

```text
fact_sales → dim_product → dim_category
```

To mitigate performance risks:

- Index all Fact foreign keys
- Index dimension linkage keys
- Use integer surrogate keys
- Avoid joining on wide text columns
- Keep Fact table narrow & tall

---

# 🏗️ Modeling Principles Demonstrated

1️⃣ Fact stores additive measures  
2️⃣ Dimensions provide analytical axes  
3️⃣ Sub-dimensions reduce redundancy  
4️⃣ Surrogate keys stabilize joins  
5️⃣ Idempotent DDL ensures reproducibility  
6️⃣ Load patterns support incremental ETL  

---

# 🚀 Current Status

Day 42–43 Completed

This module demonstrates:

- Complete Snowflake Schema DDL
- Normalized dimension modeling
- Surrogate key lookup design
- Production-aware indexing strategy
- Join validation patterns
- ETL-ready dimension management

---

# 📈 What This Module Proves

This directory demonstrates:

- Advanced dimensional modeling capability
- Understanding of normalization trade-offs
- Data warehouse architectural thinking
- Performance-aware SQL design
- ETL-ready schema governance
- Warehouse-grade data modeling discipline