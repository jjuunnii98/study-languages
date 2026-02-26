# ❄️ Snowflake Schema Modeling (SQL) — 03_snowflake_schema

This directory implements a **Snowflake Schema**, a normalized extension of the Star Schema
used in analytics and data warehousing.

Snowflake Schema keeps the **Fact table** at the center, but **normalizes Dimension tables**
into sub-dimensions to reduce redundancy and improve data integrity.

본 디렉토리는 Star Schema의 차원(Dimension)을 더 정규화한 형태인  
**Snowflake Schema(스노우플레이크 스키마)**를 SQL로 구현합니다.

- Fact는 이벤트/측정값(Measure)을 저장
- Dimension은 분석 축을 제공
- Snowflake는 Dimension을 **서브 차원으로 분해(정규화)**하여 중복을 줄이고 무결성을 강화합니다.

---

## 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain the difference between **Star Schema** and **Snowflake Schema**
- Normalize Dimensions into sub-dimensions (3NF-style thinking)
- Design stable joins using **surrogate keys**
- Enforce integrity with **foreign keys**
- Apply indexing strategies to mitigate deeper join paths
- Write idempotent DDL scripts for reproducible modeling

본 모듈 완료 후 다음을 수행할 수 있습니다:

- Star vs Snowflake 구조 차이를 명확히 설명
- 차원 테이블을 서브 차원으로 정규화(3NF 관점)
- 대리키(surrogate key) 기반 안정적 조인 설계
- FK 제약조건으로 무결성 확보
- JOIN depth 증가를 고려한 인덱스 설계
- 재현 가능한 DDL 작성(DROP IF EXISTS 등)

---

## 🧠 Snowflake Schema Quick View

### Conceptual Diagram

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