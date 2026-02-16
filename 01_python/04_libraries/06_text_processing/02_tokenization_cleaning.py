"""
Day 42 — Tokenization & Cleaning Pipeline (Text Processing)

This module implements a practical text preprocessing pipeline:
- normalization (case, whitespace)
- noise removal (URLs, emails, numbers)
- tokenization
- stopword removal
- simple n-grams
- frequency-based feature extraction

이 파일은 실전 텍스트 전처리 파이프라인을 다룹니다.
- 정규화(소문자화, 공백 정리)
- 노이즈 제거(URL, 이메일, 숫자 등)
- 토큰화(tokenization)
- 불용어(stopwords) 제거
- 간단한 n-gram 생성
- 빈도 기반 특징(feature) 추출
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, List, Tuple, Dict, Optional


# -----------------------------
# 0) Utilities & Config
# -----------------------------

DEFAULT_STOPWORDS_KO = {
    # 한국어 불용어(아주 최소 예시) — 필요하면 확장
    "은", "는", "이", "가", "을", "를", "에", "의", "와", "과", "도", "로", "으로", "에서", "에게", "한",
}

DEFAULT_STOPWORDS_EN = {
    # 영어 불용어(아주 최소 예시) — 필요하면 확장
    "a", "an", "the", "and", "or", "but", "to", "of", "in", "on", "for", "with", "is", "are", "was", "were",
}


@dataclass
class CleanConfig:
    """
    전처리 설정값을 하나로 모아 관리하기 위한 설정 객체.
    실제 프로젝트에서는 config를 파일(yaml/json)로 분리하는 것도 좋다.
    """
    lowercase: bool = True
    strip: bool = True
    normalize_whitespace: bool = True

    remove_urls: bool = True
    remove_emails: bool = True
    remove_numbers: bool = False  # 숫자도 의미가 있을 수 있어 기본 False
    remove_non_alnum: bool = False  # True면 기호 제거. 한국어/영어 혼합 데이터에서는 주의!

    min_token_length: int = 2
    stopwords_ko: Optional[set] = None
    stopwords_en: Optional[set] = None


# -----------------------------
# 1) Normalization & Cleaning
# -----------------------------

_URL_PATTERN = re.compile(r"(https?://\S+|www\.\S+)", re.IGNORECASE)
_EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+")
_WHITESPACE_PATTERN = re.compile(r"\s+")

# 숫자 제거용
_NUMBER_PATTERN = re.compile(r"\d+")
# 알파뉴메릭/한글 외 제거(선택)
# - \w는 언더스코어 포함, 유니코드 문자 처리 이슈가 있어 여기서는 명시적으로 처리
_NON_ALNUM_PATTERN = re.compile(r"[^0-9A-Za-z가-힣\s]")


def normalize_text(text: str, cfg: CleanConfig) -> str:
    """
    텍스트 정규화/클리닝의 핵심 단계.
    """
    if text is None:
        return ""

    s = text

    if cfg.strip:
        s = s.strip()

    if cfg.lowercase:
        s = s.lower()

    if cfg.remove_urls:
        s = _URL_PATTERN.sub(" ", s)

    if cfg.remove_emails:
        s = _EMAIL_PATTERN.sub(" ", s)

    if cfg.remove_numbers:
        s = _NUMBER_PATTERN.sub(" ", s)

    if cfg.remove_non_alnum:
        s = _NON_ALNUM_PATTERN.sub(" ", s)

    if cfg.normalize_whitespace:
        s = _WHITESPACE_PATTERN.sub(" ", s).strip()

    return s


# -----------------------------
# 2) Tokenization
# -----------------------------

_TOKEN_PATTERN = re.compile(r"[0-9A-Za-z가-힣]+")


def tokenize(text: str) -> List[str]:
    """
    아주 기본적인 토큰화:
    - 한글/영문/숫자 토큰을 정규표현식으로 추출
    - 실제 NLP에서는 형태소 분석기(예: KoNLPy) 또는 subword tokenization을 쓰지만,
      여기서는 라이브러리 의존 없이 기본 파이프라인을 보여준다.
    """
    return _TOKEN_PATTERN.findall(text)


def remove_stopwords(tokens: Iterable[str], cfg: CleanConfig) -> List[str]:
    """
    한국어/영어 불용어 제거.
    """
    stop_ko = cfg.stopwords_ko or DEFAULT_STOPWORDS_KO
    stop_en = cfg.stopwords_en or DEFAULT_STOPWORDS_EN

    filtered = []
    for t in tokens:
        if t in stop_ko:
            continue
        if t in stop_en:
            continue
        filtered.append(t)
    return filtered


def filter_tokens(tokens: Iterable[str], cfg: CleanConfig) -> List[str]:
    """
    토큰 길이 등 간단 필터링.
    """
    return [t for t in tokens if len(t) >= cfg.min_token_length]


# -----------------------------
# 3) N-grams & Features
# -----------------------------

def make_ngrams(tokens: List[str], n: int = 2) -> List[str]:
    """
    n-gram 생성.
    예: ["risk", "ai", "system"] → bigram: ["risk_ai", "ai_system"]
    """
    if n <= 1:
        return tokens[:]
    return ["_".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def top_k_terms(tokens: Iterable[str], k: int = 10) -> List[Tuple[str, int]]:
    """
    가장 많이 등장한 토큰 top-k 추출.
    """
    c = Counter(tokens)
    return c.most_common(k)


def bag_of_words(tokens: Iterable[str]) -> Dict[str, int]:
    """
    간단한 BoW(bag-of-words) 피처 생성.
    실전에서는 sklearn의 CountVectorizer를 쓰는 경우가 많지만,
    여기서는 원리를 명확히 보여주기 위해 직접 만든다.
    """
    return dict(Counter(tokens))


# -----------------------------
# 4) Pipeline Wrapper
# -----------------------------

def preprocess_text(text: str, cfg: Optional[CleanConfig] = None) -> List[str]:
    """
    텍스트 1개를 입력받아 토큰 리스트를 반환하는 전처리 파이프라인.
    """
    cfg = cfg or CleanConfig()
    normalized = normalize_text(text, cfg)
    tokens = tokenize(normalized)
    tokens = remove_stopwords(tokens, cfg)
    tokens = filter_tokens(tokens, cfg)
    return tokens


# -----------------------------
# 5) Demo / Example Usage
# -----------------------------

if __name__ == "__main__":
    cfg = CleanConfig(
        lowercase=True,
        remove_urls=True,
        remove_emails=True,
        remove_numbers=False,  # 숫자는 의미 있을 수 있어 유지
        remove_non_alnum=False,  # 기호는 토큰화 단계에서 자연스럽게 제거됨
        min_token_length=2,
    )

    samples = [
        "JUNIXION builds Risk AI for decision-making under uncertainty.",
        "Contact: junyeong@yonsei.ac.kr | Visit https://junixion.com for updates!",
        "UserID #1234 purchased 2 items on 2026-01-02.",
        "의료 데이터 분석은 재현성과 검증이 중요합니다. (Validation matters!)",
    ]

    for i, s in enumerate(samples, 1):
        tokens = preprocess_text(s, cfg)
        bigrams = make_ngrams(tokens, n=2)

        print(f"\n--- Sample {i} ---")
        print("Raw:", s)
        print("Tokens:", tokens)
        print("Top terms:", top_k_terms(tokens, k=5))
        print("Bigrams:", bigrams[:5], "..." if len(bigrams) > 5 else "")

    # BoW 예시
    all_tokens = []
    for s in samples:
        all_tokens.extend(preprocess_text(s, cfg))

    bow = bag_of_words(all_tokens)
    print("\n--- Bag of Words (partial) ---")
    # 상위 10개만 보기 좋게 출력
    for term, cnt in top_k_terms(all_tokens, k=10):
        print(f"{term:>15}: {cnt}")