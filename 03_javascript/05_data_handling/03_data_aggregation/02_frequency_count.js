

/*
Day 57 — Data Aggregation: Frequency Count

File
03_javascript/05_data_handling/03_data_aggregation/02_frequency_count.js

목표
배열 데이터에서 값의 출현 빈도(frequency)를 계산하는 패턴을 학습한다.

핵심 주제
1) 단순 값 빈도 계산
2) 문자열 정규화 후 빈도 계산
3) 객체 배열에서 특정 필드 빈도 계산
4) 조건부 빈도 계산
5) frequency 결과를 정렬 가능한 배열로 변환
6) 재사용 가능한 helper 함수 설계

한국어 설명
frequency count는 데이터 분석에서 매우 자주 쓰이는 기본 집계 패턴이다.

예:
- 가장 많이 등장한 카테고리 찾기
- 상태(status)별 개수 세기
- 단어 출현 횟수 계산
- 사용자 행동 이벤트 빈도 분석

JavaScript에서는 보통 reduce()를 이용해
값 → 개수
형태의 객체를 누적하면서 구현한다.
*/


/* ============================================================
1) Basic Frequency Count
============================================================ */

/*
가장 기본적인 문자열 배열 예시
*/
const fruits = [
  "apple",
  "banana",
  "apple",
  "orange",
  "banana",
  "apple",
  "grape"
];

console.log("Original fruits:", fruits);

/*
한국어 설명
- acc는 누적 객체(accumulator)
- 과일 이름을 key로 사용
- 처음 나오면 0으로 초기화
- 나올 때마다 1씩 증가
*/
const fruitFrequency = fruits.reduce((acc, fruit) => {
  if (!acc[fruit]) {
    acc[fruit] = 0;
  }

  acc[fruit] += 1;
  return acc;
}, {});

console.log("Fruit frequency:", fruitFrequency);


/* ============================================================
2) Case Normalization Before Counting
============================================================ */

/*
대소문자가 섞인 문자열 배열
*/
const rawTags = ["AI", "ai", "Data", "DATA", "data", "ML", "ml"];

/*
한국어 설명
빈도 계산 전 정규화(normalization)를 하면
같은 의미의 값을 하나로 합칠 수 있다.
*/
const normalizedTagFrequency = rawTags.reduce((acc, tag) => {
  const normalizedTag = tag.toLowerCase();

  if (!acc[normalizedTag]) {
    acc[normalizedTag] = 0;
  }

  acc[normalizedTag] += 1;
  return acc;
}, {});

console.log("Normalized tag frequency:", normalizedTagFrequency);


/* ============================================================
3) Numeric Frequency Count
============================================================ */

/*
숫자 배열에서도 동일 패턴 사용 가능
*/
const ratings = [5, 4, 5, 3, 4, 5, 2, 4, 3, 5];

const ratingFrequency = ratings.reduce((acc, rating) => {
  if (!acc[rating]) {
    acc[rating] = 0;
  }

  acc[rating] += 1;
  return acc;
}, {});

console.log("Rating frequency:", ratingFrequency);


/* ============================================================
4) Frequency Count in Object Arrays
============================================================ */

/*
주문 데이터 예시
*/
const orders = [
  { id: 1, region: "Seoul", category: "Electronics", status: "paid" },
  { id: 2, region: "Busan", category: "Food",        status: "paid" },
  { id: 3, region: "Seoul", category: "Food",        status: "cancelled" },
  { id: 4, region: "Seoul", category: "Electronics", status: "paid" },
  { id: 5, region: "Incheon", category: "Beauty",    status: "paid" },
  { id: 6, region: "Busan", category: "Food",        status: "paid" }
];

/*
region별 빈도 계산
*/
const orderFrequencyByRegion = orders.reduce((acc, order) => {
  const key = order.region;

  if (!acc[key]) {
    acc[key] = 0;
  }

  acc[key] += 1;
  return acc;
}, {});

console.log("Order frequency by region:", orderFrequencyByRegion);

/*
status별 빈도 계산
*/
const orderFrequencyByStatus = orders.reduce((acc, order) => {
  const key = order.status;

  if (!acc[key]) {
    acc[key] = 0;
  }

  acc[key] += 1;
  return acc;
}, {});

console.log("Order frequency by status:", orderFrequencyByStatus);


/* ============================================================
5) Conditional Frequency Count
============================================================ */

/*
paid 주문만 대상으로 category별 빈도 계산
*/
const paidCategoryFrequency = orders
  .filter((order) => order.status === "paid")
  .reduce((acc, order) => {
    const key = order.category;

    if (!acc[key]) {
      acc[key] = 0;
    }

    acc[key] += 1;
    return acc;
  }, {});

