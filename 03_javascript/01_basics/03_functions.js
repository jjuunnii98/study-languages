/**
 * Day 3: JavaScript Functions
 *
 * This file introduces function basics in JavaScript.
 * Functions allow us to group logic, reuse code,
 * and structure programs in a readable way.
 *
 * 이 파일은 JavaScript 함수의 기초를 다룬다.
 * 함수는 로직을 묶고, 재사용하며,
 * 프로그램을 구조적으로 작성하기 위한 핵심 개념이다.
 */

// ------------------------------------
// 1. Function Declaration
// ------------------------------------
// Traditional function declaration

function add(a, b) {
  return a + b;
}

console.log(add(3, 5)); // 8

// 한국어 설명:
// function 키워드를 사용한 가장 기본적인 함수 정의 방식
// 선언된 함수는 호이스팅(hoisting)이 발생한다.

// ------------------------------------
// 2. Function Expression
// ------------------------------------
// Function stored in a variable

const subtract = function (a, b) {
  return a - b;
};

console.log(subtract(10, 4)); // 6

// 한국어 설명:
// 함수도 하나의 값(value)이기 때문에
// 변수에 할당할 수 있다.
// 이 경우 호이스팅되지 않는다.

// ------------------------------------
// 3. Arrow Functions
// ------------------------------------
// Modern and concise syntax

const multiply = (a, b) => {
  return a * b;
};

console.log(multiply(4, 6)); // 24

// Shorter arrow function
const divide = (a, b) => a / b;

console.log(divide(20, 4)); // 5

// 한국어 설명:
// 화살표 함수(Arrow Function)는
// 간결한 문법과 this 바인딩 차이로 인해
// 현대 JavaScript에서 매우 많이 사용된다.

// ------------------------------------
// 4. Default Parameters
// ------------------------------------
// Provide default values for parameters

function greet(name = "Guest") {
  return `Hello, ${name}!`;
}

console.log(greet("Junyeong"));
console.log(greet());

// 한국어 설명:
// 인자가 전달되지 않았을 때
// 기본값(default)을 사용할 수 있다.

// ------------------------------------
// 5. Functions as Arguments
// ------------------------------------
// Callback function example

function processValue(value, callback) {
  return callback(value);
}

const square = (x) => x * x;

console.log(processValue(5, square)); // 25

// 한국어 설명:
// JavaScript에서는 함수를
// 다른 함수의 인자로 전달할 수 있다.
// 이는 비동기 처리, 이벤트 처리의 기반 개념이다.

// ------------------------------------
// 6. Summary
// ------------------------------------
// - Functions organize reusable logic
// - JavaScript supports multiple function styles
// - Arrow functions are widely used in modern code
// - Functions can be passed as values
//
// 요약:
// - 함수는 재사용 가능한 로직의 기본 단위
// - 선언식, 표현식, 화살표 함수 모두 중요
// - 콜백 함수 개념은 이후 비동기/이벤트 처리의 기초