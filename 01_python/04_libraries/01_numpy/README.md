# NumPy

This directory covers the fundamentals of **NumPy**, the core numerical
computing library in Python.

NumPy provides fast, vectorized operations on multi-dimensional arrays
and serves as the foundation for data analysis, machine learning,
and scientific computing in Python.

본 폴더는 Python의 핵심 수치 계산 라이브러리인 **NumPy**를
기본 개념부터 실전 활용까지 단계적으로 학습하는 것을 목표로 합니다.

---

## 🎯 Learning Objectives

- Understand NumPy array structures and data types
- Perform efficient numerical operations using vectorization
- Master indexing, slicing, and boolean filtering
- Learn broadcasting rules to write loop-free numerical code
- Build a strong foundation for pandas, machine learning, and statistics

---

## 📂 Files

### `01_arrays_basics.py` (Day 22)
NumPy array creation and basics

- Creating arrays (`np.array`, `zeros`, `ones`, `eye`, `arange`, `linspace`)
- Array properties (`dtype`, `shape`, `ndim`)
- Basic indexing/slicing preview
- Vectorized operations (intro)
- Boolean indexing (intro)
- Basic aggregations (`sum`, `mean`, `min`, `max`, `std`)

**한국어 요약**
- NumPy 배열 생성과 기본 속성 이해
- 리스트 대비 NumPy의 성능·표현력 차이 인식
- 수치 계산을 위한 기반 개념 정리

---

### `02_indexing_slicing.py` (Day 23)
Indexing and slicing NumPy arrays

- 1D and 2D indexing
- Slicing with start/stop/step
- Boolean indexing for filtering
- Fancy indexing
- View vs copy behavior (중요)

**한국어 요약**
- NumPy 인덱싱/슬라이싱 핵심 패턴 습득
- 데이터 필터링을 위한 Boolean indexing 이해
- view와 copy 차이로 인한 버그 예방

---

### `03_vectorization_broadcasting.py` (Day 24)
Vectorization and broadcasting

- Vectorization vs Python loops (개념 + 결과 일치 확인)
- Broadcasting rules (shape 호환 규칙)
- Row/column-wise operations (center/standardize pattern)
- Distance matrix pattern (`x[:, None] - x[None, :]`)
- Broadcasting failure cases and how to fix with `reshape`

**한국어 요약**
- 반복문을 벗어난 벡터화 사고방식 확립
- broadcasting 규칙을 예제로 체득
- (n,) vs (n,1) 차원 차이를 명확히 이해하여 실무 버그 방지

---

## 🧠 Why NumPy Matters

NumPy enables:
- High-performance numerical computation
- Vectorized data processing (fewer loops, cleaner code)
- Efficient data transformation for ML/statistics pipelines
- A standard array interface used by pandas, scikit-learn, and deep learning libraries

Most Python data libraries are built directly on top of NumPy.
A strong NumPy foundation makes advanced data analysis far more reliable and efficient.

NumPy를 이해하면:
- 데이터 전처리/변환이 쉬워지고
- 모델 입력 데이터를 안정적으로 다룰 수 있으며
- 이후 pandas, ML 라이브러리 학습 속도가 크게 빨라집니다.

---

## 🚧 Status

**In progress — NumPy (Day 22–24 completed)**

Next steps (planned):
- Universal functions (ufuncs) & aggregations (`sum/mean`, `axis`, `keepdims`)
- Random sampling & simulation (`np.random`, reproducibility)
- Linear algebra basics (`dot`, `matmul`) when needed

본 파트는 Day 22–24까지 완료되었으며,
이후 ufunc/집계/난수 시뮬레이션 중심으로 확장합니다.