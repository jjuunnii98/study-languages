"""
============================================================
Day 80 — Typed Dataclass & Protocol
File: 01_python/06_advanced/03_type_hints/03_typed_dataclass_protocol.py

목표
- dataclass를 활용한 구조화 객체 설계
- Protocol을 활용한 인터페이스 기반 개발
- 타입 안정성과 유지보수성 향상
- 실무형 설계 패턴 이해

핵심 개념
1. dataclass = 데이터를 담는 객체를 간단히 생성
2. Protocol = 특정 메서드가 있으면 같은 타입처럼 사용 가능
3. 느슨한 결합(Loose Coupling) 구조 설계
============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, List, Dict


# ------------------------------------------------------------
# 1. Dataclass Basics
# ------------------------------------------------------------
# 한국어 설명:
# dataclass는 __init__, __repr__ 등을 자동 생성한다.


@dataclass
class User:
    user_id: int
    name: str
    email: str
    is_active: bool = True


user = User(1, "Junyeong", "jun@example.com")
print(user)


# ------------------------------------------------------------
# 2. Dataclass with Business Object
# ------------------------------------------------------------
# 한국어 설명:
# 실제 서비스에서 많이 쓰는 구조화 객체 예제


@dataclass
class RiskSignal:
    symbol: str
    score: float
    level: str
    source: str
    tags: List[str] = field(default_factory=list)


btc_signal = RiskSignal(
    symbol="BTC",
    score=82.5,
    level="HIGH",
    source="risk-engine",
    tags=["volatility", "fear-greed"]
)

print(btc_signal)


# ------------------------------------------------------------
# 3. Dataclass Method Example
# ------------------------------------------------------------


@dataclass
class TradePosition:
    symbol: str
    quantity: float
    avg_price: float

    def market_value(self, current_price: float) -> float:
        return self.quantity * current_price

    def pnl(self, current_price: float) -> float:
        return (current_price - self.avg_price) * self.quantity


position = TradePosition("SOL", 20, 140000)

print("Market Value:", position.market_value(155000))
print("PnL:", position.pnl(155000))


# ------------------------------------------------------------
# 4. Protocol Basics
# ------------------------------------------------------------
# 한국어 설명:
# 아래 메서드를 구현하면 같은 타입처럼 취급 가능


class Notifier(Protocol):
    def send(self, message: str) -> None:
        ...


# ------------------------------------------------------------
# 5. Gmail Notifier
# ------------------------------------------------------------


class GmailNotifier:
    def send(self, message: str) -> None:
        print(f"[GMAIL] {message}")


# ------------------------------------------------------------
# 6. Telegram Notifier
# ------------------------------------------------------------


class TelegramNotifier:
    def send(self, message: str) -> None:
        print(f"[TELEGRAM] {message}")


# ------------------------------------------------------------
# 7. Protocol 활용 함수
# ------------------------------------------------------------


def dispatch_alert(notifier: Notifier, signal: RiskSignal) -> None:
    message = (
        f"{signal.symbol} 위험 경고 | "
        f"점수={signal.score} | "
        f"등급={signal.level}"
    )
    notifier.send(message)


gmail = GmailNotifier()
telegram = TelegramNotifier()

dispatch_alert(gmail, btc_signal)
dispatch_alert(telegram, btc_signal)


# ------------------------------------------------------------
# 8. Another Protocol Example
# ------------------------------------------------------------


class DataLoader(Protocol):
    def load(self) -> List[Dict[str, float]]:
        ...


class CsvLoader:
    def load(self) -> List[Dict[str, float]]:
        return [
            {"price": 101000.0},
            {"price": 102500.0},
            {"price": 99800.0},
        ]


class ApiLoader:
    def load(self) -> List[Dict[str, float]]:
        return [
            {"price": 110000.0},
            {"price": 111500.0},
        ]


def summarize_prices(loader: DataLoader) -> None:
    rows = loader.load()
    prices = [row["price"] for row in rows]

    print("Count:", len(prices))
    print("Average:", sum(prices) / len(prices))
    print("Max:", max(prices))
    print("Min:", min(prices))


summarize_prices(CsvLoader())
summarize_prices(ApiLoader())


# ------------------------------------------------------------
# 9. 실무형 구조 장점
# ------------------------------------------------------------
print("----- Summary -----")
print("✔ dataclass = 데이터 객체 구조화")
print("✔ Protocol = 인터페이스 기반 설계")
print("✔ 테스트 용이성 증가")
print("✔ Gmail → Telegram 교체 쉬움")
print("✔ 유지보수성과 확장성 향상")
print("-------------------")