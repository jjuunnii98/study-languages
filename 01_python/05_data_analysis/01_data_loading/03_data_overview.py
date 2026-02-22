"""
Day 49: Data Overview — 데이터 품질/구조/기본 통계 점검 템플릿

목표
- 로딩한 데이터에 대해 "빠르게" 품질을 진단한다.
- 실무에서 흔히 하는 점검 항목을 자동화한다:
  1) shape / column / dtype
  2) 결측치(NA) 비율
  3) 중복 행 / 중복 키(가능한 경우)
  4) 수치형 분포(기본 통계, 이상치 힌트)
  5) 범주형(카디널리티, top-k 빈도)
  6) 날짜/시간 컬럼 범위, 정렬, 간격 이상 여부(가능한 경우)
  7) 간단 상관관계(수치형)
- 결과를 콘솔 출력 + (선택) CSV 리포트로 저장 가능하게 구성한다.

실행 방식(권장)
- 먼저 CSV/Excel로 읽는 경우: Day 47 (01_read_csv_excel.py) 로딩 코드 참고
- SQL로 읽는 경우: Day 48 (02_read_sql.py) 로딩 코드 참고
- 이 파일은 "어떤 DF든" 넣으면 점검 리포트를 뽑는 범용 도구 형태로 작성한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


# -----------------------------------------
# 0) 설정
# -----------------------------------------
BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"


@dataclass(frozen=True)
class OverviewConfig:
    """데이터 점검 리포트 옵션"""

    # 상위 n개 값(top-k) 빈도 표 출력
    top_k: int = 5

    # 결측치 비율이 이 값 이상이면 "주의"로 표시
    na_warn_threshold: float = 0.2

    # 상관관계 출력 여부
    show_corr: bool = True

    # 상관관계에서 출력할 상위 |corr| 페어 개수
    corr_top_n: int = 10

    # 리포트 저장 여부
    save_reports: bool = True


# -----------------------------------------
# 1) 유틸: 디렉토리 생성
# -----------------------------------------
def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


# -----------------------------------------
# 2) 핵심: 데이터 요약/점검 함수
# -----------------------------------------
def summarize_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    스키마 요약 테이블 생성
    - dtype
    - 결측치 개수/비율
    - 유니크 값 개수(카디널리티)
    """
    n = len(df)
    schema = pd.DataFrame(
        {
            "dtype": df.dtypes.astype(str),
            "na_count": df.isna().sum(),
            "na_rate": (df.isna().sum() / max(n, 1)).round(4),
            "n_unique": df.nunique(dropna=True),
        }
    ).sort_values(["na_rate", "n_unique"], ascending=[False, False])

    return schema


def detect_numeric_outlier_hints(df: pd.DataFrame) -> pd.DataFrame:
    """
    수치형 컬럼에 대해 간단한 이상치 힌트를 제공.
    - IQR 기준으로 범위 밖 비율 계산(정교한 이상치 탐지 X, 스크리닝 목적)
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    rows = []

    for col in numeric_cols:
        s = df[col].dropna()
        if s.empty:
            continue

        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            # 값이 거의 고정된 경우
            rows.append(
                {
                    "col": col,
                    "q1": q1,
                    "q3": q3,
                    "iqr": iqr,
                    "outlier_rate_iqr": 0.0,
                    "note": "IQR=0 (values may be constant or low-variance)",
                }
            )
            continue

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_rate = ((s < lower) | (s > upper)).mean()

        rows.append(
            {
                "col": col,
                "q1": float(q1),
                "q3": float(q3),
                "iqr": float(iqr),
                "outlier_rate_iqr": round(float(outlier_rate), 4),
                "note": "",
            }
        )

    return pd.DataFrame(rows).sort_values("outlier_rate_iqr", ascending=False)


def topk_categorical(df: pd.DataFrame, col: str, k: int = 5) -> pd.DataFrame:
    """
    범주형 top-k 빈도 테이블
    - object/category/bool 같은 컬럼 대상으로 사용
    """
    vc = df[col].astype("object").value_counts(dropna=False).head(k)
    out = vc.reset_index()
    out.columns = [col, "count"]
    out["rate"] = (out["count"] / max(len(df), 1)).round(4)
    return out


def correlation_top_pairs(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    수치형 컬럼의 상관관계에서 |corr| 큰 페어를 top_n만 반환.
    - 대각선/중복 제거
    """
    numeric = df.select_dtypes(include=[np.number])
    if numeric.shape[1] < 2:
        return pd.DataFrame(columns=["col_a", "col_b", "corr"])

    corr = numeric.corr(numeric_only=True)
    # 상삼각 제외하고 벡터화
    pairs = (
        corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        .stack()
        .reset_index()
    )
    pairs.columns = ["col_a", "col_b", "corr"]
    pairs["abs_corr"] = pairs["corr"].abs()
    pairs = pairs.sort_values("abs_corr", ascending=False).head(top_n).drop(columns=["abs_corr"])
    return pairs


