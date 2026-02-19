"""
Day 46 (Libraries — IO Formats): SQL Read/Write with pandas

This module covers production-grade patterns to read/write data between
SQL databases and pandas.

핵심 목표:
- pandas.read_sql_query / DataFrame.to_sql 실무 패턴
- 파라미터 바인딩(보안), 트랜잭션, 스키마 검증
- 대용량 처리(chunk), 멱등(idempotent)한 테이블 생성/삽입 전략
- "데이터는 DB/SSD/iCloud에, repo에는 스키마/샘플/파이프라인 코드만"

주의:
- 범용적으로 동작하도록 기본은 sqlite3 기반(추가 설치 없이 실행 가능)
- Postgres/MySQL도 SQLAlchemy URL만 바꾸면 동일 패턴 적용 가능(설명 포함)
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

import pandas as pd


# ============================================================
# 0) Configuration
# ============================================================

@dataclass(frozen=True)
class DBConfig:
    """
    DB 연결 설정.
    - 기본: sqlite (로컬 파일 DB) -> 설치 없이 바로 실행 가능
    """
    db_path: Path  # sqlite 파일 경로


@dataclass(frozen=True)
class WriteConfig:
    """
    DataFrame -> SQL 테이블 저장 옵션.
    - if_exists: 'fail'|'replace'|'append'
    - chunksize: 대용량 insert 시 배치 크기
    """
    table: str
    if_exists: str = "append"
    index: bool = False
    chunksize: int = 1000


# ============================================================
# 1) Utilities: schema validation, safe table naming
# ============================================================

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


def assert_safe_identifier(name: str) -> None:
    """
    테이블/컬럼 이름은 외부 입력으로 받지 않는 게 원칙.
    그래도 혹시라도 받을 경우 최소한의 검증을 한다.
    (SQL injection은 값 바인딩으로 막고, 식별자는 별도 검증 필요)
    """
    if not name.replace("_", "").isalnum():
        raise ValueError(f"Unsafe SQL identifier: {name}")


# ============================================================
# 2) Connection / Transaction patterns
# ============================================================

def connect_sqlite(cfg: DBConfig) -> sqlite3.Connection:
    """
    sqlite 연결:
    - detect_types 옵션으로 날짜 타입 처리도 가능하지만, 여기선 단순화
    - foreign_keys는 sqlite에서 기본 off라서 on 권장
    """
    cfg.db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(cfg.db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# ============================================================
# 3) Read patterns (safe parameter binding)
# ============================================================

def read_query(
    conn: sqlite3.Connection,
    query: str,
    params: Optional[dict[str, Any]] = None,
) -> pd.DataFrame:
    """
    안전한 조회:
    - params를 통해 바인딩 (문자열 format 금지)
    - 예: WHERE user_id = :user_id
    """
    df = pd.read_sql_query(query, conn, params=params)
    return df


def read_in_chunks(
    conn: sqlite3.Connection,
    query: str,
    params: Optional[dict[str, Any]] = None,
    chunksize: int = 10000,
) -> Iterable[pd.DataFrame]:
    """
    대용량 조회:
    - chunksize 단위로 DataFrame iterator 반환
    - 메모리 부담이 큰 테이블에서 유용
    """
    return pd.read_sql_query(query, conn, params=params, chunksize=chunksize)


# ============================================================
# 4) Write patterns (to_sql with chunking)
# ============================================================

def write_dataframe(
    conn: sqlite3.Connection,
    df: pd.DataFrame,
    cfg: WriteConfig,
) -> None:
    """
    DataFrame -> SQL 저장:
    - chunksize로 배치 insert
    - if_exists 전략:
      - 'append': 누적 적재
      - 'replace': 테이블 갈아엎기(주의)
      - 'fail': 존재하면 에러
    """
    assert_safe_identifier(cfg.table)
    df.to_sql(
        cfg.table,
        conn,
        if_exists=cfg.if_exists,
        index=cfg.index,
        chunksize=cfg.chunksize,
        method="multi",  # sqlite에서도 동작(버전에 따라 일부 제한 가능)
    )


# ============================================================
# 5) Example workflow (runs with sqlite)
# ============================================================

def example_sql_workflow() -> None:
    """
    실행 가능한 데모:
    1) 샘플 이벤트 데이터를 DataFrame으로 생성
    2) sqlite 테이블에 적재
    3) 파라미터 바인딩으로 안전 조회
    4) chunk read 데모 (규모가 작으면 chunk 1번만 나옴)

    ✅ 이 데모는 외부 DB 없이도 재현 가능해야 하므로 sqlite 기반으로 설계.
    """
    project_root = Path(__file__).resolve().parents[5]  # .../study-languages
    db_file = project_root / "data" / "sqlite" / "demo.db"

    db_cfg = DBConfig(db_path=db_file)

    # (1) 샘플 데이터 생성
    raw = pd.DataFrame(
        {
            "user_id": [1, 1, 2, 3, 3],
            "event_time": [
                "2026-01-01 10:00:00",
                "2026-01-01 10:05:00",
                "2026-01-01 11:00:00",
                "2026-01-02 09:00:00",
                "2026-01-02 09:10:00",
            ],
            "event_name": ["page_view", "click", "page_view", "page_view", "purchase"],
            "value": [None, None, None, None, 120.0],
        }
    )

    df = normalize_columns(raw)
    df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")

    # 스키마 최소 검증(실무에서는 더 강하게)
    validate_required_columns(df, ["user_id", "event_time", "event_name"])

    # (2) DB 연결 + 트랜잭션(원자적 적재)
    conn = connect_sqlite(db_cfg)
    try:
        with conn:  # sqlite: with 블록이 트랜잭션(자동 commit/rollback)
            write_dataframe(
                conn,
                df,
                WriteConfig(table="events", if_exists="append", chunksize=1000),
            )

        # (3) 안전 조회: user_id = 3만
        q = """
        SELECT
            user_id,
            event_time,
            event_name,
            value
        FROM events
        WHERE user_id = :user_id
        ORDER BY event_time ASC
        """
        out = read_query(conn, q, params={"user_id": 3})
        print("\n[Query Result: user_id=3]")
        print(out)

        # (4) 대용량 chunk read 패턴(여기선 소량 데이터라 데모 수준)
        q_all = "SELECT * FROM events ORDER BY event_time ASC"
        print("\n[Chunk Read Demo]")
        for i, chunk in enumerate(read_in_chunks(conn, q_all, chunksize=2), start=1):
            print(f"\n-- chunk {i} --")
            print(chunk)

        # (5) 간단 집계 예시
        q_agg = """
        SELECT
            event_name,
            COUNT(*) AS cnt
        FROM events
        GROUP BY event_name
        ORDER BY cnt DESC
        """
        agg = read_query(conn, q_agg)
        print("\n[Aggregation]")
        print(agg)

    finally:
        conn.close()


# ============================================================
# 6) Notes: how to extend to Postgres/MySQL (Conceptual)
# ============================================================

def notes_for_real_databases() -> None:
    """
    실무 확장 메모(코드 실행용 아님):

    - Postgres/MySQL 등은 sqlite3 대신 SQLAlchemy 엔진 사용 권장.
    - 예:
        from sqlalchemy import create_engine
        engine = create_engine("postgresql+psycopg2://user:pw@host:5432/db")
        df = pd.read_sql_query("SELECT ... WHERE id = %(id)s", engine, params={"id": 1})
        df.to_sql("table", engine, if_exists="append", index=False, chunksize=5000, method="multi")

    - 운영 환경에서는:
        1) connection pooling
        2) role-based access control (read-only 계정 등)
        3) migration tool(Alembic)로 schema 관리
        4) 데이터 검증(great expectations 등)
      같은 개념을 추가하면 좋다.
    """
    pass


if __name__ == "__main__":
    example_sql_workflow()