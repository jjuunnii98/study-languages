"""
Day 53 (Data Analysis) — Visual EDA
파일: 01_python/05_data_analysis/02_eda/04_visual_eda.py

목표(한국어):
- 시각화 기반 EDA를 "재현 가능(reproducible)"하게 수행하는 템플릿을 만든다.
- 단순 예쁜 플롯이 아니라, 모델링/의사결정에 도움이 되는 시각 진단을 한다.
- 결측치, 분포, 이상치, 상관관계, 세그먼트 비교를 빠르게 훑는다.

핵심 설계:
- 기본 데이터셋: seaborn 'tips' (외부 파일이 없어도 실행 가능)
- 옵션: CSV 파일 로딩도 지원
- 출력: plots/ 폴더에 PNG 저장 + console에 진단 로그 출력
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence, Tuple, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# seaborn은 "스타일"보다, 샘플 데이터 및 간단 플롯 편의를 위해 사용
# (matplotlib 중심 유지)
import seaborn as sns


# -----------------------------
# 설정(설계 파라미터)
# -----------------------------
@dataclass(frozen=True)
class VisualEDAConfig:
    output_dir: str = "plots"          # 그림 저장 폴더
    max_categories: int = 15           # 범주형 top-k 표시 제한
    corr_method: str = "pearson"       # "pearson" 또는 "spearman"
    bins: int = 30                     # 히스토그램 bins
    top_numeric: int = 8               # 숫자형 상위 N개만 pairplot/scatter matrix 후보로
    random_state: int = 42             # 샘플링 재현성
    sample_rows_for_pair: int = 800    # pairplot(대체)용 샘플링(대용량 대비)


# -----------------------------
# 유틸
# -----------------------------
def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def infer_column_types(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    숫자형/범주형 컬럼을 대략적으로 분리한다.
    - 숫자형: number dtype
    - 범주형: object/category/bool 및 나머지(단, 너무 많은 unique는 제외 가능)
    """
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    return numeric_cols, categorical_cols


def safe_savefig(fig: plt.Figure, outpath: Path, dpi: int = 140) -> None:
    """한국어: 동일한 저장 정책(타이트, dpi)으로 저장."""
    fig.tight_layout()
    fig.savefig(outpath, dpi=dpi)
    plt.close(fig)


def top_k_categories(series: pd.Series, k: int) -> pd.Index:
    """한국어: 카테고리 top-k 값만 추출."""
    return series.value_counts(dropna=False).head(k).index


def print_section(title: str) -> None:
    bar = "-" * len(title)
    print(f"\n{title}\n{bar}")


# -----------------------------
# 로딩
# -----------------------------
def load_dataset(csv_path: Optional[str] = None) -> pd.DataFrame:
    """
    csv_path가 있으면 해당 CSV 로딩, 없으면 seaborn tips 로딩.
    """
    if csv_path:
        df = pd.read_csv(csv_path)
        return df
    return sns.load_dataset("tips")


# -----------------------------
# 시각화: 결측치
# -----------------------------
def plot_missingness(df: pd.DataFrame, outdir: Path) -> None:
    """
    결측치 진단:
    - 컬럼별 결측 비율 bar chart
    """
    miss_rate = df.isna().mean().sort_values(ascending=False)
    miss_rate = miss_rate[miss_rate > 0]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    if len(miss_rate) == 0:
        ax.text(0.5, 0.5, "No missing values detected", ha="center", va="center")
        ax.set_axis_off()
        safe_savefig(fig, outdir / "missingness_none.png")
        return

    ax.bar(miss_rate.index.astype(str), miss_rate.values)
    ax.set_title("Missing Rate by Column")
    ax.set_ylabel("Missing rate")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=45)
    safe_savefig(fig, outdir / "missingness_rate.png")


# -----------------------------
# 시각화: 숫자형 분포/이상치
# -----------------------------
def plot_numeric_distributions(df: pd.DataFrame, numeric_cols: Sequence[str], cfg: VisualEDAConfig, outdir: Path) -> None:
    """
    숫자형 컬럼 분포:
    - 히스토그램
    - 박스플롯(이상치 감지용)
    """
    if not numeric_cols:
        return

    for col in numeric_cols:
        series = df[col].dropna()

        # 히스토그램
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(series.values, bins=cfg.bins)
        ax.set_title(f"Histogram: {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        safe_savefig(fig, outdir / f"hist_{col}.png")

        # 박스플롯
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.boxplot(series.values, vert=True)
        ax.set_title(f"Boxplot: {col}")
        ax.set_ylabel(col)
        safe_savefig(fig, outdir / f"box_{col}.png")


# -----------------------------
# 시각화: 범주형 분포
# -----------------------------
def plot_categorical_counts(df: pd.DataFrame, categorical_cols: Sequence[str], cfg: VisualEDAConfig, outdir: Path) -> None:
    """
    범주형 컬럼:
    - top-k 빈도 bar chart
    """
    if not categorical_cols:
        return

    for col in categorical_cols:
        s = df[col]
        # 너무 많은 unique는 시각화 가독성 저하 → top-k만
        top_idx = top_k_categories(s, cfg.max_categories)
        vc = s.value_counts(dropna=False).reindex(top_idx)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.bar(vc.index.astype(str), vc.values)
        ax.set_title(f"Category Count (Top {cfg.max_categories}): {col}")
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=45)
        safe_savefig(fig, outdir / f"cat_{col}.png")


