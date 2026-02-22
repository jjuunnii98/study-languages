# Data Loading & Initial Profiling (Python — 05_data_analysis / 01_data_loading)

This directory covers **production-oriented data ingestion and initial validation workflows**
in Python using pandas and SQL interfaces.

It focuses on the first critical stage of any data project:

> Load data safely → Validate structure → Diagnose quality → Prepare for analysis

본 디렉토리는 Python 기반의 **실무형 데이터 적재 및 초기 품질 점검 패턴**을 다룹니다.

단순히 데이터를 읽는 것이 아니라,

- 안전한 로딩
- 타입 안정성 확보
- SQL 보안(파라미터 바인딩)
- 대용량 처리 전략
- 데이터 품질 진단 자동화

까지 포함한 **데이터 분석의 출발점 설계**를 목표로 합니다.

---

## 🎯 Learning Objectives

After completing this module, you will be able to:

- Safely load CSV and Excel files with proper dtype control
- Handle encoding issues and date parsing
- Read SQL data securely using parameter binding
- Process large datasets using chunk-based strategies
- Perform automated data overview & quality checks
- Detect missing values, duplicates, cardinality issues, and outlier hints

본 모듈 완료 후 다음을 수행할 수 있습니다:

- CSV/Excel을 dtype 안정성 있게 로딩
- 인코딩/날짜 파싱 문제 해결
- SQL을 안전하게 읽기 (SQL injection 방지)
- 대용량 chunk 로딩 구현
- 자동 데이터 품질 점검 템플릿 구축
- 결측치/중복/카디널리티/이상치 힌트 탐지

---

# 📂 Files & Progress

---

## ✅ Day 47 — CSV & Excel Loading  
`01_read_csv_excel.py`

### Core Coverage

- Safe CSV loading with encoding fallback
- dtype stabilization (ID as string)
- Date parsing (`parse_dates`)
- NA normalization (`na_values`)
- Chunk-based loading for large files
- Excel sheet handling

### 핵심 요약

- 실무형 CSV/Excel 안전 로딩
- dtype 손상 방지 전략
- 인코딩 문제 대응
- 대용량 파일 처리 패턴

---

## ✅ Day 48 — SQL Data Loading  
`02_read_sql.py`

### Core Coverage

- SQLite demo database (reproducible example)
- Parameter binding (SQL injection prevention)
- Join & aggregation query patterns
- Chunk-based SQL loading
- Basic indexing strategy
- Transaction-safe design

### 핵심 요약

- pandas + SQL 안전 연결
- 바인딩 기반 보안 쿼리
- 조인/집계 쿼리 패턴
- chunk 기반 대용량 처리
- 멱등적 DDL 설계

---

## ✅ Day 49 — Data Overview & Quality Diagnostics  
`03_data_overview.py`

### Core Coverage

- Shape / schema summary
- Missing value rate analysis
- Duplicate row & key detection
- Numeric distribution & IQR-based outlier hints
- Categorical cardinality & top-k frequencies
- Datetime range summary
- Correlation top-pair detection
- CSV-based report export

### 핵심 요약

- 데이터 품질 자동 점검 템플릿
- 결측/중복/카디널리티 진단
- 이상치 힌트 탐지
- 상관관계 스크리닝
- 리포트 자동 저장 구조

---

# 🧠 Architectural Flow

```text
External Source
    ↓
Safe Data Loading (CSV / Excel / SQL)
    ↓
Schema Stabilization
    ↓
Quality Diagnostics
    ↓
Clean Analytical Dataset
    ↓
EDA / Modeling