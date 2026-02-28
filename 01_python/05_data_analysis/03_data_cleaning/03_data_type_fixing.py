"""
Day 56 — Data Type Fixing (dtype normalization)
파일: 03_data_type_fixing.py

목표(실무 관점):
- 데이터 타입(dtypes)과 포맷(format)은 분석/모델링의 "전제조건"이다.
- 타입이 흔들리면 조인 실패, 집계 오류, 결측치 오판, 모델 입력 오류가 발생한다.
- 따라서 dtype fixing은 "수정"이 아니라 "정규화(normalization)" 단계로 다룬다.

핵심 기능:
1) 컬럼명 정규화(선택): 공백/대소문자/특수문자 처리
2) 숫자형 정규화: "1,234", "₩5,000", "(1,200)" 같은 문자열 → 숫자
3) 날짜/시간 정규화: 다양한 포맷 → datetime
4) 범주형 정규화: category 변환 + 희귀 카테고리 통합
5) 불리언 정규화: Yes/No, Y/N, 1/0, true/false 등 → bool
6) 결과 리포트: 변환 전/후 dtype, 변환 실패율(파싱 실패) 모니터링

주의:
- 이 파일은 외부 데이터 의존 없이도 실행 가능하도록 "데모 데이터"를 포함한다.
- 실제 프로젝트에서는 `fit/apply` 패턴(훈련 데이터에서 규칙 산출 후 테스트에 적용)을 권장한다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


# -----------------------------
# 0) 유틸: 컬럼명 정규화
# -----------------------------
def normalize_column_names(
    df: pd.DataFrame,
    *,
    lower: bool = True,
    replace_spaces: bool = True,
    keep: str = r"a-z0-9_",
) -> pd.DataFrame:
    """
    컬럼명 정규화 (선택 사항)
    - 실무에서는 컬럼명이 제각각(공백/대문자/특수문자)인 경우가 많음
    - 파이프라인 일관성을 위해 컬럼명을 통일해두면 에러가 크게 줄어듦
    """
    new_cols = []
    for c in df.columns:
        c2 = c.strip()
        if lower:
            c2 = c2.lower()
        if replace_spaces:
            c2 = re.sub(r"\s+", "_", c2)
        # 허용 문자만 남기고 나머지는 언더스코어로 치환
        c2 = re.sub(fr"[^{keep}]+", "_", c2)
        c2 = re.sub(r"_+", "_", c2).strip("_")
        new_cols.append(c2)

    out = df.copy()
    out.columns = new_cols
    return out


# -----------------------------
# 1) 숫자형 문자열 → 숫자 파서
# -----------------------------
_CURRENCY_RE = re.compile(r"[₩$€£, ]+")
_PARENS_NEG_RE = re.compile(r"^\((.*)\)$")


def coerce_numeric_series(s: pd.Series) -> Tuple[pd.Series, float]:
    """
    문자열 기반 숫자(통화/콤마/괄호 음수 등)를 안전하게 숫자(float)로 변환.
    반환:
      - 변환된 시리즈(float)
      - 파싱 실패율(0~1)

    예:
      "1,234" -> 1234
      "₩5,000" -> 5000
      "(1,200)" -> -1200
      "N/A" -> NaN
    """
    raw = s.astype("string")

    def _to_number(x: str) -> Optional[float]:
        if x is None:
            return None
        x = str(x).strip()
        if x == "" or x.lower() in {"na", "n/a", "null", "none", "nan", "-"}:
            return None

        # 괄호 음수 처리: (1200) => -1200
        m = _PARENS_NEG_RE.match(x)
        if m:
            x = "-" + m.group(1)

        # 통화/콤마/공백 제거
        x = _CURRENCY_RE.sub("", x)

        # 퍼센트 처리: "12.3%" => 0.123 (분석 목적에 따라 12.3으로 둘 수도 있음)
        is_pct = x.endswith("%")
        if is_pct:
            x = x[:-1]

        # 숫자만 남기기(소수점/부호 허용)
        x = re.sub(r"[^0-9.\-+eE]", "", x)

        try:
            val = float(x)
            if is_pct:
                val = val / 100.0
            return val
        except ValueError:
            return None

    converted = raw.map(_to_number).astype("float64")
    fail_rate = float(converted.isna().mean())
    return converted, fail_rate


# -----------------------------
# 2) 날짜/시간 파서
# -----------------------------
def coerce_datetime_series(
    s: pd.Series,
    *,
    utc: bool = False,
    dayfirst: bool = False,
) -> Tuple[pd.Series, float]:
    """
    다양한 포맷의 날짜 문자열을 datetime으로 안전 변환.
    - errors='coerce'로 실패는 NaT 처리 (실무에서 안전)
    - 파싱 실패율을 함께 반환하여 품질 모니터링

    dayfirst=True는 '31/12/2025' 같은 포맷에 유리
    """
    raw = s.astype("string")
    dt = pd.to_datetime(raw, errors="coerce", utc=utc, dayfirst=dayfirst)
    fail_rate = float(dt.isna().mean())
    return dt, fail_rate


# -----------------------------
# 3) 불리언 파서
# -----------------------------
_TRUE_SET = {"true", "t", "yes", "y", "1", "on"}
_FALSE_SET = {"false", "f", "no", "n", "0", "off"}


def coerce_bool_series(s: pd.Series) -> Tuple[pd.Series, float]:
    """
    다양한 표현을 bool로 통일.
    - "Y", "Yes", 1, "true" => True
    - "N", "No", 0, "false" => False
    - 그 외는 NaN(결측) 처리

    반환:
      - pandas BooleanDtype 시리즈 (True/False/<NA>)
      - 실패율
    """
    raw = s.astype("string")

    def _to_bool(x: str):
        if x is None:
            return pd.NA
        x = str(x).strip().lower()
        if x == "" or x in {"na", "n/a", "null", "none", "nan"}:
            return pd.NA
        if x in _TRUE_SET:
            return True
        if x in _FALSE_SET:
            return False
        return pd.NA

    out = raw.map(_to_bool).astype("boolean")
    fail_rate = float(out.isna().mean())
    return out, fail_rate


# -----------------------------
# 4) 범주형 정규화 (희귀값 통합)
# -----------------------------
def coerce_category_series(
    s: pd.Series,
    *,
    lowercase: bool = True,
    strip: bool = True,
    min_freq: int = 1,
    other_label: str = "Other",
) -> pd.Series:
    """
    범주형 데이터를 category로 변환하고, 희귀 카테고리를 Other로 통합.
    - 실무에서 high-cardinality(카테고리 너무 많음)는 모델/리포트에 악영향
    - 최소 빈도(min_freq) 미만은 Other로 통합하여 안정성 확보
    """
    raw = s.astype("string")
    if strip:
        raw = raw.str.strip()
    if lowercase:
        raw = raw.str.lower()

    # 결측은 그대로 둠
    vc = raw.value_counts(dropna=True)
    rare = vc[vc < min_freq].index
    normalized = raw.where(~raw.isin(rare), other_label)
    return normalized.astype("category")


# -----------------------------
# 5) 전체 dtype fixing 스펙
# -----------------------------
@dataclass(frozen=True)
class DTypeFixSpec:
    """
    dtype fixing 스펙 (정규화 규칙)
    - numeric_cols: 문자열/혼합형 숫자 컬럼 목록
    - datetime_cols: 날짜/시간 컬럼 목록
    - bool_cols: 불리언 컬럼 목록
    - category_cols: 범주형 컬럼 목록
    """
    numeric_cols: Tuple[str, ...] = ()
    datetime_cols: Tuple[str, ...] = ()
    bool_cols: Tuple[str, ...] = ()
    category_cols: Tuple[str, ...] = ()
    dayfirst_for_datetime: bool = False
    utc_for_datetime: bool = False
    category_min_freq: int = 1


def fix_dtypes(
    df: pd.DataFrame,
    spec: DTypeFixSpec,
    *,
    normalize_cols: bool = False,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    df에 대해 dtype fixing을 수행하고 리포트(변환 결과 요약)를 반환.

    반환:
      - fixed_df: 변환이 적용된 데이터프레임
      - report: 컬럼별 (before_dtype, after_dtype, fail_rate 등) 요약표

    실무 팁:
    - 이 함수는 "apply" 단계에 해당.
    - 대규모 파이프라인에서는 train에서 통계/룰을 fit하고
      test/serving에서 동일 룰을 apply하는 구조를 추천.
    """
    work = df.copy()
    if normalize_cols:
        work = normalize_column_names(work)

    rows: List[Dict[str, object]] = []

    def _add_report(col: str, before: str, after: str, fail_rate: Optional[float], note: str):
        rows.append(
            {
                "column": col,
                "before_dtype": before,
                "after_dtype": after,
                "parse_fail_rate": fail_rate,
                "note": note,
            }
        )

    # 숫자형 처리
    for col in spec.numeric_cols:
        if col not in work.columns:
            _add_report(col, "-", "-", None, "SKIP: column not found")
            continue
        before = str(work[col].dtype)
        converted, fail_rate = coerce_numeric_series(work[col])
        work[col] = converted
        after = str(work[col].dtype)
        _add_report(col, before, after, fail_rate, "numeric coercion (currency/commas/parentheses/percent)")

    # datetime 처리
    for col in spec.datetime_cols:
        if col not in work.columns:
            _add_report(col, "-", "-", None, "SKIP: column not found")
            continue
        before = str(work[col].dtype)
        converted, fail_rate = coerce_datetime_series(
            work[col], utc=spec.utc_for_datetime, dayfirst=spec.dayfirst_for_datetime
        )
        work[col] = converted
        after = str(work[col].dtype)
        _add_report(col, before, after, fail_rate, "datetime coercion (errors->NaT)")

    # bool 처리
    for col in spec.bool_cols:
        if col not in work.columns:
            _add_report(col, "-", "-", None, "SKIP: column not found")
            continue
        before = str(work[col].dtype)
        converted, fail_rate = coerce_bool_series(work[col])
        work[col] = converted
        after = str(work[col].dtype)
        _add_report(col, before, after, fail_rate, "boolean coercion (y/n/yes/no/1/0/true/false)")

    # category 처리
    for col in spec.category_cols:
        if col not in work.columns:
            _add_report(col, "-", "-", None, "SKIP: column not found")
            continue
        before = str(work[col].dtype)
        work[col] = coerce_category_series(work[col], min_freq=spec.category_min_freq)
        after = str(work[col].dtype)
        _add_report(col, before, after, None, f"category coercion (min_freq={spec.category_min_freq})")

    report = pd.DataFrame(rows).sort_values("column").reset_index(drop=True)
    return work, report