def date_range_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    datetime 컬럼 요약:
    - min/max
    - 유니크 날짜 수
    """
    dt_cols = df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns.tolist()
    rows = []
    for col in dt_cols:
        s = df[col].dropna()
        if s.empty:
            continue
        rows.append(
            {
                "col": col,
                "min": s.min(),
                "max": s.max(),
                "n_unique": s.nunique(),
            }
        )
    return pd.DataFrame(rows)


def data_overview(
    df: pd.DataFrame,
    *,
    config: OverviewConfig = OverviewConfig(),
    key_cols: Optional[List[str]] = None,
    name: str = "dataset",
) -> Dict[str, pd.DataFrame]:
    """
    데이터 overview를 수행하고 결과를 DataFrame dict로 반환.
    key_cols: 중복 키 검사에 사용할 컬럼들(예: ["id"], ["user_id", "date"])
    """
    results: Dict[str, pd.DataFrame] = {}

    # 1) 기본 정보
    basic = pd.DataFrame(
        {
            "metric": ["rows", "cols"],
            "value": [len(df), df.shape[1]],
        }
    )
    results["basic"] = basic

    # 2) 스키마(결측치/카디널리티 포함)
    schema = summarize_schema(df)
    results["schema"] = schema

    # 3) 중복 행
    dup_rows = int(df.duplicated().sum())
    duplicates = pd.DataFrame({"duplicate_rows": [dup_rows], "duplicate_rate": [round(dup_rows / max(len(df), 1), 4)]})
    results["duplicates"] = duplicates

    # 4) 키 중복(선택)
    if key_cols:
        missing_keys = [c for c in key_cols if c not in df.columns]
        if missing_keys:
            key_check = pd.DataFrame({"warning": [f"key cols not found: {missing_keys}"]})
        else:
            key_dup = int(df.duplicated(subset=key_cols).sum())
            key_check = pd.DataFrame(
                {
                    "key_cols": [",".join(key_cols)],
                    "duplicate_keys": [key_dup],
                    "duplicate_key_rate": [round(key_dup / max(len(df), 1), 4)],
                }
            )
        results["key_check"] = key_check

    # 5) 수치형 통계 요약
    numeric = df.select_dtypes(include=[np.number])
    if not numeric.empty:
        desc = numeric.describe().T
        # describe()를 더 읽기 좋게
        desc = desc.rename(
            columns={"50%": "median"}
        ).round(4)
        results["numeric_describe"] = desc

        outlier_hints = detect_numeric_outlier_hints(df)
        results["numeric_outlier_hints"] = outlier_hints

    # 6) 범주형 top-k
    cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    # 너무 많은 컬럼이면 상위 일부만 (실무에서는 설정으로 제한하기도 함)
    cat_summary_rows = []
    for col in cat_cols[:20]:
        cat_summary_rows.append(
            {
                "col": col,
                "n_unique": int(df[col].nunique(dropna=True)),
                "na_rate": float((df[col].isna().mean()) if len(df) else 0.0),
            }
        )
    if cat_summary_rows:
        results["categorical_summary"] = pd.DataFrame(cat_summary_rows).sort_values(["na_rate", "n_unique"], ascending=[False, False])

    # 개별 top-k 빈도표는 separate dict key로 저장
    for col in cat_cols[:10]:
        results[f"topk_{col}"] = topk_categorical(df, col, k=config.top_k)

    # 7) datetime 요약(이미 datetime으로 파싱된 컬럼이 있을 때)
    dt_summary = date_range_summary(df)
    if not dt_summary.empty:
        results["datetime_summary"] = dt_summary

    # 8) 상관관계 top pair
    if config.show_corr and (df.select_dtypes(include=[np.number]).shape[1] >= 2):
        results["corr_top_pairs"] = correlation_top_pairs(df, top_n=config.corr_top_n)

    # 9) (선택) 리포트 저장
    if config.save_reports:
        ensure_dir(REPORT_DIR)
        for k, v in results.items():
            # 파일명 안전 처리
            safe_k = k.replace("/", "_")
            out_path = REPORT_DIR / f"{name}__{safe_k}.csv"
            try:
                v.to_csv(out_path, index=True)
            except Exception:
                # 일부 테이블은 index 처리 문제가 있을 수 있어 fallback
                v.reset_index().to_csv(out_path, index=False)

    return results


# -----------------------------------------
# 3) 실행 예시 (데모)
# -----------------------------------------
def main() -> None:
    """
    이 파일은 "어떤 DF든" 넣을 수 있게 설계.
    여기서는 데모로 간단 DF를 만든다.

    실사용 방법(권장)
    - CSV/Excel 로딩 후 df를 넘기기
    - SQL 로딩 후 df를 넘기기
    """
    demo = pd.DataFrame(
        {
            "user_id": [1, 2, 2, 3, 4, 4],
            "country": ["KR", "US", "US", "KR", None, "CA"],
            "amount": [10.0, 20.0, 20.0, 999.0, np.nan, 5.0],
            "event_time": pd.to_datetime(
                ["2026-01-01", "2026-01-02", "2026-01-02", "2026-01-03", "2026-01-10", "2026-01-10"]
            ),
        }
    )

    results = data_overview(
        demo,
        config=OverviewConfig(top_k=3, corr_top_n=5, save_reports=True),
        key_cols=["user_id", "event_time"],
        name="demo",
    )

    # 콘솔 출력(핵심만)
    print("\n=== BASIC ===")
    print(results["basic"])

    print("\n=== SCHEMA (TOP) ===")
    print(results["schema"].head(10))

    print("\n=== DUPLICATES ===")
    print(results["duplicates"])

    if "key_check" in results:
        print("\n=== KEY CHECK ===")
        print(results["key_check"])

    if "numeric_describe" in results:
        print("\n=== NUMERIC DESCRIBE ===")
        print(results["numeric_describe"])

    if "numeric_outlier_hints" in results:
        print("\n=== OUTLIER HINTS (IQR) ===")
        print(results["numeric_outlier_hints"])

    if "categorical_summary" in results:
        print("\n=== CATEGORICAL SUMMARY ===")
        print(results["categorical_summary"])

    if "corr_top_pairs" in results:
        print("\n=== CORR TOP PAIRS ===")
        print(results["corr_top_pairs"])

    print(f"\n[OK] Reports saved to: {REPORT_DIR}")


if __name__ == "__main__":
    main()