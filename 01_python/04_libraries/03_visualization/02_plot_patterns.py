"""
Day 32: Matplotlib Plot Patterns

이 파일은 matplotlib을 사용할 때 자주 반복되는
'시각화 패턴(plot patterns)'을 정리한다.

목표:
- 여러 그래프를 하나의 Figure에서 관리하는 법
- 비교/추세/강조를 위한 시각화 구조 설계
- 재사용 가능한 plotting 패턴 이해

이 단계부터는
"어떤 그래프를 그릴까?"보다
"어떤 메시지를 전달할까?"가 더 중요해진다.
"""

from __future__ import annotations

import math
from typing import List

import matplotlib.pyplot as plt


# ---------------------------
# 1. Multiple Lines on One Axes
# ---------------------------
def pattern_multiple_lines() -> None:
    """
    하나의 Axes에 여러 선 그래프를 겹쳐 그리는 패턴
    - 모델 비교
    - 시나리오 비교
    - 기준선 vs 실측값
    """
    xs = list(range(100))
    ys1 = [math.sin(x / 10) for x in xs]
    ys2 = [math.cos(x / 10) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, ys1, label="sin(x/10)")
    ax.plot(xs, ys2, label="cos(x/10)", linestyle="--")

    ax.set_title("Multiple Lines Pattern")
    ax.set_xlabel("x")
    ax.set_ylabel("value")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.show()


# ---------------------------
# 2. Subplots (Comparison Layout)
# ---------------------------
def pattern_subplots() -> None:
    """
    여러 그래프를 서브플롯으로 나누는 패턴
    - 전/후 비교
    - 변수별 분리 시각화
    """
    xs = list(range(100))
    ys1 = [math.sin(x / 10) for x in xs]
    ys2 = [math.cos(x / 10) for x in xs]

    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)

    axes[0].plot(xs, ys1, color="blue")
    axes[0].set_title("sin(x/10)")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(xs, ys2, color="green")
    axes[1].set_title("cos(x/10)")
    axes[1].grid(True, alpha=0.3)

    fig.suptitle("Subplots Pattern", fontsize=12)
    fig.tight_layout()

    plt.show()


# ---------------------------
# 3. Highlighting Important Regions
# ---------------------------
def pattern_highlight_region() -> None:
    """
    특정 구간을 강조하는 패턴
    - 이상치 구간
    - 이벤트 발생 구간
    - 관심 시간대
    """
    xs = list(range(100))
    ys = [math.sin(x / 10) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, ys)

    # 특정 구간 강조
    ax.axvspan(30, 50, alpha=0.2, color="red", label="important region")

    ax.set_title("Highlight Region Pattern")
    ax.set_xlabel("x")
    ax.set_ylabel("value")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.show()


# ---------------------------
# 4. Reference Lines
# ---------------------------
def pattern_reference_lines() -> None:
    """
    기준선(reference line)을 추가하는 패턴
    - 평균선
    - 임계값(threshold)
    - 기준 KPI
    """
    xs = list(range(100))
    ys = [math.sin(x / 10) for x in xs]

    mean_value = sum(ys) / len(ys)

    fig, ax = plt.subplots()
    ax.plot(xs, ys, label="signal")

    # 수평 기준선
    ax.axhline(mean_value, linestyle="--", color="orange", label="mean")

    ax.set_title("Reference Line Pattern")
    ax.set_xlabel("x")
    ax.set_ylabel("value")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.show()


# ---------------------------
# 5. Main
# ---------------------------
if __name__ == "__main__":
    """
    실행 가이드 (한국어)
    - 각 패턴은 독립적으로 이해 가능
    - 실무에서는 이 패턴들을 조합해서 사용
    - 보고서/논문/대시보드 설계 시 기본 템플릿으로 활용 가능
    """

    pattern_multiple_lines()
    pattern_subplots()
    pattern_highlight_region()
    pattern_reference_lines()

    """
    Day 32 요약
    - 단일 그래프보다 '구조화된 시각화'가 중요
    - 비교, 강조, 기준선은 시각적 메시지를 강화한다
    - matplotlib은 '그림 도구'가 아니라 '의사소통 도구'다
    """