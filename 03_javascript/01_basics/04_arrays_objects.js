/**
 * Day 4: JavaScript Arrays & Objects
 *
 * This file covers the two most important data structures in JavaScript:
 * arrays and objects.
 *
 * 이 파일은 JavaScript의 핵심 자료구조인
 * 배열(Array)과 객체(Object)를 다룬다.
 *
 * 배열은 "순서가 있는 데이터 묶음",
 * 객체는 "이름(key)과 값(value)의 쌍"으로 데이터를 표현한다.
 */

// ------------------------------------
// 1. Arrays (배열)
// ------------------------------------

// Array creation
// 배열 생성
let numbers = [10, 20, 30, 40];
let fruits = ["apple", "banana", "orange"];

console.log(numbers);
console.log(fruits);

// Accessing elements (index starts at 0)
// 배열 요소 접근 (인덱스는 0부터 시작)
console.log(numbers[0]); // 10
console.log(fruits[1]);  // banana

// Modifying array elements
// 배열 값 수정
numbers[2] = 99;
console.log(numbers);

// Array length
// 배열 길이
console.log(numbers.length);

// ------------------------------------
// 2. Common Array Methods
// ------------------------------------

// push: add element to the end
// push: 배열 끝에 요소 추가
fruits.push("grape");
console.log(fruits);

// pop: remove last element
// pop: 마지막 요소 제거
let lastFruit = fruits.pop();
console.log(lastFruit);
console.log(fruits);

// includes: check if value exists
// includes: 특정 값 포함 여부 확인
console.log(fruits.includes("apple")); // true
console.log(fruits.includes("melon")); // false

// ------------------------------------
// 3. Objects (객체)
// ------------------------------------

// Object creation
// 객체 생성
let person = {
  name: "Junyeong",
  age: 27,
  role: "Student"
};

console.log(person);

// Accessing object properties
// 객체 속성 접근
console.log(person.name);
console.log(person["age"]);

// Modifying object properties
// 객체 속성 수정
person.role = "Researcher";
console.log(person);

// Adding new properties
// 새로운 속성 추가
person.city = "Seoul";
console.log(person);

// ------------------------------------
// 4. Arrays of Objects (실무에서 매우 중요)
// ------------------------------------

// Array containing multiple objects
// 객체를 요소로 가지는 배열
let users = [
  { id: 1, name: "Alice", score: 90 },
  { id: 2, name: "Bob", score: 75 },
  { id: 3, name: "Charlie", score: 88 }
];

console.log(users);

// Access specific object inside array
// 배열 안의 특정 객체 접근
console.log(users[0].name);   // Alice
console.log(users[2].score);  // 88

// ------------------------------------
// 5. Looping through Arrays & Objects
// ------------------------------------

// Loop through array
// 배열 반복
for (let i = 0; i < users.length; i++) {
  console.log(users[i].name, users[i].score);
}

// for...of (preferred for arrays)
// for...of 문 (배열에 권장)
for (let user of users) {
  console.log(user.name);
}

// for...in (for object keys)
// for...in 문 (객체의 key 순회)
for (let key in person) {
  console.log(key, person[key]);
}

// ------------------------------------
// 6. Summary
// ------------------------------------
/*
- Arrays store ordered data
- Objects store key-value pairs
- Arrays and objects are often combined in real-world data
- Mastering these structures is essential for:
  - API responses
  - JSON data
  - Data analysis and front-end development

요약:
- 배열은 순서 있는 데이터 구조
- 객체는 의미 있는 속성 단위의 데이터 구조
- 실무에서는 "객체의 배열" 형태가 가장 많이 사용됨
*/