"""
Day 61 — Feature Engineering: Text Features (04_text_features.py)

목표
- 텍스트(리뷰/로그/메모 등)에서 모델 입력에 유용한 피처를 생성한다.
- "문자열 조작"이 아니라, 재현 가능한 전처리/특징 추출 파이프라인을 만든다.
- 최소 의존성(표준 라이브러리 + pandas/numpy)로 동작하도록 설계하고,
  scikit-learn이 있으면 TF-IDF까지 확장한다.

핵심 피처(한국어)
1) Cleaning / Normalization
   - lowercasing, whitespace 정리, 기본적인 punctuation 제거
   - 숫자 패턴/이메일 패턴/URL 등은 규칙으로 대체 가능(간단 버전 포함)

2) Basic statistics features
   - char_len, word_count, avg_word_len
   - digit_count, uppercase_ratio(원문 기준), punctuation_count
   - has_url, has_email, has_number 등 이진 피처

3) Keyword / dictionary features (rule-based)
   - 도메인 키워드(예: 긍정/부정 단어, 구매 관련 단어) 카운트
   - 작은 데이터/프로토타입에서 강력한 베이스라인

4) (Optional) Bag-of-Words / TF-IDF
   - scikit-learn이 설치되어 있으면 TF-IDF matrix를 만든다.
   - 다만 본 파일은 "피처 엔지니어링" 관점이라,
     대규모 sparse matrix는 별도 모델링 단계에서 다루는 것을 권장.

누수(leakage) 주의
- 텍스트 피처 자체는 보통 누수 가능성이 낮지만,
  라벨(정답) 정보가 텍스트에 포함되거나(예: "refund approved"),
  예측 시점 이후의 로그/메모를 포함하면 누수가 생길 수 있다.
- 따라서 "예측 시점 기준으로 관측 가능한 텍스트만" 사용해야 한다.

실행
- 샘플 데이터를 생성하고, 텍스트 피처를 생성한 뒤 일부 출력한다.

요구사항
- pandas, numpy
- (선택) scikit-learn
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


# -------------------------------
# 0) 샘플 텍스트 데이터 생성
# -------------------------------
def make_sample_text_data(random_state: int = 42) -> pd.DataFrame:
    """
    외부 데이터 없이도 실행 가능하도록 샘플 텍스트 데이터를 만든다.
    - 실제 환경에서는 review_text, message, log_line 같은 컬럼을 대상으로 적용한다.
    """
    rng = np.random.default_rng(random_state)

    samples = [
        "Loved it!! Fast delivery and great quality. Highly recommend :)",
        "Terrible experience... item arrived broken. refund please",
        "Not bad. Could be better; packaging was okay.",
        "배송이 빨랐고 품질도 좋아요! 다음에도 구매할게요",
        "환불 요청합니다. 제품이 고장나서 왔어요.",
        "Support replied in 2 days. My email is user@example.com",
        "Check details at https://example.com/product?id=123",
        "I paid $120 for this and got 2 items. Worth it!",
        "Worst. Never again!!!",
        "Okay-ish. 3/5. Nothing special.",
    ]

    # 약간 섞어서 더 만들기
    n = 40
    text = [samples[int(rng.integers(0, len(samples)))] for _ in range(n)]
    user_id = rng.integers(1, 11, size=n)

    # 라벨은 데모용(실제 feature engineering에서는 label 없어도 됨)
    # 여기서는 감성의 rough label: positive/negative/neutral
    label = []
    for t in text:
        t_low = t.lower()
        if any(w in t_low for w in ["loved", "great", "recommend", "좋아요", "구매"]):
            label.append("positive")
        elif any(w in t_low for w in ["terrible", "broken", "refund", "worst", "환불", "고장"]):
            label.append("negative")
        else:
            label.append("neutral")

    df = pd.DataFrame({"user_id": user_id, "text": text, "label": label})
    return df


# -------------------------------
# 1) 정규화/정제 유틸
# -------------------------------
_URL_RE = re.compile(r"(https?://\S+|www\.\S+)", re.IGNORECASE)
_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
_NUMBER_RE = re.compile(r"\b\d+(?:[.,]\d+)?\b")
_PUNCT_RE = re.compile(r"[^\w\s]", re.UNICODE)


def normalize_text_basic(text: str) -> str:
    """
    기본 텍스트 정제:
    - 소문자화
    - URL/EMAIL을 토큰으로 치환(정보 유출 방지 및 패턴 일반화)
    - 숫자 토큰 치환
    - 구두점 제거(간단 버전)
    - 공백 정리

    한국어 포인트:
    - 한국어 토큰화는 형태소 분석이 필요할 수 있으나,
      본 Day 61은 '베이스라인 텍스트 피처' 중심으로 간다.
    """
    if text is None:
        return ""

    s = str(text)
    s = s.strip()

    # 원문에서 중요한 패턴은 토큰으로 치환
    s = _URL_RE.sub(" <URL> ", s)
    s = _EMAIL_RE.sub(" <EMAIL> ", s)
    s = _NUMBER_RE.sub(" <NUM> ", s)

    # 소문자화(한국어에는 영향 거의 없음)
    s = s.lower()

    # 구두점 제거(단, <> 토큰은 보존되도록 처리)
    # "<URL>" 같은 토큰이 깨지지 않게 먼저 보호
    s = s.replace("<url>", "URLTOKEN").replace("<email>", "EMAILTOKEN").replace("<num>", "NUMTOKEN")
    s = _PUNCT_RE.sub(" ", s)
    s = s.replace("URLTOKEN", "<URL>").replace("EMAILTOKEN", "<EMAIL>").replace("NUMTOKEN", "<NUM>")

    # 공백 정리
    s = re.sub(r"\s+", " ", s).strip()
    return s


def simple_tokenize(text: str) -> List[str]:
    """
    아주 단순한 토큰화:
    - 공백 기준 split
    - 빈 토큰 제거

    한국어 포인트:
    - 한국어는 공백 토큰화만으로는 한계가 있지만,
      베이스라인에서는 word_count/키워드 카운트에 유효하다.
    """
    if not text:
        return []
    return [tok for tok in text.split(" ") if tok]


# -------------------------------
# 2) 통계 기반 텍스트 피처
# -------------------------------
def compute_basic_text_features(df: pd.DataFrame, text_col: str, out_prefix: str = "txt_") -> pd.DataFrame:
    """
    텍스트의 길이/구성/패턴 기반 피처를 만든다.
    - 모델 성능에 직결되는 경우가 많음(짧은/긴 텍스트, 숫자 포함 여부 등)

    주의(한국어):
    - uppercase_ratio 같은 피처는 한국어 비중이 크면 해석이 약해질 수 있음.
      다국어 데이터에서는 언어별 분리 후 적용도 고려.
    """
    out = df.copy()

    raw = out[text_col].fillna("").astype(str)

    # 원문 기준 피처
    out[f"{out_prefix}char_len"] = raw.str.len()
    out[f"{out_prefix}punct_count"] = raw.apply(lambda s: len(re.findall(r"[^\w\s]", s)))
    out[f"{out_prefix}digit_count"] = raw.apply(lambda s: len(re.findall(r"\d", s)))
    out[f"{out_prefix}has_url"] = raw.str.contains(_URL_RE).astype(int)
    out[f"{out_prefix}has_email"] = raw.str.contains(_EMAIL_RE).astype(int)
    out[f"{out_prefix}has_number"] = raw.str.contains(_NUMBER_RE).astype(int)

    # 대문자 비율(원문 기준)
    def uppercase_ratio(s: str) -> float:
        if not s:
            return 0.0
        letters = [ch for ch in s if ch.isalpha()]
        if not letters:
            return 0.0
        upper = sum(1 for ch in letters if ch.isupper())
        return upper / len(letters)

    out[f"{out_prefix}uppercase_ratio"] = raw.apply(uppercase_ratio)

    # 정규화 텍스트 + 토큰 기반 피처
    out[f"{out_prefix}norm"] = raw.apply(normalize_text_basic)
    tokens = out[f"{out_prefix}norm"].apply(simple_tokenize)

    out[f"{out_prefix}word_count"] = tokens.apply(len)
    out[f"{out_prefix}unique_word_count"] = tokens.apply(lambda xs: len(set(xs)))
    out[f"{out_prefix}unique_ratio"] = (out[f"{out_prefix}unique_word_count"] / (out[f"{out_prefix}word_count"].replace(0, np.nan))).fillna(0.0)
    out[f"{out_prefix}avg_word_len"] = tokens.apply(lambda xs: float(np.mean([len(x) for x in xs])) if xs else 0.0)

    return out


# -------------------------------
# 3) 키워드/사전 기반 피처
# -------------------------------
@dataclass(frozen=True)
class KeywordLexicon:
    """
    규칙 기반 키워드 사전.
    - small data / cold start에서 강력한 베이스라인이 될 수 있다.
    - 도메인 단어를 추가하면서 발전시키면 된다.
    """
    positive: Tuple[str, ...] = ("love", "great", "recommend", "good", "fast", "좋아요", "만족", "추천", "구매")
    negative: Tuple[str, ...] = ("terrible", "broken", "refund", "worst", "bad", "환불", "고장", "불만", "최악")


def add_keyword_features(
    df: pd.DataFrame,
    norm_col: str,
    lexicon: KeywordLexicon = KeywordLexicon(),
    out_prefix: str = "kw_",
) -> pd.DataFrame:
    """
    정규화된 텍스트에서 키워드 카운트 피처를 만든다.
    - positive_count, negative_count, polarity_score 등

    한국어 포인트:
    - 키워드 매칭은 형태 변화에 취약할 수 있음.
      (예: "추천해요", "고장났어요") → 추후 형태소/서브워드 기반으로 확장 가능
    """
    out = df.copy()

    def count_keywords(text: str, words: Iterable[str]) -> int:
        if not text:
            return 0
        # 단순 포함 기반(토큰 기준을 쓰고 싶다면 tokenize 후 카운트)
        cnt = 0
        for w in words:
            cnt += text.count(w.lower())
        return cnt

    out[f"{out_prefix}pos_count"] = out[norm_col].apply(lambda s: count_keywords(s, lexicon.positive))
    out[f"{out_prefix}neg_count"] = out[norm_col].apply(lambda s: count_keywords(s, lexicon.negative))

    # polarity_score: (pos - neg) / (pos + neg + 1)
    denom = (out[f"{out_prefix}pos_count"] + out[f"{out_prefix}neg_count"] + 1).astype(float)
    out[f"{out_prefix}polarity_score"] = (out[f"{out_prefix}pos_count"] - out[f"{out_prefix}neg_count"]) / denom

    # flags
    out[f"{out_prefix}has_pos"] = (out[f"{out_prefix}pos_count"] > 0).astype(int)
    out[f"{out_prefix}has_neg"] = (out[f"{out_prefix}neg_count"] > 0).astype(int)

    return out


# -------------------------------
# 4) (선택) TF-IDF 피처 생성
# -------------------------------
def try_build_tfidf_features(
    texts: List[str],
    max_features: int = 200,
    ngram_range: Tuple[int, int] = (1, 2),
) -> Tuple[Optional[np.ndarray], Optional[List[str]]]:
    """
    scikit-learn이 설치되어 있으면 TF-IDF matrix를 만든다.
    - 설치되어 있지 않으면 (None, None) 반환.

    한국어 포인트:
    - TF-IDF는 sparse matrix가 기본이라 모델 단계에서 통합하는 것이 일반적.
    - 여기서는 "피처 생성 가능"을 보여주는 데모.
    """
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
    except Exception:
        return None, None

    vec = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        token_pattern=r"(?u)\b\w+\b",  # 기본 토큰 패턴 (간단)
    )
    X = vec.fit_transform(texts)
    feature_names = vec.get_feature_names_out().tolist()
    return X.toarray(), feature_names


# -------------------------------
# 5) 간단 리포트
# -------------------------------
def report_text_features(df: pd.DataFrame, cols: List[str], title: str) -> None:
    print(f"\n=== {title} ===")
    missing = df[cols].isna().mean().sort_values(ascending=False)
    print("\n[Missing Rate]")
    print(missing.head(10).round(4))

    numeric_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
    if numeric_cols:
        print("\n[Describe]")
        print(df[numeric_cols].describe().T.round(4).head(20))


# -------------------------------
# 6) 메인 데모
# -------------------------------
def main() -> None:
    df = make_sample_text_data(random_state=7)

    # 1) 기본 텍스트 피처
    df1 = compute_basic_text_features(df, text_col="text", out_prefix="txt_")

    # 2) 키워드 피처 (정규화 텍스트 기반)
    df2 = add_keyword_features(df1, norm_col="txt_norm", lexicon=KeywordLexicon(), out_prefix="kw_")

    # 3) (선택) TF-IDF
    X_tfidf, tfidf_names = try_build_tfidf_features(df2["txt_norm"].tolist(), max_features=50, ngram_range=(1, 2))

    print("\n=== Sample rows (raw + features) ===")
    show_cols = [
        "user_id",
        "text",
        "label",
        "txt_char_len",
        "txt_word_count",
        "txt_unique_ratio",
        "txt_avg_word_len",
        "txt_digit_count",
        "txt_punct_count",
        "txt_has_url",
        "txt_has_email",
        "kw_pos_count",
        "kw_neg_count",
        "kw_polarity_score",
    ]
    print(df2[show_cols].head(8).to_string(index=False))

    report_text_features(
        df2,
        cols=[
            "txt_char_len",
            "txt_word_count",
            "txt_unique_ratio",
            "txt_avg_word_len",
            "txt_digit_count",
            "txt_punct_count",
            "txt_has_url",
            "txt_has_email",
            "kw_pos_count",
            "kw_neg_count",
            "kw_polarity_score",
        ],
        title="Text feature report (Day 61)",
    )

    if X_tfidf is not None and tfidf_names is not None:
        print("\n=== TF-IDF (optional) ===")
        print(f"TF-IDF matrix shape: {X_tfidf.shape}")
        print("Top feature names (first 20):")
        print(tfidf_names[:20])
        # TF-IDF는 보통 별도 파일/모델 단계에서 다루는 것을 권장
    else:
        print("\n[TF-IDF skipped] scikit-learn is not installed. (정상)")

    print("\n✅ Done. (Day 61 text features complete)")
    print("실무 팁(한국어):")
    print("- 텍스트 피처는 '규칙 기반 + 통계 기반 + 벡터 기반(TF-IDF/임베딩)'을 조합하면 강력하다.")
    print("- 키워드/패턴 피처는 cold-start에서 특히 유용하고, TF-IDF는 중간 규모까지 좋은 베이스라인이다.")
    print("- 운영 환경에서는 전처리 규칙(정규화/토큰화)을 반드시 고정하고 버전 관리해야 재현성이 유지된다.")


if __name__ == "__main__":
    main()