"""
Day 54 — Data Cleaning: Missing Values

✅ 목표(한국어)
- 결측치(Missing Values)를 "정의 → 진단 → 처리 → 검증"까지 일관된 파이프라인으로 다룬다.
- 단순히 fillna()만 하는 것이 아니라, 아래를 체계화한다:
  1) 결측치 스냅샷(컬럼별 개수/비율)
  2) 결측 패턴(동시에 비는 컬럼 조합) 탐지
  3) 처리 전략(삭제 / 단일값 대치 / 그룹 기반 대치 / 시계열 보간 / 플래그 생성)
  4) 처리 후 품질 검증(결측 감소, 분포 왜곡 위험 점검)

📌 실무 관점 팁
- 결측치 처리 전에 "의미(왜 비었나?)"와 "하류 영향(모델/집계)"을 먼저 생각해야 한다.
- 일부 컬럼의 결측은 정보(unknown/미측정)를 의미할 수 있어, 단순 삭제가 손실을 만든다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Iterable, Literal, Dict, Any

import numpy as np
import pandas as pd


# =========================
# 0) Utilities / Types
# =========================

FillStrategy = Literal[
    "drop_rows",
    "drop_cols",
    "constant",
    "mean",
    "median",
    "mode",
    "group_median",
    "group_mode",
    "ffill",
    "bfill",
    "interpolate_linear",
]

@dataclass(frozen=True)
class MissingReport:
    """
    결측치 리포트 결과를 한 번에 들고 다니기 위한 컨테이너.
    - summary: 컬럼별 결측 개수/비율 요약
    - pattern: 결측 패턴(동시에 비는 컬럼 조합) Top-N
    """
    summary: pd.DataFrame
    pattern: pd.DataFrame


def _ensure_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """(한국어) df가 DataFrame인지 간단히 체크."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    return df


def _validate_columns(df: pd.DataFrame, columns: Optional[Iterable[str]]) -> list[str]:
    """
    (한국어)
    - columns가 None이면 df 전체 컬럼을 대상으로 한다.
    - 특정 컬럼 리스트가 들어오면 존재 여부를 검증한다.
    """
    if columns is None:
        return list(df.columns)

    cols = list(columns)
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Unknown columns: {missing}")
    return cols


# =========================
# 1) Missing Diagnostics
# =========================

def missing_summary(
    df: pd.DataFrame,
    columns: Optional[Iterable[str]] = None,
    *,
    sort_by: Literal["missing_pct", "missing_cnt", "column"] = "missing_pct",
    descending: bool = True,
) -> pd.DataFrame:
    """
    결측치 요약 테이블 생성.

    Parameters
    ----------
    df : pd.DataFrame
    columns : Optional[Iterable[str]]
        결측치를 진단할 컬럼 목록. None이면 전체 컬럼.
    sort_by : {"missing_pct","missing_cnt","column"}
        정렬 기준.
    descending : bool
        내림차순 정렬 여부.

    Returns
    -------
    pd.DataFrame
        columns: [column, missing_cnt, missing_pct, non_missing_cnt, dtype]
    """
    df = _ensure_dataframe(df)
    cols = _validate_columns(df, columns)

    s = df[cols].isna().sum()
    n = len(df)
    out = pd.DataFrame(
        {
            "column": s.index,
            "missing_cnt": s.values,
            "missing_pct": (s.values / n * 100.0) if n > 0 else 0.0,
            "non_missing_cnt": (n - s.values),
            "dtype": [str(df[c].dtype) for c in s.index],
        }
    )

    out = out.sort_values(by=sort_by, ascending=not descending).reset_index(drop=True)
    return out


