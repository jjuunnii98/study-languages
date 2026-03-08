"""
Day 65 — Cross Validation
File: 01_python/05_data_analysis/05_modeling_basics/04_cross_validation.py

목표
- 단일 train/test split만으로는 성능 추정이 불안정할 수 있다는 점을 이해한다.
- Cross Validation(CV)을 통해 모델 성능의 평균적 일반화 능력을 평가한다.
- fold별 score, 평균(mean), 표준편차(std)를 보고 모델의 안정성을 해석한다.
- 데이터 누수(leakage)를 막기 위해 전처리까지 Pipeline 안에 넣는 구조를 사용한다.

핵심 개념
1) Hold-out split
   - train / test 한 번만 나눔
   - 간단하지만 split 운에 따라 성능이 흔들릴 수 있음

2) K-Fold Cross Validation
   - 데이터를 K개로 나누고
   - 각 fold를 번갈아 validation으로 사용
   - 평균 성능을 계산

3) Stratified K-Fold
   - 분류 문제에서 클래스 비율을 각 fold에 최대한 유지
   - 불균형 데이터에서 중요

4) Pipeline + CV
   - 스케일링 같은 전처리를 fold 내부에서만 fit하도록 보장
   - 누수 방지의 핵심 구조

실무 포인트
- CV mean이 높아도 std가 너무 크면 불안정한 모델일 수 있다.
- 모델 선택 시 "성능 평균"과 "성능 변동성"을 함께 봐야 한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

import numpy as np
import pandas as pd

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, f1_score
from sklearn.model_selection import (
    StratifiedKFold,
    cross_validate,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ============================================================
# 0) Config
# ============================================================

@dataclass(frozen=True)
class CVConfig:
    n_splits: int = 5
    shuffle: bool = True
    random_state: int = 42
    test_size: float = 0.2


# ============================================================
# 1) Demo Data
# ============================================================

def load_demo_data(random_state: int = 42) -> tuple[pd.DataFrame, pd.Series]:
    """
    실습용 이진 분류 데이터 생성.
    - 약간의 클래스 불균형 포함
    - CV에서 stratification 필요성을 보여주기 좋음
    """
    X, y = make_classification(
        n_samples=1500,
        n_features=14,
        n_informative=7,
        n_redundant=3,
        n_classes=2,
        weights=[0.72, 0.28],
        flip_y=0.02,
        class_sep=1.0,
        random_state=random_state,
    )

    feature_names = [f"feature_{i}" for i in range(X.shape[1])]
    X_df = pd.DataFrame(X, columns=feature_names)
    y_sr = pd.Series(y, name="target")

    return X_df, y_sr


# ============================================================
# 2) Build Leakage-Safe Pipeline
# ============================================================

def build_pipeline(random_state: int = 42) -> Pipeline:
    """
    누수 방지 구조:
    - StandardScaler를 Pipeline 안에 넣으면
      각 fold의 train 부분에서만 fit이 일어난다.
    - CV에서 전처리를 Pipeline 밖에서 미리 해버리면 leakage 위험이 생길 수 있다.
    """
    pipe = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000, random_state=random_state)),
        ]
    )
    return pipe


# ============================================================
# 3) Cross Validation
# ============================================================

def run_cross_validation(
    X: pd.DataFrame,
    y: pd.Series,
    cfg: CVConfig,
) -> Dict[str, Any]:
    """
    Stratified K-Fold Cross Validation 실행.

    평가 지표:
    - accuracy
    - precision
    - recall
    - f1
    - roc_auc

    반환값:
    - fold별 score
    - 평균 / 표준편차
    """
    cv = StratifiedKFold(
        n_splits=cfg.n_splits,
        shuffle=cfg.shuffle,
        random_state=cfg.random_state,
    )

    pipeline = build_pipeline(random_state=cfg.random_state)

    scoring = {
        "accuracy": "accuracy",
        "precision": "precision",
        "recall": "recall",
        "f1": make_scorer(f1_score),
        "roc_auc": "roc_auc",
    }

    results = cross_validate(
        estimator=pipeline,
        X=X,
        y=y,
        cv=cv,
        scoring=scoring,
        return_train_score=True,   # train score도 같이 받아서 과적합 힌트 확인
        n_jobs=-1,
    )

    return results


# ============================================================
# 4) Report
# ============================================================

def summarize_cv_results(results: Dict[str, Any]) -> pd.DataFrame:
    """
    cross_validate 결과를 보기 좋은 summary DataFrame으로 정리.
    """
    rows = []

    metrics = ["accuracy", "precision", "recall", "f1", "roc_auc"]

    for metric in metrics:
        test_scores = results[f"test_{metric}"]
        train_scores = results[f"train_{metric}"]

        rows.append(
            {
                "metric": metric,
                "train_mean": np.mean(train_scores),
                "train_std": np.std(train_scores),
                "test_mean": np.mean(test_scores),
                "test_std": np.std(test_scores),
            }
        )

    summary = pd.DataFrame(rows)
    return summary


def print_fold_scores(results: Dict[str, Any]) -> None:
    """
    fold별 성능 출력.
    - 평균만 보면 hidden instability를 놓칠 수 있으므로
      fold별 성능 분산을 같이 보는 습관이 중요하다.
    """
    print("\n=== Fold-by-Fold Test Scores ===")

    metrics = ["accuracy", "precision", "recall", "f1", "roc_auc"]

    for metric in metrics:
        scores = results[f"test_{metric}"]
        scores_fmt = ", ".join([f"{s:.4f}" for s in scores])
        print(f"{metric:10s}: [{scores_fmt}]")


def explain_cv_interpretation() -> None:
    """
    CV 결과 해석 가이드
    """
    print("\n=== CV Interpretation Guide ===")
    print("- test_mean ↑  : 평균 성능이 좋다")
    print("- test_std ↓   : fold 간 성능 변동이 작아 안정적이다")
    print("- train_mean >> test_mean : 과적합(overfitting) 가능성")
    print("- precision/recall trade-off는 문제의 비용 구조에 따라 해석해야 한다")
    print("- CV는 hold-out보다 더 안정적인 성능 추정 방법이다")


# ============================================================
# 5) Optional Hold-out Comparison
# ============================================================

def compare_with_single_split(
    X: pd.DataFrame,
    y: pd.Series,
    cfg: CVConfig
) -> None:
    """
    단일 split과 CV의 차이를 직관적으로 보기 위한 비교 함수.
    - hold-out은 split 운에 따라 결과가 흔들릴 수 있다.
    """
    from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=cfg.test_size,
        stratify=y,
        random_state=cfg.random_state,
    )

    pipe = build_pipeline(random_state=cfg.random_state)
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    y_prob = pipe.predict_proba(X_test)[:, 1]

    print("\n=== Single Hold-out Split Comparison ===")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"F1 Score: {f1_score(y_test, y_pred):.4f}")
    print(f"ROC AUC : {roc_auc_score(y_test, y_prob):.4f}")
    print("→ 단일 split 결과는 참고용이며, CV 평균보다 더 불안정할 수 있다.")


# ============================================================
# 6) Main
# ============================================================

def main() -> None:
    cfg = CVConfig(
        n_splits=5,
        shuffle=True,
        random_state=42,
        test_size=0.2,
    )

    # 1) 데이터 준비
    X, y = load_demo_data(random_state=cfg.random_state)

    # 2) Cross Validation 실행
    results = run_cross_validation(X, y, cfg)

    # 3) fold별 점수 출력
    print_fold_scores(results)

    # 4) summary 출력
    summary = summarize_cv_results(results)
    print("\n=== Cross Validation Summary ===")
    print(summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # 5) 해석 가이드
    explain_cv_interpretation()

    # 6) 참고용 hold-out 비교
    compare_with_single_split(X, y, cfg)


if __name__ == "__main__":
    main()