# Fact & Dimension Modeling (SQL) — 01_fact_dimension

This directory introduces **data modeling fundamentals** for analytics and data warehousing,
focusing on the **Star Schema** approach:

- **Fact tables** store measurable events (measures)
- **Dimension tables** store descriptive attributes (analysis context)

본 디렉토리는 분석/데이터웨어하우스 관점에서 가장 표준적인 **Star Schema** 모델링을 다룹니다.

- **Fact 테이블**: 집계/분석 대상이 되는 수치(Measure)를 저장
- **Dimension 테이블**: 분석 기준이 되는 속성(Attribute)을 저장

---

## 🎯 Learning Objectives

- Understand the difference between **Fact** and **Dimension**
- Design a Star Schema for analytics workloads
- Use **surrogate keys** for stable modeling
- Enforce integrity using **foreign keys**
- Apply **indexes** for large-scale query performance
- Write idempotent DDL for reproducible modeling (DROP IF EXISTS, etc.)

---

## 📂 Files & Progress

### ✅ Day 38 — Define Fact Table  
`01_define_fact_table.sql`

**What it covers (English)**

- Creates a transactional **fact table** (`fact_sales`)
- Uses a **surrogate key** (`sales_key`) as the primary key
- Adds **foreign keys** to dimension tables:
  - `dim_date`, `dim_product`, `dim_customer`, `dim_store`
- Defines core measures:
  - `quantity_sold`, `unit_price`
- Includes a **generated measure**:
  - `total_amount = quantity_sold * unit_price`
- Adds indexes on FK columns for join + aggregation performance

**한국어 요약**

- 트랜잭션 기반 **Fact 테이블**(`fact_sales`) 정의
- PK는 자연키가 아닌 **대리키(surrogate key)** 사용
- 차원 테이블(`dim_date`, `dim_product`, `dim_customer`, `dim_store`)과 연결되는 **FK 제약조건** 설정
- Measure(측정값) 컬럼 정의:
  - `quantity_sold`, `unit_price`
- 파생 Measure(계산 컬럼) 추가:
  - `total_amount = quantity_sold * unit_price`
- FK 컬럼 인덱스 생성으로 Join/집계 성능 확보

---

## 🧠 Star Schema Quick View

```text
          dim_date
              |
dim_product — fact_sales — dim_customer
              |
           dim_store