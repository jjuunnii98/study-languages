/*
Day 54 — Object Transform: Object.fromEntries()

File
03_javascript/05_data_handling/02_object_transform/02_object_from_entries.js

목표
Object.entries()로 변환한 데이터를
다시 객체로 되돌리는 방법을 학습한다.

핵심 메서드:
- Object.fromEntries()

한국어 설명
Object.fromEntries()는
[key, value] 형태의 배열을 다시 객체로 변환하는 함수다.

즉,
Object.entries()의 반대 개념이다.

Object.entries(obj) → 배열
Object.fromEntries(array) → 객체
*/


/* ============================================================
1) Basic Example
============================================================ */

const user = {
  name: "junyeong",
  age: 27,
  role: "data_scientist"
};

console.log("Original object:", user);


/*
Object.entries() → 객체 → 배열
*/
const userEntries = Object.entries(user);
console.log("Entries:", userEntries);


/*
Object.fromEntries() → 배열 → 객체
*/
const reconstructedUser = Object.fromEntries(userEntries);
console.log("Reconstructed object:", reconstructedUser);


/* ============================================================
2) Transform Values (map + fromEntries)
============================================================ */

/*
모든 값을 문자열로 변환
*/

const transformedUser = Object.fromEntries(
  Object.entries(user).map(([key, value]) => {
    return [key, String(value)];
  })
);

console.log("All values as string:", transformedUser);


/* ============================================================
3) Filter Object Properties
============================================================ */

/*
숫자 타입만 남기기
*/

const mixedData = {
  a: 10,
  b: "hello",
  c: 25,
  d: "world"
};

const onlyNumbers = Object.fromEntries(
  Object.entries(mixedData).filter(([key, value]) => {
    return typeof value === "number";
  })
);

console.log("Only number values:", onlyNumbers);


/* ============================================================
4) Rename Keys
============================================================ */

/*
key 이름을 변경하는 패턴
*/

const renamedUser = Object.fromEntries(
  Object.entries(user).map(([key, value]) => {
    return [`user_${key}`, value];
  })
);

console.log("Renamed keys:", renamedUser);


/* ============================================================
5) Practical Example: API Response Cleanup
============================================================ */

/*
API 응답에서 null 값 제거
*/

const apiResponse = {
  id: 101,
  name: "Jun",
  email: null,
  phone: null,
  country: "Korea"
};

const cleanedResponse = Object.fromEntries(
  Object.entries(apiResponse).filter(([key, value]) => value !== null)
);

console.log("Cleaned API response:", cleanedResponse);


/* ============================================================
6) Convert Object → Array → Object (Full Pipeline)
============================================================ */

/*
점수 데이터를 가공 후 다시 객체로 변환
*/

const scores = {
  alice: 85,
  bob: 92,
  charlie: 78
};

/*
점수를 10점씩 증가시키기
*/

const updatedScores = Object.fromEntries(
  Object.entries(scores).map(([name, score]) => {
    return [name, score + 10];
  })
);

console.log("Updated scores:", updatedScores);


/* ============================================================
7) Key-Value Swap
============================================================ */

/*
key와 value를 뒤집는 패턴
*/

const swapped = Object.fromEntries(
  Object.entries(scores).map(([key, value]) => {
    return [value, key];
  })
);

console.log("Swapped key-value:", swapped);

/*
주의:
value가 중복되면 덮어쓰기 발생
*/


/* ============================================================
8) Reduce 없이 객체 변환 (핵심 패턴)
============================================================ */

/*
기존 방식 (reduce)
→ 복잡

Object.fromEntries()
→ 훨씬 직관적
*/

const simpleTransform = Object.fromEntries(
  Object.entries(scores).map(([key, value]) => {
    return [key, value * 2];
  })
);

console.log("Doubled scores:", simpleTransform);


/* ============================================================
9) Real-world Pattern Summary
============================================================ */

/*
핵심 패턴

1. Object → entries
2. entries → map/filter
3. 다시 Object로 변환
*/

const pipelineResult = Object.fromEntries(
  Object.entries(scores)
    .filter(([name, score]) => score >= 80)
    .map(([name, score]) => [name.toUpperCase(), score])
);

console.log("Pipeline result:", pipelineResult);


/* ============================================================
10) Summary
============================================================ */

/*
Object.fromEntries()는

- 배열 → 객체 변환
- 데이터 필터링
- 키 변경
- 값 변환

에 매우 강력한 도구다.

실무 패턴:

Object.entries(obj)
  .map(...)
  .filter(...)
→ Object.fromEntries()

이 흐름은 JavaScript 데이터 처리의 핵심이다.
*/

console.log("Summary complete.");