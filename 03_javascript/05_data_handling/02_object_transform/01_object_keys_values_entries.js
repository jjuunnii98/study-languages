/*
Day 53 — Object Transform: keys / values / entries

File
03_javascript/05_data_handling/02_object_transform/01_object_keys_values_entries.js

목표
JavaScript 객체(Object)를 배열처럼 다루기 위한 핵심 메서드를 익힌다.

1) Object.keys()
2) Object.values()
3) Object.entries()

이 메서드들은 객체 데이터를 순회하거나,
배열 메서드(map/filter/reduce)와 결합해서
실무형 데이터 변환을 할 때 매우 자주 사용된다.

한국어 설명
객체(Object)는 JavaScript에서 key-value 구조로 데이터를 저장한다.
하지만 map(), filter(), reduce() 같은 배열 메서드는
객체에 직접 사용할 수 없다.

그래서 먼저
- keys
- values
- entries
형태로 바꾼 뒤
배열처럼 처리하는 패턴이 중요하다.
*/


/* ============================================================
1) Example Object
============================================================ */

/*
사용자 점수 데이터라고 가정
key   = 사용자 이름
value = 점수
*/

const scores = {
  alice: 85,
  bob: 92,
  charlie: 78,
  david: 88
};

console.log("Original object:", scores);


/* ============================================================
2) Object.keys()
============================================================ */

/*
Object.keys(obj)
→ 객체의 key만 배열로 반환

한국어 설명
객체의 "속성 이름 목록"만 필요할 때 사용한다.
*/

const scoreKeys = Object.keys(scores);

console.log("Object.keys(scores):", scoreKeys);

/*
결과 예시
["alice", "bob", "charlie", "david"]
*/


/* ============================================================
3) Object.values()
============================================================ */

/*
Object.values(obj)
→ 객체의 value만 배열로 반환

한국어 설명
객체 안의 실제 값들만 꺼내고 싶을 때 사용한다.
*/

const scoreValues = Object.values(scores);

console.log("Object.values(scores):", scoreValues);

/*
결과 예시
[85, 92, 78, 88]
*/


/* ============================================================
4) Object.entries()
============================================================ */

/*
Object.entries(obj)
→ [key, value] 형태의 2차원 배열 반환

한국어 설명
객체를 배열처럼 변환해서 순회하거나,
map/filter/reduce를 적용할 때 가장 많이 사용된다.
*/

const scoreEntries = Object.entries(scores);

console.log("Object.entries(scores):", scoreEntries);

/*
결과 예시
[
  ["alice", 85],
  ["bob", 92],
  ["charlie", 78],
  ["david", 88]
]
*/


/* ============================================================
5) keys를 사용한 순회
============================================================ */

/*
keys 배열을 이용해서 객체를 순회
*/

console.log("Loop using Object.keys():");
Object.keys(scores).forEach((name) => {
  console.log(`${name}: ${scores[name]}`);
});


/* ============================================================
6) values를 사용한 집계
============================================================ */

/*
점수 평균 계산
*/

const averageScore =
  Object.values(scores).reduce((sum, value) => sum + value, 0) /
  Object.values(scores).length;

console.log("Average score:", averageScore);


/* ============================================================
7) entries를 사용한 변환
============================================================ */

/*
점수가 80 이상인 사용자만 추출
*/

const highScoreUsers = Object.entries(scores)
  .filter(([name, score]) => score >= 80);

console.log("High score users:", highScoreUsers);

/*
결과 예시
[
  ["alice", 85],
  ["bob", 92],
  ["david", 88]
]
*/


/* ============================================================
8) entries + map
============================================================ */

/*
문자열 리포트 생성
*/

const scoreReport = Object.entries(scores).map(([name, score]) => {
  return `${name} scored ${score}`;
});

console.log("Score report:", scoreReport);


/* ============================================================
9) entries + reduce
============================================================ */

/*
객체에서 최고 점수 찾기
*/

const topScorer = Object.entries(scores).reduce(
  (best, current) => {
    const [bestName, bestScore] = best;
    const [currentName, currentScore] = current;

    return currentScore > bestScore ? current : best;
  }
);

console.log("Top scorer:", topScorer);

/*
결과 예시
["bob", 92]
*/


/* ============================================================
10) Real-World Example: API Stats Object
============================================================ */

/*
API 응답 통계 객체라고 가정
*/

const apiStats = {
  requests: 1200,
  success: 1140,
  errors: 60
};

console.log("API stats keys:", Object.keys(apiStats));
console.log("API stats values:", Object.values(apiStats));
console.log("API stats entries:", Object.entries(apiStats));

/*
전체 합계 계산
*/

const totalEvents = Object.values(apiStats).reduce((sum, value) => sum + value, 0);
console.log("Total events:", totalEvents);


/* ============================================================
11) Convert object entries to readable rows
============================================================ */

/*
객체를 UI 출력용 배열로 변환
*/

const apiRows = Object.entries(apiStats).map(([metric, value]) => {
  return {
    metric: metric,
    value: value
  };
});

console.log("API rows:", apiRows);

/*
결과 예시
[
  { metric: "requests", value: 1200 },
  { metric: "success", value: 1140 },
  { metric: "errors", value: 60 }
]
*/


/* ============================================================
12) Summary
============================================================ */

/*
정리

Object.keys()
→ key 배열 반환

Object.values()
→ value 배열 반환

Object.entries()
→ [key, value] 배열 반환

실무에서는 보통 Object.entries()가 가장 강력하다.
왜냐하면 key와 value를 함께 다루면서
map/filter/reduce를 적용할 수 있기 때문이다.
*/

console.log("Summary complete.");