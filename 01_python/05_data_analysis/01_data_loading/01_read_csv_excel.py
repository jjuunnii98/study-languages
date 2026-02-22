"""
Day 47: Data Loading (CSV/Excel) — pandas I/O 실무 패턴

목표
- CSV/Excel 파일을 "실무 수준"으로 안전하게 읽는다.
- dtype 지정, 날짜 파싱, 결측치 처리, 인코딩 문제 대응, 대용량 chunk 로딩 등
  현실에서 자주 터지는 이슈를 예방한다.

주의
- 이 파일은 "예제 코드"이므로, 실제 데이터 경로는 프로젝트 환경에 맞게 변경하세요.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, Union

import pandas as pd


# -----------------------------
# 0) 설정: 샘플 경로/옵션
# -----------------------------
# ✅ 프로젝트 구조에 맞게 data 폴더를 만들어 두는 것을 권장합니다.
# 예: 01_python/05_data_analysis/01_data_loading/data/raw/ ...
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"  # 필요하면 폴더 생성해서 사용


@dataclass(frozen=True)
class ReadConfig:
    """CSV/Excel 로딩 시 공통 옵션을 구조화 (재사용/테스트 용이)."""

    encoding_candidates: Tuple[str, ...] = ("utf-8", "utf-8-sig", "cp949", "euc-kr")
    # dtype은 컬럼별로 지정하는 것을 추천 (특히 id, code 컬럼은 문자열로!)
    dtype_map: Optional[Dict[str, str]] = None
    # 날짜 파싱이 필요한 컬럼이 있으면 여기에 지정
    parse_dates: Optional[List[str]] = None
    # 결측치로 처리할 문자열 패턴들
    na_values: Tuple[str, ...] = ("", "NA", "N/A", "null", "NULL", "None", "-")
    # 메모리 절약 옵션(대부분 기본값 True 권장)
    low_memory: bool = False


# -----------------------------
# 1) 유틸: 파일 존재 체크
# -----------------------------
def ensure_exists(path: Path) -> None:
    """파일 존재 여부 확인. 없으면 친절한 에러를 던진다."""
    if not path.exists():
        raise FileNotFoundError(
            f"파일을 찾을 수 없습니다: {path}\n"
            f"- 경로를 확인하세요.\n"
            f"- 예: DATA_DIR={DATA_DIR}\n"
            f"- 필요한 경우 data 폴더에 파일을 넣고 다시 실행하세요."
        )


# -----------------------------
# 2) CSV 안전 로더 (인코딩 fallback 포함)
# -----------------------------
def read_csv_safely(
    path: Union[str, Path],
    config: ReadConfig,
    *,
    usecols: Optional[List[str]] = None,
    sep: str = ",",
) -> pd.DataFrame:
    """
    CSV를 안전하게 읽는 함수.

    핵심 포인트
    - 인코딩 문제(utf-8/cp949/euc-kr)를 후보군으로 순차 시도
    - dtype 지정으로 ID/코드 컬럼 손상 방지
    - parse_dates로 날짜 컬럼 자동 변환
    - na_values로 결측치 통일
    """
    path = Path(path)
    ensure_exists(path)

    last_err: Optional[Exception] = None

    for enc in config.encoding_candidates:
        try:
            df = pd.read_csv(
                path,
                sep=sep,
                encoding=enc,
                dtype=config.dtype_map,
                parse_dates=config.parse_dates,
                na_values=list(config.na_values),
                usecols=usecols,
                low_memory=config.low_memory,
            )
            # ✅ 성공하면 어떤 인코딩으로 읽었는지 기록(로그)
            print(f"[OK] CSV loaded with encoding='{enc}' | shape={df.shape}")
            return df
        except Exception as e:  # 인코딩 에러/파싱 에러 등 포괄
            last_err = e

    raise ValueError(
        f"CSV 로딩 실패: {path}\n"
        f"- 시도한 인코딩: {config.encoding_candidates}\n"
        f"- 마지막 에러: {last_err}"
    )


# -----------------------------
# 3) 대용량 CSV: chunk 로딩 패턴
# -----------------------------
def read_csv_in_chunks(
    path: Union[str, Path],
    config: ReadConfig,
    *,
    chunksize: int = 100_000,
    sep: str = ",",
) -> pd.DataFrame:
    """
    대용량 CSV를 chunksize 단위로 읽어 누적 처리하는 예시.

    실무 팁
    - 정말 큰 파일이면 "전부 concat"이 아니라, chunk 단위로 집계/필터링 후 결과만 저장하는 방식 권장
    """
    path = Path(path)
    ensure_exists(path)

    # 인코딩 fallback은 read_csv_safely와 동일 전략을 chunk에도 적용
    last_err: Optional[Exception] = None

    for enc in config.encoding_candidates:
        try:
            chunks: List[pd.DataFrame] = []
            reader = pd.read_csv(
                path,
                sep=sep,
                encoding=enc,
                dtype=config.dtype_map,
                parse_dates=config.parse_dates,
                na_values=list(config.na_values),
                chunksize=chunksize,
                low_memory=config.low_memory,
            )

            for i, chunk in enumerate(reader, start=1):
                # ✅ 예시: chunk에서 간단 정제 (필요시 커스텀)
                chunk = chunk.drop_duplicates()
                chunks.append(chunk)
                if i % 5 == 0:
                    print(f"[INFO] processed chunks={i} | current_rows={sum(c.shape[0] for c in chunks):,}")

            df = pd.concat(chunks, ignore_index=True)
            print(f"[OK] Chunk CSV loaded with encoding='{enc}' | shape={df.shape}")
            return df

        except Exception as e:
            last_err = e

    raise ValueError(
        f"Chunk CSV 로딩 실패: {path}\n"
        f"- 시도한 인코딩: {config.encoding_candidates}\n"
        f"- 마지막 에러: {last_err}"
    )


# -----------------------------
# 4) Excel 로더 (시트/범위/헤더)
# -----------------------------
def read_excel_safely(
    path: Union[str, Path],
    config: ReadConfig,
    *,
    sheet_name: Union[str, int, None] = 0,
    usecols: Optional[str] = None,
) -> pd.DataFrame:
    """
    Excel을 안전하게 읽는 함수.

    핵심 포인트
    - sheet_name 지정 가능 (0, "Sheet1", None(전체시트 dict))
    - usecols로 필요한 범위만 로딩해서 성능 개선
    - dtype/parse_dates/na_values 적용
    """
    path = Path(path)
    ensure_exists(path)

    df = pd.read_excel(
        path,
        sheet_name=sheet_name,
        dtype=config.dtype_map,
        parse_dates=config.parse_dates,
        na_values=list(config.na_values),
        usecols=usecols,
        engine=None,  # pandas가 자동 선택
    )

    # sheet_name=None이면 dict[str, DataFrame]가 반환되므로 처리 분기
    if isinstance(df, dict):
        print(f"[OK] Excel loaded (all sheets) | sheets={list(df.keys())}")
        # 예시: 첫 시트만 반환하거나, dict 그대로 반환하도록 변경 가능
        first_sheet = next(iter(df.values()))
        print(f"[INFO] returning first sheet only | shape={first_sheet.shape}")
        return first_sheet

    print(f"[OK] Excel loaded | sheet={sheet_name} | shape={df.shape}")
    return df


# -----------------------------
# 5) 실무용 “표준 로딩” 템플릿
# -----------------------------
def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    컬럼명 표준화(실무에서 정말 자주 함).
    - 공백 제거
    - 소문자화
    - 특수문자/공백을 '_'로 치환
    """
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^a-z0-9_]+", "", regex=True)
    )
    return df


