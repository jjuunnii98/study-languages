"""
Day 44 (Libraries — IO Formats): CSV & Excel I/O

This module covers production-grade patterns for reading/writing CSV and Excel
using pandas.

핵심 목표:
- CSV/Excel을 "그냥 읽고 쓰기"가 아니라,
  실무에서 필요한 안정성(검증/에러처리), 재현성(옵션 고정),
  그리고 파이프라인화(유틸 함수)까지 포함해 설계한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

import pandas as pd


# ============================================================
# 0) Configuration (실무형 옵션 고정)
# ============================================================

@dataclass(frozen=True)
class CSVReadConfig:
    """
    CSV 읽기 옵션을 명시적으로 고정해서 재현성을 높인다.
    """
    encoding: str = "utf-8"
    sep: str = ","
    na_values: tuple[str, ...] = ("", "NA", "N/A", "null", "None")
    keep_default_na: bool = True
    low_memory: bool = False  # dtype 추론 안정성 (대신 메모리 조금 더)
    parse_dates: Optional[Sequence[str]] = None


@dataclass(frozen=True)
class CSVWriteConfig:
    """
    CSV 저장 옵션을 명시적으로 고정해서 결과 파일의 일관성을 유지한다.
    """
    encoding: str = "utf-8"
    sep: str = ","
    index: bool = False
    line_terminator: str = "\n"


# ============================================================
# 1) Utility: Path & Validation
# ============================================================

def ensure_parent_dir(path: Path) -> None:
    """저장 경로의 상위 디렉토리를 보장한다."""
    path.parent.mkdir(parents=True, exist_ok=True)


def validate_required_columns(df: pd.DataFrame, required: Sequence[str]) -> None:
    """필수 컬럼이 누락되면 즉시 실패하게 만들어 데이터 품질을 보호한다."""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def preview(df: pd.DataFrame, n: int = 5) -> None:
    """콘솔에서 빠르게 구조를 확인하는 실무용 프리뷰."""
    print("\n[Preview]")
    print(df.head(n))
    print("\n[Info]")
    print(df.info())
    print("\n[Describe]")
    # 숫자형이 없을 수 있으니 errors='ignore'처럼 안전하게 처리
    try:
        print(df.describe(include="all"))
    except Exception as e:
        print(f"describe() failed: {e}")


# ============================================================
# 2) CSV: Read / Write (실무형)
# ============================================================

def read_csv_safely(path: Path, cfg: CSVReadConfig, dtype: Optional[dict] = None) -> pd.DataFrame:
    """
    안정적으로 CSV를 읽는다.
    - encoding, NA 처리, 날짜 파싱 등을 통일
    - dtype을 외부에서 주입 가능 (권장: 스키마를 명시하는 습관)
    """
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    df = pd.read_csv(
        path,
        encoding=cfg.encoding,
        sep=cfg.sep,
        na_values=cfg.na_values,
        keep_default_na=cfg.keep_default_na,
        low_memory=cfg.low_memory,
        parse_dates=list(cfg.parse_dates) if cfg.parse_dates else None,
        dtype=dtype,
    )
    return df


def write_csv_safely(df: pd.DataFrame, path: Path, cfg: CSVWriteConfig) -> None:
    """
    안정적으로 CSV 저장.
    - 저장 경로 생성
    - 인덱스 저장 여부 통일 (실무에서는 대부분 index=False)
    """
    ensure_parent_dir(path)
    df.to_csv(
        path,
        encoding=cfg.encoding,
        sep=cfg.sep,
        index=cfg.index,
        lineterminator=cfg.line_terminator,
    )


# ============================================================
# 3) Excel: Read / Write + Sheet Handling
# ============================================================

def read_excel_safely(
    path: Path,
    sheet_name: str | int = 0,
    engine: Optional[str] = None,
    parse_dates: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """
    Excel을 안전하게 읽는다.
    - sheet_name: 시트명 또는 인덱스
    - parse_dates: 날짜 컬럼을 명시적으로 파싱 (가능하면 권장)
    """
    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")

    df = pd.read_excel(
        path,
        sheet_name=sheet_name,
        engine=engine,
        parse_dates=list(parse_dates) if parse_dates else None,
    )
    return df


def write_excel_safely(
    df: pd.DataFrame,
    path: Path,
    sheet_name: str = "data",
    index: bool = False,
) -> None:
    """
    Excel 저장 (실무 패턴)
    - 저장 경로 생성
    - sheet_name 지정
    """
    ensure_parent_dir(path)
    with pd.ExcelWriter(path) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=index)


def list_excel_sheets(path: Path) -> list[str]:
    """
    Excel 파일의 시트 목록을 확인 (데이터 탐색/검증에 유용)
    """
    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")

    xls = pd.ExcelFile(path)
    return xls.sheet_names


# ============================================================
# 4) Example Workflow (샘플 파이프라인)
# ============================================================

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    컬럼명을 표준화하는 간단한 전처리 예시.
    - 공백 제거, 소문자화, 공백을 언더스코어로
    """
    df = df.copy()
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df


def main() -> None:
    """
    실행 예시:
    - data/input/sample.csv 를 읽어서
    - 컬럼명 표준화 후
    - data/output/cleaned.csv 와 data/output/cleaned.xlsx 로 저장

    ⚠️ 실제 레포에는 대용량 원본 데이터를 올리지 않는 것을 권장.
    (data/에 .gitkeep, samples/에 소량 샘플 + schema/에 스키마)
    """

    # 예시 경로 (프로젝트 구조에 맞춰 조정)
    project_root = Path(__file__).resolve().parents[5]  # .../study-languages 까지
    input_csv = project_root / "data" / "input" / "sample.csv"
    output_csv = project_root / "data" / "output" / "cleaned.csv"
    output_xlsx = project_root / "data" / "output" / "cleaned.xlsx"

    # CSV 읽기
    read_cfg = CSVReadConfig(parse_dates=None)
    try:
        df = read_csv_safely(input_csv, read_cfg)
    except FileNotFoundError:
        print(f"[Skip] Example input not found: {input_csv}")
        print("Create a small sample CSV under data/input/sample.csv to run this demo.")
        return

    # 기본 검증 (필요시 required 컬럼 리스트 작성)
    # validate_required_columns(df, required=["id", "created_at"])

    # 컬럼 표준화
    df2 = normalize_columns(df)

    # 프리뷰
    preview(df2)

    # CSV/Excel 저장
    write_cfg = CSVWriteConfig()
    write_csv_safely(df2, output_csv, write_cfg)
    write_excel_safely(df2, output_xlsx, sheet_name="cleaned", index=False)

    print("\n[Done]")
    print(f"- Saved CSV : {output_csv}")
    print(f"- Saved XLSX: {output_xlsx}")

    # Excel sheet list example (output 확인)
    sheets = list_excel_sheets(output_xlsx)
    print(f"- Excel sheets: {sheets}")


if __name__ == "__main__":
    main()