/**
 * Day 6: JavaScript Scope & Hoisting
 *
 * This file explains:
 * - Scope (global / function / block)
 * - var vs let/const scoping differences
 * - Hoisting behaviors (function declarations vs function expressions)
 * - Temporal Dead Zone (TDZ) in let/const
 *
 * 이 파일은 다음을 다룬다:
 * - 스코프(scope): 전역/함수/블록 스코프
 * - var vs let/const 스코프 차이
 * - 호이스팅(hoisting) 동작 방식
 * - let/const의 TDZ(Temporal Dead Zone)
 *
 * NOTE:
 * 일부 예제는 의도적으로 에러를 발생시킨다.
 * 실행할 때는 try/catch 구간의 출력 결과를 확인하자.
 */

// ------------------------------------
// 1. Global Scope (전역 스코프)
// ------------------------------------
const GLOBAL_VALUE = "I am global";

function printGlobal() {
  console.log("[global]", GLOBAL_VALUE);
}
printGlobal();

// 한국어 설명:
// - 전역 스코프 변수는 어디서든 접근 가능
// - 다만 전역 오염(global pollution)이 생기므로 실무에서는 최소화 권장

// ------------------------------------
// 2. Function Scope (함수 스코프) - var
// ------------------------------------
function varFunctionScopeExample() {
  var x = 10;
  if (true) {
    var x = 20; // 같은 함수 스코프이므로 "재선언/재할당"처럼 동작
  }
  console.log("[var function scope]", x); // 20
}
varFunctionScopeExample();

// 한국어 설명:
// - var는 "블록"이 아닌 "함수" 단위로 스코프가 잡힌다.
// - if/for 같은 블록 안에서 var를 써도 함수 전체에서 같은 변수로 취급
// - 이런 특성이 버그를 만들기 쉬워서 var는 거의 사용하지 않는 것이 일반적

// ------------------------------------
// 3. Block Scope (블록 스코프) - let/const
// ------------------------------------
function blockScopeExample() {
  let y = 10;

  if (true) {
    let y = 20; // 블록 스코프: 바깥 y와 다른 변수
    const z = 99;
    console.log("[inside block] y =", y); // 20
    console.log("[inside block] z =", z); // 99
  }

  console.log("[outside block] y =", y); // 10

  // z는 블록 밖에서 접근 불가
  try {
    console.log(z);
  } catch (e) {
    console.log("[outside block] z 접근 에러:", e.name);
  }
}
blockScopeExample();

// 한국어 설명:
// - let/const는 블록({ ... }) 단위로 스코프가 분리된다.
// - 따라서 동일한 변수명을 블록 안에서 다시 선언해도 바깥 변수에 영향 없음
// - 실무에서 의도치 않은 값 변경을 방지해줘서 let/const가 권장됨

// ------------------------------------
// 4. Hoisting Basics (호이스팅 기본)
// ------------------------------------

// (1) Function Declaration: hoisted fully
// 함수 선언문은 "전체가 호이스팅"되어 선언 전에 호출 가능
sayHello();

function sayHello() {
  console.log("[function declaration] Hello!");
}

// (2) var: hoisted (declaration only), initialized as undefined
// var는 선언만 호이스팅되고, 값 할당은 호이스팅되지 않음
console.log("[var hoisting] a =", a); // undefined
var a = 123;

// (3) let/const: hoisted but TDZ prevents access before declaration
// let/const도 내부적으로 호이스팅되지만, 선언 전 접근은 TDZ로 막힘
try {
  console.log("[let TDZ] b =", b);
} catch (e) {
  console.log("[let TDZ] 선언 전 접근 에러:", e.name);
}
let b = 456;

// ------------------------------------
// 5. Function Expression vs Arrow Function (호이스팅 차이)
// ------------------------------------

// (1) Function expression with var
// 선언(var)은 호이스팅되지만 함수 값은 아직 undefined → 호출 불가
try {
  greet(); // TypeError 가능
} catch (e) {
  console.log("[function expression] 호출 에러:", e.name);
}

var greet = function () {
  console.log("[function expression] Hi!");
};
greet();

// (2) Arrow function with const
// const는 TDZ로 선언 전 접근 자체가 불가
try {
  arrowGreet();
} catch (e) {
  console.log("[arrow function] 선언 전 호출 에러:", e.name);
}

const arrowGreet = () => {
  console.log("[arrow function] Hi from arrow!");
};
arrowGreet();

// 한국어 설명:
// - 함수 선언문(function foo(){})은 호이스팅되어 선언 전에 호출 가능
// - 함수 표현식(var foo = function(){})은 var 선언만 올라가고 값은 undefined라 호출 시 에러
// - const/let + 화살표 함수는 TDZ 때문에 선언 전 접근 자체가 불가

// ------------------------------------
// 6. Practical Tip (실무 팁)
// ------------------------------------
/*
실무 권장 규칙:

1) 기본은 const
2) 변경이 필요한 변수만 let
3) var는 피하기
4) 함수는 가능하면 "사용 전 정의"를 유지하면 가독성이 좋다
5) TDZ/호이스팅을 이해하면 디버깅 속도가 크게 빨라진다
*/

console.log("\n[Done] Day 6: Scope & Hoisting");