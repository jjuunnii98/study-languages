"""
Day 69 — Result Summary
File: 01_python/05_data_analysis/07_reporting/01_result_summary.py

목표
- 모델 결과를 단순 숫자 나열이 아니라 "보고 가능한 형태"로 요약한다.
- 실무에서는 모델 성능을 계산하는 것만큼,
  결과를 명확하게 정리해서 전달하는 것이 중요하다.
- 이 파일은 classification baseline 결과를
  summary table + text report 형태로 정리하는 예시를 보여준다.

핵심 포인트
1) metric 계산
2) confusion matrix 요약
3) 사람이 읽기 쉬운 result summary 생성
4) reporting-friendly DataFrame 구성
5) 해석 문장 자동 생성

실무 포인트
- 분석가는 결과를 "계산"하는 사람인 동시에
  결과를 "전달"하는 사람이어야 한다.
- 보고서는 숫자 + 해석 + 맥락이 함께 있어야 한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Tuple

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
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ============================================================
# 0) Config
# ============================================================

@dataclass(frozen=True)
class ReportConfig:
    test_size: float = 0.2
    random_state: int = 42
    threshold: float = 0.5


# ============================================================
# 1) Demo Data
# ============================================================

def load_demo_data(random_state: int = 42) -> Tuple[pd.DataFrame, pd.Series]:
    """
    실습용 이진 분류 데이터 생성
    - reporting 예제이므로 적당한 크기의 데이터 사용
    """
    X, y = make_classification(
        n_samples=1200,
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
    cfg: ReportConfig
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
    baseline classification pipeline
    - scaler + logistic regression
    - 누수 방지를 위해 pipeline 사용
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
    classification 결과 평가
    - predict_proba()를 사용하여 threshold 기반 예측 생성
    """
    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    results = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
        "support_total": int(len(y_test)),
        "positive_rate_actual": float(y_test.mean()),
        "positive_rate_predicted": float(y_pred.mean()),
    }

    return results


# ============================================================
# 5) Build Summary Table
# ============================================================

def build_result_summary(results: Dict[str, Any]) -> pd.DataFrame:
    """
    주요 성능 지표를 reporting-friendly table로 변환
    """
    summary = pd.DataFrame(
        [
            {"metric": "accuracy", "value": results["accuracy"]},
            {"metric": "precision", "value": results["precision"]},
            {"metric": "recall", "value": results["recall"]},
            {"metric": "f1_score", "value": results["f1_score"]},
            {"metric": "roc_auc", "value": results["roc_auc"]},
            {"metric": "actual_positive_rate", "value": results["positive_rate_actual"]},
            {"metric": "predicted_positive_rate", "value": results["positive_rate_predicted"]},
        ]
    )
    return summary


def build_confusion_matrix_summary(results: Dict[str, Any]) -> pd.DataFrame:
    """
    confusion matrix를 별도 표로 정리
    """
    cm_summary = pd.DataFrame(
        [
            {"component": "true_negative", "count": results["tn"]},
            {"component": "false_positive", "count": results["fp"]},
            {"component": "false_negative", "count": results["fn"]},
            {"component": "true_positive", "count": results["tp"]},
        ]
    )
    return cm_summary


# ============================================================
# 6) Generate Narrative Report
# ============================================================

def generate_narrative_report(results: Dict[str, Any]) -> str:
    """
    숫자를 사람이 읽기 쉬운 해석 문장으로 바꾼다.
    실무에서는 이런 summary text가 매우 중요하다.
    """
    accuracy = results["accuracy"]
    precision = results["precision"]
    recall = results["recall"]
    f1 = results["f1_score"]
    auc = results["roc_auc"]
    fp = results["fp"]
    fn = results["fn"]

    lines = [
        "=== Model Result Summary ===",
        f"- The baseline classification model achieved an accuracy of {accuracy:.4f}.",
        f"- Precision was {precision:.4f}, indicating how reliable positive predictions were.",
        f"- Recall was {recall:.4f}, indicating how well the model captured actual positives.",
        f"- F1 score was {f1:.4f}, providing a balanced summary of precision and recall.",
        f"- ROC AUC was {auc:.4f}, representing the model's ranking performance across thresholds.",
        "",
        "=== Error Interpretation ===",
        f"- False Positives (FP): {fp}",
        f"- False Negatives (FN): {fn}",
    ]

    # 간단한 자동 해석 추가
    if recall < precision:
        lines.append("- The model appears to be more conservative: it misses some positives more often than it over-predicts them.")
    elif precision < recall:
        lines.append("- The model appears to be more aggressive in predicting positives: recall is relatively stronger than precision.")
    else:
        lines.append("- Precision and recall are relatively balanced.")

    if fn > fp:
        lines.append("- False negatives are more frequent than false positives, so recall improvement may be important.")
    elif fp > fn:
        lines.append("- False positives are more frequent than false negatives, so precision improvement may be important.")
    else:
        lines.append("- False positives and false negatives are balanced.")

    return "\n".join(lines)


# ============================================================
# 7) Print Reporting Output
# ============================================================

def print_report(
    summary_df: pd.DataFrame,
    cm_df: pd.DataFrame,
    narrative: str
) -> None:
    """
    콘솔 기준 reporting 출력
    """
    print("\n=== Metrics Summary Table ===")
    print(summary_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n=== Confusion Matrix Summary ===")
    print(cm_df.to_string(index=False))

    print("\n" + narrative)


# ============================================================
# 8) Main
# ============================================================

def main() -> None:
    cfg = ReportConfig(
        test_size=0.2,
        random_state=42,
        threshold=0.5,
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

    # 4) summary 생성
    summary_df = build_result_summary(results)
    cm_df = build_confusion_matrix_summary(results)
    narrative = generate_narrative_report(results)

    # 5) 출력
    print_report(summary_df, cm_df, narrative)


if __name__ == "__main__":
    main()