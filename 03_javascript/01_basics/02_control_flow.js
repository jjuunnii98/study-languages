/**
 * Day 2: JavaScript Control Flow (Basics)
 *
 * This file covers basic control flow in JavaScript:
 * - if / else conditions
 * - comparison and logical operators
 * - switch statement
 * - for / while loops
 * - break / continue
 *
 * 본 파일은 JavaScript의 기본 흐름 제어를 다룬다.
 * 조건문과 반복문은 프로그램의 "의사결정 구조"를 만든다.
 */

// ------------------------------------
// 1. if / else 조건문
// ------------------------------------
// 조건식이 true/false인지에 따라 실행 흐름이 갈린다.

let score = 85;

if (score >= 90) {
  console.log("Grade: A");
} else if (score >= 80) {
  console.log("Grade: B");
} else {
  console.log("Grade: C or below");
}

// 한국어 해설:
// - if / else if / else 구조는 Python과 매우 유사
// - 조건식에는 비교 연산자가 들어간다 (>, <, >=, <=, ===)

// ------------------------------------
// 2. 비교 연산자 & 논리 연산자
// ------------------------------------

let age = 27;
let isStudent = true;

// 비교 연산자
console.log(age > 20);     // true
console.log(age === 27);   // true (값 + 타입 비교)
console.log(age == "27");  // true  (타입 변환 발생, 권장 ❌)
console.log(age === "27"); // false (권장 ✅)

// 논리 연산자
console.log(age > 20 && isStudent); // AND
console.log(age > 30 || isStudent); // OR
console.log(!isStudent);            // NOT

// 한국어 해설:
// - ===, !== 사용을 기본으로 하자 (타입 강제 변환 방지)
// - &&, ||, ! 는 조건 결합에 사용

// ------------------------------------
// 3. switch 문
// ------------------------------------
// 여러 분기 조건을 깔끔하게 표현할 때 사용

let day = 3;

switch (day) {
  case 1:
    console.log("Monday");
    break;
  case 2:
    console.log("Tuesday");
    break;
  case 3:
    console.log("Wednesday");
    break;
  default:
    console.log("Other day");
}

// 한국어 해설:
// - break를 쓰지 않으면 아래 case까지 실행됨 (fall-through)
// - if/else가 길어질 때 switch가 가독성에 유리

// ------------------------------------
// 4. for 반복문
// ------------------------------------
// 정해진 횟수만큼 반복할 때 사용

for (let i = 0; i < 5; i++) {
  console.log("for loop i =", i);
}

// 한국어 해설:
// - i++ : 반복마다 1 증가
// - Python의 range()와 유사한 역할

// ------------------------------------
// 5. while 반복문
// ------------------------------------
// 조건이 true인 동안 반복

let count = 0;

while (count < 3) {
  console.log("while count =", count);
  count++;
}

// 한국어 해설:
// - 반복 종료 조건을 반드시 보장해야 함
// - 그렇지 않으면 무한 루프 발생

// ------------------------------------
// 6. break / continue
// ------------------------------------
// 반복문 흐름을 제어

for (let n = 1; n <= 5; n++) {
  if (n === 3) {
    continue; // 3은 건너뜀
  }
  if (n === 5) {
    break; // 5에서 반복 종료
  }
  console.log("n =", n);
}

// 한국어 해설:
// - continue: 현재 반복만 건너뜀
// - break: 반복문 전체 종료

// ------------------------------------
// 7. Practical Example
// ------------------------------------
// 숫자 배열에서 짝수만 출력

let numbers = [1, 2, 3, 4, 5, 6];

for (let num of numbers) {
  if (num % 2 !== 0) {
    continue;
  }
  console.log("even number:", num);
}

// ------------------------------------
// 8. Summary
// ------------------------------------
/*
Day 2 요약 (한국어)

- 조건문(if / else / switch)은 프로그램의 의사결정 구조를 만든다
- === 연산자를 기본으로 사용해 타입 문제를 방지한다
- for / while 반복문으로 반복 로직을 구현한다
- break / continue로 반복 흐름을 세밀하게 제어할 수 있다
- 제어 흐름은 이후 DOM, 비동기, 로직 설계의 기반이 된다
*/