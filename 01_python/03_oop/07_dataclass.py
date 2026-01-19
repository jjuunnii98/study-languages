"""
Day 19: Python OOP — dataclasses (실무 데이터 모델링)

This file demonstrates how to use Python's `dataclasses` to build
clean, maintainable data models.

Key topics:
- dataclass basics: auto __init__, __repr__, __eq__
- default values & default_factory
- type hints and readability
- post-init validation (__post_init__)
- immutability with frozen=True
- ordering and comparison
- practical patterns for research / data engineering / product code

본 파일은 파이썬 dataclass를 사용해 "데이터 중심 클래스"를
실무적으로 설계하는 방법을 다룬다.

dataclass는 다음 상황에서 특히 유용하다:
- 데이터 전처리 파이프라인에서 레코드/스키마를 표현할 때
- 실험/연구에서 파라미터 세트를 명확히 기록할 때
- 서비스 코드에서 DTO(Data Transfer Object) 같은 객체가 필요할 때
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict, replace
from datetime import datetime
from typing import Optional, List


# ============================================================
# 1) dataclass 기본: boilerplate 제거
# ============================================================
# dataclass는 __init__, __repr__, __eq__ 등을 자동 생성해준다.
# 특히 데이터 중심 클래스(필드가 중심인 클래스)에서 생산성을 크게 올린다.

@dataclass
class PatientRecord:
    """
    환자 레코드 예시 (학습용)
    - dataclass 기본 기능을 확인하기 위한 간단한 모델
    """
    patient_id: str
    age: int
    diagnosis: str


def demo_basics() -> None:
    p1 = PatientRecord(patient_id="P001", age=52, diagnosis="breast_cancer")
    p2 = PatientRecord(patient_id="P001", age=52, diagnosis="breast_cancer")

    # __repr__ 자동 생성 → 디버깅/로그에서 유리
    print("p1:", p1)

    # __eq__ 자동 생성 → 값 기반 비교 가능
    print("p1 == p2:", p1 == p2)


# ============================================================
# 2) default / default_factory: 안전한 기본값
# ============================================================
# 리스트/딕셔너리 같은 "mutable default"는 default_factory로 생성해야 안전하다.
# (그렇지 않으면 모든 인스턴스가 같은 리스트를 공유하는 버그가 난다.)

@dataclass
class ExperimentConfig:
    """
    실험 설정 예시 (연구/ML 파이프라인에서 자주 등장)
    """
    experiment_name: str
    seed: int = 42
    created_at: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)  # 안전한 기본값


def demo_defaults() -> None:
    c1 = ExperimentConfig(experiment_name="baseline")
    c2 = ExperimentConfig(experiment_name="baseline")

    c1.tags.append("v1")
    print("c1:", c1)
    print("c2:", c2)  # c2.tags는 영향을 받지 않음


# ============================================================
# 3) __post_init__: 검증/정규화 로직 (실무 핵심)
# ============================================================
# dataclass는 단순히 필드만 담는 객체로 쓰기도 하지만,
# 실무에서는 "상태 무결성(invariants)"을 유지하기 위해 검증이 필요하다.

@dataclass
class TradeOrder:
    """
    금융 주문 예시
    - amount는 양수여야 한다.
    - symbol은 대문자로 정규화한다.
    - order_type은 제한된 값만 허용한다.
    """
    symbol: str
    amount: float
    order_type: str = "market"  # market | limit
    limit_price: Optional[float] = None

    def __post_init__(self) -> None:
        # 입력 정규화: 심볼을 대문자로 통일
        self.symbol = self.symbol.upper().strip()

        # 검증 1: amount
        if self.amount <= 0:
            raise ValueError("amount must be positive.")

        # 검증 2: order_type
        allowed = {"market", "limit"}
        if self.order_type not in allowed:
            raise ValueError(f"order_type must be one of {allowed}.")

        # 검증 3: limit 주문이면 limit_price 필수
        if self.order_type == "limit":
            if self.limit_price is None:
                raise ValueError("limit_price is required for limit orders.")
            if self.limit_price <= 0:
                raise ValueError("limit_price must be positive.")

        # market 주문이면 limit_price는 의미 없으므로 None으로 정리 (선택)
        if self.order_type == "market":
            self.limit_price = None


def demo_post_init() -> None:
    o1 = TradeOrder(symbol=" btcusdt ", amount=1000, order_type="market")
    print("o1:", o1)

    o2 = TradeOrder(symbol="ethusdt", amount=2, order_type="limit", limit_price=2500)
    print("o2:", o2)

    # 아래는 에러 예시:
    # TradeOrder(symbol="xrp", amount=-1)
    # TradeOrder(symbol="xrp", amount=1, order_type="limit", limit_price=None)


# ============================================================
# 4) frozen=True: 불변(immutable) 데이터 모델
# ============================================================
# 불변 객체는:
# - 실험 파라미터(재현성)
# - 캐싱 키
# - 멀티스레드 환경에서 안전성
# 등에서 매우 유용하다.

@dataclass(frozen=True)
class ModelParams:
    """
    모델 파라미터(불변) 예시
    """
    model_name: str
    learning_rate: float
    n_estimators: int


def demo_frozen() -> None:
    params = ModelParams(model_name="xgboost", learning_rate=0.05, n_estimators=500)
    print("params:", params)

    # frozen이므로 필드 수정 불가
    # params.learning_rate = 0.1  # ❌ dataclasses.FrozenInstanceError


# ============================================================
# 5) ordering=True: 정렬/비교가 필요한 경우
# ============================================================
# ordering=True를 사용하면 <, <=, >, >= 비교 연산이 자동 생성된다.
# 단, 필드 정의 순서에 따라 비교가 이루어지므로
# "어떤 기준으로 비교할지"를 의도적으로 설계해야 한다.

@dataclass(order=True)
class RiskScore:
    """
    위험 점수 예시 (정렬 가능한 데이터 모델)
    - score 기준으로 정렬되도록 score를 첫 필드로 둔다.
    """
    score: float
    entity_id: str = field(compare=False)  # entity_id는 비교에 포함하지 않음
    note: str = field(default="", compare=False)


def demo_ordering() -> None:
    scores = [
        RiskScore(score=0.72, entity_id="A"),
        RiskScore(score=0.15, entity_id="B"),
        RiskScore(score=0.72, entity_id="C"),
    ]
    print("sorted:", sorted(scores))  # score 기준 정렬


# ============================================================
# 6) asdict / replace: 직렬화 및 안전한 수정
# ============================================================
# asdict: dataclass -> dict 변환 (로그/저장/전송)
# replace: 불변(frozen) 객체도 새로운 인스턴스를 만들어 일부 필드만 바꿀 수 있다.

def demo_asdict_replace() -> None:
    params = ModelParams(model_name="xgboost", learning_rate=0.05, n_estimators=500)

    # dict로 변환
    print("asdict:", asdict(params))

    # learning_rate만 바꾼 새 객체 생성
    params2 = replace(params, learning_rate=0.1)
    print("params2:", params2)


# ============================================================
# 7) Summary (요약)
# ============================================================
"""
핵심 요약
- dataclass는 데이터 중심 클래스를 깔끔하고 안전하게 만든다.
- default_factory로 mutable 기본값 버그를 방지한다.
- __post_init__에서 검증/정규화를 수행해 데이터 무결성을 지킨다.
- frozen=True는 실험 재현성과 안전성을 높인다.
- ordering=True는 정렬 가능한 모델이 필요한 분석/랭킹 상황에서 유용하다.
- asdict/replace는 로깅, 직렬화, 안전한 수정에 도움된다.
"""


if __name__ == "__main__":
    demo_basics()
    print("-" * 60)
    demo_defaults()
    print("-" * 60)
    demo_post_init()
    print("-" * 60)
    demo_frozen()
    print("-" * 60)
    demo_ordering()
    print("-" * 60)
    demo_asdict_replace()