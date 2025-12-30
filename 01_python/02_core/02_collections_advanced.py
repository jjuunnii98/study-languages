"""
Day 6: Adanvced Collections (컬렉션 심화)

이 파일에서는 파이썬 컬렉션을 '실전 데이터 처리' 관점에서 심화 학습한다. 
핵심: 
- 중첩 자료구조(list/dict of dict) 
- 정렬(key 함수) 
- dict 빈도 계산 패턴(get, setdefault) 
- collections.Counter / defaultdict 
- 안전한 조회(get)와 병합(update) 
- 실전: 간단한 집계/그룹핑 구현

데이터 분석(EDA/feature engineering)과 백엔드 로직에서도 컬렉션을 다루는 능력은 필수다. 
"""

from collections import Counter, defaultdict

# ==================================================
# 1. 중첩 자료구조: list of dict (가장 흔한 형태)
# ==================================================
# 실전 데이터는 종종 "레코드들의 리스트" 형태로 온다. (JSON, API 응답 등)

records = [
    {"id": 1, "name": "Junyeong", "dept": "IT", "score": 92},
    {"id": 2, "name": "Mina", "dept": "HR", "score": 76},
    {"id": 3, "name": "Alex", "dept": "IT", "score": 88}, 
    {"id": 4, "name": "Sora", "dept": "Finace", "score": 90}, 
    {"id": 5, "name": "Jin", "dept": "IT", "score": 61},
]

print("records[0]:", records[0])  # 첫 번째 레코드
print("names:", [r["name"] for r in records])  # 모든 이름 추출

# ==================================================
# 2. 정렬: sorted(key=...) 활용
# ==================================================
# - score 높은 순으로 정렬
# - dept 기준 정렬 후 score 정렬

