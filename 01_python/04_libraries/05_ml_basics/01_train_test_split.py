"""
Day 37: Train / Test Split (훈련/테스트 분리)

[EN]
This file explains and demonstrates best practices for train/test splitting:
- Why we split and what can go wrong (data leakage)
- Random split with reproducibility (seed)
- Stratified split for classification imbalance
- Time series split (no shuffle)
- Group-aware split (avoid group leakage)

[KR]
이 파일은 머신러닝에서 가장 기본이지만,
가장 많이 실수하는 주제인 train/test split을 다룬다.

핵심 포인트:
- 데이터 누수(leakage) 방지
- 재현성(random_state)
- 분류 문제에서 stratify(불균형 대응)
- 시계열 데이터는 shuffle 금지
- 환자/사용자/세션 단위 데이터는 group 단위로 분리

✅ 외부 라이브러리 없이도 동작하는 "기본 구현" + (선택) scikit-learn 사용 예시를 포함한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple, Dict, Any
import random
import math


# ------------------------------------------------------------
# 0) Types
# ------------------------------------------------------------

@dataclass(frozen=True)
class SplitResult:
    X_train: List[Any]
    X_test: List[Any]
    y_train: Optional[List[Any]] = None
    y_test: Optional[List[Any]] = None
    info: Optional[Dict[str, Any]] = None


# ------------------------------------------------------------
# 1) Core utilities
# ------------------------------------------------------------

def _validate_test_size(test_size: float) -> None:
    if not (0.0 < test_size < 1.0):
        raise ValueError("test_size must be in (0, 1).")


def _indices(n: int) -> List[int]:
    return list(range(n))


def _split_indices(indices: List[int], test_size: float) -> Tuple[List[int], List[int]]:
    """
    Split index list into train/test by test_size.
    [KR] 인덱스 리스트를 test_size 비율로 train/test로 나눈다.
    """
    n = len(indices)
    n_test = int(math.ceil(n * test_size))
    test_idx = indices[:n_test]
    train_idx = indices[n_test:]
    return train_idx, test_idx


def _subset(arr: Sequence[Any], idx: Sequence[int]) -> List[Any]:
    return [arr[i] for i in idx]


# ------------------------------------------------------------
# 2) Random split (shuffle + seed)
# ------------------------------------------------------------

def train_test_split_random(
    X: Sequence[Any],
    y: Optional[Sequence[Any]] = None,
    test_size: float = 0.2,
    shuffle: bool = True,
    random_state: int = 42,
) -> SplitResult:
    """
    Basic random train/test split.

    [KR]
    가장 기본적인 분리:
    - shuffle=True: 데이터 순서를 섞고 분리(일반적인 tabular 데이터)
    - random_state: 재현성 보장
    """
    _validate_test_size(test_size)
    n = len(X)
    if y is not None and len(y) != n:
        raise ValueError("X and y must have the same length.")

    idx = _indices(n)
    if shuffle:
        rng = random.Random(random_state)
        rng.shuffle(idx)

    train_idx, test_idx = _split_indices(idx, test_size)

    X_train = _subset(X, train_idx)
    X_test = _subset(X, test_idx)

    if y is None:
        return SplitResult(X_train=X_train, X_test=X_test, info={"method": "random"})

    y_train = _subset(y, train_idx)
    y_test = _subset(y, test_idx)

    return SplitResult(
        X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test,
        info={"method": "random", "shuffle": shuffle, "random_state": random_state}
    )


# ------------------------------------------------------------
# 3) Stratified split (classification)
# ------------------------------------------------------------

def train_test_split_stratified(
    X: Sequence[Any],
    y: Sequence[Any],
    test_size: float = 0.2,
    random_state: int = 42,
) -> SplitResult:
    """
    Stratified split: preserve class proportions in train/test.

    [KR]
    분류 문제에서 클래스 불균형이 있을 때 중요한 stratify 분리.
    - 각 클래스별로 같은 비율로 test에 배정하여 분포를 유지한다.
    """
    _validate_test_size(test_size)
    n = len(X)
    if len(y) != n:
        raise ValueError("X and y must have the same length.")

    # group indices by class label
    by_class: Dict[Any, List[int]] = {}
    for i, label in enumerate(y):
        by_class.setdefault(label, []).append(i)

    rng = random.Random(random_state)

    train_idx: List[int] = []
    test_idx: List[int] = []

    for label, idxs in by_class.items():
        idxs = idxs[:]  # copy
        rng.shuffle(idxs)
        n_test = int(math.ceil(len(idxs) * test_size))
        test_part = idxs[:n_test]
        train_part = idxs[n_test:]
        test_idx.extend(test_part)
        train_idx.extend(train_part)

    # shuffle combined indices to remove class-block order
    rng.shuffle(train_idx)
    rng.shuffle(test_idx)

    X_train = _subset(X, train_idx)
    X_test = _subset(X, test_idx)
    y_train = _subset(y, train_idx)
    y_test = _subset(y, test_idx)

    info = {
        "method": "stratified",
        "random_state": random_state,
        "class_counts_total": {k: len(v) for k, v in by_class.items()},
    }
    return SplitResult(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test, info=info)


# ------------------------------------------------------------
# 4) Time series split (no shuffle)
# ------------------------------------------------------------

def train_test_split_time_series(
    X: Sequence[Any],
    y: Optional[Sequence[Any]] = None,
    test_size: float = 0.2,
) -> SplitResult:
    """
    Time series split: keep chronological order. NO shuffle.

    [KR]
    시계열 분리에서 가장 중요한 규칙:
    - 미래 데이터를 훈련에 섞으면 leakage가 발생한다.
    - 따라서 '앞 구간=train', '뒤 구간=test'로 자른다.
    """
    _validate_test_size(test_size)
    n = len(X)
    if y is not None and len(y) != n:
        raise ValueError("X and y must have the same length.")

    idx = _indices(n)  # already ordered
    train_idx, test_idx = _split_indices(idx, test_size)

    X_train = _subset(X, train_idx)
    X_test = _subset(X, test_idx)

    if y is None:
        return SplitResult(X_train=X_train, X_test=X_test, info={"method": "time_series", "shuffle": False})

    y_train = _subset(y, train_idx)
    y_test = _subset(y, test_idx)
    return SplitResult(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test, info={"method": "time_series"})


# ------------------------------------------------------------
# 5) Group-aware split (avoid entity leakage)
# ------------------------------------------------------------

def train_test_split_group(
    X: Sequence[Any],
    groups: Sequence[Any],
    y: Optional[Sequence[Any]] = None,
    test_size: float = 0.2,
    random_state: int = 42,
) -> SplitResult:
    """
    Group-aware split: ensure no group appears in both train and test.

    [KR]
    환자/사용자/세션 단위 데이터에서 매우 중요.
    같은 group(예: patient_id)이 train과 test에 동시에 있으면
    모델이 "사람을 외우는" leakage가 발생할 수 있다.
    """
    _validate_test_size(test_size)
    n = len(X)
    if len(groups) != n:
        raise ValueError("X and groups must have the same length.")
    if y is not None and len(y) != n:
        raise ValueError("X and y must have the same length.")

    # unique groups
    unique_groups = list(dict.fromkeys(groups))  # stable unique
    rng = random.Random(random_state)
    rng.shuffle(unique_groups)

    n_test_groups = int(math.ceil(len(unique_groups) * test_size))
    test_groups = set(unique_groups[:n_test_groups])

    train_idx: List[int] = []
    test_idx: List[int] = []
    for i, g in enumerate(groups):
        if g in test_groups:
            test_idx.append(i)
        else:
            train_idx.append(i)

    X_train = _subset(X, train_idx)
    X_test = _subset(X, test_idx)

    if y is None:
        return SplitResult(
            X_train=X_train, X_test=X_test,
            info={"method": "group", "random_state": random_state, "n_test_groups": n_test_groups}
        )

    y_train = _subset(y, train_idx)
    y_test = _subset(y, test_idx)

    return SplitResult(
        X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test,
        info={"method": "group", "random_state": random_state, "n_test_groups": n_test_groups}
    )


# ------------------------------------------------------------
# 6) (Optional) scikit-learn equivalents (reference only)
# ------------------------------------------------------------

def sklearn_reference_examples() -> None:
    """
    [EN] Reference snippet for scikit-learn usage (not executed by default).
    [KR] scikit-learn을 사용하는 표준 방식 참고용(기본 실행에서는 호출하지 않음).

    - train_test_split(..., stratify=y)
    - GroupShuffleSplit
    - TimeSeriesSplit (for CV)
    """
    # from sklearn.model_selection import train_test_split, GroupShuffleSplit, TimeSeriesSplit
    #
    # X_train, X_test, y_train, y_test = train_test_split(
    #     X, y, test_size=0.2, random_state=42, shuffle=True, stratify=y
    # )
    #
    # gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    # train_idx, test_idx = next(gss.split(X, y, groups=groups))
    #
    # tss = TimeSeriesSplit(n_splits=5)
    # for train_idx, val_idx in tss.split(X):
    #     ...
    pass


# ------------------------------------------------------------
# 7) Demo
# ------------------------------------------------------------

if __name__ == "__main__":
    # 예제 데이터(단순)
    X = list(range(1, 21))
    y_binary = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]  # 불균형 예시
    groups = ["A"] * 5 + ["B"] * 5 + ["C"] * 5 + ["D"] * 5  # 그룹(예: 환자/사용자)

    # 1) Random split
    res_random = train_test_split_random(X, y_binary, test_size=0.25, shuffle=True, random_state=2026)
    print("\n[Random Split]")
    print("X_train:", res_random.X_train)
    print("X_test :", res_random.X_test)

    # 2) Stratified split
    res_strat = train_test_split_stratified(X, y_binary, test_size=0.25, random_state=2026)
    print("\n[Stratified Split]")
    print("y_train positive:", sum(res_strat.y_train), "/", len(res_strat.y_train))
    print("y_test  positive:", sum(res_strat.y_test), "/", len(res_strat.y_test))

    # 3) Time series split
    res_ts = train_test_split_time_series(X, y_binary, test_size=0.25)
    print("\n[Time Series Split]")
    print("X_train last:", res_ts.X_train[-3:], " | X_test first:", res_ts.X_test[:3])

    # 4) Group-aware split
    res_group = train_test_split_group(X, groups, y_binary, test_size=0.25, random_state=2026)
    print("\n[Group Split]")
    print("train groups:", sorted(set(_subset(groups, [X.index(v) for v in res_group.X_train]))))
    print("test groups :", sorted(set(_subset(groups, [X.index(v) for v in res_group.X_test]))))

    print("\n[Key Reminder]")
    print("- Shuffle하면 안 되는 데이터(시계열/환자 단위)가 있다는 점이 핵심이다.")
    print("- 분류 문제에서 stratify는 거의 기본 옵션이다(특히 불균형일 때).")