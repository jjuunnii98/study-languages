"""
Day 20: Python OOP — Abstract Base Classes (ABC) & Interfaces

This file demonstrates how to use Python's Abstract Base Classes (ABC)
to design clear, extensible, and safe interfaces.

Key concepts:
- Why interfaces matter in large systems
- How ABC enforces contracts
- abstractmethod usage
- Polymorphism via interfaces
- Practical design examples (service / pipeline / strategy patterns)

본 파일은 Python의 ABC(Abstract Base Class)를 사용해
"인터페이스 기반 설계"를 구현하는 방법을 다룬다.

ABC는 다음 상황에서 매우 중요하다:
- 여러 구현체를 동일한 방식으로 다뤄야 할 때
- 팀/프로젝트 규모가 커질 때
- 실험 코드 → 제품 코드로 확장할 때
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


# ============================================================
# 1) 인터페이스가 왜 필요한가?
# ============================================================
# "같은 역할(role)을 하지만 구현은 다른 객체"를
# 동일한 방식으로 다루기 위해 인터페이스가 필요하다.
#
# 예:
# - 서로 다른 모델(XGBoost, LogisticRegression, NN)
# - 서로 다른 데이터 소스(DB, CSV, API)
# - 서로 다른 리스크 계산 방식
#
# 인터페이스는 "무엇을 해야 하는지"만 정의하고,
# "어떻게 하는지"는 구현 클래스에 맡긴다.


# ============================================================
# 2) ABC 기본 구조
# ============================================================

class RiskModel(ABC):
    """
    RiskModel 인터페이스
    - 모든 리스크 모델이 반드시 구현해야 할 메서드를 정의
    """

    @abstractmethod
    def fit(self, data: Any) -> None:
        """모델 학습"""
        pass

    @abstractmethod
    def predict_risk(self, data: Any) -> float:
        """리스크 점수 예측"""
        pass

    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        """모델 메타데이터 반환"""
        pass


# ============================================================
# 3) 구현 클래스 1: 통계 기반 모델
# ============================================================

class StatisticalRiskModel(RiskModel):
    """
    단순 통계 기반 리스크 모델 예시
    """

    def __init__(self) -> None:
        self._mean = 0.0

    def fit(self, data: Any) -> None:
        # 실제로는 numpy/pandas 사용
        self._mean = sum(data) / len(data)

    def predict_risk(self, data: Any) -> float:
        # 평균 대비 편차를 리스크로 해석 (단순 예시)
        return abs(sum(data) / len(data) - self._mean)

    def metadata(self) -> Dict[str, Any]:
        return {
            "model_type": "statistical",
            "description": "Mean-deviation based risk model",
        }


# ============================================================
# 4) 구현 클래스 2: 규칙 기반 모델
# ============================================================

class RuleBasedRiskModel(RiskModel):
    """
    규칙 기반 리스크 모델 예시
    """

    def fit(self, data: Any) -> None:
        # 규칙 기반 모델은 학습 단계가 없을 수도 있다
        pass

    def predict_risk(self, data: Any) -> float:
        # 임계값 초과 여부로 리스크 계산 (단순 예시)
        threshold = 10
        return 1.0 if max(data) > threshold else 0.0

    def metadata(self) -> Dict[str, Any]:
        return {
            "model_type": "rule_based",
            "description": "Threshold-based risk model",
        }


# ============================================================
# 5) 인터페이스 기반 다형성 (핵심)
# ============================================================
# 중요한 포인트:
# - 아래 코드는 "구체 클래스"를 전혀 알 필요가 없다.
# - RiskModel 인터페이스만 만족하면 모두 동일하게 동작한다.

def run_risk_pipeline(model: RiskModel, data: Any) -> float:
    """
    리스크 파이프라인
    - 어떤 RiskModel 구현체가 오더라도 동일하게 처리
    """
    model.fit(data)
    risk_score = model.predict_risk(data)
    print("Model info:", model.metadata())
    return risk_score


# ============================================================
# 6) 잘못된 구현 예 (에러 확인용)
# ============================================================
# 아래 클래스는 abstractmethod를 구현하지 않았기 때문에
# 인스턴스 생성 시 TypeError가 발생한다.
#
# class InvalidRiskModel(RiskModel):
#     def fit(self, data: Any) -> None:
#         pass


# ============================================================
# 7) Summary (요약)
# ============================================================
"""
핵심 요약
- ABC는 "반드시 구현해야 할 메서드 계약(contract)"을 강제한다.
- 인터페이스 기반 설계는 확장성과 안정성을 크게 높인다.
- 구체 구현체 대신 인터페이스에 의존하면 결합도가 낮아진다.
- 연구 코드 → 제품 코드로 넘어갈수록 ABC의 가치가 커진다.
- Risk AI / ML / 서비스 설계에서 매우 중요한 패턴이다.
"""


if __name__ == "__main__":
    sample_data = [3, 5, 7, 9, 11]

    stat_model = StatisticalRiskModel()
    rule_model = RuleBasedRiskModel()

    print("Statistical model risk:", run_risk_pipeline(stat_model, sample_data))
    print("Rule-based model risk:", run_risk_pipeline(rule_model, sample_data))