"""
Day 39 — Linear Models (Regression & Classification)

This file covers:
1. Linear Regression
2. Logistic Regression
3. Regularization (Ridge, Lasso concept)

Linear models are the foundation of machine learning.
They are simple, interpretable, and often strong baselines.

이 파일은 머신러닝의 가장 기본이 되는
선형 모델을 다룬다.

- 선형 회귀
- 로지스틱 회귀
- 규제 개념
"""

# --------------------------------------------------
# 1️⃣ Imports
# --------------------------------------------------

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import r2_score, accuracy_score

# --------------------------------------------------
# 2️⃣ Linear Regression Example
# --------------------------------------------------

"""
Regression Task:
Predict continuous values
"""

# Synthetic regression data
np.random.seed(42)
X = np.random.rand(100, 2)
y = 3 * X[:, 0] + 5 * X[:, 1] + np.random.randn(100)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("=== Linear Regression ===")
print("R² Score:", r2_score(y_test, y_pred))
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

"""
📌 한국어 설명

- coef_: 각 변수의 영향력 (기울기)
- intercept_: 절편
- R²: 모델 설명력

선형 회귀는 해석이 명확하고
베이스라인 모델로 매우 중요하다.
"""

# --------------------------------------------------
# 3️⃣ Logistic Regression Example
# --------------------------------------------------

"""
Classification Task:
Binary classification
"""

# Synthetic classification data
X_cls = np.random.randn(200, 2)
y_cls = (X_cls[:, 0] + X_cls[:, 1] > 0).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X_cls, y_cls, test_size=0.2, random_state=42
)

clf = LogisticRegression()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print("\n=== Logistic Regression ===")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Coefficients:", clf.coef_)

"""
📌 한국어 설명

- Logistic Regression은 확률을 예측
- 선형 결합 → sigmoid 함수 → 확률
- 해석 가능한 분류 모델
"""

# --------------------------------------------------
# 4️⃣ Regularization Example (Ridge)
# --------------------------------------------------

"""
Regularization helps prevent overfitting.
Ridge adds L2 penalty to coefficients.
"""

ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)

print("\n=== Ridge Regularization ===")
print("Coefficients:", ridge.coef_)

"""
📌 한국어 설명

- alpha ↑ → 계수 shrinkage 증가
- 과적합 방지
- 변수 많을 때 안정적

선형 모델은:
- 해석 가능
- 빠름
- 베이스라인으로 강력함
"""