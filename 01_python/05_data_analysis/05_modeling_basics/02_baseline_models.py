"""
02_baseline_models.py

[목표]
- 모델링을 시작하기 전, '최소 기준선(baseline)' 성능을 빠르게 확보한다.
- 분류(Classification): DummyClassifier (most_frequent / stratified / uniform)
- 회귀(Regression): DummyRegressor (mean / median)

[왜 필요?]
- 고급 모델(RandomForest, XGBoost 등)을 쓰더라도 baseline보다 못하면 의미가 없다.
- 데이터 누수, 잘못된 평가 설정, 라벨 불균형 등 문제를 조기에 잡는다.

[실행]
python 02_baseline_models.py
"""

from __future__ import annotations

import numpy as np

from sklearn.datasets import load_breast_cancer, fetch_california_housing
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split


# -----------------------------
# 1) 분류 베이스라인
# -----------------------------
def run_classification_baselines(random_state: int = 42) -> None:
    """
    분류 문제에서 baseline 성능을 측정한다.

    - most_frequent: 항상 가장 많이 등장하는 클래스만 예측 (불균형 데이터에서 꽤 강해 보일 수 있음)
    - stratified: 학습 데이터의 클래스 비율에 맞춰 랜덤 예측
    - uniform: 클래스 균등 확률로 랜덤 예측

    지표:
    - accuracy: 직관적이지만 불균형 데이터에 취약
    - f1: 불균형 상황에서 더 유용한 경우 많음(특히 positive class에 관심 있을 때)
    - roc_auc: 확률/스코어 기반 지표(이진분류에서 유용)
    """
    data = load_breast_cancer()
    X, y = data.data, data.target  # y: 0/1

    # stratify=y: train/test 모두 클래스 비율을 유지
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=random_state
    )

    strategies = ["most_frequent", "stratified", "uniform"]

    print("\n" + "=" * 80)
    print("[Classification] Dummy baselines on Breast Cancer dataset")
    print(f"Train size: {X_train.shape}, Test size: {X_test.shape}")
    print("=" * 80)

    for strat in strategies:
        clf = DummyClassifier(strategy=strat, random_state=random_state)
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)

        # roc_auc는 확률 점수가 필요: predict_proba 가능할 때 사용
        # (DummyClassifier는 보통 predict_proba를 제공)
        y_proba = clf.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba)

        print(f"\n- strategy = {strat}")
        print(f"  accuracy : {acc:.4f}")
        print(f"  f1       : {f1:.4f}")
        print(f"  roc_auc  : {auc:.4f}")


# -----------------------------
# 2) 회귀 베이스라인
# -----------------------------
def run_regression_baselines(random_state: int = 42) -> None:
    """
    회귀 문제에서 baseline 성능을 측정한다.

    - mean: 항상 y_train 평균으로 예측
    - median: 항상 y_train 중앙값으로 예측 (이상치(outlier)에 더 강한 경우가 많음)

    지표:
    - MAE: 평균 절대 오차 (해석 쉬움)
    - RMSE: 큰 오차에 더 민감
    - R^2: 1에 가까울수록 좋음, baseline에서는 음수가 나올 수도 있음(평균 예측보다 못하다는 의미)
    """
    data = fetch_california_housing()
    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )

    strategies = ["mean", "median"]

    print("\n" + "=" * 80)
    print("[Regression] Dummy baselines on California Housing dataset")
    print(f"Train size: {X_train.shape}, Test size: {X_test.shape}")
    print("=" * 80)

    for strat in strategies:
        reg = DummyRegressor(strategy=strat)
        reg.fit(X_train, y_train)

        y_pred = reg.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred) ** 0.5
        r2 = r2_score(y_test, y_pred)

        print(f"\n- strategy = {strat}")
        print(f"  mae  : {mae:.4f}")
        print(f"  rmse : {rmse:.4f}")
        print(f"  r2   : {r2:.4f}")


def main() -> None:
    # 난수 고정: 결과 재현 가능성 확보
    random_state = 42

    # 1) 분류 baseline
    run_classification_baselines(random_state=random_state)

    # 2) 회귀 baseline
    run_regression_baselines(random_state=random_state)


if __name__ == "__main__":
    main()