def missing_pattern(
    df: pd.DataFrame,
    columns: Optional[Iterable[str]] = None,
    *,
    top_n: int = 10,
) -> pd.DataFrame:
    """
    결측 패턴(동시에 결측인 컬럼 조합) Top-N을 추출.

    (한국어)
    - 결측이 "독립적으로" 발생하는지, 특정 컬럼들이 "같이" 비는지 보는 것은 매우 중요하다.
    - 예: 설문 미응답, 특정 단계에서 수집 실패 등은 결측이 묶음으로 발생한다.

    Returns
    -------
    pd.DataFrame
        columns: [missing_columns, pattern_count, pattern_pct]
    """
    df = _ensure_dataframe(df)
    cols = _validate_columns(df, columns)

    if len(df) == 0:
        return pd.DataFrame(columns=["missing_columns", "pattern_count", "pattern_pct"])

    mask = df[cols].isna()

    # (한국어) 각 row마다 결측인 컬럼 리스트를 튜플로 만든다.
    patterns = mask.apply(lambda r: tuple(r.index[r].tolist()), axis=1)

    # (한국어) "결측이 전혀 없는 row" 패턴은 제외하는 경우가 많다.
    patterns = patterns[patterns.apply(lambda t: len(t) > 0)]

    vc = patterns.value_counts().head(top_n)
    out = pd.DataFrame(
        {
            "missing_columns": [", ".join(p) for p in vc.index],
            "pattern_count": vc.values,
            "pattern_pct": (vc.values / len(df) * 100.0),
        }
    )
    return out.reset_index(drop=True)


def build_missing_report(
    df: pd.DataFrame,
    columns: Optional[Iterable[str]] = None,
    *,
    top_n_patterns: int = 10,
) -> MissingReport:
    """
    결측치 리포트를 한 번에 생성.

    Returns
    -------
    MissingReport(summary, pattern)
    """
    summary = missing_summary(df, columns=columns)
    pattern = missing_pattern(df, columns=columns, top_n=top_n_patterns)
    return MissingReport(summary=summary, pattern=pattern)


# =========================
# 2) Missing Handling Strategies
# =========================

def add_missing_flags(
    df: pd.DataFrame,
    columns: Iterable[str],
    *,
    suffix: str = "_is_missing",
) -> pd.DataFrame:
    """
    결측 플래그 컬럼 추가.

    (한국어)
    - 모델링에서 결측은 자체로 중요한 신호일 수 있다.
    - 예: 소득 미기재 = 특정 계층/상황과 관련 → 단순 대치보다 '결측 여부'를 피처로 남기는 것이 유리한 경우가 많다.

    Returns
    -------
    pd.DataFrame (copy)
    """
    df = _ensure_dataframe(df).copy()
    cols = _validate_columns(df, columns)

    for c in cols:
        df[f"{c}{suffix}"] = df[c].isna().astype(int)
    return df


