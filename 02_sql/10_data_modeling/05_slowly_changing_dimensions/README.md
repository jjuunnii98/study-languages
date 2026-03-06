# 🕰 Slowly Changing Dimensions (SQL) — 05_slowly_changing_dimensions

This module covers **Slowly Changing Dimensions (SCD)**, one of the most important
concepts in dimensional modeling and data warehousing.

Dimensions do not always stay static.  
Customer attributes, product categories, regions, and business classifications
can change over time.

SCD patterns define **how those changes should be stored and managed**.

본 디렉토리는 데이터웨어하우스 모델링의 핵심 개념인  
**Slowly Changing Dimensions (SCD)** 를 SQL 기반으로 구현합니다.

차원 테이블의 속성은 시간이 지나면서 변경될 수 있습니다.

예를 들어:

- 고객 주소 변경
- 고객 등급 변경
- 상품 카테고리 변경
- 조직/지역 정보 변경

이때 중요한 것은:

- 최신값만 유지할 것인지
- 과거 이력을 남길 것인지
- 어떤 방식으로 변경을 관리할 것인지

를 명확히 설계하는 것입니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain why dimension attributes change over time
- Distinguish between **SCD Type 1** and **SCD Type 2**
- Implement overwrite-based updates for current-state dimensions
- Implement history-preserving inserts for temporal dimensions
- Design surrogate-key-based historical tracking structures
- Choose the correct SCD strategy based on business needs

본 모듈 완료 후 다음을 수행할 수 있습니다:

- 차원 속성이 시간에 따라 변하는 이유 설명
- **SCD Type 1** 과 **SCD Type 2** 구조 차이 이해
- 최신값만 유지하는 overwrite 패턴 구현
- 이력을 보존하는 history tracking 패턴 구현
- surrogate key 기반 이력 관리 구조 설계
- 업무 목적에 맞는 SCD 전략 선택

---

# 📂 Files & Progress

---

## ✅ Day 46 — SCD Type 1  
`01_scd_type1.sql`

### What It Implements

- Business key–based change matching
- Existing row overwrite (`UPDATE`)
- New row insert for unseen business keys
- Current-state dimension maintenance
- Staging table → dimension synchronization

### 핵심 개념

SCD Type 1은 **기존 값을 덮어쓴다**.

즉:

- 과거 이력을 저장하지 않음
- 최신 상태만 유지
- 구조가 단순하고 저장 비용이 낮음

### Example Use Cases

- 고객 이메일 오타 수정
- 이름 표기 정정
- 잘못 입력된 속성 수정
- 과거값보다 현재값만 중요한 경우

### Summary

```text
Old value  → overwritten
History    → not preserved
State      → current only
```
---

### ✅ Day 47 — SCD Type 2

02_scd_type2.sql

What It Implements
	•	Change detection against current dimension rows
	•	Expiration of existing current row
	•	Insert of new current row
	•	Historical tracking with:
	•	start_date
	•	end_date
	•	is_current
	•	Surrogate-key-based versioned dimension design

핵심 개념

SCD Type 2는 변경 이력을 보존한다.

즉:
	•	기존 row를 수정하지 않음
	•	기존 row를 종료(expire) 처리
	•	새로운 row를 insert
	•	과거 상태를 그대로 보존

Example Use Cases
	•	고객 주소 이력 추적
	•	고객 등급 변경 추적
	•	상품 분류 변경 이력 관리
	•	시점 기준 분석(point-in-time analysis)이 필요한 경우

Summary
'''
Old value  → retained
History    → preserved
State      → versioned rows
'''

---

### 🔄 SCD Change Flow

# Type 1
'''
Incoming change
    ↓
Match by business key
    ↓
UPDATE existing row
    ↓
Only latest value remains
'''

# Type 2
'''
Incoming change
    ↓
Match current row by business key
    ↓
Expire current row
    ↓
Insert new row
    ↓
History preserved
'''

---

### 🏗 Core Modeling Principles

### 1️⃣ Business Key vs Surrogate Key
	•	Business Key: real-world identifier (customer_id)
	•	Surrogate Key: warehouse-generated identifier (customer_key)

SCD Type 2 especially requires surrogate keys because
the same business key can have multiple historical versions.

---

### 2️⃣ Current Row Flag

In Type 2, is_current is used to identify the active version quickly.

Example:
'''
customer_id = C001
version 1 → is_current = FALSE
version 2 → is_current = TRUE
'''

---

### 3️⃣ Effective Date Range

Type 2 typically uses:
	•	start_date
	•	end_date

This supports:
	•	point-in-time lookup
	•	historical reporting
	•	temporal consistency

---

### 📊 Practical Design Guidance

Use Type 1 when:
	•	only the latest value matters
	•	history is not needed
	•	storage simplicity is preferred
	•	correction-type updates are common

Use Type 2 when:
	•	historical tracking is required
	•	regulatory / audit needs exist
	•	business analysis depends on past states
	•	time-aware joins are needed

---

### 🚀 Current Status

Day 46–47 Completed

This module now demonstrates:
	•	current-state dimension overwrite logic
	•	history-preserving dimension versioning
	•	staging-to-dimension change processing
	•	surrogate-key-based temporal modeling

---

### 🔜 Future Expansion

Possible next topics:
	•	SCD Type 3
	•	Hybrid SCD strategies
	•	Late-arriving dimensions
	•	Fact-to-dimension temporal joins
	•	Effective-dated lookups in ETL pipelines

---

### 🏁 Summary

This module moves dimensional modeling beyond static lookup tables.

It shows how warehouse dimensions can evolve over time through:
	•	Type 1 → overwrite current state
	•	Type 2 → preserve historical state

Understanding SCD is essential for building
production-grade analytical systems with temporal accuracy.
