# SQL for ML — Train/Test Split

This module covers **train/test split strategies in SQL** for machine learning workflows.

Before training a machine learning model in Python, it is often useful to prepare
the dataset split directly in SQL.

This means:

- features are created in SQL
- labels are generated in SQL
- train/test membership is also assigned in SQL
- Python then consumes a ready-to-use dataset

This approach is especially useful in production-style analytics pipelines,
where reproducibility and dataset consistency matter.

---

# 🎯 Learning Objectives

After completing this module, you should be able to:

- explain why train/test split is necessary
- implement a random train/test split in SQL
- implement a stratified split that preserves label proportions
- validate split ratios and label distributions
- understand when random split is sufficient and when stratified split is better

---

# Why Train/Test Split Matters

A machine learning model must be evaluated on data that was **not used for training**.

That is why we separate the dataset into:

- **Train Set** → used to fit the model
- **Test Set** → used to evaluate generalization performance

Without this separation, evaluation results can become misleading.

### 한국어 설명
train/test split은 모델 성능을 공정하게 평가하기 위한 기본 절차다.

- train: 모델 학습용
- test: 모델 평가용

즉, 모델이 이미 본 데이터가 아니라  
**처음 보는 데이터에서 얼마나 잘 작동하는지 확인하기 위한 구조**다.

---

# Why Do It in SQL?

In many real-world workflows, SQL is the place where:

- source data is stored
- features are engineered
- labels are defined
- training datasets are assembled

So it can be practical to assign train/test membership in SQL before exporting data to Python.

Benefits include:

- reproducibility
- consistent dataset definitions
- less memory pressure in Python
- easier integration with feature tables and label tables

### 한국어 설명
Python에서 split을 할 수도 있지만,  
SQL에서 미리 split을 만들면 데이터셋을 더 일관되게 관리할 수 있다.

특히 대용량 데이터나 팀 단위 협업에서는  
SQL 단계에서 split을 고정하는 방식이 매우 유용하다.

---

# Module Files

| File | Description |
|---|---|
| `01_random_split.sql` | Random train/test split using row-level random values |
| `02_stratified_split.sql` | Stratified train/test split that preserves label proportions |

---

# 1️⃣ Random Split

File  
`01_random_split.sql`

This file demonstrates the most basic train/test split approach.

### Core idea

- assign a random value to each row
- rows below a threshold go to train
- rows above the threshold go to test

Example:

```text
random_score < 0.8  → train
random_score >= 0.8 → test
```

This gives an approximate:

- 80% train
- 20% test

### Strengths

- simple
- easy to implement
- works well as a baseline split strategy

### Limitations

- label proportions may drift between train and test
- less reliable for highly imbalanced classification problems
- not suitable for time-based problems

### 한국어 설명
random split은 가장 기본적인 방식이다.  
각 row에 random 값을 부여해서 train/test를 나눈다.

다만 데이터가 불균형하면  
train/test의 label 비율이 꽤 달라질 수 있다.

---

# 2️⃣ Stratified Split

File  
`02_stratified_split.sql`

This file demonstrates a more robust split method for classification tasks.

### Core idea

Instead of splitting the entire dataset randomly at once:

1. divide rows by label
2. randomize rows within each label group
3. split each label group separately into train/test

This helps preserve label proportions across train and test.

Example:

```text
label = 0 group → 80% train / 20% test
label = 1 group → 80% train / 20% test
```

### Why it matters

If the positive class is rare, pure random split may produce unstable class balance.

Stratified split helps ensure that:

- train distribution is similar to overall distribution
- test distribution is similar to overall distribution

### Best use cases

- binary classification
- imbalanced labels
- fraud detection
- churn prediction
- medical outcome classification

### 한국어 설명
stratified split은 label 비율을 유지하는 분할 방식이다.  
특히 positive class 비율이 낮은 불균형 데이터에서 중요하다.

예를 들어 전체 데이터에서 label=1 비율이 10%라면,  
train도 대략 10%, test도 대략 10%가 되도록 분할한다.

---

# Random vs Stratified Split

| Split Type | 특징 | 장점 | 주의점 |
|---|---|---|---|
| Random Split | 전체 데이터를 한 번에 무작위 분할 | 간단함 | label 분포가 흔들릴 수 있음 |
| Stratified Split | label별로 따로 분할 | label 비율 유지 | classification에 더 적합 |

### 한국어 설명
random split은 입문용/기본형이고,  
stratified split은 classification 실무에서 더 자주 쓰이는 개선형이다.

---

# Validation After Split

Creating the split is not enough.  
You should always validate the result.

Recommended checks:

1. **Split Ratio Check**
   - train/test 비율이 의도대로 나왔는지 확인

2. **Label Distribution Check**
   - train/test 내부 label 비율이 적절한지 확인

3. **Overall vs Split Comparison**
   - 원본 데이터의 분포와 크게 다르지 않은지 확인

### 한국어 설명
split을 만든 뒤에는 반드시 검증해야 한다.

- train/test 비율
- 각 dataset 내부 label 분포
- 전체 데이터 분포 대비 차이

를 확인해야 split이 잘 되었는지 판단할 수 있다.

---

# Practical Workflow

A practical SQL-for-ML pipeline often looks like this:

```text
Raw Tables
    ↓
Feature Engineering
    ↓
Label Generation
    ↓
Train/Test Split
    ↓
Python / R Modeling
```

This module focuses on the **split stage** of that workflow.

### 한국어 설명
지금 이 모듈은 머신러닝 전체 파이프라인에서  
**“모델링 직전 데이터셋 분할 단계”**를 담당한다.

즉 Python에서 모델을 학습하기 전에  
SQL에서 train/test 구조를 완성하는 단계다.

---

# Important Notes

## 1) Reproducibility

If random functions are used directly, the split may change on each run.

To improve reproducibility, consider:

- saving the split result as a table
- using deterministic hash-based rules
- using seed-enabled split logic where supported

## 2) Data Leakage

Split logic alone does not prevent leakage.

You must also ensure:

- features use only valid historical data
- duplicated entities do not leak across train/test
- future information is not embedded in features

## 3) Time-Based Problems

For time series or survival-style data, random or stratified split may be inappropriate.

In such cases, use:

- time-ordered split
- rolling window split
- temporal validation

### 한국어 설명
reproducibility와 leakage는 split 단계에서 매우 중요하다.

또한 시계열 데이터나 time-to-event 문제에서는  
random / stratified split보다 **time-based split**이 더 적절하다.

---

# Summary

This module introduces two essential train/test split patterns in SQL:

```text
Random Split
→ simplest baseline split

Stratified Split
→ preserves label balance across train and test
```

Together, these methods provide the foundation for preparing
machine-learning-ready datasets directly in SQL.

By using SQL for split assignment, you can build workflows that are:

- reproducible
- scalable
- easier to integrate with production data pipelines