def handle_missing(
    df: pd.DataFrame,
    *,
    columns: Optional[Iterable[str]] = None,
    strategy: FillStrategy = "median",
    constant_value: Any = 0,
    drop_threshold_pct: float = 60.0,
    groupby_col: Optional[str] = None,
    time_col: Optional[str] = None,
    sort_time: bool = True,
) -> pd.DataFrame:
    """
    결측치 처리 메인 함수.

    Parameters
    ----------
    df : pd.DataFrame
    columns : Optional[Iterable[str]]
        처리 대상 컬럼. None이면 전체 컬럼.
    strategy : FillStrategy
        결측 처리 방식.
    constant_value : Any
        strategy="constant"에서 사용할 값.
    drop_threshold_pct : float
        drop_cols 시 결측 비율이 이 값 이상인 컬럼을 제거.
    groupby_col : Optional[str]
        group_median / group_mode에서 그룹 기준 컬럼명.
    time_col : Optional[str]
        ffill/bfill/interpolate에서 시간 정렬 기준 컬럼명.
    sort_time : bool
        time_col이 있을 때 정렬할지 여부.

    Returns
    -------
    pd.DataFrame (copy)
    """
    df = _ensure_dataframe(df).copy()
    cols = _validate_columns(df, columns)

    # -------------------------
    # Drop rows
    # -------------------------
    if strategy == "drop_rows":
        # (한국어) 특정 컬럼 중 하나라도 NA면 row 제거
        return df.dropna(subset=cols)

    # -------------------------
    # Drop columns
    # -------------------------
    if strategy == "drop_cols":
        # (한국어) 결측 비율이 임계치 이상인 컬럼을 제거 (정보 손실이 크므로 신중히)
        summ = missing_summary(df, columns=cols, sort_by="missing_pct")
        to_drop = summ.loc[summ["missing_pct"] >= drop_threshold_pct, "column"].tolist()
        return df.drop(columns=to_drop)

    # -------------------------
    # Constant fill
    # -------------------------
    if strategy == "constant":
        for c in cols:
            df[c] = df[c].fillna(constant_value)
        return df

    # -------------------------
    # Numeric central tendency fills
    # -------------------------
    if strategy in {"mean", "median"}:
        for c in cols:
            if pd.api.types.is_numeric_dtype(df[c]):
                val = df[c].mean() if strategy == "mean" else df[c].median()
                df[c] = df[c].fillna(val)
            else:
                # (한국어) 숫자가 아닌데 mean/median을 요구하면 위험 → 그대로 두거나 mode로 처리 권장
                # 여기서는 안전하게 그대로 둔다.
                pass
        return df

    # -------------------------
    # Mode fill
    # -------------------------
    if strategy == "mode":
        for c in cols:
            # (한국어) mode는 다중 최빈값이 있을 수 있어 첫 번째를 사용 (업무 규칙으로 정해야 함)
            modes = df[c].mode(dropna=True)
            if len(modes) > 0:
                df[c] = df[c].fillna(modes.iloc[0])
        return df

    # -------------------------
    # Group-based fills
    # -------------------------
    if strategy in {"group_median", "group_mode"}:
        if groupby_col is None:
            raise ValueError("groupby_col is required for group-based strategies.")
        if groupby_col not in df.columns:
            raise ValueError(f"groupby_col '{groupby_col}' not found in df.")

        for c in cols:
            if strategy == "group_median":
                if not pd.api.types.is_numeric_dtype(df[c]):
                    continue
                # (한국어) 그룹별 중앙값으로 대치 (세그먼트 편차를 보존)
                df[c] = df[c].fillna(df.groupby(groupby_col)[c].transform("median"))
            else:
                # group_mode
                def _mode(series: pd.Series):
                    m = series.mode(dropna=True)
                    return m.iloc[0] if len(m) > 0 else np.nan
                df[c] = df[c].fillna(df.groupby(groupby_col)[c].transform(_mode))
        return df

    # -------------------------
    # Time-series oriented fills
    # -------------------------
    if strategy in {"ffill", "bfill", "interpolate_linear"}:
        if time_col is not None:
            if time_col not in df.columns:
                raise ValueError(f"time_col '{time_col}' not found in df.")
            if sort_time:
                # (한국어) 시간 정렬 후 결측 처리 (시계열에서 매우 중요)
                df = df.sort_values(by=time_col).reset_index(drop=True)

        if strategy == "ffill":
            df[cols] = df[cols].ffill()
            return df

        if strategy == "bfill":
            df[cols] = df[cols].bfill()
            return df

        if strategy == "interpolate_linear":
            # (한국어) 수치형 컬럼에 대해서만 선형 보간을 권장
            numeric_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
            df[numeric_cols] = df[numeric_cols].interpolate(method="linear", limit_direction="both")
            return df

    raise ValueError(f"Unknown strategy: {strategy}")


# =========================
# 3) Validation / Before-After Check
# =========================

