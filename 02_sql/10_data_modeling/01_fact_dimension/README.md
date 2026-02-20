# 📊 Fact & Dimension Modeling (SQL) — 01_fact_dimension

This directory introduces **data warehouse modeling fundamentals**
based on the **Star Schema** design pattern.

It focuses on designing:

- Central **Fact tables** that store measurable business events  
- Surrounding **Dimension tables** that provide descriptive analysis context  

Rather than writing analytical queries alone, this module emphasizes
**structural modeling for scalable analytics systems**.

---

본 디렉토리는 데이터웨어하우스 설계의 핵심 구조인  
**Star Schema 기반 Fact / Dimension 모델링**을 다룹니다.

단순 SELECT 학습이 아니라,

- 수치(Measure) 중심의 Fact 설계
- 분석 축(Attribute) 중심의 Dimension 설계
- 대리키 기반 안정적 모델링 구조
- 무결성과 성능을 고려한 DDL 작성

까지 포함한 **아키텍처 수준 설계 능력**을 목표로 합니다.

---

## 🎯 Learning Objectives

After completing this module, you will be able to:

- Clearly distinguish **Fact vs Dimension** responsibilities
- Design a complete Star Schema for analytics workloads
- Apply **surrogate key strategy** for stable modeling
- Enforce referential integrity using **foreign keys**
- Optimize joins and aggregations using **indexes**
- Write idempotent DDL scripts for reproducible schema management

---

## 📂 Files & Progress

---

### ✅ Day 38 — Define Fact Table  
`01_define_fact_table.sql`

#### What it implements

- Creates a transactional **fact table** (`fact_sales`)
- Uses a **surrogate key** (`sales_key`) as primary key
- Establishes foreign key relationships to:
  - `dim_date`
  - `dim_product`
  - `dim_customer`
  - `dim_store`
- Defines core measures:
  - `quantity_sold`
  - `unit_price`
- Adds a computed measure:
  - `total_amount = quantity_sold * unit_price`
- Applies indexes on FK columns for join and aggregation performance

#### 한국어 요약

- 트랜잭션 기반 **Fact 테이블(`fact_sales`)** 정의
- PK는 자연키가 아닌 **대리키(surrogate key)** 사용
- 차원 테이블과의 **FK 제약조건** 설정
- Measure(측정값) 정의:
  - `quantity_sold`, `unit_price`
- 계산 컬럼 추가:
  - `total_amount`
- FK 컬럼 인덱스 생성으로 대용량 집계 성능 확보

---

### ✅ Day 39 — Define Dimension Tables  
`02_define_dimension_tables.sql`

#### What it implements

- Defines core dimension tables:
  - `dim_date`
  - `dim_product`
  - `dim_customer`
  - `dim_store`
- Separates **surrogate key** and **natural key**
- Applies CHECK constraints for data integrity
- Adds performance-aware indexing on frequently filtered columns

#### 한국어 요약

- 분석 축(날짜/상품/고객/매장) 구조 정의
- PK는 surrogate key, 자연키는 UNIQUE 유지
- 무결성 제약조건 적용
- 자주 조회되는 속성에 인덱스 적용
- Fact와 연결 가능한 Star Schema 완성

---

## 🧠 Star Schema Structure

```text
          dim_date
              |
dim_product — fact_sales — dim_customer
              |
           dim_store