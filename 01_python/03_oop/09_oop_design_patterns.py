"""
Day 21: Python OOP — Practical Design Patterns

This file demonstrates a professional, practical introduction to OOP design patterns.
Instead of memorizing pattern names, the focus is on:
- why the pattern exists
- what problem it solves
- how to implement it cleanly in Python

Patterns covered:
1) Strategy Pattern   : interchangeable algorithms (risk scoring strategies)
2) Factory Pattern    : configuration-based object creation
3) Template Method    : fixed pipeline skeleton with customizable steps
(+ small Repository-like abstraction for data source)

본 파일은 "패턴 이름 암기"가 아니라,
실무/연구 코드에서 실제로 발생하는 문제를 패턴으로 해결하는 방법을 다룬다.

핵심 목표:
- 결합도 낮추기 (loose coupling)
- 확장성 높이기 (extensibility)
- 테스트하기 쉬운 구조 만들기 (testability)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Any, Dict, List, Sequence


# ============================================================
# 0) Problem Setting (문제 상황)
# ============================================================
# "리스크 점수를 계산하는 방법"이 상황에 따라 계속 바뀐다고 가정해보자.
# - 의료: 재발 위험, 부작용 위험, 치료 시점 위험
# - 금융: 변동성, 급락(drawdown), 손실 위험
#
# 단순 if-else로 늘리면:
# - 코드가 비대해지고
# - 테스트가 어려워지며
# - 새 방식 추가가 힘들어진다
#
# 이런 문제는 Strategy / Factory 패턴으로 해결하는 게 좋다.


# ============================================================
# 1) Strategy Pattern (전략 패턴)
# ============================================================
# "알고리즘을 객체로 캡슐화"해서, 런타임에 교체 가능하도록 만드는 패턴.
# 핵심은 "행동(계산 로직)"을 분리하는 것.

class RiskStrategy(ABC):
    """리스크 계산 알고리즘(전략) 인터페이스"""

    @abstractmethod
    def score(self, values: Sequence[float]) -> float:
        """리스크 점수 계산"""
        raise NotImplementedError


class VolatilityRisk(RiskStrategy):
    """
    변동성 기반 리스크
    - 값들의 표준편차(pstdev)를 리스크로 사용 (단순 예시)
    """

    def score(self, values: Sequence[float]) -> float:
        if len(values) < 2:
            return 0.0
        return float(pstdev(values))


class DeviationFromMeanRisk(RiskStrategy):
    """
    평균 대비 편차 기반 리스크
    - 평균에서 얼마나 벗어나는지(절댓값 평균)를 리스크로 사용
    """

    def score(self, values: Sequence[float]) -> float:
        if not values:
            return 0.0
        m = mean(values)
        return float(mean(abs(v - m) for v in values))


@dataclass
class RiskEngine:
    """
    Strategy를 주입받아 리스크를 계산하는 엔진
    - 엔진은 '어떤 전략인지' 몰라도 된다 (인터페이스만 알면 됨)
    """
    strategy: RiskStrategy

    def run(self, values: Sequence[float]) -> float:
        return self.strategy.score(values)


def demo_strategy() -> None:
    values = [10, 11, 13, 9, 15, 14]

    engine_a = RiskEngine(strategy=VolatilityRisk())
    engine_b = RiskEngine(strategy=DeviationFromMeanRisk())

    print("[Strategy] VolatilityRisk:", engine_a.run(values))
    print("[Strategy] DeviationFromMeanRisk:", engine_b.run(values))


# ============================================================
# 2) Factory Pattern (팩토리 패턴)
# ============================================================
# "설정/입력"에 따라 적절한 객체를 생성하는 패턴.
# 실무에서 config-driven 시스템(실험관리, 서비스 옵션)에 매우 유용하다.

class RiskStrategyFactory:
    """전략 생성 팩토리"""

    _registry: Dict[str, Any] = {
        "volatility": VolatilityRisk,
        "deviation_mean": DeviationFromMeanRisk,
    }

    @classmethod
    def create(cls, strategy_name: str) -> RiskStrategy:
        """
        strategy_name에 따라 RiskStrategy 구현체를 생성한다.
        - 지원하지 않는 이름이면 명확한 에러를 발생시킨다.
        """
        key = strategy_name.strip().lower()
        if key not in cls._registry:
            supported = ", ".join(sorted(cls._registry.keys()))
            raise ValueError(f"Unknown strategy '{strategy_name}'. Supported: {supported}")
        return cls._registry[key]()


def demo_factory() -> None:
    values = [3, 5, 7, 11, 13]

    strategy = RiskStrategyFactory.create("volatility")
    engine = RiskEngine(strategy=strategy)
    print("[Factory] strategy=volatility:", engine.run(values))

    strategy2 = RiskStrategyFactory.create("deviation_mean")
    engine2 = RiskEngine(strategy=strategy2)
    print("[Factory] strategy=deviation_mean:", engine2.run(values))


# ============================================================
# 3) Template Method Pattern (템플릿 메서드)
# ============================================================
# "파이프라인의 골격(순서/흐름)"은 고정하되,
# 일부 단계(step)는 하위 클래스가 구현하도록 하는 패턴.
#
# 연구/ML 프로젝트에서:
# - 데이터 로딩 -> 전처리 -> 학습 -> 평가 -> 리포트
# 같은 구조가 반복되는데,
# 흐름을 표준화하면서도 각 프로젝트별로 구현을 바꿀 수 있다.

class BasePipeline(ABC):
    """
    파이프라인 템플릿
    - run()의 흐름은 고정
    - 세부 단계는 하위 클래스에서 구현
    """

    def run(self) -> Dict[str, Any]:
        data = self.load_data()
        data = self.preprocess(data)
        model = self.train(data)
        metrics = self.evaluate(model, data)
        report = self.report(metrics)
        return {
            "metrics": metrics,
            "report": report,
        }

    @abstractmethod
    def load_data(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def preprocess(self, data: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def train(self, data: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def evaluate(self, model: Any, data: Any) -> Dict[str, float]:
        raise NotImplementedError

    def report(self, metrics: Dict[str, float]) -> str:
        # 공통 리포트 포맷 (원하면 하위 클래스에서 override 가능)
        lines = ["Pipeline Report"]
        for k, v in metrics.items():
            lines.append(f"- {k}: {v:.4f}")
        return "\n".join(lines)


# (보너스) Repository-like abstraction:
# 데이터 소스가 CSV/DB/API로 바뀌어도 파이프라인 코드는 동일하게 유지되도록 한다.

class DataSource(ABC):
    """데이터 소스 인터페이스"""

    @abstractmethod
    def fetch(self) -> List[float]:
        raise NotImplementedError


class InMemoryDataSource(DataSource):
    """메모리 기반 데이터 소스 (학습용)"""

    def __init__(self, values: List[float]) -> None:
        self._values = values

    def fetch(self) -> List[float]:
        return list(self._values)


class RiskScoringPipeline(BasePipeline):
    """
    Template Method + Strategy를 결합한 예시 파이프라인
    - 데이터 소스(DataSource)에서 값을 가져오고
    - 전처리 후
    - RiskEngine(Strategy)로 리스크 점수를 계산한다
    """

    def __init__(self, source: DataSource, engine: RiskEngine) -> None:
        self.source = source
        self.engine = engine

    def load_data(self) -> List[float]:
        return self.source.fetch()

    def preprocess(self, data: List[float]) -> List[float]:
        # 간단한 전처리 예: None 제거, 음수 제거, 타입 변환 등
        cleaned = [float(x) for x in data if x is not None]
        cleaned = [x for x in cleaned if x >= 0]
        return cleaned

    def train(self, data: List[float]) -> Dict[str, Any]:
        # 여기서는 학습이라는 개념 대신 "전략 준비" 정도로 처리 (예시)
        # 실제 ML이라면 model.fit(...) 등이 들어간다.
        return {"strategy": self.engine.strategy.__class__.__name__}

    def evaluate(self, model: Dict[str, Any], data: List[float]) -> Dict[str, float]:
        # 리스크 점수 계산을 평가 지표처럼 사용
        risk = self.engine.run(data)
        return {
            "risk_score": risk,
            "n": float(len(data)),
        }


def demo_template_method() -> None:
    values = [10, 12, 9, 20, 18, 16]
    source = InMemoryDataSource(values)

    # Factory로 전략을 선택 → Strategy 주입
    strategy = RiskStrategyFactory.create("volatility")
    engine = RiskEngine(strategy=strategy)

    pipeline = RiskScoringPipeline(source=source, engine=engine)
    result = pipeline.run()

    print("[Template Method] metrics:", result["metrics"])
    print("[Template Method] report:\n", result["report"])


# ============================================================
# 4) Summary (요약)
# ============================================================
"""
핵심 요약
- Strategy 패턴: 알고리즘(리스크 계산)을 객체로 분리 → 교체/확장 쉬움
- Factory 패턴: 설정 기반 객체 생성 → config-driven 설계에 유리
- Template Method: 파이프라인 흐름 표준화 + 단계별 커스터마이징
- (보너스) DataSource 인터페이스: 데이터 로딩 방식이 바뀌어도 파이프라인 유지

이 조합은
연구 코드(실험/재현) -> 제품 코드(서비스/확장)로 넘어가는 과정에서
가장 강력하게 "구조적 설계 역량"을 보여준다.
"""


if __name__ == "__main__":
    demo_strategy()
    print("-" * 60)
    demo_factory()
    print("-" * 60)
    demo_template_method()