"""
Day 64 — Model Evaluation
File: 01_python/05_data_analysis/05_modeling_basics/03_model_evaluation.py

목표
- 분류 모델의 성능을 "정확도 하나"가 아니라 다각도로 평가한다.
- 실무에서 자주 사용하는 핵심 지표를 코드로 정리한다.
- 데이터 누수(leakage)를 피하기 위해 train/test 분리 후 test 기준으로 평가한다.

핵심 평가 지표
1) Accuracy
   - 전체 예측 중 맞춘 비율
   - 클래스 불균형에서는 misleading 할 수 있음

2) Precision
   - Positive라고 예측한 것 중 실제 Positive 비율
   - False Positive 비용이 클 때 중요

3) Recall
   - 실제 Positive 중 찾아낸 비율
   - False Negative 비용이 클 때 중요

4) F1 Score
   - Precision과 Recall의 조화평균
   - 불균형 데이터에서 자주 사용

5) ROC AUC
   - threshold 전반에 걸친 분류 성능
   - 확률 예측 품질을 평가

6) Confusion Matrix
   - TP / FP / TN / FN 구조 확인
   - 어떤 종류의 에러가 많은지 해석 가능

실무 포인트
- metric은 "문제의 비용 구조"에 따라 선택해야 한다.
- 예: 의료 진단 -> recall 중요
- 예: 스팸 필터 -> precision 중요
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

import numpy as np
import pandas as pd

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ============================================================
# 0) Config
# ============================================================

@dataclass(frozen=True)
class EvalConfig:
    test_size: float = 0.2
    random_state: int = 42
    threshold: float = 0.5


# ============================================================
# 1) Demo Data
# ============================================================

def load_demo_classification_data(random_state: int = 42) -> tuple[pd.DataFrame, pd.Series]:
    """
    실습용 이진 분류 데이터 생성.
    - 일부 클래스 불균형을 주어 평가 지표 차이를 보기 좋게 만든다.
    """
    X, y = make_classification(
        n_samples=1200,
        n_features=12,
        n_informative=6,
        n_redundant=2,
        n_classes=2,
        weights=[0.75, 0.25],   # 불균형 데이터
        flip_y=0.02,
        class_sep=1.0,
        random_state=random_state,
    )

    feature_names = [f"feature_{i}" for i in range(X.shape[1])]
    X_df = pd.DataFrame(X, columns=feature_names)
    y_sr = pd.Series(y, name="target")

    return X_df, y_sr


# ============================================================
# 2) Preprocessing (Leakage-safe)
# ============================================================

def split_and_scale(
    X: pd.DataFrame,
    y: pd.Series,
    cfg: EvalConfig
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    누수 방지 구조:
    - train/test split 먼저
    - scaler는 train에서만 fit
    - test에는 transform만 적용
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=cfg.test_size,
        random_state=cfg.random_state,
        stratify=y,  # 분류 문제에서는 stratify 권장
    )

    scaler = StandardScaler()

    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns,
        index=X_train.index,
    )

    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns,
        index=X_test.index,
    )

    return X_train_scaled, X_test_scaled, y_train, y_test


# ============================================================
# 3) Model Training
# ============================================================

def train_baseline_model(X_train: pd.DataFrame, y_train: pd.Series) -> LogisticRegression:
    """
    baseline 분류 모델:
    Logistic Regression
    - 해석 가능성 좋음
    - 확률 출력 가능
    - 모델 평가 학습에 적합
    """
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    return model


# ============================================================
# 4) Evaluation
# ============================================================

def evaluate_classification_model(
    model: LogisticRegression,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    threshold: float = 0.5,
) -> Dict[str, Any]:
    """
    분류 모델 성능 평가 함수.

    한국어 설명:
    - predict_proba()로 positive class 확률을 얻는다.
    - threshold를 기준으로 최종 class 예측값을 만든다.
    - threshold를 조정하면 precision/recall trade-off가 달라진다.
    """
    # positive class(1) 확률
    y_proba = model.predict_proba(X_test)[:, 1]

    # threshold 기반 예측
    y_pred = (y_proba >= threshold).astype(int)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "classification_report": classification_report(y_test, y_pred, digits=4),
    }

    return metrics


# ============================================================
# 5) Reporting
# ============================================================

def print_evaluation_report(metrics: Dict[str, Any], threshold: float) -> None:
    """
    평가 결과를 사람이 읽기 쉬운 형태로 출력한다.
    """
    print("\n=== Model Evaluation Report ===")
    print(f"Decision threshold: {threshold:.2f}")

    print(f"Accuracy : {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall   : {metrics['recall']:.4f}")
    print(f"F1 Score : {metrics['f1']:.4f}")
    print(f"ROC AUC  : {metrics['roc_auc']:.4f}")

    print("\n=== Confusion Matrix ===")
    print(metrics["confusion_matrix"])

    print("\n=== Classification Report ===")
    print(metrics["classification_report"])


def explain_metrics() -> None:
    """
    지표 해석 가이드 출력
    """
    print("\n=== Metric Interpretation Guide ===")
    print("- Accuracy : 전체적으로 얼마나 맞췄는가")
    print("- Precision: Positive라고 예측한 것 중 실제 Positive 비율")
    print("- Recall   : 실제 Positive를 얼마나 놓치지 않았는가")
    print("- F1 Score : Precision과 Recall의 균형")
    print("- ROC AUC  : threshold 전반에서 확률 예측 품질")


# ============================================================
# 6) Main
# ============================================================

def main() -> None:
    cfg = EvalConfig(
        test_size=0.2,
        random_state=42,
        threshold=0.5,
    )

    # 1) 데이터 로드
    X, y = load_demo_classification_data(random_state=cfg.random_state)

    # 2) split + scaling
    X_train, X_test, y_train, y_test = split_and_scale(X, y, cfg)

    # 3) 모델 학습
    model = train_baseline_model(X_train, y_train)

    # 4) 평가
    metrics = evaluate_classification_model(
        model=model,
        X_test=X_test,
        y_test=y_test,
        threshold=cfg.threshold,
    )

    # 5) 리포트 출력
    print_evaluation_report(metrics, threshold=cfg.threshold)
    explain_metrics()


if __name__ == "__main__":
    main()