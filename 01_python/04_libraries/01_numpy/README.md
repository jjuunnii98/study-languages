# NumPy

This directory covers the fundamentals of **NumPy**, the core numerical
computing library in Python.

NumPy provides fast, vectorized operations on multi-dimensional arrays
and serves as the foundation for data analysis, machine learning,
and scientific computing in Python.

본 폴더는 Python의 핵심 수치 계산 라이브러리인 **NumPy**의
기본 개념부터 실전 활용까지 단계적으로 학습하는 것을 목표로 합니다.

---

## 🎯 Learning Objectives

- Understand NumPy array structures and data types
- Perform efficient numerical operations using vectorization
- Master indexing, slicing, and boolean filtering
- Build a solid foundation for pandas, machine learning, and statistics

---

## 📂 Files & Progress

Each file focuses on a single NumPy concept and is completed
incrementally with daily commits.

각 파일은 하나의 핵심 개념을 다루며,
일 단위 학습 로그 형태로 점진적으로 확장됩니다.

### ✅ Completed

#### `01_arrays_basics.py` (Day 22)
NumPy array creation and basics

- Creating arrays from Python lists
- Understanding `ndarray` structure
- Shape, dimension, and data types
- Comparison with Python lists

**한국어 요약**
- NumPy 배열의 기본 구조 이해
- 리스트 대비 NumPy의 성능·표현력 차이 인식
- 수치 계산을 위한 기반 개념 정리

---

#### `02_indexing_slicing.py` (Day 23)
Indexing and slicing NumPy arrays

- 1D and 2D indexing
- Slicing with start/stop/step
- Boolean indexing for filtering
- Fancy indexing
- View vs copy behavior

**한국어 요약**
- NumPy 인덱싱/슬라이싱 핵심 패턴 습득
- 데이터 필터링을 위한 Boolean indexing 이해
- view와 copy 차이로 인한 버그 예방

---

### ⏳ Planned

#### `03_broadcasting.py`
Broadcasting rules and vectorized operations

- Broadcasting fundamentals
- Shape alignment rules
- Eliminating explicit loops
- Performance-aware computation

#### `04_ufuncs.py`
Universal functions and numerical operations

- Built-in ufuncs
- Element-wise operations
- Aggregation functions

#### `05_random_sampling.py`
Random number generation and simulation

- Random sampling
- Distributions
- Reproducibility with seeds

---

## 🧠 Why NumPy Matters

NumPy enables:
- High-performance numerical computation
- Vectorized data processing
- Clean and expressive mathematical code
- Scalable data pipelines for ML and statistics

Most Python data libraries (pandas, scikit-learn, PyTorch)
are built directly on top of NumPy.

Without a strong NumPy foundation,
advanced data analysis and machine learning become fragile and inefficient.

---

## 🚧 Status

**In progress — NumPy fundamentals (Day 22–23 completed)**

This module is actively developed and will expand toward
broadcasting, vectorization, and simulation techniques.