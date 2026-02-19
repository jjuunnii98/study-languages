# IO Formats (Python Libraries — 07)

This module covers **production-grade data input/output architecture**
using Python.

Rather than demonstrating basic file reading examples,
this module treats I/O as a **data engineering boundary layer**
between raw storage systems and analytical / ML pipelines.

It focuses on how structured and semi-structured data flows across:

- Flat files (CSV, Excel)
- Semi-structured formats (JSON)
- Columnar storage (Parquet)
- Relational databases (SQL)

---

본 모듈은 Python 기반의 **실무 수준 데이터 입출력(I/O) 아키텍처 설계**를 다룹니다.

단순 파일 입출력이 아니라,  
파일 시스템·컬럼형 저장소·관계형 DB와  
분석/모델링 파이프라인을 연결하는 **데이터 인터페이스 레이어**를 설계합니다.

---

## 🎯 Learning Objectives

After completing this module, you will be able to:

- Safely read and write CSV / Excel files with schema control
- Normalize and serialize JSON data for analytics pipelines
- Leverage Parquet for efficient columnar storage
- Connect pandas with SQL databases securely
- Implement chunk-based processing for large datasets
- Use parameter binding to prevent SQL injection
- Design idempotent, reproducible data ingestion workflows

본 모듈 완료 후 다음을 수행할 수 있습니다:

- 스키마 통제가 가능한 CSV/Excel 입출력
- JSON 정규화 및 직렬화 처리
- Parquet 기반 고성능 컬럼 저장 전략 이해
- pandas ↔ SQL 안전 연결 설계
- 대용량 chunk 처리 구현
- SQL injection 방지를 위한 파라미터 바인딩
- 멱등적이고 재현 가능한 데이터 적재 구조 설계

---

# 📂 Files & Progress

---

## ✅ Day 44 — CSV & Excel I/O  
`01_csv_excel.py`

### Core Coverage

- `pd.read_csv()` advanced configuration
- dtype enforcement
- Date parsing strategies
- Missing value normalization
- Excel multi-sheet read/write patterns
- Controlled export formatting

### 한국어 요약

- CSV 고급 옵션 설계
- dtype 및 날짜 파싱 전략
- 결측치 정규화 처리
- Excel 다중 시트 입출력
- 안정적 export 포맷 설계

---

## ✅ Day 45 — JSON & Parquet  
`02_json_parquet.py`

### Core Coverage

- JSON normalization with `pd.json_normalize()`
- Nested structure flattening
- Parquet read/write patterns
- Columnar storage performance rationale
- Serialization best practices

### 한국어 요약

- JSON 구조 정규화
- 중첩 데이터 평탄화
- Parquet 저장 전략
- 컬럼형 저장소 성능 장점
- 데이터 직렬화 설계 개념

---

## ✅ Day 46 — SQL Read/Write Architecture  
`03_sql_read_write.py`

### Core Coverage

- `pandas.read_sql_query`
- `DataFrame.to_sql`
- Secure parameter binding (`:param`)
- Transaction control (`with connection`)
- Chunked batch inserts
- Schema validation pattern
- Safe identifier handling
- SQLite demo for reproducibility
- Production extension via SQLAlchemy (Postgres/MySQL ready)

### 한국어 요약

- pandas ↔ SQL 인터페이스 설계
- 파라미터 바인딩 기반 보안 처리
- 트랜잭션 기반 데이터 적재
- 대용량 batch insert 전략
- 스키마 검증 패턴
- SQL 식별자 안전 처리
- SQLite 기반 재현 가능한 데모
- 실무 DB 확장 설계 개념

---

# 🧠 Architectural Perspective

I/O is not just data loading.

It is a **system boundary definition layer**.

Poorly designed I/O leads to:

- Schema drift
- Data corruption
- Performance bottlenecks
- Security vulnerabilities
- Non-reproducible pipelines

Well-designed I/O guarantees:

- Reproducibility
- Auditability
- Scalability
- Security
- Stable downstream analytics

---

데이터 입출력은 단순 파일 처리 단계가 아닙니다.  
**시스템 경계를 정의하는 핵심 설계 계층**입니다.

잘 설계된 I/O 구조는  
재현성, 안정성, 확장성, 보안성을 동시에 보장합니다.

---

# 🔄 Conceptual Data Flow

```text
External Storage
        ↓
File / Database Interface
        ↓
Validation & Normalization
        ↓
Structured DataFrame
        ↓
Analytics / ML Pipeline