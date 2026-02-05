"""
Day 31: Matplotlib Basics

이 파일은 matplotlib의 기본 사용법을 다룹니다.
데이터 분석/리포팅에서 자주 쓰는 그래프(선/산점도/막대/히스토그램)를
'Figure-Axes' 패턴으로 작성하는 연습을 합니다.

핵심 포인트
- plt.figure()만 쓰는 방식보다, (fig, ax) 패턴이 더 표준적이고 확장성이 좋다.
- 그래프에는 반드시: 제목(title), 축 라벨(xlabel/ylabel), 범례(legend, 필요 시), 격자(grid, 필요 시)
- 저장(savefig)은 리포트/논문/대시보드 작업에 필수
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt


# ---------------------------
# 0. Helper: Save wrapper
# ---------------------------
def save_figure(fig: plt.Figure, filename: str) -> None:
    """
    Figure 저장 유틸 함수
    - bbox_inches="tight": 여백 최소화
    - dpi=150: GitHub에 올릴 이미지로 적당한 해상도
    """
    fig.savefig(filename, dpi=150, bbox_inches="tight")


# ---------------------------
# 1. Line Plot (선 그래프)
# ---------------------------
def demo_line_plot() -> None:
    # 예시 데이터 생성: x=0..99, y=sin(x/10)
    xs = list(range(100))
    ys = [math.sin(x / 10) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, ys, label="sin(x/10)")  # 선 그래프

    ax.set_title("Line Plot: sin(x/10)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.3)
    ax.legend()

    save_figure(fig, "day31_line_plot.png")
    plt.show()


# ---------------------------
# 2. Scatter Plot (산점도)
# ---------------------------
def demo_scatter_plot() -> None:
    # 예시 데이터: x=0..49, y는 약간의 비선형 + noise 느낌(간단히 sin으로 대체)
    xs = list(range(50))
    ys = [x * 0.2 + math.sin(x / 2) for x in xs]

    fig, ax = plt.subplots()
    ax.scatter(xs, ys, label="points")  # 산점도

    ax.set_title("Scatter Plot: simple relationship")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.3)
    ax.legend()

    save_figure(fig, "day31_scatter_plot.png")
    plt.show()


# ---------------------------
# 3. Bar Chart (막대 그래프)
# ---------------------------
def demo_bar_chart() -> None:
    # 범주형 데이터 예시
    categories = ["A", "B", "C", "D"]
    values = [12, 7, 15, 9]

    fig, ax = plt.subplots()
    ax.bar(categories, values)

    ax.set_title("Bar Chart: category counts")
    ax.set_xlabel("category")
    ax.set_ylabel("count")
    ax.grid(True, axis="y", alpha=0.3)

    # 막대 위에 값 표시(리포트에서 매우 자주 씀)
    for i, v in enumerate(values):
        ax.text(i, v, str(v), ha="center", va="bottom")

    save_figure(fig, "day31_bar_chart.png")
    plt.show()


# ---------------------------
# 4. Histogram (히스토그램)
# ---------------------------
def demo_histogram() -> None:
    # 간단한 분포 데이터 생성 (정규분포 대신 sin 기반으로 변형)
    data = [math.sin(x / 10) + (x % 7) * 0.05 for x in range(300)]

    fig, ax = plt.subplots()
    ax.hist(data, bins=20)

    ax.set_title("Histogram: distribution overview")
    ax.set_xlabel("value")
    ax.set_ylabel("frequency")
    ax.grid(True, axis="y", alpha=0.3)

    save_figure(fig, "day31_histogram.png")
    plt.show()


# ---------------------------
# 5. Main (실행 엔트리)
# ---------------------------
if __name__ == "__main__":
    # ✅ 필요할 때만 원하는 데모를 실행하도록 구성
    demo_line_plot()
    demo_scatter_plot()
    demo_bar_chart()
    demo_histogram()

    """
    실행 팁(한국어)
    - VS Code에서 실행 시, 그래프 창이 여러 번 뜰 수 있다.
    - 원하면 demo_...() 호출을 주석 처리하고 하나씩 실행해도 좋다.
    - 결과 이미지(day31_*.png)는 repo에 포함될 수 있으니,
      용량 관리가 필요하면 .gitignore에 png를 제외하거나,
      reports/ 폴더로 모아 관리하는 전략도 가능하다.
    """