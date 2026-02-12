"""
Day 40 — Tree Models (Decision Tree & Random Forest)

This file covers:
1) DecisionTreeClassifier (baseline tree)
2) RandomForestClassifier (ensemble)
3) Feature importance interpretation
4) Overfitting control (max_depth, min_samples_leaf)

Tree models are powerful because they can capture non-linear patterns
and interactions without explicit feature engineering.

이 파일은 트리 기반 모델의 핵심을 다룬다.
- 의사결정나무(Decision Tree)
- 랜덤포레스트(Random Forest)
- 과적합 제어 하이퍼파라미터
- 특성 중요도(feature importance) 해석
"""

from __future__ import annotations

import numpy as np

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


# ------------------------------------------------------------
# 1️⃣ Helper: Print metrics neatly
# ------------------------------------------------------------

def print_classification_metrics(y_true: np.ndarray, y_pred: np.ndarray, title: str) -> None:
    """Print standard classification metrics for quick evaluation."""
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    cm = confusion_matrix(y_true, y_pred)

    print(f"\n=== {title} ===")
    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1-score : {f1:.4f}")
    print("Confusion Matrix:\n", cm)


# ------------------------------------------------------------
# 2️⃣ Create synthetic classification dataset
# ------------------------------------------------------------
"""
We use a synthetic dataset so that this script runs anywhere.

make_classification creates data with:
- informative features: truly predictive
- redundant/noise features: distractors

이 예시는 어느 환경에서도 실행 가능하도록
합성 데이터(make_classification)를 사용한다.
"""

RANDOM_STATE = 42

X, y = make_classification(
    n_samples=1200,
    n_features=12,
    n_informative=6,
    n_redundant=2,
    n_repeated=0,
    n_clusters_per_class=2,
    weights=[0.55, 0.45],          # mild imbalance
    flip_y=0.02,                   # label noise
    class_sep=1.0,
    random_state=RANDOM_STATE,
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=RANDOM_STATE,
)

print("Dataset shapes:", X_train.shape, X_test.shape)


# ------------------------------------------------------------
# 3️⃣ Decision Tree (baseline)
# ------------------------------------------------------------
"""
Decision Trees can easily overfit if unconstrained.

Important controls:
- max_depth: limits tree depth
- min_samples_leaf: minimum samples at leaf node
- min_samples_split: minimum samples to split a node

의사결정나무는 제한 없이 학습하면 과적합이 매우 쉽게 발생한다.
따라서 max_depth/min_samples_leaf 같은 제한이 핵심이다.
"""

tree = DecisionTreeClassifier(
    max_depth=4,
    min_samples_leaf=10,
    random_state=RANDOM_STATE,
)

tree.fit(X_train, y_train)
y_pred_tree = tree.predict(X_test)

print_classification_metrics(y_test, y_pred_tree, "Decision Tree (max_depth=4, min_samples_leaf=10)")


# ------------------------------------------------------------
# 4️⃣ Random Forest (ensemble)
# ------------------------------------------------------------
"""
Random Forest reduces overfitting by averaging many trees.

Key idea:
- many decision trees trained on bootstrap samples
- each split considers a random subset of features
→ reduces variance, improves generalization

랜덤포레스트는 여러 트리를 평균내어(앙상블)
의사결정나무의 과적합(variance)을 줄인다.
"""

rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,           # let trees grow, but control with other params
    min_samples_leaf=5,
    max_features="sqrt",      # common default: sqrt(num_features)
    n_jobs=-1,
    random_state=RANDOM_STATE,
)

rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print_classification_metrics(y_test, y_pred_rf, "Random Forest (300 trees, min_samples_leaf=5)")


# ------------------------------------------------------------
# 5️⃣ Feature importance (interpretation)
# ------------------------------------------------------------
"""
Feature importance helps identify which variables matter.

⚠️ Note:
- Importance is model-specific and can be biased
  toward high-cardinality or correlated features.
- For robust interpretation, consider permutation importance or SHAP.

특성 중요도는 “어떤 변수가 모델에 영향이 컸는지”를 보여준다.
다만 편향 가능성이 있으므로 해석 시 주의가 필요하다.
"""

importances = rf.feature_importances_
sorted_idx = np.argsort(importances)[::-1]

print("\n=== Feature Importance (Random Forest) ===")
for rank, idx in enumerate(sorted_idx[:10], start=1):
    print(f"{rank:02d}. Feature {idx:02d}  importance={importances[idx]:.4f}")


# ------------------------------------------------------------
# 6️⃣ Quick summary
# ------------------------------------------------------------
"""
✅ Summary (KR)
- Decision Tree: 해석이 쉽지만 과적합 위험이 큼 → depth/leaf 제약 필수
- Random Forest: 여러 트리 앙상블로 일반화 성능이 좋아짐
- Feature importance: 변수 영향도를 빠르게 파악 가능(편향 주의)

Next:
- Gradient Boosting (XGBoost/LightGBM 스타일)
- Cross Validation + Hyperparameter tuning
"""
print("\nDone. (Day 40 — Tree Models)")