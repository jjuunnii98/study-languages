# ⭐ Star Schema Modeling (SQL) — 02_star_schema

This module implements a **production-grade Star Schema architecture**
for analytical and data warehousing workloads.

Rather than focusing on isolated DDL examples,
it formalizes how transactional data should be modeled
to support:

- Scalable aggregation
- Predictable OLAP query patterns
- BI-friendly joins
- Performance-aware analytics systems

본 디렉토리는 분석 및 데이터웨어하우스 환경에서 가장 표준적인  
**Star Schema 모델링 구조**를 SQL 기반으로 체계적으로 설계합니다.

단순 테이블 생성이 아니라,

- 분석 친화적 구조 설계
- 무결성(Integrity) 보장
- 성능(Indexing) 고려
- 재현 가능한 DDL 스크립트 작성

을 목표로 합니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Clearly distinguish between **Fact** and **Dimension** modeling roles
- Design a Star Schema optimized for read-heavy analytics workloads
- Apply surrogate key strategies for stable joins
- Enforce referential integrity using foreign keys
- Implement indexing strategies for large-scale aggregation
- Write idempotent DDL for reproducible data modeling

본 모듈 완료 후 다음을 수행할 수 있습니다:

- Fact / Dimension의 역할을 구조적으로 설명
- 분석용 Star Schema 설계
- 대리키 기반 안정적 조인 구조 구현
- FK 제약조건을 통한 무결성 확보
- 집계 중심 인덱스 전략 설계
- 재현 가능한 DDL 작성

---

# 🧠 Architectural Perspective

Star Schema separates responsibilities:

- **Fact Table** → Measurable events (수치 중심)
- **Dimension Tables** → Analytical context (속성 중심)

핵심 원칙:

- Fact는 **narrow & tall**
- Dimension은 **wide & descriptive**
- Join은 단순하고 예측 가능해야 한다

---

## 🔷 Conceptual Diagram

```text
              dim_date
                  |
dim_product — fact_sales — dim_customer
                  |
               dim_store