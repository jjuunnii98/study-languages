# ⭐ Star Schema Modeling (SQL) — 02_star_schema

This module implements a **production-grade Star Schema architecture**
for analytical and data warehousing workloads.

It demonstrates how transactional data should be modeled
to support:

- Scalable aggregation
- Predictable OLAP-style queries
- BI-friendly joins
- Performance-aware analytics systems

본 디렉토리는 분석 및 데이터웨어하우스 환경에서 가장 표준적인  
**Star Schema 모델링 구조**를 SQL 기반으로 체계적으로 설계합니다.

단순 테이블 생성이 아니라,

- 분석 친화적 구조 설계
- 무결성(Integrity) 보장
- 성능(Indexing) 고려
- 재현 가능한 DDL 설계
- 실제 분석 쿼리 검증

까지 포함합니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Clearly distinguish between **Fact** and **Dimension** tables
- Design a Star Schema optimized for read-heavy workloads
- Apply surrogate key strategies for stable joins
- Enforce referential integrity using foreign keys
- Implement indexing strategies for large-scale aggregation
- Write analytical queries leveraging dimensional modeling

본 모듈 완료 후 다음을 수행할 수 있습니다:

- Fact / Dimension 구조를 논리적으로 설명
- 분석 중심 Star Schema 설계
- 대리키 기반 안정적 조인 구조 구현
- FK 제약조건으로 무결성 확보
- 집계 성능을 고려한 인덱스 설계
- 차원 기반 분석 쿼리 작성

---

# 🧠 Conceptual Architecture

Star Schema separates responsibilities:

- **Fact Table** → Measurable events (수치 중심)
- **Dimension Tables** → Analytical context (속성 중심)

## 🔷 Conceptual Diagram

          dim_date
              |
dim_product — fact_sales — dim_customer
              |
          dim_store

이 구조는:

- 단순한 조인 패턴
- 빠른 GROUP BY 집계
- BI 도구 최적화
- 분석 쿼리 가독성 향상

을 가능하게 합니다.

---

# 📂 Files & Progress

---

## ✅ Day 40 — Star Schema Design  
`01_star_schema_design.sql`

### What it Implements

- Dimension Tables:
  - `dim_date`
  - `dim_customer`
  - `dim_product`
  - `dim_store`
- Fact Table:
  - `fact_sales`
- Surrogate key strategy
- Foreign key constraints
- Indexes on fact FK columns
- Idempotent DDL (`DROP IF EXISTS`)
- Sample validation queries

---

## ✅ Day 41 — Analytical Query Examples  
`02_star_schema_query_examples.sql`

### What it Demonstrates

- Monthly revenue aggregation (Time dimension)
- Category-based revenue analysis (Product dimension)
- Age-band customer segmentation (Customer dimension)
- Regional & channel breakdown (Store dimension)
- Top-N product analysis
- Simple lifetime value (LTV) calculation
- Multi-dimensional aggregation (Year + Category)

이 파일은 Star Schema가 실제 분석 환경에서
어떻게 활용되는지를 보여주는 실전 예시입니다.

---

# 🏗️ Modeling Principles

## 1️⃣ Fact Table Design

Fact table characteristics:

- Narrow & tall structure
- Stores additive measures
- Contains foreign keys to dimensions
- Optimized for aggregation

Example measures:

- `quantity_sold`
- `unit_price`
- `total_amount`

---

## 2️⃣ Dimension Table Design

Dimension table characteristics:

- Wide & descriptive
- Stores business attributes
- Provides analytical axes
- Enables slicing & dicing

Examples:

- Date hierarchy (year → month → day)
- Product category
- Customer age band
- Store region/channel

---

# ⚙️ Performance Strategy

Star Schema optimizes:

- Read-heavy workloads
- Large-scale aggregation
- Predictable execution plans

Performance tactics used:

- Integer surrogate keys
- Foreign key indexing on fact table
- Minimal join depth
- Additive measure design

---

# 📊 Example Analytical Query

```sql
SELECT
  d.year,
  d.month,
  SUM(f.total_amount) AS monthly_revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;