console.log("Paid category frequency:", paidCategoryFrequency);


/* ============================================================
6) Word Frequency Count
============================================================ */

/*
문장 안의 단어 빈도 계산 예시
*/
const sentence = "risk intelligence ai risk modeling ai platform risk";

/*
한국어 설명
- 공백 기준 분리
- 모두 소문자로 정규화
- 빈도 계산
*/
const wordFrequency = sentence
  .toLowerCase()
  .split(" ")
  .reduce((acc, word) => {
    if (!acc[word]) {
      acc[word] = 0;
    }

    acc[word] += 1;
    return acc;
  }, {});

console.log("Word frequency:", wordFrequency);


/* ============================================================
7) Convert Frequency Object to Sorted Rows
============================================================ */

/*
빈도 객체를 정렬 가능한 배열로 변환

한국어 설명
실무에서는 객체 그대로보다
[{ value, count }] 형태로 바꿔서
정렬 / UI 출력 / 테이블 렌더링을 하는 경우가 많다.
*/
const fruitFrequencyRows = Object.entries(fruitFrequency)
  .map(([value, count]) => {
    return {
      value,
      count
    };
  })
  .sort((a, b) => b.count - a.count);

console.log("Fruit frequency rows (sorted):", fruitFrequencyRows);


/* ============================================================
8) Find Most Frequent Value
============================================================ */

/*
가장 많이 등장한 과일 찾기
*/
const mostFrequentFruit = fruitFrequencyRows[0];
console.log("Most frequent fruit:", mostFrequentFruit);


/* ============================================================
9) Reusable Helper: countFrequency
============================================================ */

/*
재사용 가능한 기본 frequency helper

한국어 설명
단순 값 배열에서 바로 사용 가능한 함수
*/
function countFrequency(array) {
  return array.reduce((acc, value) => {
    if (!acc[value]) {
      acc[value] = 0;
    }

    acc[value] += 1;
    return acc;
  }, {});
}

const colorFrequency = countFrequency(["red", "blue", "red", "green", "blue", "red"]);
console.log("Color frequency (helper):", colorFrequency);


/* ============================================================
10) Reusable Helper: countBy
============================================================ */

/*
객체 배열에서 특정 keySelector 기준으로 빈도 계산
*/
function countBy(array, keySelector) {
  return array.reduce((acc, item) => {
    const key = keySelector(item);

    if (!acc[key]) {
      acc[key] = 0;
    }

    acc[key] += 1;
    return acc;
  }, {});
}

const categoryFrequency = countBy(orders, (order) => order.category);
console.log("Category frequency (countBy):", categoryFrequency);

const regionFrequency = countBy(orders, (order) => order.region);
console.log("Region frequency (countBy):", regionFrequency);


/* ============================================================
11) Reusable Helper: frequencyRows
============================================================ */

/*
frequency 결과를 정렬된 rows로 변환하는 helper
*/
function frequencyRows(frequencyObject) {
  return Object.entries(frequencyObject)
    .map(([value, count]) => ({ value, count }))
    .sort((a, b) => b.count - a.count);
}

const categoryFrequencyRows = frequencyRows(categoryFrequency);
console.log("Category frequency rows:", categoryFrequencyRows);


/* ============================================================
12) Real-world Example: Event Frequency
============================================================ */

/*
사용자 이벤트 로그 예시
*/
const events = [
  { userId: 1, event: "view" },
  { userId: 1, event: "click" },
  { userId: 2, event: "view" },
  { userId: 3, event: "view" },
  { userId: 2, event: "purchase" },
  { userId: 1, event: "view" },
  { userId: 3, event: "click" }
];

const eventFrequency = countBy(events, (item) => item.event);
console.log("Event frequency:", eventFrequency);

const userFrequency = countBy(events, (item) => item.userId);
console.log("User frequency:", userFrequency);


/* ============================================================
13) Summary
============================================================ */

/*
정리

frequency count의 핵심 패턴:
1. reduce() 사용
2. key를 기준으로 acc[key] 누적
3. 처음 등장하면 0으로 초기화
4. 등장할 때마다 +1

실무 활용:
- 카테고리 개수 집계
- 상태별 개수 세기
- 단어 빈도 계산
- 이벤트 로그 요약
- 가장 많이 나온 값 찾기

즉,
frequency count는 JavaScript 데이터 집계의 가장 기본이면서
가장 자주 쓰이는 패턴 중 하나다.
*/

console.log("Summary complete.");