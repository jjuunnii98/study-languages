/*
Day 50 — Array Data Processing (map / filter / reduce)

File
03_javascript/05_data_handling/01_array_methods/01_map_filter_reduce.js

목표
JavaScript에서 배열 데이터를 처리할 때 가장 많이 사용되는
3가지 핵심 메서드를 이해한다.

1️⃣ map
2️⃣ filter
3️⃣ reduce

이 세 가지는 데이터 처리, API 응답 처리, 통계 계산 등
실무에서 매우 자주 사용된다.
*/


/* ============================================================
1️⃣ Example Dataset
============================================================ */

/*
API에서 받아온 사용자 데이터라고 가정
*/

const users = [
  { id: 1, name: "Alice", age: 25, score: 82 },
  { id: 2, name: "Bob", age: 31, score: 91 },
  { id: 3, name: "Charlie", age: 28, score: 76 },
  { id: 4, name: "David", age: 35, score: 88 }
];

console.log("Original users:", users);


/* ============================================================
2️⃣ map — 데이터 변환
============================================================ */

/*
map은 배열의 각 요소를 변환하여
새로운 배열을 만든다.

예시
사용자 이름만 추출
*/

const userNames = users.map(user => user.name);

console.log("User names:", userNames);


/*
점수를 기반으로 새로운 구조 생성
*/

const scoreSummary = users.map(user => ({
  id: user.id,
  name: user.name,
  passed: user.score >= 80
}));

console.log("Score summary:", scoreSummary);


/*
핵심 개념

map
입력 배열 → 동일 길이의 새로운 배열
*/


/* ============================================================
3️⃣ filter — 조건 기반 데이터 선택
============================================================ */

/*
filter는 조건을 만족하는 요소만 남긴다.

예시
score >= 85인 사용자
*/

const highScores = users.filter(user => user.score >= 85);

console.log("High score users:", highScores);


/*
나이가 30 이상인 사용자
*/

const age30Plus = users.filter(user => user.age >= 30);

console.log("Age 30+ users:", age30Plus);


/*
핵심 개념

filter
입력 배열 → 조건을 만족하는 일부 요소만 반환
*/


/* ============================================================
4️⃣ reduce — 집계 계산
============================================================ */

/*
reduce는 배열을 하나의 값으로 축소한다.

예시
전체 점수 합계 계산
*/

const totalScore = users.reduce((sum, user) => {
  return sum + user.score;
}, 0);

console.log("Total score:", totalScore);


/*
평균 점수 계산
*/

const avgScore = totalScore / users.length;

console.log("Average score:", avgScore);


/*
reduce 구조

array.reduce((accumulator, currentValue) => {
    return updatedAccumulator
}, initialValue)
*/


/* ============================================================
5️⃣ reduce — 객체 기반 집계
============================================================ */

/*
점수 기준 pass/fail 집계
*/

const scoreStats = users.reduce((acc, user) => {

  if (user.score >= 80) {
    acc.pass += 1;
  } else {
    acc.fail += 1;
  }

  return acc;

}, { pass: 0, fail: 0 });

console.log("Score stats:", scoreStats);


/*
출력 예시

{
  pass: 3,
  fail: 1
}
*/


/* ============================================================
6️⃣ map + filter + reduce Pipeline
============================================================ */

/*
실무에서는 이 세 가지를 조합해서 사용한다.

예시
30세 이상 사용자 평균 점수 계산
*/

const avgScore30Plus = users
  .filter(user => user.age >= 30)
  .map(user => user.score)
  .reduce((sum, score, _, arr) => sum + score / arr.length, 0);

console.log("Average score (age >= 30):", avgScore30Plus);


/*
Pipeline 구조

users
  → filter
  → map
  → reduce
*/


/* ============================================================
7️⃣ Real-World Example (API Data Processing)
============================================================ */

/*
API에서 게시글 데이터를 받았다고 가정
*/

const posts = [
  { id: 1, views: 120 },
  { id: 2, views: 90 },
  { id: 3, views: 240 },
  { id: 4, views: 60 }
];


/*
조회수 100 이상 게시글 조회
*/

const popularPosts = posts.filter(post => post.views >= 100);

console.log("Popular posts:", popularPosts);


/*
전체 조회수 계산
*/

const totalViews = posts.reduce((sum, post) => sum + post.views, 0);

console.log("Total views:", totalViews);


/*
조회수 평균
*/

const avgViews = totalViews / posts.length;

console.log("Average views:", avgViews);


/* ============================================================
Summary
============================================================ */

/*
map
→ 데이터 변환

filter
→ 조건 기반 선택

reduce
→ 집계 계산

세 가지는 JavaScript 데이터 처리의 핵심이다.
*/