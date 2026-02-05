"""
Day 33: Save & Export Figures (Matplotlib)

이 파일은 matplotlib 그림(Figure)을 저장/내보내기(export) 하는
실무 패턴을 정리한다.

왜 중요한가?
- 분석 결과는 "보여주는 것"에서 끝나지 않는다.
- 보고서(PDF), 논문, 슬라이드, 웹 대시보드, 제품 UI에 넣기 위해
  반드시 '저장 품질'이 보장되어야 한다.

핵심 포인트
1) 파일명 규칙/폴더 구조(자동 생성)
2) dpi, bbox_inches, facecolor(배경), transparent
3) 벡터 포맷(svg/pdf) vs 래스터(png/jpg) 구분
4) 동일 코드로 재현 가능하도록 함수화
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt


# ---------------------------
# 0. Export Configuration
# ---------------------------
@dataclass(frozen=True)
class ExportConfig:
    """
    Export 설정을 한 곳에 모아 관리하는 구조
    - 실무에서는 프로젝트마다 저장 정책이 존재한다.
    """
    out_dir: Path = Path("reports/figures")  # 결과 저장 폴더(권장: reports 아래)
    dpi: int = 150  # 화면/웹용 기본 해상도
    bbox_inches: str = "tight"  # 여백 최소화
    facecolor: str = "white"  # 배경색(논문/리포트 기본은 white)
    transparent: bool = False  # 투명 배경이 필요하면 True


def ensure_dir(path: Path) -> None:
    """폴더가 없으면 생성한다."""
    path.mkdir(parents=True, exist_ok=True)


def build_filename(
    stem: str,
    ext: str,
    add_timestamp: bool = False,
) -> str:
    """
    파일명 생성 규칙
    - stem: 기본 이름(예: "line_plot")
    - ext: 확장자(예: "png", "svg")
    - add_timestamp: 덮어쓰기 방지용 타임스탬프 추가 여부

    한국어 팁:
    - GitHub에 올릴 땐 보통 timestamp 없이 '고정된 파일명'이 더 좋다.
      (README에서 항상 같은 링크를 가리킬 수 있기 때문)
    """
    if add_timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{stem}_{ts}.{ext}"
    return f"{stem}.{ext}"


def save_figure(
    fig: plt.Figure,
    stem: str,
    config: ExportConfig,
    ext: str = "png",
    add_timestamp: bool = False,
) -> Path:
    """
    Figure 저장 함수
    - ext: png, jpg, svg, pdf 등
    - 벡터(svg/pdf)는 확대해도 깨지지 않아 논문/슬라이드에 매우 유리
    """
    ensure_dir(config.out_dir)
    filename = build_filename(stem=stem, ext=ext, add_timestamp=add_timestamp)
    out_path = config.out_dir / filename

    fig.savefig(
        out_path,
        dpi=config.dpi if ext.lower() in {"png", "jpg", "jpeg"} else None,
        bbox_inches=config.bbox_inches,
        facecolor=config.facecolor,
        transparent=config.transparent,
    )
    return out_path


# ---------------------------
# 1. Demo Plot: Minimal Example
# ---------------------------
def make_demo_plot() -> plt.Figure:
    """저장 테스트용 간단한 그래프를 만든다."""
    xs = [0, 1, 2, 3, 4, 5]
    ys = [0, 1, 4, 9, 16, 25]

    fig, ax = plt.subplots()
    ax.plot(xs, ys, label="y = x^2")
    ax.set_title("Demo Plot")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.3)
    ax.legend()
    return fig


# ---------------------------
# 2. Recommended Export Strategy
# ---------------------------
def export_demo() -> None:
    """
    실무 권장 전략:
    - 웹/README: png
    - 논문/슬라이드/디자인: svg 또는 pdf

    한국어 팁:
    - png는 GitHub preview가 편하지만 확대하면 깨진다.
    - svg는 확대해도 선명하고, 가볍고, 문서에 넣기 좋다.
    """
    config = ExportConfig(
        out_dir=Path("reports/figures"),
        dpi=200,  # 조금 더 선명하게(웹/README에 좋음)
        facecolor="white",
        transparent=False,
    )

    fig = make_demo_plot()

    # 1) PNG 저장 (웹/README용)
    png_path = save_figure(fig, stem="day33_demo_plot", config=config, ext="png")
    print(f"[Saved] PNG -> {png_path}")

    # 2) SVG 저장 (벡터: 논문/슬라이드용)
    svg_path = save_figure(fig, stem="day33_demo_plot", config=config, ext="svg")
    print(f"[Saved] SVG -> {svg_path}")

    # 리소스 해제(대량 생성 시 메모리 관리)
    plt.close(fig)


# ---------------------------
# 3. Notes on Git Tracking
# ---------------------------
def print_git_notes() -> None:
    """
    GitHub 업로드 전략(한국어)
    - 코드 + (필요한 경우) 대표 이미지 1~2개만 커밋하는 것을 권장
    - 너무 많은 png 생성물을 올리면 repo가 빠르게 커진다.

    추천 방식:
    - reports/figures 아래에서 "대표 결과"만 추려서 커밋
    - 나머지는 로컬/외장/클라우드에 보관
    """
    msg = """
[GitHub 업로드 팁]
- reports/figures/* : 대표 결과물만 선택적으로 커밋
- 데이터/대량 결과물은 repo에 올리지 말고 로컬/SSD에 보관
- README에는 대표 이미지 링크를 연결해서 "성과"를 보여주기
"""
    print(msg.strip())


# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    export_demo()
    print_git_notes()