"""
Day 59 — Feature Engineering: Scaling (02_scaling.py)

목표
- 스케일링(scaling)이 왜 필요한지, 어떤 상황에서 어떤 스케일러를 선택하는지 이해한다.
- 데이터 누수(leakage)를 피하기 위해 "train에서 fit → test/serving에 transform"을 강제한다.
- 실무에서 자주 쓰는 스케일링 패턴을 유틸 형태로 구조화한다.

다루는 스케일링/변환
1) Standardization (표준화)     : 평균 0, 표준편차 1 (StandardScaler)
2) Min-Max Scaling (정규화)     : [0, 1] 범위 (MinMaxScaler)
3) Robust Scaling (로버스트)    : 중앙값/사분위 기반 (RobustScaler) -> 이상치에 강함
4) Log Transform (로그 변환)    : 강한 right-skew 완화 (log1p)
5) Power Transform (Yeo-Johnson): 분포 안정화(0/음수도 처리 가능) (PowerTransformer)

실무 관점 핵심
- 선형모델/거리 기반 모델(KNN, SVM, KMeans, PCA)은 스케일링이 성능에 큰 영향을 준다.
- 트리 기반 모델(RandomForest, XGBoost/LightGBM 등)은 상대적으로 덜 민감하지만,
  그래도 전처리 일관성과 다른 모델과의 비교를 위해 스케일링 파이프라인을 준비하는 것이 좋다.
- "fit은 train에서만" (통계량이 정보이기 때문에) -> 누수 방지의 기본.

요구사항
- scikit-learn이 설치되어 있어야 한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, PowerTransformer, RobustScaler, StandardScaler


# -------------------------------
# 0) 샘플 데이터 (바로 실행 가능)
# -------------------------------
def make_sample_data(n: int = 300, random_state: int = 42) -> Tuple[pd.DataFrame, pd.Series]:
    """
    스케일링이 필요해 보이는 "현실형 분포"를 일부러 만든다.

    features:
    - age: 비교적 정상분포(약간의 noise)
    - income: 강한 right-skew (로그정규 분포)
    - spend: income과 연관된 소비(스케일 차이 존재)
    - transactions: count 형태 (포아송 + tail)
    - debt_ratio: [0,1] 범위의 비율
    """
    rng = np.random.default_rng(random_state)

    age = rng.normal(loc=35, scale=10, size=n).clip(18, 80)
    income = rng.lognormal(mean=10.5, sigma=0.6, size=n)  # 큰 스케일 + right-skew
    spend = (income * rng.normal(0.25, 0.05, size=n)).clip(0, None)
    transactions = rng.poisson(lam=8, size=n).astype(float)
    # 일부 tail을 추가해서 robust scaling 필요성을 보여준다
    transactions[rng.choice(n, size=max(1, n // 30), replace=False)] *= 6

    debt_ratio = rng.beta(a=2.0, b=5.0, size=n)  # 0~1

    # 이진 타겟(예: churn) 예시
    # income 낮고 debt 높으면 1 확률이 높아지는 식으로 대충 생성
    logits = -3.0 + (-0.00003 * income) + (3.0 * debt_ratio) + (0.03 * (transactions - 8))
    prob = 1 / (1 + np.exp(-logits))
    y = (rng.random(n) < prob).astype(int)

    X = pd.DataFrame(
        {
            "age": age,
            "income": income,
            "spend": spend,
            "transactions": transactions,
            "debt_ratio": debt_ratio,
        }
    )
    y = pd.Series(y, name="target")
    return X, y


# ---------------------------------------------------------
# 1) 스케일링 선택 가이드 (간단 룰 기반 추천)
# ---------------------------------------------------------
def suggest_scaler_by_stats(series: pd.Series) -> str:
    """
    매우 단순한 휴리스틱 추천(학습용).
    실무에서는 모델/목적/검증 기반으로 최종 결정.

    한국어 설명:
    - 이상치가 많아 보이면 RobustScaler
    - 값 범위가 명확히 제한([0,1])이면 그대로 두거나 MinMax
    - 강한 right-skew면 log1p 또는 PowerTransformer(Yeo-Johnson)
    """
    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        return "unknown"

    q1, q3 = np.percentile(s, [25, 75])
    iqr = q3 - q1
    if iqr == 0:
        return "none"

    # outlier 비율(아주 대충)
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outlier_rate = ((s < lower) | (s > upper)).mean()

    # skewness(대충)
    skew = s.skew()

    # 0~1 범위 여부
    if s.min() >= 0 and s.max() <= 1:
        return "none_or_minmax"

    if skew > 1.5:
        return "log1p_or_power"

    if outlier_rate > 0.03:
        return "robust"

    return "standard"


# ---------------------------------------------------------
# 2) 누수 방지 스케일러 래퍼 (fit/train only)
# ---------------------------------------------------------
@dataclass
class NumericScalerPipeline:
    """
    숫자 컬럼에만 적용되는 스케일링 파이프라인.

    특징(한국어):
    - fit: train에서만 수행 (평균/표준편차/분위수 등이 학습 데이터 정보이기 때문)
    - transform: 동일 통계량으로 test/serving 변환
    - 스케일링 전 log 변환 등을 옵션으로 포함

    modes:
    - "standard"  : StandardScaler
    - "minmax"    : MinMaxScaler
    - "robust"    : RobustScaler
    - "power"     : PowerTransformer(yeo-johnson)
    - "none"      : 변환 없음
    """
    cols: List[str]
    mode: str = "standard"
    use_log1p: bool = False
    log1p_cols: Optional[List[str]] = None  # 특정 컬럼만 log1p 적용 가능
    clip_negative_for_log: bool = True      # log1p는 음수 처리에 주의 필요
    scaler_: Optional[object] = None
    fitted_cols_: Optional[List[str]] = None

    def _build_scaler(self):
        if self.mode == "standard":
            return StandardScaler()
        if self.mode == "minmax":
            return MinMaxScaler()
        if self.mode == "robust":
            return RobustScaler()
        if self.mode == "power":
            # Yeo-Johnson은 0/음수도 처리 가능 -> 실무에서 안전한 편
            return PowerTransformer(method="yeo-johnson", standardize=True)
        if self.mode == "none":
            return None
        raise ValueError(f"Unknown mode: {self.mode}")

    def _apply_log1p(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        log1p 변환 적용.
        - right-skew 완화 목적
        - 음수 값이 있을 수 있으면 Yeo-Johnson(power) 쪽이 더 안전
        """
        X_out = X.copy()
        if not self.use_log1p:
            return X_out

        target_cols = self.log1p_cols if self.log1p_cols is not None else self.cols
        for c in target_cols:
            if c not in X_out.columns:
                continue
            v = pd.to_numeric(X_out[c], errors="coerce")
            if self.clip_negative_for_log:
                # log1p는 -1보다 작은 값에서 문제가 발생하므로,
                # 여기서는 안전하게 0 미만은 0으로 클리핑(학습용 단순 정책)
                # 실무에서는 음수 의미를 먼저 해석하고 정책을 정해야 한다.
                v = v.clip(lower=0)
            X_out[c] = np.log1p(v)
        return X_out

    def fit(self, X_train: pd.DataFrame) -> "NumericScalerPipeline":
        """
        train 데이터로만 scaler를 학습(fit)한다.
        """
        self.fitted_cols_ = [c for c in self.cols if c in X_train.columns]
        X_work = self._apply_log1p(X_train[self.fitted_cols_].copy())

        scaler = self._build_scaler()
        if scaler is None:
            self.scaler_ = None
            return self

        scaler.fit(X_work.values)
        self.scaler_ = scaler
        return self

    def transform(self, X: pd.DataFrame, suffix: Optional[str] = None) -> pd.DataFrame:
        """
        동일한 스케일러를 사용해서 데이터를 변환한다.
        suffix가 있으면 변환 컬럼명을 새 컬럼으로 만들어 원본을 보존할 수 있다.
        """
        if self.fitted_cols_ is None:
            raise ValueError("Pipeline is not fitted. Call fit() first.")

        X_out = X.copy()
        cols = self.fitted_cols_
        X_work = self._apply_log1p(X_out[cols].copy())

        if self.scaler_ is None:
            # 스케일링 없음
            return X_out

        transformed = self.scaler_.transform(X_work.values)
        transformed_df = pd.DataFrame(transformed, columns=cols, index=X_out.index)

        if suffix:
            # 원본 컬럼을 보존하고 새 컬럼을 만든다.
            for c in cols:
                X_out[f"{c}{suffix}"] = transformed_df[c]
        else:
            # 원본 컬럼을 덮어쓴다.
            X_out[cols] = transformed_df[cols]

        return X_out