# -----------------------------
# 6) 데모 실행 (외부 데이터 없이 실행 가능)
# -----------------------------
def build_demo_df() -> pd.DataFrame:
    """데모용 데이터프레임 생성 (실무에서 자주 나오는 dirty 패턴 포함)"""
    return pd.DataFrame(
        {
            "Order ID": ["A-001", "A-002", "A-003", "A-004"],
            "Amount": ["₩1,200", "(3,500)", "12.5%", "N/A"],
            "OrderDate": ["2026-01-01", "01/02/2026", "2026.03.05", "invalid-date"],
            "IsMember": ["Y", "no", "1", "unknown"],
            "City": ["Seoul", "Seoul", "Busan", "VeryRareCity"],
        }
    )


def main() -> None:
    df = build_demo_df()

    # 한국어 설명:
    # - normalize_cols=True로 컬럼명을 정규화하면,
    #   "Order ID" -> "order_id" 처럼 파이프라인에서 쓰기 쉬워진다.
    df2 = normalize_column_names(df, lower=True, replace_spaces=True)

    # dtype fixing 스펙 정의
    spec = DTypeFixSpec(
        numeric_cols=("amount",),
        datetime_cols=("orderdate",),
        bool_cols=("ismember",),
        category_cols=("city",),
        dayfirst_for_datetime=False,   # "01/02/2026"을 월/일로 볼지 일/월로 볼지 데이터에 맞춰 결정
        utc_for_datetime=False,
        category_min_freq=2,           # 2회 미만 등장 카테고리는 Other로 통합
    )

    fixed, report = fix_dtypes(df2, spec, normalize_cols=False)

    print("\n[원본]")
    print(df2)
    print("\n[dtypes - before]")
    print(df2.dtypes)

    print("\n[변환 후]")
    print(fixed)
    print("\n[dtypes - after]")
    print(fixed.dtypes)

    print("\n[변환 리포트]")
    print(report.to_string(index=False))


if __name__ == "__main__":
    main()