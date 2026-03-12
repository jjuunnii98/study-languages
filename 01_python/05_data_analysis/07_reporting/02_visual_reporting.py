"""
Day 70 — Visual Reporting
File: 01_python/05_data_analysis/07_reporting/02_visual_reporting.py

목표
- 모델 결과를 시각적으로 전달하는 reporting 패턴을 익힌다.
- 단순 숫자 표를 넘어 confusion matrix, probability distribution,
  metric summary를 시각화한다.
- 실무에서는 "성능 계산"과 "보고용 시각화"가 분리되어 있어야 한다.

핵심 구성
1) confusion matrix heatmap
2) predicted probability distribution
3) metric comparison bar chart
4) reporting figure 저장

실무 포인트
- 시각화는 예쁘게 그리는 것이 목적이 아니라,
  의사결정자가 빠르게 이해하도록 만드는 것이 목적이다.
- reporting chart는 "설명 가능성"과 "읽기 쉬움"이 중요하다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ============================================================
# 0) Config
# ============================================================

@dataclass(frozen=True)
class VisualReportConfig:
    test_size: float = 0.2
    random_state: int = 42
    threshold: float = 0.5
    save_dir: str = "reports"


# ============================================================
# 1) Demo Data
# ============================================================

def load_demo_data(random_state: int = 42) -> Tuple[pd.DataFrame, pd.Series]:
    """
    실습용 classification 데이터 생성
    """
    X, y = make_classification(
        n_samples=1400,
        n_features=10,
        n_informative=5,
        n_redundant=2,
        n_classes=2,
        weights=[0.7, 0.3],
        flip_y=0.02,
        class_sep=1.0,
        random_state=random_state,
    )

    feature_names = [f"feature_{i}" for i in range(X.shape[1])]
    X_df = pd.DataFrame(X, columns=feature_names)
    y_sr = pd.Series(y, name="target")

    return X_df, y_sr


# ============================================================
# 2) Split Data
# ============================================================

def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    cfg: VisualReportConfig
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    stratify로 클래스 비율 유지
    """
    return train_test_split(
        X,
        y,
        test_size=cfg.test_size,
        random_state=cfg.random_state,
        stratify=y,
    )


# ============================================================
# 3) Build Baseline Model
# ============================================================

def build_model(random_state: int = 42) -> Pipeline:
    """
    scaler + logistic regression
    - reporting 예제이지만 누수 방지를 위해 pipeline 사용
    """
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000, random_state=random_state)),
        ]
    )
    return model


# ============================================================
# 4) Evaluate Model
# ============================================================

def evaluate_model(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    threshold: float = 0.5
) -> Dict[str, Any]:
    """
    모델 성능 평가 및 reporting용 데이터 반환
    """
    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)

    cm = confusion_matrix(y_test, y_pred)

    results = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion_matrix": cm,
        "y_true": y_test.reset_index(drop=True),
        "y_pred": pd.Series(y_pred, name="y_pred"),
        "y_proba": pd.Series(y_proba, name="y_proba"),
    }
    return results


# ============================================================
# 5) Chart 1 — Confusion Matrix Heatmap
# ============================================================

def plot_confusion_matrix(cm: np.ndarray, save_path: str | None = None) -> None:
    """
    confusion matrix를 heatmap처럼 시각화
    한국어 설명:
    - 어떤 종류의 오분류(FP/FN)가 많은지 직관적으로 전달 가능
    """
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, interpolation="nearest")
    plt.colorbar(im, ax=ax)

    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])

    # 셀 안 숫자 표시
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, cm[i, j], ha="center", va="center")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
    plt.show()


# ============================================================
# 6) Chart 2 — Predicted Probability Distribution
# ============================================================

def plot_probability_distribution(
    y_true: pd.Series,
    y_proba: pd.Series,
    save_path: str | None = None
) -> None:
    """
    실제 class별 예측 확률 분포를 시각화
    한국어 설명:
    - 실제 0 / 실제 1 그룹의 확률 분포가 잘 분리되는지 확인 가능
    - 모델이 애매한 예측을 많이 하는지 직관적으로 볼 수 있음
    """
    fig, ax = plt.subplots(figsize=(7, 4))

    proba_neg = y_proba[y_true == 0]
    proba_pos = y_proba[y_true == 1]

    ax.hist(proba_neg, bins=20, alpha=0.6, label="Actual 0")
    ax.hist(proba_pos, bins=20, alpha=0.6, label="Actual 1")

    ax.set_title("Predicted Probability Distribution")
    ax.set_xlabel("Predicted Probability (Positive Class)")
    ax.set_ylabel("Count")
    ax.legend()

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
    plt.show()


# ============================================================
# 7) Chart 3 — Metric Bar Chart
# ============================================================

def plot_metric_summary(
    results: Dict[str, Any],
    save_path: str | None = None
) -> None:
    """
    주요 metric을 bar chart로 시각화
    한국어 설명:
    - accuracy, precision, recall, f1, roc_auc를 한눈에 비교
    - 보고서용 summary chart로 적합
    """
    metric_names = ["accuracy", "precision", "recall", "f1_score", "roc_auc"]
    metric_values = [results[m] for m in metric_names]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(metric_names, metric_values)

    ax.set_title("Model Metric Summary")
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Score")

    # 막대 위 숫자 표시
    for bar, value in zip(bars, metric_values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.02,
            f"{value:.3f}",
            ha="center",
            va="bottom"
        )

    plt.xticks(rotation=20)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
    plt.show()


# ============================================================
# 8) Main
# ============================================================

def main() -> None:
    cfg = VisualReportConfig(
        test_size=0.2,
        random_state=42,
        threshold=0.5,
        save_dir="reports",
    )

    # 1) 데이터 준비
    X, y = load_demo_data(random_state=cfg.random_state)
    X_train, X_test, y_train, y_test = split_data(X, y, cfg)

    # 2) 모델 학습
    model = build_model(random_state=cfg.random_state)
    model.fit(X_train, y_train)

    # 3) 평가
    results = evaluate_model(
        model=model,
        X_test=X_test,
        y_test=y_test,
        threshold=cfg.threshold,
    )

    # 4) metric 출력
    print("=== Metric Summary ===")
    print(f"Accuracy : {results['accuracy']:.4f}")
    print(f"Precision: {results['precision']:.4f}")
    print(f"Recall   : {results['recall']:.4f}")
    print(f"F1 Score : {results['f1_score']:.4f}")
    print(f"ROC AUC  : {results['roc_auc']:.4f}")

    # 5) 시각화
    plot_confusion_matrix(results["confusion_matrix"])
    plot_probability_distribution(results["y_true"], results["y_proba"])
    plot_metric_summary(results)


if __name__ == "__main__":
    main()