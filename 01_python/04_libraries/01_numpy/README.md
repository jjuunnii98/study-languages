# NumPy

This directory covers the fundamentals of **NumPy**, the core library for
numerical computing in Python. NumPy arrays are the foundation for
data analysis, machine learning, and scientific computing workflows.

본 폴더는 파이썬 수치 연산의 핵심 라이브러리인 **NumPy**를 다룹니다.  
NumPy 배열은 pandas, scikit-learn, 딥러닝 프레임워크까지 이어지는
데이터 분석/머신러닝 워크플로우의 기반입니다.

---

## 📂 Files

### `01_arrays_basics.py` (Day 22)
NumPy array fundamentals

- Creating arrays (`np.array`, `zeros`, `ones`, `arange`, `linspace`)
- Array properties (`dtype`, `shape`, `ndim`)
- Indexing & slicing (1D/2D)
- Vectorized operations (broadcast-like scalar ops)
- Boolean indexing
- Basic aggregations (`sum`, `mean`, `min`, `max`, `std`)

**한국어 요약**
- NumPy 배열 생성과 기본 속성 이해
- 인덱싱/슬라이싱으로 데이터 접근
- 반복문 없이 벡터화 연산 수행
- 조건 필터링(불리언 인덱싱) 및 기본 통계 집계

---

## 🎯 Learning Objectives

- Understand why NumPy arrays are faster than Python lists for numeric work
- Build confidence with array creation, indexing, and slicing
- Write clean numerical code using vectorized operations
- Prepare for pandas and machine learning pipelines using NumPy arrays

---

## 🧠 Why NumPy Matters

NumPy enables:
- Efficient numerical computation (fast + memory-friendly)
- Clean, readable vectorized code (less for-loops)
- Standard data representation for ML models
- Seamless integration with pandas, scikit-learn, and deep learning libraries

NumPy를 이해하면:
- 데이터 전처리/변환이 쉬워지고
- 모델 입력 데이터를 안정적으로 다룰 수 있으며
- 이후 라이브러리 학습 속도가 크게 빨라집니다.

---

## 🚧 Status

**In progress — NumPy (started Day 22)**

Next steps (planned):
- Array operations & broadcasting (`reshape`, `transpose`, `broadcast`)
- Advanced indexing (`where`, `take`, `clip`)
- Linear algebra basics (`dot`, `matmul`)
- Random sampling (`np.random`)

본 파트는 Day 22부터 시작되었으며,
이후 실전 데이터 분석에 필요한 배열 연산/변환/난수 생성까지 확장할 예정입니다.