# -----------------------------
# 시각화: 상관관계 히트맵
# -----------------------------
def plot_correlation_heatmap(df: pd.DataFrame, numeric_cols: Sequence[str], cfg: VisualEDAConfig, outdir: Path) -> None:
    """
    상관관계:
    - pearson/spearman heatmap
    """
    if len(numeric_cols) < 2:
        return

    corr = df[numeric_cols].corr(method=cfg.corr_method)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    im = ax.imshow(corr.values, aspect="auto")

    ax.set_title(f"Correlation Heatmap ({cfg.corr_method})")
    ax.set_xticks(range(len(numeric_cols)))
    ax.set_yticks(range(len(numeric_cols)))
    ax.set_xticklabels(numeric_cols, rotation=45, ha="right")
    ax.set_yticklabels(numeric_cols)

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    safe_savefig(fig, outdir / f"corr_heatmap_{cfg.corr_method}.png")


# -----------------------------
# 시각화: 세그먼트 비교(박스플롯)
# -----------------------------
def plot_segment_boxplots(
    df: pd.DataFrame,
    numeric_cols: Sequence[str],
    categorical_cols: Sequence[str],
    cfg: VisualEDAConfig,
    outdir: Path,
) -> None:
    """
    세그먼트 비교:
    - 범주형 1개 × 숫자형 1개 박스플롯
    - 범주형 후보는 unique가 너무 큰 것 제외
    """
    if not numeric_cols or not categorical_cols:
        return

    # unique가 적당한(2~15 정도) 범주형만 사용
    candidate_cats = []
    for c in categorical_cols:
        nunique = df[c].nunique(dropna=False)
        if 2 <= nunique <= min(cfg.max_categories, 15):
            candidate_cats.append(c)

    if not candidate_cats:
        return

    # 너무 많은 조합은 과도 → 상위 2개 범주형만 사용
    candidate_cats = candidate_cats[:2]
    use_numeric = list(numeric_cols)[: min(len(numeric_cols), 5)]

    for cat in candidate_cats:
        for num in use_numeric:
            tmp = df[[cat, num]].dropna()
            if tmp.empty:
                continue

            # seaborn boxplot 활용(표준화된 보기)
            fig = plt.figure(figsize=(8, 5))
            ax = fig.add_subplot(111)
            sns.boxplot(data=tmp, x=cat, y=num, ax=ax)
            ax.set_title(f"Segment Boxplot: {num} by {cat}")
            ax.tick_params(axis="x", rotation=45)
            safe_savefig(fig, outdir / f"seg_box_{num}_by_{cat}.png")


# -----------------------------
# 텍스트/로그: 상관 Top Pairs 출력(실무용)
# -----------------------------
def report_top_correlations(df: pd.DataFrame, numeric_cols: Sequence[str], method: str = "pearson", top_n: int = 10) -> None:
    """
    한국어:
    - 상관계수 상위 pair를 콘솔에 출력하여
      feature redundancy/다중공선성 후보를 빠르게 확인한다.
    """
    if len(numeric_cols) < 2:
        return

    corr = df[numeric_cols].corr(method=method).abs()
    # 자기 자신 제거 후 upper triangle만 추출
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    pairs = corr.where(mask).stack().sort_values(ascending=False).head(top_n)

    print_section(f"Top {top_n} absolute correlations ({method})")
    if pairs.empty:
        print("No correlation pairs available.")
        return

    for (a, b), v in pairs.items():
        print(f"- {a} vs {b}: |corr|={v:.4f}")


# -----------------------------
# 메인 실행
# -----------------------------
def run_visual_eda(csv_path: Optional[str] = None, cfg: Optional[VisualEDAConfig] = None) -> None:
    cfg = cfg or VisualEDAConfig()
    outdir = ensure_dir(cfg.output_dir)

    df = load_dataset(csv_path)

    print_section("Dataset Overview")
    print(f"Shape: {df.shape}")
    print(df.head(5))

    numeric_cols, categorical_cols = infer_column_types(df)
    print_section("Inferred Column Types")
    print(f"Numeric columns ({len(numeric_cols)}): {numeric_cols}")
    print(f"Categorical columns ({len(categorical_cols)}): {categorical_cols}")

    # 1) 결측치
    print_section("Missingness")
    miss = df.isna().mean().sort_values(ascending=False)
    print(miss[miss > 0].head(20) if (miss > 0).any() else "No missing values.")
    plot_missingness(df, outdir)

    # 2) 숫자형 분포 + 이상치
    print_section("Numeric Distributions & Outliers")
    plot_numeric_distributions(df, numeric_cols, cfg, outdir)

    # 3) 범주형 빈도
    print_section("Categorical Counts")
    plot_categorical_counts(df, categorical_cols, cfg, outdir)

    # 4) 상관관계
    print_section("Correlation")
    plot_correlation_heatmap(df, numeric_cols, cfg, outdir)
    report_top_correlations(df, numeric_cols, method=cfg.corr_method, top_n=10)

    # 5) 세그먼트 비교
    print_section("Segment Comparisons")
    plot_segment_boxplots(df, numeric_cols, categorical_cols, cfg, outdir)

    print_section("Done")
    print(f"Saved plots to: {outdir.resolve()}")
    print("Tip: Change cfg.output_dir to keep plots organized by project/date.")


if __name__ == "__main__":
    # 기본 실행: tips 데이터로 실행 (외부 파일 필요 없음)
    # CSV로 실행하려면: run_visual_eda(csv_path="path/to/your.csv")
    run_visual_eda()