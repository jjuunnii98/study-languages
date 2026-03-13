/*
Day 52 — Nested Array Processing (flat / flatMap)

File
03_javascript/05_data_handling/01_array_methods/03_flat_flatmap.js

목표
JavaScript에서 중첩된 배열 데이터를 처리하는 방법을 이해한다.

핵심 메서드

1️⃣ flat()
2️⃣ flatMap()

이 메서드들은 API 응답 데이터나 복잡한 데이터 구조를
정규화(normalization)할 때 매우 유용하다.
*/


/* ============================================================
1️⃣ Example: Nested Array Dataset
============================================================ */

/*
중첩 배열 예시
*/

const nestedNumbers = [
  [1, 2],
  [3, 4],
  [5, 6]
];

console.log("Nested numbers:", nestedNumbers);


/* ============================================================
2️⃣ flat — 배열 평탄화
============================================================ */

/*
flat()

중첩된 배열을 하나의 배열로 펼친다.
*/

const flattenedNumbers = nestedNumbers.flat();

console.log("Flattened numbers:", flattenedNumbers);


/*
결과

[1,2,3,4,5,6]
*/


/*
flat(depth)

depth를 지정하면 더 깊은 중첩도 펼칠 수 있다.
*/

const deepNested = [1, [2, [3, [4]]]];

console.log("Flat depth=1:", deepNested.flat(1));
console.log("Flat depth=2:", deepNested.flat(2));
console.log("Flat depth=Infinity:", deepNested.flat(Infinity));


/* ============================================================
3️⃣ Real Example — API Response
============================================================ */

/*
블로그 API 응답이라고 가정

각 사용자마다 posts 배열이 존재
*/

const users = [
  {
    name: "Alice",
    posts: ["Post A", "Post B"]
  },
  {
    name: "Bob",
    posts: ["Post C"]
  },
  {
    name: "Charlie",
    posts: ["Post D", "Post E"]
  }
];


/*
모든 post를 하나의 배열로 만들기
*/

const allPosts = users.map(user => user.posts).flat();

console.log("All posts:", allPosts);


/*
map + flat 패턴
*/


/* ============================================================
4️⃣ flatMap — map + flat 동시에 수행
============================================================ */

/*
flatMap()

map을 수행한 후 결과를 자동으로 flat(1) 한다.
*/

const postsFlatMap = users.flatMap(user => user.posts);

console.log("All posts (flatMap):", postsFlatMap);


/*
flatMap은 다음 코드와 동일하다.

users.map(...).flat()
*/


/* ============================================================
5️⃣ Data Transformation Example
============================================================ */

/*
각 사용자 post를
"user: post" 형태로 변환
*/

const postDescriptions = users.flatMap(user =>
  user.posts.map(post => `${user.name}: ${post}`)
);

console.log("Post descriptions:", postDescriptions);


/*
결과

[
 "Alice: Post A",
 "Alice: Post B",
 "Bob: Post C",
 "Charlie: Post D",
 "Charlie: Post E"
]
*/


/* ============================================================
6️⃣ Data Cleaning Example
============================================================ */

/*
배열 안에 배열 + 빈값이 섞여 있는 경우
*/

const messyData = [
  ["apple", "banana"],
  [],
  ["orange"],
  ["grape", "melon"]
];


/*
flat으로 데이터 정리
*/

const cleanedData = messyData.flat();

console.log("Cleaned data:", cleanedData);


/* ============================================================
Summary
============================================================ */

/*
flat
→ 중첩 배열을 평탄화

flatMap
→ map + flat(1)

flatMap은 다음과 동일

array.map(...)
     .flat()

주요 활용

- API 응답 정리
- 데이터 정규화
- 중첩 구조 flatten
*/