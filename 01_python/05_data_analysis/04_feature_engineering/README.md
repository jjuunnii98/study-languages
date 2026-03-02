# 🧩 Feature Engineering — 04_feature_engineering (Python Data Analysis)

This directory implements a **production-aware feature engineering workflow**
for analytics and machine learning pipelines.

Feature engineering is not “adding a few columns.”
It is a controlled transformation layer that converts raw signals into:

- model-readable representations
- statistically stable inputs
- reproducible and auditable transformations

본 디렉토리는 분석/ML 파이프라인에서 필요한  
**실무형 피처 엔지니어링 아키텍처**를 구현합니다.

피처 엔지니어링은 단순히 컬럼을 몇 개 추가하는 작업이 아니라,

- 원시 데이터 → 모델 입력 형태 변환
- 스케일/분포 안정화
- 시간/텍스트/범주형 구조화
- 재현 가능한 규칙 기반 변환

을 목표로 하는 핵심 단계입니다.

---

## 🎯 Learning Objectives

After completing this module, you will be able to:

- Encode categorical variables safely (one-hot / ordinal / frequency)
- Scale numeric features appropriately (standard / min-max / robust)
- Generate time-based features without leakage
- Convert unstructured text into structured model features
- Build reusable feature transformation utilities
- Maintain reproducibility via deterministic rules and reporting

본 모듈 완료 후 다음을 수행할 수 있습니다:

- 범주형 변수를 안전하게 인코딩(one-hot/ordinal/frequency)
- 수치형 피처를 상황에 맞게 스케일링(standard/min-max/robust)
- 누수(leakage) 없이 날짜/시간 파생 피처 생성
- 텍스트를 구조화된 피처로 변환(통계/키워드/선택적 TF-IDF)
- 재사용 가능한 피처 변환 유틸 구성
- 규칙 기반/결과 리포트 기반으로 재현성 유지

---

## 📂 Files & Progress

### ✅ Day 58 — Encoding (Categorical Features)
`01_encoding.py`

**Core Coverage (English)**

- One-hot encoding patterns (baseline, safe handling)
- Ordinal encoding use-cases (ordered categories)
- Frequency / count encoding patterns
- Unknown category handling strategy
- Reproducible mapping generation (fit → transform mindset)

**한국어 요약**

- 범주형 기본 One-hot 인코딩
- 순서형 카테고리(ordinal) 인코딩 적용 기준
- 빈도 기반 인코딩으로 희소성/고차원 문제 완화
- 미지 카테고리(Unknown) 처리 규칙
- train/test 분리 관점의 mapping 설계

---

### ✅ Day 59 — Scaling (Numeric Features)
`02_scaling.py`

**Core Coverage (English)**

- Standard scaling vs Min-Max scaling vs Robust scaling
- Outlier-heavy distributions and robust strategy
- Fit-on-train / apply-on-test concept (leakage prevention mindset)
- Summary statistics reporting for scaling effect checks

**한국어 요약**

- 표준화(Standard) / 정규화(Min-Max) / Robust 스케일링 비교
- 이상치가 많은 분포에서 robust 전략이 유리한 이유
- leakage 방지 관점(fit rules 분리)
- 스케일링 전/후 통계 리포트로 안전 점검

---

### ✅ Day 60 — Date/Time Features (Temporal Engineering)
`03_date_features.py`

**Core Coverage (English)**

- Datetime parsing and timezone-safe handling
- Calendar features: year/month/day/weekday/weekend
- Cyclical encoding (sin/cos) for periodic signals
- Lag / rolling / time-since features (concept + safe pattern)
- Leakage warnings and “as-of time” mindset

**한국어 요약**

- 날짜 파싱 및 timezone 안정성
- 캘린더 파생 피처(요일/주말/월 등)
- 주기성 피처의 cyclical encoding(sin/cos)
- lag/rolling/time-since 개념 및 설계 패턴
- 예측 시점 기준(as-of)으로 누수 방지

---

### ✅ Day 61 — Text Features (Text → Structured Features)
`04_text_features.py`

**Core Coverage (English)**

- Basic normalization (lower/whitespace/pattern replacement)
- Text statistics features:
  - char length, word count, unique ratio, avg word length
  - digit/punctuation counts, URL/email flags
- Keyword / lexicon features (rule-based baseline)
- Optional TF-IDF feature generation (if scikit-learn available)
- Reproducibility mindset: fixed preprocessing rules

**한국어 요약**

- 텍스트 정규화(토큰화 이전의 안정화 단계)
- 길이/단어수/중복률 등 통계 기반 피처
- URL/이메일/숫자 포함 여부 같은 패턴 피처
- 키워드 사전 기반 베이스라인 피처
- (선택) TF-IDF로 벡터 피처 생성
- 전처리 규칙을 고정하여 재현성 유지

---

## 🧠 Recommended Feature Engineering Order (실무 흐름)

```text
Raw Dataset
  ↓
Schema & dtype normalization (정합성 확보)
  ↓
Missing / outlier control (분포 안정화)
  ↓
Categorical encoding (Day 58)
  ↓
Numeric scaling (Day 59)
  ↓
Datetime feature engineering (Day 60)
  ↓
Text feature engineering (Day 61)
  ↓
Model-ready feature set + audit report