def quick_profile(df: pd.DataFrame, n: int = 5) -> None:
    """로딩 직후 빠르게 품질 확인(행/열/결측/타입/샘플)."""
    print("\n=== QUICK PROFILE ===")
    print(f"shape: {df.shape}")
    print("\n-- dtypes --")
    print(df.dtypes)
    print("\n-- missing (top 10) --")
    print(df.isna().sum().sort_values(ascending=False).head(10))
    print("\n-- head --")
    print(df.head(n))


# -----------------------------
# 6) 실행 예시 (샘플)
# -----------------------------
def main() -> None:
    # ✅ 예: ID 컬럼은 문자열로 고정(앞자리 0 손실 방지)
    config = ReadConfig(
        dtype_map={
            # "user_id": "string",
            # "product_code": "string",
        },
        parse_dates=[
            # "created_at",
            # "order_date",
        ],
    )

    # ===== CSV 예시 =====
    csv_path = DATA_DIR / "sample.csv"  # 실제 파일명으로 변경
    if csv_path.exists():
        df_csv = read_csv_safely(csv_path, config)
        df_csv = standardize_columns(df_csv)
        quick_profile(df_csv)

    # ===== Excel 예시 =====
    excel_path = DATA_DIR / "sample.xlsx"  # 실제 파일명으로 변경
    if excel_path.exists():
        df_xlsx = read_excel_safely(excel_path, config, sheet_name=0)
        df_xlsx = standardize_columns(df_xlsx)
        quick_profile(df_xlsx)

    # ===== Chunk 예시(대용량) =====
    big_csv_path = DATA_DIR / "big_sample.csv"
    if big_csv_path.exists():
        df_big = read_csv_in_chunks(big_csv_path, config, chunksize=50_000)
        df_big = standardize_columns(df_big)
        quick_profile(df_big)

    if not any(p.exists() for p in [csv_path, excel_path, big_csv_path]):
        print(
            "\n[INFO] 실행할 샘플 데이터가 없습니다.\n"
            f"- 폴더에 샘플 파일을 넣어주세요: {DATA_DIR}\n"
            "- 예: sample.csv / sample.xlsx"
        )


if __name__ == "__main__":
    main()