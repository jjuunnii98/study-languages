"""
Day 66 — Feature Importance
File: 01_python/05_data_analysis/06_interpretation/01_feature_importance.py

목표
- 머신러닝 모델이 어떤 feature를 중요하게 사용했는지 해석한다.
- Tree 기반 모델의 내장 feature importance를 확인한다.
- Permutation Importance를 통해 모델 불가지론 방식으로 중요도를 평가한다.

왜 중요한가?

모델 성능만 보는 것은 충분하지 않다.
실무에서는 반드시 다음 질문에 답해야 한다.

- 어떤 변수가 예측에 가장 큰 영향을 주는가?
- 모델이 논리적으로 납득 가능한 패턴을 학습했는가?
- 특정 feature에 과도하게 의존하고 있지는 않은가?

이 과정을 **Model Interpretation** 또는 **Model Explainability**라고 한다.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# ============================================================
# 1) Demo Dataset
# ============================================================

def load_demo_dataset(random_state: int = 42) -> tuple[pd.DataFrame, pd.Series]:
    """
    실습용 classification dataset 생성.

    일부 feature만 실제로 informative하게 만들어
    feature importance 차이를 확인하기 좋게 만든다.
    """

    X, y = make_classification(
        n_samples=1200,
        n_features=12,
        n_informative=5,
        n_redundant=2,
        n_classes=2,
        random_state=random_state
    )

    feature_names = [f"feature_{i}" for i in range(X.shape[1])]

    X_df = pd.DataFrame(X, columns=feature_names)
    y_sr = pd.Series(y, name="target")

    return X_df, y_sr


# ============================================================
# 2) Train/Test Split
# ============================================================

def split_data(X: pd.DataFrame, y: pd.Series):
    """
    모델 평가를 위해 train/test split 수행
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    return X_train, X_test, y_train, y_test


# ============================================================
# 3) Train Model
# ============================================================

def train_model(X_train, y_train):
    """
    RandomForestClassifier 사용
    - Tree 기반 모델
    - feature_importances_ 속성 제공
    """

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    return model


# ============================================================
# 4) Built-in Feature Importance
# ============================================================

def get_tree_feature_importance(model, feature_names):
    """
    Tree 모델 내부 importance 계산

    RandomForest / GradientBoosting 등에서 제공되는
    feature_importances_ 사용
    """

    importance = model.feature_importances_

    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importance
    }).sort_values("importance", ascending=False)

    return importance_df


# ============================================================
# 5) Permutation Importance
# ============================================================

def get_permutation_importance(model, X_test, y_test):
    """
    Permutation Importance

    원리:
    특정 feature 값을 랜덤으로 섞어서
    모델 성능이 얼마나 떨어지는지 측정한다.

    성능이 크게 떨어지면 → 중요한 feature
    """

    result = permutation_importance(
        model,
        X_test,
        y_test,
        n_repeats=10,
        random_state=42,
        scoring="accuracy"
    )

    importance_df = pd.DataFrame({
        "feature": X_test.columns,
        "importance_mean": result.importances_mean,
        "importance_std": result.importances_std
    }).sort_values("importance_mean", ascending=False)

    return importance_df


# ============================================================
# 6) Print Results
# ============================================================

def print_importance_results(tree_imp, perm_imp):

    print("\n==============================")
    print("Tree Feature Importance")
    print("==============================")
    print(tree_imp.head(10))

    print("\n==============================")
    print("Permutation Importance")
    print("==============================")
    print(perm_imp.head(10))


# ============================================================
# 7) Interpretation Guide
# ============================================================

def explain_importance():

    print("\n=== Feature Importance Interpretation ===")

    print("""
Feature Importance 해석 가이드

1️⃣ 값이 높은 feature
→ 모델 예측에 큰 영향을 주는 변수

2️⃣ 값이 거의 0인 feature
→ 모델이 거의 사용하지 않는 변수

3️⃣ Tree importance vs Permutation importance
- Tree importance는 모델 내부 기준
- Permutation importance는 모델 외부 평가

실무에서는 Permutation Importance를
더 신뢰하는 경우가 많다.
""")


# ============================================================
# 8) Main
# ============================================================

def main():

    # 데이터 로드
    X, y = load_demo_dataset()

    # 데이터 분할
    X_train, X_test, y_train, y_test = split_data(X, y)

    # 모델 학습
    model = train_model(X_train, y_train)

    # 성능 확인
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"\nModel Accuracy: {acc:.4f}")

    # Tree Feature Importance
    tree_importance = get_tree_feature_importance(model, X.columns)

    # Permutation Importance
    perm_importance = get_permutation_importance(model, X_test, y_test)

    # 결과 출력
    print_importance_results(tree_importance, perm_importance)

    # 해석 가이드
    explain_importance()


if __name__ == "__main__":
    main()