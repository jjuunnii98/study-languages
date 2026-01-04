"""
Day 12: Python Core - DateTime & Time Handling

This file covers practical date/time handling in Python:
- datetime / date / time objects
- formatting and parsing (strftime / strptime)
- time delta arithmetic
- timezone-aware datetimes (zoneinfo)
- UNIX timestamp conversions
- common patterns for logs, pipelines, and analysis

본 파일은 파이썬에서 날짜/시간을 다루는 핵심 패턴을 정리한다.
실무/연구에서는 로그, 시계열 데이터, 이벤트 시간 정렬, 기간 계산이 빈번하므로
datetime 처리 역량은 매우 중요하다.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Optional

# Python 3.9+ timezone support
try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore


# ---------------------------------------------------------
# 1. Basic datetime objects
# ---------------------------------------------------------
print("\n[1] Basic datetime objects")

today = date.today()
now = datetime.now()

print("date.today()      =", today)
print("datetime.now()    =", now)

# 한국어 설명:
# - date: 날짜(연-월-일)만
# - datetime: 날짜 + 시간(시:분:초)까지 포함


# ---------------------------------------------------------
# 2. Creating datetime explicitly
# ---------------------------------------------------------
print("\n[2] Creating datetime explicitly")

dt = datetime(2026, 1, 1, 9, 30, 0)
d = date(2026, 1, 1)
t = time(9, 30, 0)

print("datetime(...) =", dt)
print("date(...)     =", d)
print("time(...)     =", t)

# 한국어 설명:
# - 명시적으로 datetime을 생성하면 테스트/재현성에 유리
# - 분석 코드에서 '고정 기준 날짜'를 잡을 때 자주 사용


# ---------------------------------------------------------
# 3. Formatting (strftime) and parsing (strptime)
# ---------------------------------------------------------
print("\n[3] Formatting & Parsing")

formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print("formatted =", formatted)

raw = "2026-01-01 09:30:00"
parsed = datetime.strptime(raw, "%Y-%m-%d %H:%M:%S")
print("parsed    =", parsed)

# 한국어 설명:
# - strftime: datetime -> 문자열
# - strptime: 문자열 -> datetime
# - 데이터 정제/로그 파싱에서 가장 많이 쓰는 패턴


# ---------------------------------------------------------
# 4. Timedelta arithmetic (기간 계산)
# ---------------------------------------------------------
print("\n[4] Timedelta arithmetic")

one_week = timedelta(days=7)
two_hours = timedelta(hours=2)

print("now              =", now)
print("now + 7 days     =", now + one_week)
print("now - 2 hours    =", now - two_hours)

# 날짜 차이 계산
dt1 = datetime(2026, 1, 1, 9, 0, 0)
dt2 = datetime(2026, 1, 3, 12, 0, 0)
diff = dt2 - dt1

print("diff             =", diff)
print("diff.days        =", diff.days)
print("diff.seconds     =", diff.seconds)
print("diff.total_seconds =", diff.total_seconds())

# 한국어 설명:
# - timedelta는 날짜/시간 간 차이를 표현
# - total_seconds()는 시계열/로그 분석에서 매우 유용


# ---------------------------------------------------------
# 5. Common analytics patterns
# ---------------------------------------------------------
print("\n[5] Common analytics patterns")

# (1) "기간 내" 필터링: start <= event_time < end
start = datetime(2026, 1, 1, 0, 0, 0)
end = datetime(2026, 1, 8, 0, 0, 0)

event_times = [
    datetime(2025, 12, 31, 23, 59),
    datetime(2026, 1, 2, 10, 0),
    datetime(2026, 1, 7, 23, 0),
    datetime(2026, 1, 8, 0, 0),
]

in_range = [x for x in event_times if start <= x < end]
print("events in range:", in_range)

# (2) "flooring" / "rounding" (시/분 단위 내림)
rounded_to_hour = now.replace(minute=0, second=0, microsecond=0)
print("rounded_to_hour:", rounded_to_hour)

# 한국어 설명:
# - start <= x < end 패턴은 분석에서 매우 자주 사용 (경계 포함/미포함 명확)
# - replace()로 특정 단위로 시간을 내림 처리 가능


# ---------------------------------------------------------
# 6. Timezone-aware datetime (zoneinfo)
# ---------------------------------------------------------
print("\n[6] Timezone-aware datetime")

if ZoneInfo is not None:
    seoul = ZoneInfo("Asia/Seoul")
    utc = ZoneInfo("UTC")

    aware_seoul = datetime.now(tz=seoul)
    aware_utc = aware_seoul.astimezone(utc)

    print("aware (Seoul) =", aware_seoul)
    print("aware (UTC)   =", aware_utc)

    # naive -> aware (주의: 실제로는 원본이 어느 timezone인지 명확해야 함)
    naive = datetime(2026, 1, 1, 9, 30, 0)
    assumed_seoul = naive.replace(tzinfo=seoul)
    print("naive         =", naive)
    print("assumed_seoul =", assumed_seoul)
else:
    print("ZoneInfo not available. (Python 3.9+에서 권장)")

# 한국어 설명:
# - naive datetime: timezone 정보 없음
# - aware datetime: timezone 정보 포함
# - 실무에서는 가능한 한 timezone-aware를 권장 (특히 서버/글로벌 데이터)


# ---------------------------------------------------------
# 7. UNIX timestamp conversions
# ---------------------------------------------------------
print("\n[7] UNIX timestamp conversions")

ts = now.timestamp()  # seconds since epoch
back = datetime.fromtimestamp(ts)

print("timestamp =", ts)
print("fromtimestamp =", back)

# 한국어 설명:
# - timestamp는 시스템/로그/DB에서 자주 사용
# - fromtimestamp는 로컬 timezone 기준으로 생성될 수 있으니(환경에 따라)
#   글로벌 환경에서는 timezone-aware 변환을 고려


# ---------------------------------------------------------
# 8. Practical helper functions
# ---------------------------------------------------------
print("\n[8] Helper functions")

def parse_datetime_safe(value: str, fmt: str) -> Optional[datetime]:
    """
    Safely parse datetime string. Return None if parsing fails.

    한국어 설명:
    - 실무 데이터에는 형식이 깨진 문자열이 섞이는 경우가 많음
    - 실패 시 예외를 던지기보다 None으로 처리하고, 이후 결측 처리/로그로 넘기는 패턴이 유용
    """
    try:
        return datetime.strptime(value, fmt)
    except ValueError:
        return None

samples = ["2026-01-01 09:30:00", "bad-format", "2026-01-02 12:00:00"]
parsed_list = [parse_datetime_safe(x, "%Y-%m-%d %H:%M:%S") for x in samples]
print("parsed_list =", parsed_list)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------
"""
Day 12 (Core) 요약

- date/datetime/time 객체의 차이를 이해한다
- strftime/strptime으로 포맷팅/파싱을 수행한다
- timedelta로 기간 계산과 time arithmetic을 수행한다
- start <= x < end 패턴으로 기간 필터링을 안정적으로 구현한다
- zoneinfo로 timezone-aware datetime을 생성/변환한다
- timestamp 변환은 로그/시계열 처리에 유용하다
- 실무에선 안전 파서(parse_datetime_safe) 같은 방어적 패턴이 중요하다
"""