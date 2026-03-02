"""
Day 58 — Feature Engineering: Encoding (01_encoding.py)

목표
- 범주형(feature)을 모델이 이해할 수 있는 수치 형태로 변환(encoding)하는 실무 패턴을 익힌다.
- 데이터 누수(leakage)를 피하기 위해 "학습 데이터로 규칙을 학습(fit) → 테스트/서빙 데이터에 적용(transform)" 구조를 습관화한다.

다루는 인코딩
1) One-Hot Encoding (명목형 / 순서 없음)  : 예) city = Seoul/Busan/...
2) Ordinal Encoding (서열형 / 순서 있음)  : 예) grade = low < mid < high
3) Frequency / Count Encoding (카디널리티 큰 범주) : 예) user_id, zipcode 등
4) Target Encoding (주의: 누수 위험 높음) : CV/스무딩/학습데이터 제한 원칙

주의
- 이 파일은 "학습용 예제"이므로 sklearn 사용 예시도 포함하되,
  핵심은 '규칙을 만들고 적용하는 구조'와 '검증/누수 방지'에 있다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


# -------------------------------
# 0) 샘플 데이터 (바로 실행 가능)
# -------------------------------
def make_sample_data() -> Tuple[pd.DataFrame, pd.Series]:
    """
    간단한 분류 문제(타겟 y) 형태로 샘플 데이터를 만든다.
    - city: 명목형
    - grade: 서열형
    - channel: 명목형(카디널리티 낮음)
    - user_group: 카디널리티 중간(빈도 인코딩 예시)
    """
    X = pd.DataFrame(
        {
            "city": ["Seoul", "Seoul", "Busan", "Incheon", "Busan", "Seoul", "Daegu", "Busan"],
            "grade": ["low", "mid", "high", "mid", "low", "high", "mid", "low"],
            "channel": ["web", "app", "web", "app", "web", "web", "app", "app"],
            "user_group": ["A", "B", "A", "C", "D", "A", "C", "E"],
            "age": [24, 31, 28, 45, 22, 36, 40, 27],
        }
    )
    # y는 예시용 타겟(0/1)
    y = pd.Series([1, 0, 1, 0, 0, 1, 0, 1], name="target")
    return X, y


# -----------------------------------------
# 1) One-Hot Encoding (명목형: city, channel)
# -----------------------------------------
def one_hot_encode(
    X: pd.DataFrame,
    cols: List[str],
    drop_first: bool = False,
    handle_unknown: str = "ignore",
) -> pd.DataFrame:
    """
    pandas.get_dummies 기반 One-Hot 인코딩.

    실무 팁(한국어):
    - 학습/테스트가 분리된 경우, 학습 데이터에서 만들어진 더미 컬럼 셋을 기준으로
      테스트 데이터에도 동일한 컬럼을 맞춰줘야 한다.
    - 여기서는 단일 DataFrame 기준으로 보여주지만,
      아래의 `OneHotSchema` 클래스로 "학습 컬럼 스키마"를 저장/적용하는 패턴을 제공한다.
    """
    # pandas.get_dummies는 unknown 처리 옵션이 없기 때문에,
    # 실제 운영에서는 sklearn OneHotEncoder(handle_unknown="ignore")가 더 안전하다.
    # 다만 학습 목적으로는 get_dummies가 직관적이다.
    dummies = pd.get_dummies(X[cols], prefix=cols, drop_first=drop_first, dtype=int)
    X_out = X.drop(columns=cols).join(dummies)
    return X_out


@dataclass
class OneHotSchema:
    """
    학습 데이터에서 생성된 One-Hot 컬럼 스키마를 저장하고,
    새로운 데이터(테스트/서빙)에 동일 스키마를 적용하는 유틸.

    핵심(한국어):
    - 'fit' 단계에서 생성된 더미 컬럼을 저장
    - 'transform' 단계에서 누락 컬럼은 0으로 채우고, 추가 컬럼은 제거하여 스키마 고정
    """
    cols: List[str]
    drop_first: bool = False
    dummy_columns_: Optional[List[str]] = None

    def fit(self, X_train: pd.DataFrame) -> "OneHotSchema":
        X_enc = pd.get_dummies(X_train[self.cols], prefix=self.cols, drop_first=self.drop_first, dtype=int)
        self.dummy_columns_ = list(X_enc.columns)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if self.dummy_columns_ is None:
            raise ValueError("OneHotSchema is not fitted. Call fit() first.")

        X_dum = pd.get_dummies(X[self.cols], prefix=self.cols, drop_first=self.drop_first, dtype=int)

        # 학습 스키마에 맞춰 컬럼 정렬/보정
        # 1) 학습에 없던 컬럼은 제거
        X_dum = X_dum.reindex(columns=self.dummy_columns_, fill_value=0)

        X_out = X.drop(columns=self.cols).join(X_dum)
        return X_out


# -----------------------------------------
# 2) Ordinal Encoding (서열형: grade)
# -----------------------------------------
def ordinal_encode(
    X: pd.DataFrame,
    col: str,
    order: List[str],
    unknown_value: int = -1,
    out_col: Optional[str] = None,
) -> pd.DataFrame:
    """
    서열형(ordinal) 변수 인코딩.

    예) grade: low < mid < high

    한국어 설명:
    - 순서가 있는 범주는 원-핫보다 "순서 정보"를 유지하는 것이 유리할 수 있다.
    - 단, 모델에 따라(선형모델 등) 수치 간격이 '동일 간격'처럼 해석될 수 있으므로
      도메인적으로 적절한지 확인해야 한다.
    """
    mapping = {k: i for i, k in enumerate(order)}
    out_col = out_col or f"{col}_ord"
    X_out = X.copy()
    X_out[out_col] = X_out[col].map(mapping).fillna(unknown_value).astype(int)
    return X_out


# -------------------------------------------------------
# 3) Frequency / Count Encoding (카디널리티 큰 범주 대응)
# -------------------------------------------------------
@dataclass
class FrequencyEncoder:
    """
    범주별 등장 빈도(또는 비율)를 수치로 변환하는 인코더.

    한국어 설명:
    - high-cardinality 카테고리(예: user_id, product_id)에서는 One-Hot이 폭발한다.
    - 이럴 때 '빈도/비율'은 간단하지만 강력한 baseline feature가 된다.
    - 누수 방지: 빈도 테이블은 train에서만 계산하고 test에 적용한다.
    """
    col: str
    normalize: bool = True  # True면 비율(0~1), False면 count
    min_freq: int = 1       # 너무 희귀한 범주를 "RARE"로 합칠 수 있는 옵션
    value_map_: Optional[Dict[str, float]] = None

    def fit(self, X_train: pd.DataFrame) -> "FrequencyEncoder":
        s = X_train[self.col].astype("string").fillna("<NA>")

        vc = s.value_counts(dropna=False)
        if self.min_freq > 1:
            # min_freq 미만 범주는 RARE로 통합(희귀 범주 처리)
            rare = vc[vc < self.min_freq].index
            s = s.where(~s.isin(rare), other="RARE")
            vc = s.value_counts(dropna=False)

        if self.normalize:
            freq = (vc / vc.sum()).to_dict()
        else:
            freq = vc.astype(float).to_dict()

        self.value_map_ = freq
        return self

    def transform(self, X: pd.DataFrame, out_col: Optional[str] = None) -> pd.DataFrame:
        if self.value_map_ is None:
            raise ValueError("FrequencyEncoder is not fitted. Call fit() first.")

        out_col = out_col or f"{self.col}_freq"
        X_out = X.copy()

        s = X_out[self.col].astype("string").fillna("<NA>")
        # 학습에 없던 범주는 0으로 처리(또는 global mean으로 처리하는 방식도 가능)
        X_out[out_col] = s.map(self.value_map_).fillna(0.0).astype(float)
        return X_out


# -----------------------------------------
# 4) Target Encoding (누수 위험 높음)
# -----------------------------------------
@dataclass
class TargetEncoderSimple:
    """
    (학습용) 단순 타겟 인코딩: category → target 평균값

    ⚠️ 주의(한국어):
    - 타겟 인코딩은 매우 강력하지만 누수 위험이 크다.
    - 실무에서는 K-Fold target encoding / smoothing / noise 등을 적용한다.
    - 여기서는 원리를 이해하기 위한 "baseline"만 제공한다.
    """
    col: str
    smoothing: float = 10.0  # 스무딩 강도(클수록 global mean에 더 가까워짐)
    global_mean_: Optional[float] = None
    enc_map_: Optional[Dict[str, float]] = None

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series) -> "TargetEncoderSimple":
        df = pd.DataFrame({"x": X_train[self.col].astype("string").fillna("<NA>"), "y": y_train})
        self.global_mean_ = float(df["y"].mean())

        stats = df.groupby("x")["y"].agg(["mean", "count"])
        # smoothing: (count*mean + smoothing*global_mean) / (count + smoothing)
        enc = (stats["count"] * stats["mean"] + self.smoothing * self.global_mean_) / (stats["count"] + self.smoothing)

        self.enc_map_ = enc.to_dict()
        return self

    def transform(self, X: pd.DataFrame, out_col: Optional[str] = None) -> pd.DataFrame:
        if self.enc_map_ is None or self.global_mean_ is None:
            raise ValueError("TargetEncoderSimple is not fitted. Call fit() first.")

        out_col = out_col or f"{self.col}_te"
        X_out = X.copy()
        s = X_out[self.col].astype("string").fillna("<NA>")
        X_out[out_col] = s.map(self.enc_map_).fillna(self.global_mean_).astype(float)
        return X_out


# -----------------------------------------
# 5) 데모 실행 (원리 확인)
# -----------------------------------------
def main() -> None:
    X, y = make_sample_data()

    print("=== Raw X ===")
    print(X)
    print("\n=== y ===")
    print(y)

    # 1) Ordinal
    X1 = ordinal_encode(X, col="grade", order=["low", "mid", "high"])
    print("\n=== Ordinal Encoded (grade_ord) ===")
    print(X1[["grade", "grade_ord"]])

    # 2) OneHot (스키마 기반)
    schema = OneHotSchema(cols=["city", "channel"], drop_first=False).fit(X_train=X)
    X2 = schema.transform(X)
    print("\n=== One-Hot Encoded (schema-based) ===")
    print(X2.head())
    print(f"\nOne-Hot dummy columns count: {len(schema.dummy_columns_ or [])}")

    # 3) Frequency
    fe = FrequencyEncoder(col="user_group", normalize=True, min_freq=1).fit(X_train=X)
    X3 = fe.transform(X)
    print("\n=== Frequency Encoded (user_group_freq) ===")
    print(X3[["user_group", "user_group_freq"]])

    # 4) Target Encoding (학습용 단순 버전)
    te = TargetEncoderSimple(col="city", smoothing=5.0).fit(X_train=X, y_train=y)
    X4 = te.transform(X)
    print("\n=== Target Encoded (city_te) ===")
    print(X4[["city", "city_te"]].head())

    # 최종적으로는 원하는 인코딩 조합을 선택해서 모델 입력으로 사용
    # 예시: (grade는 ordinal + city/channel은 one-hot + user_group은 freq)
    X_final = schema.transform(ordinal_encode(fe.transform(X), col="grade", order=["low", "mid", "high"]))
    print("\n=== Final Feature Set Example ===")
    print(X_final.head())
    print(f"\nFinal shape: {X_final.shape}")


if __name__ == "__main__":
    main()