"""
Day 67 — Model Diagnostics
File: 01_python/05_data_analysis/06_interpretation/02_model_diagnostics.py

목표
- 모델이 "얼마나 잘 맞추는가"를 넘어서,
  "어디서 / 왜 / 어떻게 실패하는가"를 진단한다.
- train/test 성능 차이, 예측 확률 분포, 오분류 샘플을 함께 살펴본다.
- 모델 디버깅 관점에서 재사용 가능한 진단 템플릿을 만든다.

핵심 진단 포인트
1) Train vs Test 성능 비교
   - train 성능이 지나치게 높고 test 성능이 낮으면 과적합 가능성

2) Confusion Matrix
   - 어떤 오류(FP/FN)가 많은지 확인

3) Probability Diagnostics
   - 모델이 예측 확률을 너무 극단적으로 주는가?
   - positive / negative 클래스의 확률 분포가 잘 분리되는가?

4) Error Inspection
   - 오분류 샘플을 직접 확인
   - 어떤 feature 패턴에서 자주 틀리는지 탐색

5) Calibration-like Check
   - 확률 구간(bin)별 실제 정답률을 비교
   - 예: 0.8 확률 예측이면 실제로도 80% 정도 맞는가?

실무 포인트
- 모델 평가는 숫자 하나가 아니라 "진단 세트"로 봐야 한다.
- diagnostics 단계가 있어야 feature engineering / threshold tuning / model 변경 방향이 보인다.
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
class DiagnosticConfig:
    test_size: float = 0.2
    random_state: int = 42
    threshold: float = 0.5
    calibration_bins: int = 10
    top_error_rows: int = 10


# ============================================================
# 1) Demo Data
# ============================================================

def load_demo_data(random_state: int = 42) -> Tuple[pd.DataFrame, pd.Series]:
    """
    진단 실습용 분류 데이터 생성.
    - 약간의 클래스 불균형 포함
    - 일부 feature만 informative하게 설정
    """
    X, y = make_classification(
        n_samples=1500,
        n_features=10,
        n_informative=5,
        n_redundant=2,
        n_repeated=0,
        n_classes=2,
        weights=[0.7, 0.3],
        flip_y=0.03,
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
    cfg: DiagnosticConfig
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    분류 문제이므로 stratify로 클래스 비율 유지
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=cfg.test_size,
        random_state=cfg.random_state,
        stratify=y,
    )
    return X_train, X_test, y_train, y_test


# ============================================================
# 3) Train Model (Leakage-safe Pipeline)
# ============================================================

def build_and_train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    random_state: int = 42
) -> Pipeline:
    """
    누수 방지:
    - 스케일링을 Pipeline 안에 넣는다.
    - train에서만 fit되고, test에는 transform만 적용됨
    """
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000, random_state=random_state)),
        ]
    )

    model.fit(X_train, y_train)
    return model


# ============================================================
# 4) Basic Evaluation
# ============================================================

def evaluate_split(
    model: Pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    threshold: float = 0.5
) -> Dict[str, Any]:
    """
    단일 split(train or test)에 대한 성능 평가
    """
    y_proba = model.predict_proba(X)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)

    return {
        "accuracy": accuracy_score(y, y_pred),
        "precision": precision_score(y, y_pred, zero_division=0),
        "recall": recall_score(y, y_pred, zero_division=0),
        "f1": f1_score(y, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y, y_proba),
        "confusion_matrix": confusion_matrix(y, y_pred),
        "y_pred": y_pred,
        "y_proba": y_proba,
    }


# ============================================================
# 5) Train vs Test Gap Diagnostics
# ============================================================

def compare_train_test_performance(
    train_metrics: Dict[str, Any],
    test_metrics: Dict[str, Any]
) -> pd.DataFrame:
    """
    train/test 성능 차이를 표로 정리
    - gap이 크면 과적합 가능성
    """
    rows = []
    for metric in ["accuracy", "precision", "recall", "f1", "roc_auc"]:
        rows.append({
            "metric": metric,
            "train_score": train_metrics[metric],
            "test_score": test_metrics[metric],
            "gap_train_minus_test": train_metrics[metric] - test_metrics[metric],
        })
    return pd.DataFrame(rows)


# ============================================================
# 6) Probability Diagnostics
# ============================================================

def probability_summary(y_true: pd.Series, y_proba: np.ndarray) -> pd.DataFrame:
    """
    예측 확률 분포 요약
    - 실제 positive / negative 각각에서 확률이 어떻게 분포하는지 확인
    """
    df = pd.DataFrame({
        "y_true": y_true.values,
        "y_proba": y_proba,
    })

    summary_rows = []
    for label in [0, 1]:
        subset = df[df["y_true"] == label]["y_proba"]
        summary_rows.append({
            "actual_class": label,
            "count": len(subset),
            "mean_proba": subset.mean(),
            "std_proba": subset.std(),
            "min_proba": subset.min(),
            "p25": subset.quantile(0.25),
            "median": subset.median(),
            "p75": subset.quantile(0.75),
            "max_proba": subset.max(),
        })

    return pd.DataFrame(summary_rows)


def calibration_like_table(
    y_true: pd.Series,
    y_proba: np.ndarray,
    n_bins: int = 10
) -> pd.DataFrame:
    """
    간단한 calibration 관찰용 테이블
    - 확률 구간별 평균 예측 확률 vs 실제 positive rate 비교

    주의:
    - 이건 정식 calibration curve plotting은 아니고
      텍스트 기반 진단용 테이블이다.
    """
    df = pd.DataFrame({
        "y_true": y_true.values,
        "y_proba": y_proba,
    })

    # 0~1 구간을 균등 분할
    df["prob_bin"] = pd.cut(df["y_proba"], bins=np.linspace(0, 1, n_bins + 1), include_lowest=True)

    grouped = df.groupby("prob_bin", observed=False).agg(
        count=("y_true", "size"),
        avg_pred_proba=("y_proba", "mean"),
        actual_positive_rate=("y_true", "mean"),
    ).reset_index()

    return grouped


# ============================================================
# 7) Error Inspection
# ============================================================

def collect_error_cases(
    X: pd.DataFrame,
    y_true: pd.Series,
    y_pred: np.ndarray,
    y_proba: np.ndarray,
    top_n: int = 10
) -> pd.DataFrame:
    """
    오분류 샘플 수집
    - 어떤 사례에서 틀렸는지 직접 보는 것이 diagnostics의 핵심
    - 확률까지 같이 보면 '확신하고 틀렸는지'도 알 수 있다.
    """
    result = X.copy()
    result["y_true"] = y_true.values
    result["y_pred"] = y_pred
    result["y_proba"] = y_proba
    result["is_error"] = (result["y_true"] != result["y_pred"]).astype(int)

    errors = result[result["is_error"] == 1].copy()

    # 확신이 큰 오답을 먼저 보기 위해
    # 실제 0인데 높은 확률로 1 예측 / 실제 1인데 낮은 확률로 0 예측
    errors["error_confidence"] = np.where(
        errors["y_pred"] == 1,
        errors["y_proba"],
        1 - errors["y_proba"]
    )

    errors = errors.sort_values("error_confidence", ascending=False)
    return errors.head(top_n)


# ============================================================
# 8) Print Report
# ============================================================

def print_metrics(title: str, metrics: Dict[str, Any]) -> None:
    print(f"\n=== {title} ===")
    print(f"Accuracy : {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall   : {metrics['recall']:.4f}")
    print(f"F1 Score : {metrics['f1']:.4f}")
    print(f"ROC AUC  : {metrics['roc_auc']:.4f}")
    print("Confusion Matrix:")
    print(metrics["confusion_matrix"])


def explain_diagnostics() -> None:
    print("\n=== Diagnostics Interpretation Guide ===")
    print("- train 성능이 높고 test 성능이 낮으면 과적합 신호일 수 있다.")
    print("- FN이 많으면 recall 개선이 필요할 수 있다.")
    print("- FP가 많으면 precision 개선 또는 threshold 상향 조정이 필요할 수 있다.")
    print("- 예측 확률 분포가 잘 분리되지 않으면 feature engineering이 필요할 수 있다.")
    print("- calibration-like table에서 avg_pred_proba와 actual_positive_rate 차이가 크면 확률 보정이 필요할 수 있다.")


# ============================================================
# 9) Main
# ============================================================

def main() -> None:
    cfg = DiagnosticConfig(
        test_size=0.2,
        random_state=42,
        threshold=0.5,
        calibration_bins=10,
        top_error_rows=10,
    )

    # 1) 데이터 로드
    X, y = load_demo_data(random_state=cfg.random_state)

    # 2) split
    X_train, X_test, y_train, y_test = split_data(X, y, cfg)

    # 3) 모델 학습
    model = build_and_train_model(X_train, y_train, random_state=cfg.random_state)

    # 4) train/test 평가
    train_metrics = evaluate_split(model, X_train, y_train, threshold=cfg.threshold)
    test_metrics = evaluate_split(model, X_test, y_test, threshold=cfg.threshold)

    # 5) 기본 성능 출력
    print_metrics("Train Performance", train_metrics)
    print_metrics("Test Performance", test_metrics)

    # 6) train/test gap
    gap_df = compare_train_test_performance(train_metrics, test_metrics)
    print("\n=== Train vs Test Gap ===")
    print(gap_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # 7) probability diagnostics
    prob_df = probability_summary(y_test, test_metrics["y_proba"])
    print("\n=== Probability Summary (Test) ===")
    print(prob_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # 8) calibration-like table
    calib_df = calibration_like_table(
        y_true=y_test,
        y_proba=test_metrics["y_proba"],
        n_bins=cfg.calibration_bins,
    )
    print("\n=== Calibration-like Table (Test) ===")
    print(calib_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # 9) error inspection
    error_df = collect_error_cases(
        X=X_test,
        y_true=y_test,
        y_pred=test_metrics["y_pred"],
        y_proba=test_metrics["y_proba"],
        top_n=cfg.top_error_rows,
    )
    print("\n=== Top Error Cases (Test) ===")
    print(error_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # 10) interpretation guide
    explain_diagnostics()


if __name__ == "__main__":
    main()