# ---------------------------------------------------------
# 3) Before/After 리포트 (간단 요약)
# ---------------------------------------------------------
def summarize_numeric(df: pd.DataFrame, cols: List[str], title: str) -> None:
    """
    스케일링 전후를 비교할 때 자주 보는 통계 요약 출력.
    """
    print(f"\n=== {title} ===")
    sub = df[cols].copy()
    desc = sub.describe(percentiles=[0.01, 0.05, 0.5, 0.95, 0.99]).T
    # 보기 좋게 일부만
    show_cols = ["mean", "std", "min", "1%", "5%", "50%", "95%", "99%", "max"]
    print(desc[show_cols].round(4))


# ---------------------------------------------------------
# 4) 데모 실행
# ---------------------------------------------------------
def main() -> None:
    X, y = make_sample_data()

    # train/test split (누수 방지: scaler는 train에서만 fit)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=7, stratify=y
    )

    numeric_cols = ["age", "income", "spend", "transactions", "debt_ratio"]

    # 0) 스케일러 추천(학습용)
    print("=== Simple scaler suggestions (heuristic) ===")
    for c in numeric_cols:
        print(f"- {c}: {suggest_scaler_by_stats(X_train[c])}")

    summarize_numeric(X_train, numeric_cols, "Train BEFORE scaling")
    summarize_numeric(X_test, numeric_cols, "Test BEFORE scaling")

    # 1) StandardScaler (기본)
    standard_pipe = NumericScalerPipeline(cols=numeric_cols, mode="standard").fit(X_train)
    X_train_std = standard_pipe.transform(X_train, suffix="_std")
    X_test_std = standard_pipe.transform(X_test, suffix="_std")

    summarize_numeric(X_train_std, [f"{c}_std" for c in numeric_cols], "Train AFTER StandardScaler")
    summarize_numeric(X_test_std, [f"{c}_std" for c in numeric_cols], "Test AFTER StandardScaler")

    # 2) RobustScaler (이상치에 더 강함)
    robust_pipe = NumericScalerPipeline(cols=numeric_cols, mode="robust").fit(X_train)
    X_train_rb = robust_pipe.transform(X_train, suffix="_rb")
    X_test_rb = robust_pipe.transform(X_test, suffix="_rb")

    summarize_numeric(X_train_rb, [f"{c}_rb" for c in numeric_cols], "Train AFTER RobustScaler")
    summarize_numeric(X_test_rb, [f"{c}_rb" for c in numeric_cols], "Test AFTER RobustScaler")

    # 3) Log1p + StandardScaler (강한 right-skew 완화 예시: income/spend)
    log_std_pipe = NumericScalerPipeline(
        cols=numeric_cols,
        mode="standard",
        use_log1p=True,
        log1p_cols=["income", "spend", "transactions"],  # 주로 right-skew 컬럼만
        clip_negative_for_log=True,
    ).fit(X_train)

    X_train_logstd = log_std_pipe.transform(X_train, suffix="_logstd")
    X_test_logstd = log_std_pipe.transform(X_test, suffix="_logstd")

    summarize_numeric(X_train_logstd, [f"{c}_logstd" for c in numeric_cols], "Train AFTER log1p + StandardScaler")
    summarize_numeric(X_test_logstd, [f"{c}_logstd" for c in numeric_cols], "Test AFTER log1p + StandardScaler")

    # 4) PowerTransformer (Yeo-Johnson) — 분포 안정화 + 표준화 포함
    power_pipe = NumericScalerPipeline(cols=numeric_cols, mode="power").fit(X_train)
    X_train_pw = power_pipe.transform(X_train, suffix="_pw")
    X_test_pw = power_pipe.transform(X_test, suffix="_pw")

    summarize_numeric(X_train_pw, [f"{c}_pw" for c in numeric_cols], "Train AFTER PowerTransformer (Yeo-Johnson)")
    summarize_numeric(X_test_pw, [f"{c}_pw" for c in numeric_cols], "Test AFTER PowerTransformer (Yeo-Johnson)")

    print("\n✅ Done. (Day 59 Scaling pipeline demo complete)")
    print("실무 적용 팁(한국어):")
    print("- 모델 비교를 할 때는 동일한 split에서 스케일링 방식만 바꿔 성능을 비교하세요.")
    print("- 반드시 train에서만 fit하고, test/serving은 transform만 하세요(누수 방지).")


if __name__ == "__main__":
    main()