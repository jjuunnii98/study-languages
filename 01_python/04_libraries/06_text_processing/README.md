# Text Processing (Python Libraries — 06)

This module covers **practical text processing techniques** in Python,
focusing on methods used in real-world data analysis and ML/NLP pipelines.

It emphasizes:

- Text normalization and cleaning
- Pattern extraction (regex)
- Structuring raw text into usable features
- Preparing text for downstream modeling (NLP, classification, clustering)

본 모듈은 Python에서 텍스트 데이터를 **실무 수준으로 처리**하기 위한 기초를 다룹니다.  
단순 문자열 조작이 아니라, **전처리 → 추출 → 구조화**까지 이어지는 흐름을 목표로 합니다.

---

## 🎯 Learning Objectives

By completing this module, you will be able to:

- Clean and normalize messy text safely
- Extract information from raw text using regex
- Convert unstructured text into structured features
- Build reusable text-processing utilities for analytics pipelines
- Prepare text datasets for NLP and machine learning tasks

---

## 📂 Files & Progress

### ✅ Day 41 — Regex Fundamentals  
`01_regex_basics.py`

**Covers:**

- `re.findall()` for extracting multiple matches
- Email / digit / pattern extraction examples
- `re.sub()` for text cleaning and normalization
- `re.match()` vs `re.search()` differences
- `re.compile()` for reusable patterns and performance
- Capturing groups (`()`) and `.group()` for structured extraction

**한국어 요약:**

- 정규표현식 기본 패턴 설계
- 이메일/숫자/키워드 등 정보 추출
- `re.sub()`를 활용한 텍스트 정리(정규화)
- `match`와 `search`의 차이 이해
- `compile` 기반 반복 처리 최적화
- 그룹 캡처로 구조화된 정보 추출

---

## 🧠 Why Text Processing Matters

Text is one of the most common real-world data formats:

- logs
- reviews
- clinical notes
- emails and messages
- financial news

Without strong text-processing skills, it is difficult to:

- clean messy raw inputs
- extract meaningful signals
- convert text into model-ready features

텍스트 데이터는 가장 흔한 “현실 데이터” 형태입니다.  
텍스트 처리 능력은 단순 문자열 조작이 아니라,  
**데이터를 모델링 가능한 형태로 바꾸는 핵심 역량**입니다.

---

## 🧩 Typical Use Cases

- Log parsing (event/ID extraction)
- NLP preprocessing (normalization, filtering)
- Feature engineering from raw text (entities, patterns)
- Data quality checks (format validation)

---

## ✅ Status

**In progress — Text Processing (started Day 41)**

This module is developed incrementally with practical examples,
and will expand into full text-cleaning pipelines and NLP-ready preprocessing.

본 모듈은 Day 41부터 시작되었으며,  
향후 텍스트 정규화 파이프라인과 NLP 전처리까지 확장될 예정입니다.