"""
Day 71 — Reproducibility Notes
File: 01_python/05_data_analysis/07_reporting/03_reproducibility_notes.py

목표
- 데이터 분석 / ML 실험의 재현가능성(reproducibility)을 높이기 위한 기본 기록 구조를 만든다.
- 같은 코드와 같은 설정으로 다시 실행했을 때,
  최대한 같은 결과를 재현할 수 있도록 실험 정보를 체계적으로 남긴다.

핵심 구성
1) random seed 고정
2) 실험 config 기록
3) 데이터 개요 기록
4) 라이브러리 / 환경 버전 기록
5) 실행 시간 기록
6) 최종 reproducibility report 생성

실무 포인트
- "결과가 좋다" 보다 중요한 것은
  "그 결과를 다시 만들 수 있는가" 이다.
- 재현가능성이 없으면 실험 비교, 협업, 디버깅이 매우 어려워진다.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

import json
import os
import platform
import random
import time

import numpy as np
import pandas as pd
import sklearn
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split


# ============================================================
# 0) Config
# ============================================================

@dataclass(frozen=True)
class ReproConfig:
    random_state: int = 42
    test_size: float = 0.2
    n_samples: int = 1000
    n_features: int = 8
    n_informative: int = 4
    n_redundant: int = 2
    n_classes: int = 2
    report_dir: str = "reports"
    report_filename: str = "reproducibility_notes.txt"


# ============================================================
# 1) Seed Control
# ============================================================

def set_global_seed(seed: int) -> None:
    """
    전역 random seed 고정

    한국어 설명:
    - random
    - numpy
    - (필요시 torch, tensorflow 등도 추가 가능)

    이렇게 seed를 고정하면
    난수 기반 실험 결과를 최대한 동일하게 재현할 수 있다.
    """
    random.seed(seed)
    np.random.seed(seed)

    # 일부 라이브러리/환경은 아래 환경변수를 활용하기도 함
    os.environ["PYTHONHASHSEED"] = str(seed)


# ============================================================
# 2) Demo Data
# ============================================================

def load_demo_data(cfg: ReproConfig) -> Tuple[pd.DataFrame, pd.Series]:
    """
    실습용 classification 데이터 생성
    - reproducibility 예제이므로 dataset 생성 조건도 config에 포함
    """
    X, y = make_classification(
        n_samples=cfg.n_samples,
        n_features=cfg.n_features,
        n_informative=cfg.n_informative,
        n_redundant=cfg.n_redundant,
        n_classes=cfg.n_classes,
        random_state=cfg.random_state,
    )

    feature_names = [f"feature_{i}" for i in range(cfg.n_features)]
    X_df = pd.DataFrame(X, columns=feature_names)
    y_sr = pd.Series(y, name="target")

    return X_df, y_sr


# ============================================================
# 3) Dataset Summary
# ============================================================

def summarize_dataset(X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
    """
    데이터셋의 기본 구조를 기록
    """
    summary = {
        "n_rows": int(X.shape[0]),
        "n_features": int(X.shape[1]),
        "feature_names": list(X.columns),
        "target_positive_rate": float(y.mean()),
        "missing_total": int(X.isna().sum().sum()),
    }
    return summary


def summarize_split(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> Dict[str, Any]:
    """
    train/test split 요약
    """
    return {
        "train_shape": tuple(X_train.shape),
        "test_shape": tuple(X_test.shape),
        "train_positive_rate": float(y_train.mean()),
        "test_positive_rate": float(y_test.mean()),
    }


# ============================================================
# 4) Environment Summary
# ============================================================

def get_environment_info() -> Dict[str, Any]:
    """
    실행 환경 정보 기록

    한국어 설명:
    - Python 버전
    - OS / platform
    - 주요 라이브러리 버전

    이런 정보가 있어야 나중에 환경 차이로 발생하는 문제를 추적하기 쉽다.
    """
    env = {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "sklearn_version": sklearn.__version__,
    }
    return env


# ============================================================
# 5) Build Reproducibility Report
# ============================================================

def build_repro_report(
    cfg: ReproConfig,
    dataset_summary: Dict[str, Any],
    split_summary: Dict[str, Any],
    env_info: Dict[str, Any],
    run_started_at: str,
    run_finished_at: str,
    runtime_seconds: float,
) -> Dict[str, Any]:
    """
    재현가능성 보고서 dict 생성
    """
    report = {
        "run_started_at": run_started_at,
        "run_finished_at": run_finished_at,
        "runtime_seconds": round(runtime_seconds, 4),
        "config": asdict(cfg),
        "dataset_summary": dataset_summary,
        "split_summary": split_summary,
        "environment": env_info,
        "notes": [
            "Global random seed was fixed before dataset generation and split.",
            "Dataset generation parameters are included in config.",
            "Library versions are recorded for reproducibility.",
            "Train/test split used random_state from config.",
        ],
    }
    return report


# ============================================================
# 6) Save Report
# ============================================================

def save_report_as_text(report: Dict[str, Any], save_path: Path) -> None:
    """
    report를 txt 형식으로 저장

    한국어 설명:
    - JSON 그대로 저장해도 되지만
      txt는 사람이 바로 읽기 편하다.
    """
    lines = []
    lines.append("=== Reproducibility Notes ===\n")

    lines.append(f"Run Started At : {report['run_started_at']}")
    lines.append(f"Run Finished At: {report['run_finished_at']}")
    lines.append(f"Runtime Seconds: {report['runtime_seconds']}\n")

    lines.append("[Config]")
    for k, v in report["config"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    lines.append("[Dataset Summary]")
    for k, v in report["dataset_summary"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    lines.append("[Split Summary]")
    for k, v in report["split_summary"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    lines.append("[Environment]")
    for k, v in report["environment"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    lines.append("[Notes]")
    for note in report["notes"]:
        lines.append(f"- {note}")

    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text("\n".join(lines), encoding="utf-8")


def save_report_as_json(report: Dict[str, Any], save_path: Path) -> None:
    """
    report를 JSON 형식으로 저장
    """
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


# ============================================================
# 7) Console Print
# ============================================================

def print_report_summary(report: Dict[str, Any]) -> None:
    """
    콘솔 출력용 간단 요약
    """
    print("\n=== Reproducibility Summary ===")
    print(f"Run Started At : {report['run_started_at']}")
    print(f"Run Finished At: {report['run_finished_at']}")
    print(f"Runtime Seconds: {report['runtime_seconds']:.4f}")

    print("\n=== Config ===")
    for k, v in report["config"].items():
        print(f"{k}: {v}")

    print("\n=== Dataset Summary ===")
    for k, v in report["dataset_summary"].items():
        print(f"{k}: {v}")

    print("\n=== Split Summary ===")
    for k, v in report["split_summary"].items():
        print(f"{k}: {v}")

    print("\n=== Environment ===")
    for k, v in report["environment"].items():
        print(f"{k}: {v}")


# ============================================================
# 8) Main
# ============================================================

def main() -> None:
    cfg = ReproConfig(
        random_state=42,
        test_size=0.2,
        n_samples=1000,
        n_features=8,
        n_informative=4,
        n_redundant=2,
        n_classes=2,
        report_dir="reports",
        report_filename="reproducibility_notes.txt",
    )

    run_started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_time = time.time()

    # 1) seed 고정
    set_global_seed(cfg.random_state)

    # 2) 데이터 생성
    X, y = load_demo_data(cfg)

    # 3) split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=cfg.test_size,
        random_state=cfg.random_state,
        stratify=y,
    )

    # 4) 요약 정보 수집
    dataset_summary = summarize_dataset(X, y)
    split_summary = summarize_split(X_train, X_test, y_train, y_test)
    env_info = get_environment_info()

    # 5) 시간 기록
    end_time = time.time()
    run_finished = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    runtime_seconds = end_time - start_time

    # 6) report 생성
    report = build_repro_report(
        cfg=cfg,
        dataset_summary=dataset_summary,
        split_summary=split_summary,
        env_info=env_info,
        run_started_at=run_started,
        run_finished_at=run_finished,
        runtime_seconds=runtime_seconds,
    )

    # 7) 저장
    report_dir = Path(cfg.report_dir)
    txt_path = report_dir / cfg.report_filename
    json_path = report_dir / "reproducibility_notes.json"

    save_report_as_text(report, txt_path)
    save_report_as_json(report, json_path)

    # 8) 콘솔 출력
    print_report_summary(report)
    print(f"\nSaved text report : {txt_path}")
    print(f"Saved JSON report : {json_path}")


if __name__ == "__main__":
    main()