def compare_missing_before_after(
    before: pd.DataFrame,
    after: pd.DataFrame,
    *,
    columns: Optional[Iterable[str]] = None,
) -> pd.DataFrame:
    """
    결측 처리 전/후 비교 테이블.

    (한국어)
    - 처리 결과를 '감'으로 보지 말고 수치로 확인한다.
    - missing_cnt / missing_pct가 실제로 줄었는지, 특정 컬럼만 과하게 변했는지 점검.
    """
    before = _ensure_dataframe(before)
    after = _ensure_dataframe(after)

    cols = _validate_columns(before, columns)
    # after에도 동일 컬럼이 존재해야 비교 가능
    cols = [c for c in cols if c in after.columns]

    b = missing_summary(before, columns=cols).set_index("column")
    a = missing_summary(after, columns=cols).set_index("column")

    out = pd.DataFrame(
        {
            "missing_cnt_before": b["missing_cnt"],
            "missing_pct_before": b["missing_pct"],
            "missing_cnt_after": a["missing_cnt"],
            "missing_pct_after": a["missing_pct"],
        }
    )
    out["missing_cnt_delta"] = out["missing_cnt_after"] - out["missing_cnt_before"]
    out["missing_pct_delta"] = out["missing_pct_after"] - out["missing_pct_before"]
    out = out.sort_values("missing_pct_before", ascending=False).reset_index()
    return out


# =========================
# 4) Demo / Self-test
# =========================

def _make_demo_df(seed: int = 7) -> pd.DataFrame:
    """
    (한국어) 외부 데이터 없이도 동작 확인 가능한 데모 데이터 생성.
    - 결측을 의도적으로 섞어서 결측 진단/처리 함수들을 검증한다.
    """
    rng = np.random.default_rng(seed)
    n = 50

    df = pd.DataFrame(
        {
            "user_id": np.arange(1, n + 1),
            "segment": rng.choice(["A", "B", "C"], size=n, replace=True),
            "age": rng.integers(18, 60, size=n).astype(float),
            "income": rng.normal(5000, 1200, size=n).round(0),
            "event_date": pd.date_range("2026-01-01", periods=n, freq="D"),
        }
    )

    # (한국어) 결측 주입
    df.loc[rng.choice(n, size=10, replace=False), "age"] = np.nan
    df.loc[rng.choice(n, size=12, replace=False), "income"] = np.nan
    df.loc[rng.choice(n, size=6, replace=False), "segment"] = np.nan

    return df


def main() -> None:
    """
    (한국어)
    - 실행 예시:
      python 01_missing_values.py
    """
    df = _make_demo_df()

    print("\n=== [Before] Missing Report ===")
    report = build_missing_report(df, top_n_patterns=5)
    print(report.summary.head(10).to_string(index=False))
    print("\n--- Missing Pattern (Top) ---")
    print(report.pattern.to_string(index=False))

    # 1) 결측 플래그 추가
    df_flagged = add_missing_flags(df, columns=["age", "income", "segment"])
    print("\n=== Added missing flags columns ===")
    print([c for c in df_flagged.columns if c.endswith("_is_missing")])

    # 2) 그룹 기반 중앙값 대치(세그먼트별 income의 스케일을 보존)
    df_filled = handle_missing(
        df_flagged,
        columns=["income"],
        strategy="group_median",
        groupby_col="segment",
    )

    # 3) age는 전체 중앙값으로 대치
    df_filled = handle_missing(
        df_filled,
        columns=["age"],
        strategy="median",
    )

    # 4) segment는 mode로 대치
    df_filled = handle_missing(
        df_filled,
        columns=["segment"],
        strategy="mode",
    )

    print("\n=== [After] Missing Summary ===")
    after_report = build_missing_report(df_filled, top_n_patterns=5)
    print(after_report.summary.head(10).to_string(index=False))

    print("\n=== Compare Before vs After ===")
    cmp = compare_missing_before_after(df, df_filled, columns=["age", "income", "segment"])
    print(cmp.to_string(index=False))

    # (한국어) 결과 미리 보기
    print("\n=== Preview cleaned df ===")
    print(df_filled.head(5).to_string(index=False))


if __name__ == "__main__":
    main()