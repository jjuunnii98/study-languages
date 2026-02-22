"""
Day 48: Data Loading (SQL) — pandas + SQL 실무 패턴

목표
- pandas로 SQL 데이터를 안전하게 읽는 표준 패턴을 익힌다.
- 파라미터 바인딩(보안), 트랜잭션, 스키마/테이블 확인,
  chunk 로딩(대용량), 인덱스 설계 등 실무 요소를 포함한다.

구현 전략
- 외부 DB 의존성 없이도 실행되도록 SQLite를 사용한다 (표준 라이브러리).
- 실제 실무에서는 SQLAlchemy + Postgres/MySQL로 쉽게 확장 가능하다.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import pandas as pd


# -----------------------------------------
# 0) 경로/설정
# -----------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "demo.sqlite3"


@dataclass(frozen=True)
class SQLReadConfig:
    """SQL 읽기 옵션을 구조화해서 재사용/테스트 가능하게."""

    # read_sql_query chunksize (대용량 처리)
    chunksize: Optional[int] = None

    # pandas dtype 지정 (필요시)
    dtype_map: Optional[Dict[str, str]] = None

    # 날짜 파싱
    parse_dates: Optional[List[str]] = None


def ensure_dir(path: Path) -> None:
    """폴더가 없으면 생성."""
    path.mkdir(parents=True, exist_ok=True)


# -----------------------------------------
# 1) SQLite 연결(컨텍스트) + 기본 안전 규칙
# -----------------------------------------
def connect_sqlite(db_path: Union[str, Path]) -> sqlite3.Connection:
    """
    SQLite 연결 생성.

    실무 팁
    - check_same_thread=False: 멀티스레드 상황에서 필요할 수 있지만,
      여기서는 단일 실행이므로 기본값 유지
    - row_factory를 설정하면 dict-like row도 가능하지만 pandas에선 불필요
    """
    db_path = Path(db_path)
    ensure_dir(db_path.parent)
    conn = sqlite3.connect(db_path)
    # 외래키 제약 활성화(SQLite는 기본 OFF인 경우가 있음)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# -----------------------------------------
# 2) 데모 데이터베이스 초기화(재현 가능한 샘플)
# -----------------------------------------
def init_demo_db(conn: sqlite3.Connection) -> None:
    """
    실습용 테이블 생성 + 샘플 데이터 적재.
    - 이미 있으면 DROP/CREATE로 멱등적(idempotent) 수행
    """
    cur = conn.cursor()

    # ✅ 멱등적 DDL: 반복 실행해도 깨지지 않게
    cur.executescript(
        """
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS events;

        CREATE TABLE users (
            user_id     INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            country     TEXT NOT NULL,
            created_at  TEXT NOT NULL   -- ISO 문자열로 저장(파싱은 pandas에서)
        );

        CREATE TABLE events (
            event_id    INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            event_type  TEXT NOT NULL,
            event_time  TEXT NOT NULL,
            amount      REAL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE INDEX IF NOT EXISTS idx_events_user_time ON events(user_id, event_time);
        """
    )

    users = [
        (1, "Junyeong", "KR", "2026-01-01"),
        (2, "Alex", "US", "2026-01-02"),
        (3, "Mina", "KR", "2026-01-03"),
        (4, "Sam", "CA", "2026-01-04"),
    ]
    events = [
        (101, 1, "signup", "2026-01-01 09:00:00", None),
        (102, 1, "purchase", "2026-01-05 12:10:00", 49.99),
        (103, 2, "signup", "2026-01-02 10:00:00", None),
        (104, 2, "purchase", "2026-01-08 08:30:00", 19.99),
        (105, 3, "signup", "2026-01-03 15:00:00", None),
        (106, 3, "purchase", "2026-01-10 20:00:00", 99.0),
        (107, 4, "signup", "2026-01-04 07:00:00", None),
    ]

    cur.executemany("INSERT INTO users(user_id, name, country, created_at) VALUES (?, ?, ?, ?);", users)
    cur.executemany(
        "INSERT INTO events(event_id, user_id, event_type, event_time, amount) VALUES (?, ?, ?, ?, ?);",
        events,
    )
    conn.commit()
    print("[OK] Demo DB initialized:", DB_PATH)


# -----------------------------------------
# 3) SQL 읽기: 보안(파라미터 바인딩) + 표준 패턴
# -----------------------------------------
def read_sql(
    conn: sqlite3.Connection,
    query: str,
    params: Optional[Dict[str, Any]] = None,
    config: Optional[SQLReadConfig] = None,
) -> pd.DataFrame:
    """
    pandas.read_sql_query 래퍼.

    핵심 포인트(실무)
    - 문자열 포맷팅으로 SQL 만들지 말고, params를 통해 바인딩할 것 (SQL injection 방지)
    - parse_dates로 datetime 파싱
    - chunksize는 대용량에서만 사용 (그 경우에는 반환 타입이 iterator가 되므로 별도 처리 필요)
    """
    config = config or SQLReadConfig()

    if config.chunksize:
        # chunksize 사용 시 iterator 반환 → 여기서는 concat해서 DF로 반환(데모)
        chunks = pd.read_sql_query(
            query,
            conn,
            params=params,
            parse_dates=config.parse_dates,
            chunksize=config.chunksize,
        )
        df = pd.concat(list(chunks), ignore_index=True)
    else:
        df = pd.read_sql_query(
            query,
            conn,
            params=params,
            parse_dates=config.parse_dates,
        )

    # dtype_map이 있으면 후처리로 안정적으로 캐스팅(실무에서 자주 씀)
    if config.dtype_map:
        for col, dt in config.dtype_map.items():
            if col in df.columns:
                df[col] = df[col].astype(dt)

    return df


# -----------------------------------------
# 4) 실무형 쿼리 예시(조인/집계/필터)
# -----------------------------------------
def query_user_purchases(conn: sqlite3.Connection, country: str) -> pd.DataFrame:
    """
    특정 국가(country) 유저들의 구매 내역을 조인해서 조회.

    - users + events join
    - event_type='purchase' 필터
    - params 바인딩 사용(보안)
    """
    sql = """
    SELECT
        u.user_id,
        u.name,
        u.country,
        u.created_at,
        e.event_time,
        e.amount
    FROM users u
    JOIN events e
      ON u.user_id = e.user_id
    WHERE u.country = :country
      AND e.event_type = 'purchase'
    ORDER BY e.event_time;
    """

    config = SQLReadConfig(parse_dates=["created_at", "event_time"])
    df = read_sql(conn, sql, params={"country": country}, config=config)
    return df


def query_daily_revenue(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    일별 매출 집계 예시.

    - DATE(event_time)로 일 단위 bucket
    - SUM(amount) 집계
    - NULL amount는 제외 (purchase만 집계하면 자연스럽게 해결)
    """
    sql = """
    SELECT
        DATE(event_time) AS event_date,
        COUNT(*)         AS purchases,
        ROUND(SUM(amount), 2) AS revenue
    FROM events
    WHERE event_type = 'purchase'
    GROUP BY DATE(event_time)
    ORDER BY event_date;
    """
    df = read_sql(conn, sql)
    return df


def query_big_table_chunk_example(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    chunk 로딩 예시(데모 수준).
    실제로는 '전체 concat' 대신 chunk 단위 집계/필터만 남기는 게 일반적.
    """
    sql = """
    SELECT user_id, event_type, event_time, amount
    FROM events
    ORDER BY event_time;
    """
    config = SQLReadConfig(chunksize=2, parse_dates=["event_time"])
    df = read_sql(conn, sql, config=config)
    return df


# -----------------------------------------
# 5) 로딩 결과 품질 체크(간단 프로파일링)
# -----------------------------------------
def quick_profile(df: pd.DataFrame, n: int = 5) -> None:
    print("\n=== QUICK PROFILE ===")
    print("shape:", df.shape)
    print("\n-- dtypes --")
    print(df.dtypes)
    print("\n-- missing (top) --")
    print(df.isna().sum().sort_values(ascending=False).head(10))
    print("\n-- head --")
    print(df.head(n))


# -----------------------------------------
# 6) 실행 엔트리포인트
# -----------------------------------------
def main() -> None:
    ensure_dir(DATA_DIR)

    with connect_sqlite(DB_PATH) as conn:
        # 데모 DB 초기화(반복 실행 가능)
        init_demo_db(conn)

        print("\n[CASE 1] KR 유저 구매 내역 조인 조회")
        df_kr = query_user_purchases(conn, country="KR")
        quick_profile(df_kr)

        print("\n[CASE 2] 일별 매출 집계")
        df_rev = query_daily_revenue(conn)
        quick_profile(df_rev)

        print("\n[CASE 3] chunk 로딩 데모")
        df_chunk = query_big_table_chunk_example(conn)
        quick_profile(df_chunk)


if __name__ == "__main__":
    main()