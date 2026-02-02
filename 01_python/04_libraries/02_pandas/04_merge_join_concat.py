"""
Day 29: pandas Merge / Join / Concat

This module covers:
- merge() for SQL-like joins (inner/left/right/outer)
- join() for index-based joins
- concat() for stacking rows or columns

본 파일은 pandas의 데이터 결합 핵심 기능을 다룬다.
실무에서는 여러 테이블(유저/주문/로그/상품 등)을 결합하여
분석용 데이터셋을 만드는 과정이 매우 많다.

핵심 포인트:
- merge = SQL JOIN과 동일한 개념 (on, how)
- join = index 기반 결합에 편리
- concat = 행/열 방향으로 단순 결합 (stacking)
"""

import pandas as pd


# --------------------------------------------------
# 1. Sample DataFrames
# --------------------------------------------------
users = pd.DataFrame({
    "user_id": [1, 2, 3, 4],
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "segment": ["A", "B", "A", "C"]
})

orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104, 105],
    "user_id": [1, 1, 2, 4, 5],  # user_id=5는 users에 없는 케이스(outer join 예시용)
    "revenue": [120, 80, 200, 90, 50]
})

print("Users:")
print(users)
print("\nOrders:")
print(orders)


# --------------------------------------------------
# 2. merge(): SQL-like joins
# --------------------------------------------------
# (1) Inner Join: 양쪽에 모두 존재하는 key만 유지
inner_joined = pd.merge(users, orders, on="user_id", how="inner")
print("\n[merge - inner] users ∩ orders:")
print(inner_joined)

# (2) Left Join: 왼쪽(users) 기준 유지
left_joined = pd.merge(users, orders, on="user_id", how="left")
print("\n[merge - left] keep all users:")
print(left_joined)

# (3) Right Join: 오른쪽(orders) 기준 유지
right_joined = pd.merge(users, orders, on="user_id", how="right")
print("\n[merge - right] keep all orders:")
print(right_joined)

# (4) Outer Join: 양쪽 모두 포함(합집합)
outer_joined = pd.merge(users, orders, on="user_id", how="outer", indicator=True)
print("\n[merge - outer] union + indicator:")
print(outer_joined)

"""
[한국어 해설]
- how="inner": SQL INNER JOIN
- how="left": SQL LEFT JOIN
- how="right": SQL RIGHT JOIN
- how="outer": FULL OUTER JOIN
- indicator=True를 켜면 결합 결과가 어디에서 왔는지(_merge) 확인 가능
"""


# --------------------------------------------------
# 3. merge(): different key names (left_on / right_on)
# --------------------------------------------------
# 예: 사용자 테이블에는 user_id, 로그 테이블에는 uid 같은 경우
logs = pd.DataFrame({
    "uid": [1, 2, 2, 4],
    "event": ["click", "view", "purchase", "click"]
})

merged_diff_keys = pd.merge(users, logs, left_on="user_id", right_on="uid", how="left")
print("\n[merge - diff keys] left_on/right_on:")
print(merged_diff_keys)

"""
[한국어 해설]
- left_on/right_on은 컬럼명이 다를 때 사용
- 결합 후 중복 키 컬럼(uid 등)은 필요 없으면 drop 가능
"""


# --------------------------------------------------
# 4. join(): index-based join
# --------------------------------------------------
# join은 index를 기준으로 결합할 때 편리하다.

users_idx = users.set_index("user_id")
orders_sum = orders.groupby("user_id")["revenue"].sum().to_frame("total_revenue")

print("\nUsers indexed:")
print(users_idx)
print("\nOrders aggregated by user_id:")
print(orders_sum)

joined_by_index = users_idx.join(orders_sum, how="left")
print("\n[join - index] users join aggregated orders:")
print(joined_by_index)

"""
[한국어 해설]
- join은 기본적으로 index로 결합한다.
- 분석에서 '집계 테이블'을 원본 테이블에 붙일 때 매우 자주 사용된다.
"""


# --------------------------------------------------
# 5. concat(): stacking rows or columns
# --------------------------------------------------
# (1) Row-wise concat (세로로 붙이기)
new_users = pd.DataFrame({
    "user_id": [5, 6],
    "name": ["Evan", "Fiona"],
    "segment": ["B", "A"]
})

users_extended = pd.concat([users, new_users], axis=0, ignore_index=True)
print("\n[concat - rows] users extended:")
print(users_extended)

# (2) Column-wise concat (가로로 붙이기)
# 동일한 행 개수가 있고, 컬럼만 추가할 때 사용
user_scores = pd.DataFrame({
    "score": [90, 85, 88, 92]
})

users_with_scores = pd.concat([users, user_scores], axis=1)
print("\n[concat - cols] users + scores:")
print(users_with_scores)

"""
[한국어 해설]
- axis=0: 행 방향(아래로) 추가
- axis=1: 열 방향(옆으로) 추가
- ignore_index=True: 인덱스 새로 부여 (행 concat 시 보통 사용)
"""


# --------------------------------------------------
# 6. Common Pitfalls & Best Practices
# --------------------------------------------------
"""
✅ Best Practices
1) merge 전에 key 중복/결측 여부 확인:
   - users['user_id'].isna().sum()
   - users['user_id'].duplicated().sum()

2) 결합 후 row 수가 예상과 다른지 확인:
   - 예상보다 row가 증가하면 many-to-many merge 가능성

3) outer join + indicator로 데이터 정합성 체크:
   - 어떤 key가 한쪽에만 존재하는지 확인 가능

⚠ Common Pitfalls
- many-to-many merge로 데이터가 폭발적으로 증가
- key 타입 불일치(int vs str)로 결합 실패
- concat(axis=1) 시 행 정렬(index alignment) 때문에 NaN 발생
"""


# --------------------------------------------------
# 7. Summary
# --------------------------------------------------
"""
Day 29 Summary
- merge(): SQL JOIN과 동일한 결합 방식 (inner/left/right/outer)
- join(): index 기반 결합에 편리 (집계 테이블 붙이기)
- concat(): 데이터 쌓기/확장 (rows/cols)

이 기능들은 '분석용 테이블을 만드는 능력' 그 자체다.
"""