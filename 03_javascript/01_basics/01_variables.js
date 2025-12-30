/**
 * Day 1: JavaScript Variables
 *
 * This file covers the basics of variables in JavaScript.
 * JavaScript is a dynamically typed language, similar to Python,
 * but with its own rules and behaviors.
 *
 * 이 파일은 JavaScript 변수의 기초를 다룬다.
 * JavaScript는 Python과 마찬가지로 동적 타입 언어이지만,
 * 선언 방식(var/let/const)과 스코프(범위) 규칙에서 차이가 있다.
 *
 * ✅ 목표:
 * - var / let / const 차이 이해
 * - typeof로 타입 확인
 * - 재할당(reassignment) vs 변경(mutability) 구분
 */

// ------------------------------------
// 1. Variable Declarations
// ------------------------------------
// JavaScript provides three main ways to declare variables:
// var, let, and const
//
// 한국어 해설:
// - var: 함수 스코프(function scope). 오래된 방식. 예기치 않은 버그 유발 가능.
// - let: 블록 스코프(block scope). 값이 바뀔 수 있는 변수에 사용.
// - const: 블록 스코프. "재할당"이 불가능. 기본값(default)으로 추천.
//
// ✅ 실무 원칙(중요):
// - 기본은 const
// - 값이 바뀌어야 하면 let
// - var는 특별한 이유 없으면 쓰지 않기

// var: function-scoped (old style, not recommended)
var oldStyle = "var variable";

// let: block-scoped (recommended for mutable variables)
let age = 27;

// const: block-scoped, cannot be reassigned
const name = "Junyeong";

console.log(oldStyle);
console.log(age);
console.log(name);

// ------------------------------------
// 2. Data Types
// ------------------------------------
// JavaScript has dynamic typing.
// The type of a variable is determined at runtime.
//
// 한국어 해설:
// - JS는 동적 타입: 변수에 들어가는 값에 따라 타입이 결정됨
// - number 하나로 정수/실수 모두 표현 (Python의 int/float 구분과 다름)
// - undefined: "값이 아직 할당되지 않음"
// - null: "의도적으로 비어 있음(없음을 명시)"

// 기본 타입 예시
let score = 95;            // number
let height = 175.5;        // number (no separate float type)
let isStudent = true;      // boolean
let city = "Seoul";        // string
let nothing = null;        // null (의도적으로 비어있음을 의미)
let notDefined;            // undefined (선언만 하고 값 할당 안 함)

console.log(typeof score);
console.log(typeof height);
console.log(typeof isStudent);
console.log(typeof city);

// ⚠️ 매우 유명한 JS 특이점(면접에도 자주 나옴)
// typeof null === "object" 로 출력된다. JS 초기 설계의 역사적 이슈.
console.log(typeof nothing);     // object (JavaScript quirk)

console.log(typeof notDefined);  // undefined

// ------------------------------------
// 3. Reassignment and Mutability
// ------------------------------------
// let variables can be reassigned
//
// 한국어 해설:
// - 재할당(reassignment): 변수 이름에 새로운 값을 다시 넣는 것
// - 변경 가능성(mutability): 객체/배열 내부 값을 바꾸는 것
//
// ✅ 핵심:
// - const는 "재할당"은 불가
// - 하지만 const로 선언된 객체/배열은 "내부 값 변경"은 가능

age = 28; // 재할당 가능(let)
console.log(age);

// const variables cannot be reassigned
// name = "Other"; // ❌ 재할당 불가(const). 실행 시 TypeError 발생

// However, objects declared with const can be mutated
const person = {
  name: "Junyeong",
  role: "Student"
};

// 객체 내부 값 변경은 가능 (mutate)
person.role = "Researcher";
console.log(person);

// ------------------------------------
// 4. Comparison with Python (Conceptual)
// ------------------------------------
// Python:
// x = 10
// x = "ten"
//
// JavaScript:
//
// 한국어 해설:
// - Python과 JS 모두 동적 타입 언어라서,
//   같은 변수 이름에 다른 타입 값을 넣는 것이 가능하다.
// - 단, 실무에서는 이런 패턴을 남발하면 가독성이 떨어지므로 주의.

let x = 10;
x = "ten";

console.log(x);

// ------------------------------------
// 5. Summary
// ------------------------------------
// - Use let for variables that will change
// - Use const by default for safety
// - Avoid var in modern JavaScript
// - JavaScript variables are dynamically typed
//
// 한국어 요약:
// - 기본은 const 사용(안전성)
// - 값이 바뀌면 let 사용
// - var는 되도록 사용하지 않기
// - JS는 동적 타입이며, typeof로 타입 확인 가능