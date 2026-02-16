"""
Day 43 — Simple Sentiment Baseline (Rule/Lexicon-based)

Goal:
- Build a simple, explainable sentiment analysis baseline
- Connect Day 41–42 text preprocessing to a scoring model
- Demonstrate an end-to-end pipeline:
  normalization -> tokenization -> feature extraction -> scoring -> evaluation

이 파일의 목표:
- "설명 가능한" 감성분석 베이스라인(룰/사전 기반)을 만든다.
- Day 41–42에서 만든 텍스트 전처리를 실제 모델(점수화)에 연결한다.
- 전처리 -> 토큰화 -> 피처화 -> 스코어링 -> 평가 흐름을 한 번에 보여준다.

Notes:
- This is NOT an ML classifier. It's an interpretable baseline.
- In real projects, you'd compare this baseline vs ML/LLM models.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Tuple, Iterable


# -----------------------------
# 0) Minimal preprocessing (from Day 42 concept)
# -----------------------------

_TOKEN_PATTERN = re.compile(r"[0-9A-Za-z가-힣]+")


def normalize_text(text: str) -> str:
    """Basic normalization: lowercase + whitespace cleanup."""
    if text is None:
        return ""
    s = text.strip().lower()
    s = re.sub(r"\s+", " ", s).strip()
    return s


def tokenize(text: str) -> List[str]:
    """Regex-based tokenization (EN/KR/number tokens)."""
    return _TOKEN_PATTERN.findall(text)


# -----------------------------
# 1) Sentiment Lexicon (simple baseline)
# -----------------------------
# 실전에서는 도메인별 사전을 확장하거나, 데이터 기반으로 사전을 튜닝한다.
# 여기서는 예시 수준의 최소 사전만 제공한다.

POSITIVE_WORDS = {
    # English
    "good", "great", "excellent", "amazing", "love", "awesome", "nice", "happy", "best", "wonderful",
    "fast", "smooth", "helpful", "recommend",
    # Korean
    "좋다", "최고", "훌륭", "대박", "만족", "추천", "감사", "빠르", "편하", "행복",
}

NEGATIVE_WORDS = {
    # English
    "bad", "terrible", "awful", "hate", "worst", "slow", "bug", "bugs", "broken", "angry",
    "disappointed", "problem", "issues",
    # Korean
    "별로", "최악", "느리", "불편", "짜증", "실망", "문제", "오류", "고장", "나쁘",
}

NEGATIONS = {
    # English
    "not", "no", "never",
    # Korean (very simplified)
    "안", "못", "아니",
}

INTENSIFIERS = {
    # English
    "very": 1.5, "really": 1.4, "so": 1.2, "extremely": 1.8,
    # Korean (simplified)
    "진짜": 1.4, "너무": 1.5, "완전": 1.4, "엄청": 1.6,
}


@dataclass
class SentimentResult:
    label: str              # "positive" | "negative" | "neutral"
    score: float            # signed sentiment score
    pos_hits: List[str]     # matched positive tokens
    neg_hits: List[str]     # matched negative tokens


# -----------------------------
# 2) Scoring logic
# -----------------------------

def score_sentiment(tokens: List[str]) -> SentimentResult:
    """
    Lexicon-based scoring with simple rules:
    - +1 for positive term, -1 for negative term
    - negation flips the next sentiment token (very simplified window rule)
    - intensifier scales the next sentiment token (very simplified window rule)

    한국어 설명:
    - 긍정 단어면 +1, 부정 단어면 -1
    - 부정어(not/안 등)가 직후 감성단어를 뒤집는 간단 규칙
    - 강조어(very/너무 등)가 직후 감성단어 점수를 배율로 확대
    """
    score = 0.0
    pos_hits: List[str] = []
    neg_hits: List[str] = []

    i = 0
    while i < len(tokens):
        t = tokens[i]

        # 1) look ahead modifiers (negation / intensifier)
        negation = False
        intensity = 1.0

        if t in NEGATIONS:
            negation = True
            i += 1
            if i >= len(tokens):
                break
            t = tokens[i]  # move to next token

        if t in INTENSIFIERS:
            intensity = INTENSIFIERS[t]
            i += 1
            if i >= len(tokens):
                break
            t = tokens[i]  # move to next token

        # 2) sentiment word match
        s = 0.0
        if t in POSITIVE_WORDS:
            s = 1.0
            pos_hits.append(t)
        elif t in NEGATIVE_WORDS:
            s = -1.0
            neg_hits.append(t)

        # 3) apply modifiers
        if s != 0.0:
            s *= intensity
            if negation:
                s *= -1.0

            score += s

        i += 1

    # label decision (simple threshold)
    if score >= 1.0:
        label = "positive"
    elif score <= -1.0:
        label = "negative"
    else:
        label = "neutral"

    return SentimentResult(label=label, score=score, pos_hits=pos_hits, neg_hits=neg_hits)


def predict(text: str) -> SentimentResult:
    """Full pipeline: normalize -> tokenize -> score."""
    norm = normalize_text(text)
    tokens = tokenize(norm)
    return score_sentiment(tokens)


# -----------------------------
# 3) Evaluation (toy example)
# -----------------------------

def accuracy(y_true: Iterable[str], y_pred: Iterable[str]) -> float:
    y_true = list(y_true)
    y_pred = list(y_pred)
    if len(y_true) == 0:
        return 0.0
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    return correct / len(y_true)


def demo():
    """
    A small labeled dataset for demonstration.
    In real projects, you would:
    - load labeled dataset
    - tune lexicon / thresholds
    - compare vs ML models
    """
    samples: List[Tuple[str, str]] = [
        ("This product is very good and fast", "positive"),
        ("The service is terrible and I am disappointed", "negative"),
        ("It is okay, nothing special", "neutral"),
        ("진짜 너무 좋다 추천", "positive"),
        ("최악이다 너무 불편", "negative"),
        ("그냥 그렇다", "neutral"),
        ("not good", "negative"),          # negation test
        ("not bad", "positive"),           # negation flip test
        ("너무 별로", "negative"),
        ("완전 최고", "positive"),
    ]

    y_true = []
    y_pred = []

    print("\n--- Sentiment Baseline Demo ---")
    for text, label in samples:
        res = predict(text)
        y_true.append(label)
        y_pred.append(res.label)

        print(f"\nText: {text}")
        print(f"True: {label} | Pred: {res.label} | Score: {res.score:.2f}")
        print(f"Pos hits: {res.pos_hits}")
        print(f"Neg hits: {res.neg_hits}")

    print("\n--- Metrics ---")
    print(f"Accuracy: {accuracy(y_true, y_pred):.2%}")

    # Error analysis hint
    print("\n--- Notes ---")
    print("- This is an interpretable baseline, not a trained ML classifier.")
    print("- Improve by expanding lexicon, domain-specific terms, and better negation scope.")
    print("- Next step: Compare vs ML model (TF-IDF + LogisticRegression).")


if __name__ == "__main__":
    demo()