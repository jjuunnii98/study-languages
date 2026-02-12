"""
Day 38 — Machine Learning Metrics (Basics)

This file covers fundamental evaluation metrics for:
1. Classification
2. Regression

Evaluation is more important than the model itself.
A model without proper evaluation is meaningless.

이 파일은 머신러닝 평가 지표의 기초를 다룬다.

모델의 성능은 알고리즘보다
"어떤 지표로 평가했는가"에 의해 더 크게 좌우된다.
"""

# --------------------------------------------------
# 1️⃣ Imports
# --------------------------------------------------

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    mean_squared_error,
    mean_absolute_error,
    r2_score
)

# --------------------------------------------------
# 2️⃣ Classification Metrics
# --------------------------------------------------

"""
Classification example:
Binary classification (0 / 1)
"""

y_true = np.array([0, 1, 1, 0, 1, 0, 1, 1])
y_pred = np.array([0, 1, 0, 0, 1, 0, 1, 1])

# Accuracy
accuracy = accuracy_score(y_true, y_pred)

# Precision
precision = precision_score(y_true, y_pred)

# Recall
recall = recall_score(y_true, y_pred)

# F1 Score
f1 = f1_score(y_true, y_pred)

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred)

print("=== Classification Metrics ===")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:\n", cm)


"""
📌 한국어 설명

Accuracy:
- 전체 예측 중 맞춘 비율
- 클래스 불균형일 때 신뢰하기 어려움

Precision:
- 양성으로 예측한 것 중 실제 양성 비율
- False Positive 비용이 클 때 중요

Recall:
- 실제 양성 중 예측 성공 비율
- False Negative 비용이 클 때 중요

F1:
- Precision과 Recall의 조화평균
- 불균형 데이터에서 유용
"""

# --------------------------------------------------
# 3️⃣ Regression Metrics
# --------------------------------------------------

"""
Regression example:
Continuous prediction
"""

y_true_reg = np.array([100, 120, 130, 150, 170])
y_pred_reg = np.array([110, 118, 125, 140, 180])

# MSE
mse = mean_squared_error(y_true_reg, y_pred_reg)

# RMSE
rmse = np.sqrt(mse)

# MAE
mae = mean_absolute_error(y_true_reg, y_pred_reg)

# R^2
r2 = r2_score(y_true_reg, y_pred_reg)

print("\n=== Regression Metrics ===")
print("MSE:", mse)
print("RMSE:", rmse)
print("MAE:", mae)
print("R^2:", r2)


"""
📌 한국어 설명

MSE:
- 오차 제곱 평균
- 큰 오차에 민감

RMSE:
- MSE의 제곱근
- 원래 단위로 해석 가능

MAE:
- 절대 오차 평균
- 이상치에 덜 민감

R²:
- 설명력 지표
- 1에 가까울수록 좋음
"""