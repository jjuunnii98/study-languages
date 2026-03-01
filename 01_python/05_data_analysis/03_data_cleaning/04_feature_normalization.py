"""
Day 57 — Feature Normalization & Scaling
파일: 04_feature_normalization.py

목표:
- 모델링 전 feature scale을 안정화한다.
- 서로 다른 단위를 가진 변수(예: age vs income)를
  모델이 동일 선상에서 해석할 수 있도록 만든다.

핵심 기능:
1) Standard Scaling (Z-score)
2) Min-Max Scaling
3) Robust Scaling (median/IQR 기반)
4) Log Transformation
5) Yeo-Johnson Power Transform
6) fit / transform 분리 구조
7) 변환 리포트 생성

중요:
- 통계 기반 변환(mean/std 등)은 반드시 train에서 fit 후 test에 apply해야 한다.
- 이 파일은 실무형 transformer 구조를 반영한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import PowerTransformer


# ------------------------------------------------
# 1) 스케일링 정책 정의
# ------------------------------------------------

@dataclass
class NormalizationSpec:
    """
    normalization 설정 객체

    method:
        - "standard"
        - "minmax"
        - "robust"
        - "log"
        - "yeo_johnson"
    """
    method: str = "standard"
    columns: Optional[Iterable[str]] = None
    clip: bool = False
    clip_range: Tuple[float, float] = (-5.0, 5.0)


# ------------------------------------------------
# 2) Transformer 클래스 (fit/apply 구조)
# ------------------------------------------------

class FeatureNormalizer:

    def __init__(self, spec: NormalizationSpec):
        self.spec = spec
        self.params_: Dict[str, Dict[str, float]] = {}
        self.power_transformer_: Optional[PowerTransformer] = None

    # --------------------------------------------
    # fit 단계 (통계 계산)
    # --------------------------------------------
    def fit(self, df: pd.DataFrame):
        """
        학습 데이터에서 통계량을 계산한다.
        (mean/std, min/max, median/IQR 등)
        """

        cols = self._get_columns(df)

        if self.spec.method == "standard":
            for c in cols:
                self.params_[c] = {
                    "mean": df[c].mean(),
                    "std": df[c].std(ddof=0) or 1.0,
                }

        elif self.spec.method == "minmax":
            for c in cols:
                self.params_[c] = {
                    "min": df[c].min(),
                    "max": df[c].max(),
                }

        elif self.spec.method == "robust":
            for c in cols:
                q1 = df[c].quantile(0.25)
                q3 = df[c].quantile(0.75)
                iqr = q3 - q1 or 1.0
                self.params_[c] = {
                    "median": df[c].median(),
                    "iqr": iqr,
                }

        elif self.spec.method == "yeo_johnson":
            self.power_transformer_ = PowerTransformer(method="yeo-johnson")
            self.power_transformer_.fit(df[cols])

        # log는 fit 필요 없음

        return self

    # --------------------------------------------
    # transform 단계
    # --------------------------------------------
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        계산된 통계량을 기반으로 실제 변환 적용
        """

        df = df.copy()
        cols = self._get_columns(df)

        if self.spec.method == "standard":
            for c in cols:
                mean = self.params_[c]["mean"]
                std = self.params_[c]["std"]
                df[c] = (df[c] - mean) / std

        elif self.spec.method == "minmax":
            for c in cols:
                min_ = self.params_[c]["min"]
                max_ = self.params_[c]["max"]
                denom = (max_ - min_) or 1.0
                df[c] = (df[c] - min_) / denom

        elif self.spec.method == "robust":
            for c in cols:
                median = self.params_[c]["median"]
                iqr = self.params_[c]["iqr"]
                df[c] = (df[c] - median) / iqr

        elif self.spec.method == "log":
            for c in cols:
                # log1p는 0과 음수 처리에 상대적으로 안전
                df[c] = np.log1p(df[c].clip(lower=0))

        elif self.spec.method == "yeo_johnson":
            df[cols] = self.power_transformer_.transform(df[cols])

        # 선택적 클리핑
        if self.spec.clip:
            lo, hi = self.spec.clip_range
            df[cols] = df[cols].clip(lower=lo, upper=hi)

        return df

    # --------------------------------------------
    # fit + transform 한번에
    # --------------------------------------------
    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.fit(df).transform(df)

    # --------------------------------------------
    # 내부 유틸
    # --------------------------------------------
    def _get_columns(self, df: pd.DataFrame) -> List[str]:
        if self.spec.columns is not None:
            return [c for c in self.spec.columns if c in df.columns]
        return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]


# ------------------------------------------------
# 3) 리포트 함수
# ------------------------------------------------

def build_normalization_report(
    before: pd.DataFrame,
    after: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:
    """
    변환 전/후 통계 비교 리포트
    """

    rows = []
    for c in columns:
        rows.append({
            "column": c,
            "mean_before": before[c].mean(),
            "std_before": before[c].std(),
            "mean_after": after[c].mean(),
            "std_after": after[c].std(),
        })

    return pd.DataFrame(rows)


# ------------------------------------------------
# 4) 데모 실행
# ------------------------------------------------

def _demo():
    """
    외부 데이터 없이 실행 가능한 데모
    """

    rng = np.random.default_rng(42)
    df = pd.DataFrame({
        "age": rng.normal(40, 10, 300),
        "income": rng.lognormal(10, 0.6, 300),
        "score": rng.normal(70, 15, 300),
    })

    print("\n[Before]")
    print(df.describe().T)

    spec = NormalizationSpec(method="standard", clip=True)
    normalizer = FeatureNormalizer(spec)
    df_scaled = normalizer.fit_transform(df)

    print("\n[After Standard Scaling]")
    print(df_scaled.describe().T)

    report = build_normalization_report(df, df_scaled, df.columns)
    print("\n[Normalization Report]")
    print(report)


if __name__ == "__main__":
    _demo()