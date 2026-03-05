"""
Day 62 — Train/Test Split (Modeling Basics)
File: 01_python/05_data_analysis/05_modeling_basics/01_train_test_split.py

목표(실무 관점)
- 모델링의 첫 단추는 "정확한 데이터 분리"다.
- Train/Test split을 올바르게 하지 않으면 데이터 누수(leakage)로 성능이 과대평가된다.
- 이 파일은 다음을 '코드로 증명'한다:
  1) 랜덤 시드 기반 재현성(reproducibility)
  2) stratify를 통한 클래스 분포 유지(class balance)
  3) 시간 데이터(time series)에서는 shuffle 금지
  4) 전처리/스케일링/인코딩은 "train 기준으로 fit" 후 test에 transform (누수 방지)
  5) 스플릿 결과 리포팅(분포/크기/기초 검증)

주의
- 이 파일은 데이터셋이 어떤 형태든 적용 가능하게 "템플릿" 형태로 작성되었다.
- 실제 프로젝트에서는 아래 load_data()를 실데이터 로딩으로 교체하면 된다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ============================================================
# 0) Config (실무에서는 설정을 명시적으로 관리)
# ============================================================

@dataclass(frozen=True)
class SplitConfig:
    test_size: float = 0.2
    random_state: int = 42
    stratify: bool = True            # 분류 문제에서 라벨 분포 유지
    shuffle: bool = True             # 시계열이면 False
    target_col: str = "target"       # 타깃 컬럼명
    time_col: Optional[str] = None   # 시계열 분할 시 사용할 시간 컬럼(선택)


# ============================================================
# 1) Data Loading (데모용) — 실제 데이터 로딩으로 교체
# ============================================================

def load_data_demo(n: int = 1000, random_state: int = 42) -> pd.DataFrame:
    """
    데모 데이터 생성 함수.
    - 분류 문제를 가정(불균형 타깃)
    - numeric feature + categorical feature 흉내
    """
    rng = np.random.default_rng(random_state)

    df = pd.DataFrame({
        "age": rng.normal(40, 12, size=n).clip(18, 80).round(0),
        "income": rng.lognormal(mean=10.0, sigma=0.4, size=n),
        "region": rng.choice(["seoul", "busan", "daegu", "etc"], size=n, p=[0.4, 0.2, 0.15, 0.25]),
    })

    # 불균형한 타깃 생성(예: positive 약 15%)
    # income과 age가 조금 영향을 주도록
    score = 0.015 * (df["age"] - 40) + 0.000002 * (df["income"] - df["income"].median())
    prob = 1 / (1 + np.exp(-score))
    df["target"] = (rng.random(n) < (0.15 + 0.25 * (prob - prob.mean()))).astype(int)

    return df


# ============================================================
# 2) Split Utilities
# ============================================================

def split_tabular(
    df: pd.DataFrame,
    cfg: SplitConfig
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    일반(tabular) 데이터의 train/test 분리.
    - 분류 문제라면 stratify를 적극 권장(타깃 분포 유지)
    - 실무에서는 "ID" 기반으로 누수 방지(사용자 단위 분리 등)도 고려해야 함
    """
    if cfg.target_col not in df.columns:
        raise ValueError(f"target_col='{cfg.target_col}' not found in columns")

    X = df.drop(columns=[cfg.target_col])
    y = df[cfg.target_col]

    stratify_y = y if cfg.stratify else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=cfg.test_size,
        random_state=cfg.random_state,
        stratify=stratify_y,
        shuffle=cfg.shuffle,
    )
    return X_train, X_test, y_train, y_test


def split_time_series(
    df: pd.DataFrame,
    cfg: SplitConfig
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    시계열(Time Series) 데이터 분리:
    - 가장 기본 원칙: "과거로 학습 → 미래로 평가"
    - shuffle=False가 핵심
    - 간단하게 time_col 기준 정렬 후 마지막 test_size 비율을 test로 분리
    """
    if cfg.time_col is None:
        raise ValueError("time_col must be provided for time series split")
    if cfg.time_col not in df.columns:
        raise ValueError(f"time_col='{cfg.time_col}' not found in columns")
    if cfg.target_col not in df.columns:
        raise ValueError(f"target_col='{cfg.target_col}' not found in columns")

    df_sorted = df.sort_values(cfg.time_col).reset_index(drop=True)

    n = len(df_sorted)
    n_test = int(np.ceil(n * cfg.test_size))
    split_idx = n - n_test

    train_df = df_sorted.iloc[:split_idx].copy()
    test_df = df_sorted.iloc[split_idx:].copy()

    X_train = train_df.drop(columns=[cfg.target_col])
    y_train = train_df[cfg.target_col]
    X_test = test_df.drop(columns=[cfg.target_col])
    y_test = test_df[cfg.target_col]

    return X_train, X_test, y_train, y_test


# ============================================================
# 3) Leakage-Safe Preprocessing Example
# ============================================================

def scale_numeric_leakage_safe(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    numeric_cols: List[str]
) -> Tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
    """
    누수 방지 스케일링 예시:
    - scaler.fit은 train에만!
    - test에는 scaler.transform만 적용!
    """
    scaler = StandardScaler()

    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()

    # 한국어 핵심: "fit은 train, transform은 둘 다"
    X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])

    return X_train_scaled, X_test_scaled, scaler


# ============================================================
# 4) Reporting
# ============================================================

def report_split(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series
) -> None:
    """
    스플릿 결과 리포트(실무에서 꼭 하는 기본 점검)
    - shape
    - 타깃 분포(분류) 확인
    - 결측치/기초 통계는 EDA/cleaning 단계에서 이미 했다는 가정
    """
    print("\n=== Split Report ===")
    print(f"X_train: {X_train.shape} | y_train: {y_train.shape}")
    print(f"X_test : {X_test.shape} | y_test : {y_test.shape}")

    # 분류 타깃이라면 클래스 비율 확인 (stratify가 잘 됐는지)
    if set(y_train.unique()).issubset({0, 1}) and set(y_test.unique()).issubset({0, 1}):
        train_pos = float(y_train.mean())
        test_pos = float(y_test.mean())
        print(f"Target positive rate (train): {train_pos:.4f}")
        print(f"Target positive rate (test) : {test_pos:.4f}")

    # 샘플 확인
    print("\nSample rows (train):")
    print(pd.concat([X_train.head(3), y_train.head(3)], axis=1))
    print("\nSample rows (test):")
    print(pd.concat([X_test.head(3), y_test.head(3)], axis=1))


# ============================================================
# 5) Main (데모 실행)
# ============================================================

def main() -> None:
    # 1) 데이터 준비(데모)
    df = load_data_demo(n=1000, random_state=42)

    # 2) 설정
    cfg = SplitConfig(
        test_size=0.2,
        random_state=42,
        stratify=True,     # 분류면 True 권장
        shuffle=True,      # 시계열이면 False
        target_col="target",
        time_col=None
    )

    # 3) 분할
    X_train, X_test, y_train, y_test = split_tabular(df, cfg)

    # 4) 누수 방지 전처리(예: numeric scaling)
    numeric_cols = ["age", "income"]
    X_train_s, X_test_s, _ = scale_numeric_leakage_safe(X_train, X_test, numeric_cols)

    # 5) 리포트
    report_split(X_train_s, X_test_s, y_train, y_test)


if __name__ == "__main__":
    main()