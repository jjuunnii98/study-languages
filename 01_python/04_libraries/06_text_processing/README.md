# Text Processing (Python Libraries — 06)

This module focuses on **production-grade text preprocessing and transformation**
using Python.

Rather than treating text as simple strings, this module approaches it as a  
**feature engineering system** — transforming raw, unstructured text into
structured, model-ready representations suitable for analytics,
machine learning, and NLP pipelines.

본 모듈은 Python 기반의 **실무 수준 텍스트 전처리 설계**를 다룹니다.  
텍스트를 단순 문자열이 아니라,  
**비정형 데이터 → 정형 피처로 변환하는 엔지니어링 대상**으로 접근합니다.

---

## 🎯 Learning Objectives

After completing this module, you will be able to:

- Normalize noisy real-world text deterministically  
- Extract structured information using regular expressions  
- Design reusable tokenization and cleaning pipelines  
- Convert unstructured text into ML-ready feature spaces  
- Implement interpretable baseline NLP models  
- Understand how preprocessing affects downstream model performance  

---

## 📂 Files & Progress

---

### ✅ Day 41 — Regex Fundamentals  
`01_regex_basics.py`

**Core Topics**

- `re.findall()` for multi-pattern extraction  
- Email / digit / keyword pattern detection  
- `re.sub()` for deterministic normalization  
- `re.match()` vs `re.search()` comparison  
- `re.compile()` for reusable and optimized patterns  
- Capturing groups (`()`) for structured extraction  

**한국어 요약**

- 정규표현식 기반 정보 추출 설계  
- 텍스트 정규화 처리 전략  
- match / search 동작 차이 이해  
- compile을 통한 성능 및 재사용성 개선  
- 그룹 캡처 기반 구조화된 데이터 생성  

---

### ✅ Day 42 — Tokenization & Cleaning  
`02_tokenization_cleaning.py`

**Core Topics**

- Lowercasing and normalization strategies  
- Whitespace and punctuation handling  
- Regex-based tokenization logic  
- Stopword-style filtering rules  
- Custom cleaning function architecture  
- Reusable preprocessing pipeline design  

**한국어 요약**

- 텍스트 표준화 및 정규화 전략  
- 공백/특수문자 제거 구조 설계  
- 토큰 분리 로직 구현  
- 불필요 단어 제거 규칙 설계  
- 재사용 가능한 전처리 파이프라인 구성  

---

### ✅ Day 43 — Simple Sentiment Baseline  
`03_simple_sentiment_baseline.py`

**Core Topics**

- Lexicon-based sentiment scoring  
- Positive / negative word dictionary construction  
- Negation handling (e.g., *not good* → negative)  
- Intensifier logic (e.g., *very good*)  
- End-to-end pipeline:  
  - normalization → tokenization → scoring → evaluation  
- Basic accuracy computation  
- Error case inspection  

**Architectural Focus**

- Explainable rule-based model  
- Deterministic scoring logic  
- Baseline comparison point for future ML models  

**한국어 요약**

- 사전 기반 감성 점수화 설계  
- 부정어 처리 구조 구현  
- 강조어 로직 설계  
- 전처리부터 평가까지 전체 흐름 구현  
- 설명 가능한 베이스라인 모델 구축  
- 향후 ML 모델과 비교 기준 마련  

---

## 🧠 Architectural Perspective

Text preprocessing is not cosmetic cleaning —  
it is a **core modeling stage**.

Poor preprocessing results in:

- Noisy feature representations  
- Reduced model stability  
- Increased overfitting risk  
- Low interpretability  

Well-designed preprocessing ensures:

- Reproducibility  
- Stable feature space  
- Robust model behavior  
- Scalable pipeline architecture  

텍스트 전처리는 모델 성능을 결정하는 핵심 단계입니다.  
전처리 품질이 곧 모델 품질을 좌우합니다.

잘 설계된 전처리는  
**재현성, 안정성, 해석 가능성, 확장성**을 동시에 보장합니다.

---

## 🔄 Conceptual Pipeline

```text
Raw Text
    ↓
Normalization
    ↓
Regex-Based Extraction
    ↓
Tokenization
    ↓
Cleaning / Filtering
    ↓
Feature Engineering
    ↓
Baseline Modeling
    ↓
ML / NLP Model Input