"""
Day 6: Advanced Collections (컬렉션 심화)

이 파일에서는 파이썬 컬렉션을 '실전 데이터 처리' 관점에서 심화 학습한다.
핵심:
- 중첩 자료구조(list/dict of dict)
- 정렬(key 함수)
- dict 빈도 계산 패턴(get, setdefault)
- collections.Counter / defaultdict
- 안전한 조회(get)와 병합(update)
- 실전: 간단한 집계/그룹핑 구현

데이터 분석(EDA/feature engineering)과 백엔드 로직에서도
컬렉션을 다루는 능력은 필수다.
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
    {"id": 4, "name": "Sora", "dept": "Finance", "score": 90},
    {"id": 5, "name": "Jin", "dept": "IT", "score": 61},
]

print("records[0]:", records[0])
print("names:", [r["name"] for r in records])


# ==================================================
# 2. 정렬: sorted(key=...) 활용
# ==================================================
# - score 높은 순으로 정렬
# - dept 기준 정렬 후 score 정렬

sorted_by_score_desc = sorted(records, key=lambda r: r["score"], reverse=True)
print("\nTop by score:", [(r["name"], r["score"]) for r in sorted_by_score_desc])

sorted_by_dept_then_score = sorted(records, key=lambda r: (r["dept"], -r["score"]))
print("Sorted by dept then score desc:", [(r["dept"], r["name"], r["score"]) for r in sorted_by_dept_then_score])


# ==================================================
# 3. dict 빈도 계산 패턴 (get / setdefault)
# ==================================================
depts = [r["dept"] for r in records]

freq_get = {}
for d in depts:
    freq_get[d] = freq_get.get(d, 0) + 1  # get으로 기본값 0 처리
print("\nDepartment frequency (get):", freq_get)

freq_setdefault = {}
for d in depts:
    freq_setdefault.setdefault(d, 0)      # 없으면 0으로 초기화
    freq_setdefault[d] += 1
print("Department frequency (setdefault):", freq_setdefault)


# ==================================================
# 4. Counter: 빈도 계산의 표준
# ==================================================
freq_counter = Counter(depts)
print("\nDepartment frequency (Counter):", freq_counter)
print("Most common:", freq_counter.most_common(2))


# ==================================================
# 5. defaultdict: 그룹핑/누적 집계에 최적
# ==================================================
# dept별로 score 리스트를 모아보자 (그룹핑)

group_scores = defaultdict(list)
for r in records:
    group_scores[r["dept"]].append(r["score"])

print("\nGroup scores (defaultdict(list)):", dict(group_scores))

# dept별 평균 계산
dept_mean = {}
for dept, scores in group_scores.items():
    dept_mean[dept] = sum(scores) / len(scores)

print("Department mean score:", dept_mean)


# ==================================================
# 6. 중첩 dict 만들기: dict of dict
# ==================================================
# id를 key로 빠르게 조회 가능한 인덱스를 만든다.

index_by_id = {r["id"]: r for r in records}
print("\nIndex by id:", index_by_id[3])  # id=3 레코드 조회

# 안전한 조회(get): 없는 id 조회 시 에러 대신 None 반환
print("Get unknown id:", index_by_id.get(999))


# ==================================================
# 7. dict 병합과 업데이트: update / | (Python 3.9+)
# ==================================================
base_config = {"env": "dev", "debug": True, "timeout": 10}
override_config = {"debug": False, "timeout": 30}

merged = base_config.copy()
merged.update(override_config)  # override가 우선
print("\nMerged config (update):", merged)

# Python 3.9+에서는 | 연산자 병합도 가능
merged_pipe = base_config | override_config
print("Merged config (|):", merged_pipe)


# ==================================================
# 8. 실전 예제: 간단한 "조건 필터 + 집계" 구현
# ==================================================
# 목표:
# - IT 부서만 필터링
# - score 기준으로 high(>=85), mid(70-84), low(<70)로 카운트

it_records = [r for r in records if r["dept"] == "IT"]
print("\nIT records:", [(r["name"], r["score"]) for r in it_records])

bucket = {"high": 0, "mid": 0, "low": 0}
for r in it_records:
    s = r["score"]
    if s >= 85:
        bucket["high"] += 1
    elif 70 <= s <= 84:
        bucket["mid"] += 1
    else:
        bucket["low"] += 1

print("IT score buckets:", bucket)


# ==================================================
# 9. (보너스) 흔한 실수: 얕은 복사 vs 깊은 복사
# ==================================================
# 중첩 구조를 다룰 때 copy()는 얕은 복사(shallow copy)라서 주의 필요

nested = {"a": [1, 2], "b": [3, 4]}
shallow = nested.copy()
shallow["a"].append(999)

print("\nNested:", nested)
print("Shallow copy:", shallow)
print("설명: 얕은 복사는 내부 리스트를 공유하므로 원본도 같이 변할 수 있음")


"""
Day 6 요약
- 실전 데이터는 list[dict] 형태가 매우 흔하다 (API/JSON/CSV 로딩 결과)
- sorted(key=...)로 다중 조건 정렬을 구현할 수 있다
- 빈도/집계는 get/setdefault보다 Counter가 더 간결하고 안전하다
- 그룹핑은 defaultdict(list)가 매우 강력하다
- dict 인덱싱(index_by_id)로 조회 성능과 코드 가독성이 크게 개선된다
- 중첩 구조는 얕은 복사(shallow copy)에 주의
"""