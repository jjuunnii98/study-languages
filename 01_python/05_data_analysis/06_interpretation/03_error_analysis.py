"""
Day 68 — Error Analysis
File: 01_python/05_data_analysis/06_interpretation/03_error_analysis.py

목표
- 모델이 "얼마나 잘 맞는가"를 넘어서, "어디서 틀리는가"를 구조적으로 분석한다.
- 오분류를 세그먼트/구간/확신도(confidence) 기준으로 나누어 본다.
- 향후 개선 방향(feature engineering, threshold tuning, re-sampling, data collection)을 찾는 근거를 만든다.

핵심 질문
1) 어떤 유형의 샘플에서 오분류가 많이 발생하는가?
2) 특정 feature 구간(예: income 낮음, age 높음)에서 성능이 나쁜가?
3) 특정 categorical segment(예: region='etc')에서 오류율이 높은가?
4) 모델이 "확신하고 틀리는" 위험한 사례가 있는가?
5) FN(False Negative) / FP(False Positive)가 각각 어떤 패턴을 가지는가?

실무 포인트
- Error analysis는 단순 디버깅이 아니라 모델 개선의 출발점이다.
- 성능 지표만 봐서는 절대 알 수 없는 "구조적 약점"을 발견할 수 있다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ============================================================
# 0) Config
# ============================================================

@dataclass(frozen=True)
class ErrorAnalysisConfig:
    test_size: float = 0.2
    random_state: int = 42
    threshold: float = 0.5
    top_n_confident_errors: int = 10


# ============================================================
# 1) Demo Data
# ============================================================

def load_demo_dataset(random_state: int = 42) -> Tuple[pd.DataFrame, pd.Series]:
    """
    실습용 classification 데이터 생성.
    - numeric + categorical feature 혼합
    - error analysis에서 segment/grouping을 해볼 수 있도록 region 추가
    """
    X_num, y = make_classification(
        n_samples=1800,
        n_features=6,
        n_informative=4,
        n_redundant=1,
        n_classes=2,
        weights=[0.72, 0.28],
        flip_y=0.03,
        class_sep=1.0,
        random_state=random_state,
    )

    df = pd.DataFrame(X_num, columns=[
        "age_signal",
        "income_signal",
        "usage_signal",
        "risk_signal",
        "noise_1",
        "noise_2",
    ])

    # 해석 쉬운 컬럼으로 이름과 분포를 조금 다듬음
    rng = np.random.default_rng(random_state)
    df["age"] = (40 + df["age_signal"] * 10).clip(18, 80).round(0)
    df["income"] = np.exp(10 + df["income_signal"] * 0.25)
    df["monthly_usage"] = (50 + df["usage_signal"] * 15).clip(0, None)
    df["risk_score"] = (50 + df["risk_signal"] * 12).clip(0, 100)

    # category feature 추가
    df["region"] = rng.choice(["seoul", "busan", "daegu", "etc"], size=len(df), p=[0.42, 0.23, 0.15, 0.20])
    df["channel"] = rng.choice(["web", "app"], size=len(df), p=[0.45, 0.55])

    # 원본 신호 컬럼 정리 (분석용 컬럼만 남김)
    df = df[["age", "income", "monthly_usage", "risk_score", "region", "channel"]]

    y_sr = pd.Series(y, name="target")
    return df, y_sr


# ============================================================
# 2) Split
# ============================================================

def split_data(X: pd.DataFrame, y: pd.Series, cfg: ErrorAnalysisConfig):
    """
    분류 문제이므로 stratify 적용
    """
    return train_test_split(
        X,
        y,
        test_size=cfg.test_size,
        random_state=cfg.random_state,
        stratify=y,
    )


# ============================================================
# 3) Build Model (leakage-safe pipeline)
# ============================================================

def build_model() -> Pipeline:
    """
    numeric + categorical 혼합 데이터를 처리하기 위한 Pipeline
    - numeric: StandardScaler
    - categorical: OneHotEncoder
    - model: LogisticRegression

    한국어 설명:
    전처리를 Pipeline 안에 넣어야 train/test 누수를 방지할 수 있다.
    """
    numeric_cols = ["age", "income", "monthly_usage", "risk_score"]
    categorical_cols = ["region", "channel"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )

    return model


# ============================================================
# 4) Prediction Result Table
# ============================================================

def build_prediction_frame(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    threshold: float = 0.5,
) -> pd.DataFrame:
    """
    예측 결과를 한 테이블로 정리한다.

    포함 컬럼:
    - 원본 feature
    - y_true
    - y_pred
    - y_proba
    - is_error
    - error_type (FP/FN/CORRECT)
    - confidence
    """
    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)

    result = X_test.copy().reset_index(drop=True)
    result["y_true"] = y_test.reset_index(drop=True)
    result["y_pred"] = y_pred
    result["y_proba"] = y_proba
    result["is_error"] = (result["y_true"] != result["y_pred"]).astype(int)

    # error type 구분
    def _error_type(row):
        if row["y_true"] == row["y_pred"]:
            return "CORRECT"
        if row["y_true"] == 0 and row["y_pred"] == 1:
            return "FP"
        return "FN"

    result["error_type"] = result.apply(_error_type, axis=1)

    # 모델의 확신도(confidence)
    # 예측한 클래스 기준 확률로 정의
    result["confidence"] = np.where(result["y_pred"] == 1, result["y_proba"], 1 - result["y_proba"])

    return result


# ============================================================
# 5) Segment-Level Error Analysis
# ============================================================

def error_rate_by_segment(df_pred: pd.DataFrame, segment_col: str) -> pd.DataFrame:
    """
    범주형 세그먼트별 오류율 분석

    예:
    - region별 오류율
    - channel별 오류율
    """
    grouped = (
        df_pred
        .groupby(segment_col, observed=False)
        .agg(
            n=("is_error", "size"),
            error_count=("is_error", "sum"),
            error_rate=("is_error", "mean"),
            positive_rate=("y_true", "mean"),
            avg_confidence=("confidence", "mean"),
        )
        .reset_index()
        .sort_values("error_rate", ascending=False)
    )
    return grouped


# ============================================================
# 6) Numeric-Bin Error Analysis
# ============================================================

def error_rate_by_numeric_bin(
    df_pred: pd.DataFrame,
    numeric_col: str,
    bins: int = 5,
) -> pd.DataFrame:
    """
    수치형 feature를 구간(bin)으로 나눠 오류율을 본다.

    예:
    - income 구간별 오류율
    - risk_score 구간별 오류율

    한국어 설명:
    특정 구간에서 오류율이 튀면 feature engineering이나 threshold 조정 힌트가 된다.
    """
    temp = df_pred.copy()
    temp[f"{numeric_col}_bin"] = pd.qcut(temp[numeric_col], q=bins, duplicates="drop")

    grouped = (
        temp
        .groupby(f"{numeric_col}_bin", observed=False)
        .agg(
            n=("is_error", "size"),
            error_count=("is_error", "sum"),
            error_rate=("is_error", "mean"),
            avg_target=("y_true", "mean"),
            avg_pred_proba=("y_proba", "mean"),
        )
        .reset_index()
        .sort_values("error_rate", ascending=False)
    )

    return grouped


# ============================================================
# 7) Confident Error Cases
# ============================================================

def top_confident_errors(
    df_pred: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:
    """
    모델이 "확신하고 틀린" 위험한 사례를 추출
    - confidence 높은 오답은 특히 중요한 점검 대상
    """
    errors = df_pred[df_pred["is_error"] == 1].copy()
    errors = errors.sort_values("confidence", ascending=False)
    return errors.head(top_n)


# ============================================================
# 8) FP / FN Pattern Summary
# ============================================================

def error_type_summary(df_pred: pd.DataFrame) -> pd.DataFrame:
    """
    FP / FN / CORRECT 개수 및 비율 요약
    """
    summary = (
        df_pred["error_type"]
        .value_counts(normalize=False)
        .rename_axis("error_type")
        .reset_index(name="count")
    )
    summary["ratio"] = summary["count"] / summary["count"].sum()
    return summary


# ============================================================
# 9) Main
# ============================================================

def main() -> None:
    cfg = ErrorAnalysisConfig(
        test_size=0.2,
        random_state=42,
        threshold=0.5,
        top_n_confident_errors=10,
    )

    # 1) 데이터 준비
    X, y = load_demo_dataset(random_state=cfg.random_state)
    X_train, X_test, y_train, y_test = split_data(X, y, cfg)

    # 2) 모델 학습
    model = build_model()
    model.fit(X_train, y_train)

    # 3) 기본 성능 확인
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("\n=== Basic Test Performance ===")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # 4) 예측 프레임 생성
    df_pred = build_prediction_frame(model, X_test, y_test, threshold=cfg.threshold)

    # 5) 에러 타입 요약
    print("\n=== Error Type Summary ===")
    print(error_type_summary(df_pred).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # 6) 세그먼트별 오류율
    print("\n=== Error Rate by Region ===")
    print(error_rate_by_segment(df_pred, "region").to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n=== Error Rate by Channel ===")
    print(error_rate_by_segment(df_pred, "channel").to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # 7) 수치형 구간별 오류율
    print("\n=== Error Rate by Income Bin ===")
    print(error_rate_by_numeric_bin(df_pred, "income", bins=5).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n=== Error Rate by Risk Score Bin ===")
    print(error_rate_by_numeric_bin(df_pred, "risk_score", bins=5).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # 8) 확신하고 틀린 사례
    print("\n=== Top Confident Errors ===")
    print(
        top_confident_errors(df_pred, top_n=cfg.top_n_confident_errors)
        .to_string(index=False, float_format=lambda x: f"{x:.4f}")
    )

    # 9) 해석 가이드
    print("\n=== Interpretation Guide ===")
    print("- 특정 region에서 error_rate가 높으면 세그먼트 편향 가능성을 의심할 수 있다.")
    print("- 특정 numeric bin에서 오류율이 높으면 feature transformation / binning / interaction feature를 고려할 수 있다.")
    print("- FN이 많으면 recall 개선이 필요하고, FP가 많으면 precision 개선이나 threshold 조정이 필요할 수 있다.")
    print("- confidence가 높은 오답은 모델이 잘못된 패턴을 '강하게' 학습했을 가능성이 있으므로 우선 점검 대상이다.")


if __name__ == "__main__":
    main()