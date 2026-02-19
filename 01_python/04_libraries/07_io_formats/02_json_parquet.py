"""
Day 45 (Libraries — IO Formats): JSON/NDJSON & Parquet I/O

This module covers production-grade patterns for reading/writing JSON and Parquet
using pandas (and optional pyarrow).

핵심 목표:
- JSON/NDJSON(라인 단위 로그/이벤트)에 대한 실무형 로딩/저장
- Parquet(분석용 컬럼 기반 포맷)로의 변환/압축/파티셔닝(개념)
- 스키마/검증/원자적 저장(atomic write)로 안정성 확보
- "데이터는 저장소(SSD/iCloud/DB)에", repo에는 샘플/스키마/파이프라인만

주의:
- Parquet는 보통 `pyarrow` 또는 `fastparquet` 엔진이 필요합니다.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

import pandas as pd


# ============================================================
# 0) Configurations (실무형 옵션 고정)
# ============================================================

@dataclass(frozen=True)
class JSONReadConfig:
    """
    JSON/NDJSON 읽기 옵션.
    - NDJSON: line-delimited JSON (한 줄에 한 JSON 오브젝트)
    """
    encoding: str = "utf-8"
    lines: bool = False           # True면 NDJSON
    orient: Optional[str] = None  # pandas read_json의 orient 옵션 (필요 시)


@dataclass(frozen=True)
class JSONWriteConfig:
    """
    JSON 저장 옵션.
    - lines=True로 저장하면 NDJSON으로 저장됨 (로그/이벤트에 강력)
    """
    encoding: str = "utf-8"
    orient: str = "records"
    lines: bool = True
    force_ascii: bool = False
    indent: Optional[int] = None  # NDJSON이면 보통 None 추천


@dataclass(frozen=True)
class ParquetConfig:
    """
    Parquet 저장/읽기 옵션.
    - engine: 'pyarrow' 권장 (없으면 자동 fallback 시도)
    - compression: 'snappy' (기본), 'gzip', 'brotli', 'zstd' 등
    """
    engine: Optional[str] = None
    compression: str = "snappy"
    index: bool = False


# ============================================================
# 1) Utility: Path, Atomic Write, Validation
# ============================================================

def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def atomic_write_bytes(dst: Path, data: bytes) -> None:
    """
    원자적 저장(atomic write):
    - 임시 파일에 먼저 쓰고,
    - 마지막에 rename/replace로 교체
    -> 중간 실패 시 깨진 파일이 남지 않도록 방지
    """
    ensure_parent_dir(dst)
    tmp = dst.with_suffix(dst.suffix + ".tmp")

    with open(tmp, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())

    tmp.replace(dst)  # atomic on same filesystem


def validate_required_columns(df: pd.DataFrame, required: Sequence[str]) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """컬럼명 표준화: strip/lower/space->underscore"""
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df


# ============================================================
# 2) JSON / NDJSON: Read / Write
# ============================================================

def read_json_safely(path: Path, cfg: JSONReadConfig) -> pd.DataFrame:
    """
    JSON 또는 NDJSON(=lines=True)을 안전하게 읽는다.
    - NDJSON은 로그/이벤트 파이프라인에서 흔함.
    """
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")

    df = pd.read_json(
        path,
        encoding=cfg.encoding,
        lines=cfg.lines,
        orient=cfg.orient,
    )
    return df


def write_json_safely(df: pd.DataFrame, path: Path, cfg: JSONWriteConfig) -> None:
    """
    JSON/NDJSON 저장 (원자적 저장 적용).
    - 실무에서는 NDJSON(lines=True)이 디버깅/스트리밍에 유리.
    """
    ensure_parent_dir(path)

    # pandas to_json은 파일 경로로 바로 쓰는 것도 가능하지만,
    # atomic write를 위해 bytes로 만든 뒤 직접 저장한다.
    json_str = df.to_json(
        orient=cfg.orient,
        lines=cfg.lines,
        force_ascii=cfg.force_ascii,
        indent=cfg.indent,
    )
    atomic_write_bytes(path, json_str.encode(cfg.encoding))


def write_ndjson_records(records: Iterable[dict[str, Any]], path: Path, encoding: str = "utf-8") -> None:
    """
    pandas 없이도 NDJSON을 직접 쓰는 유틸.
    - 스트리밍/대용량 생성 시 유리 (한 줄씩 append 가능)
    """
    ensure_parent_dir(path)
    lines = []
    for r in records:
        lines.append(json.dumps(r, ensure_ascii=False))
    atomic_write_bytes(path, ("\n".join(lines) + "\n").encode(encoding))


# ============================================================
# 3) Parquet: Read / Write
# ============================================================

def _choose_parquet_engine(preferred: Optional[str] = None) -> str:
    """
    parquet engine 선택:
    - preferred가 있으면 우선 시도
    - 없으면 pyarrow -> fastparquet 순으로 시도
    """
    candidates = [preferred] if preferred else []
    candidates += ["pyarrow", "fastparquet"]

    for eng in candidates:
        if not eng:
            continue
        try:
            __import__(eng)
            return eng
        except Exception:
            continue

    raise RuntimeError(
        "No parquet engine available. Install one of: pyarrow, fastparquet."
    )


def write_parquet_safely(df: pd.DataFrame, path: Path, cfg: ParquetConfig) -> None:
    """
    Parquet 저장 (실무 권장 포맷).
    - 컬럼 기반, 압축 효율/쿼리 효율 좋음
    """
    ensure_parent_dir(path)
    engine = _choose_parquet_engine(cfg.engine)

    # pandas는 parquet에 대해 atomic write를 기본 제공하지 않음.
    # 따라서 임시 경로에 먼저 쓰고 교체하는 방식으로 안정성 강화.
    tmp = path.with_suffix(path.suffix + ".tmp")

    df.to_parquet(
        tmp,
        engine=engine,
        compression=cfg.compression,
        index=cfg.index,
    )
    tmp.replace(path)


def read_parquet_safely(path: Path, cfg: ParquetConfig) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Parquet file not found: {path}")

    engine = _choose_parquet_engine(cfg.engine)
    df = pd.read_parquet(path, engine=engine)
    return df


# ============================================================
# 4) Example Workflow: JSON -> Clean -> Parquet (Pipeline)
# ============================================================

def example_pipeline() -> None:
    """
    예시 파이프라인:
    - data/input/events.ndjson 를 읽고
    - 컬럼명 표준화 + 간단한 타입 정리 후
    - data/output/events.parquet 로 저장

    ⚠️ 레포에는 원본 대용량 데이터 업로드 금지 권장.
    - repo: schema/ (컬럼 정의), samples/ (소량 샘플), code (파이프라인)
    - raw data: 외장SSD/iCloud/DB/데이터레이크
    """
    project_root = Path(__file__).resolve().parents[5]  # .../study-languages
    input_ndjson = project_root / "data" / "input" / "events.ndjson"
    out_parquet = project_root / "data" / "output" / "events.parquet"
    out_json = project_root / "data" / "output" / "events_clean.ndjson"

    # 1) NDJSON 읽기
    cfg_read = JSONReadConfig(lines=True)
    try:
        df = read_json_safely(input_ndjson, cfg_read)
    except FileNotFoundError:
        print(f"[Skip] Example input not found: {input_ndjson}")
        print("Create a small NDJSON under data/input/events.ndjson to run this demo.")
        return

    # 2) 표준화
    df = normalize_columns(df)

    # (선택) 필수 컬럼 검증 예시
    # validate_required_columns(df, ["user_id", "event_time", "event_name"])

    # (선택) 타입 정리 예시: event_time을 datetime으로
    if "event_time" in df.columns:
        df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")

    # 3) 클린 NDJSON 저장 (디버깅/교환에 유리)
    cfg_write = JSONWriteConfig(lines=True, indent=None)
    write_json_safely(df, out_json, cfg_write)

    # 4) Parquet 저장 (분석/쿼리에 유리)
    pq_cfg = ParquetConfig(engine=None, compression="snappy", index=False)
    write_parquet_safely(df, out_parquet, pq_cfg)

    print("\n[Done]")
    print(f"- Saved cleaned NDJSON: {out_json}")
    print(f"- Saved Parquet       : {out_parquet}")

    # 5) Parquet 로드 확인
    df2 = read_parquet_safely(out_parquet, pq_cfg)
    print("\n[Parquet Preview]")
    print(df2.head())


if __name__ == "__main__":
    example_pipeline()