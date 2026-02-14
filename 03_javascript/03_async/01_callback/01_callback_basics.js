/**
 * Day 23 — JavaScript Callback Basics
 *
 * This file introduces callback functions,
 * which are foundational to asynchronous programming in JavaScript.
 *
 * 이 파일은 콜백 함수의 개념을 다루며,
 * JavaScript 비동기 프로그래밍의 핵심 구조를 이해하는 것을 목표로 한다.
 */

/* =========================================================
   1️⃣ What is a Callback?
   ========================================================= */

/*
A callback is a function passed as an argument to another function.
The receiving function executes it later.

콜백(callback)이란,
다른 함수의 인자로 전달되어
나중에 실행되는 함수이다.
*/

function greet(name, callback) {
  console.log("Hello, " + name);
  callback();
}

function sayGoodbye() {
  console.log("Goodbye!");
}

greet("Junyeong", sayGoodbye);


/* =========================================================
   2️⃣ Callback with Anonymous Function
   ========================================================= */

/*
콜백은 익명 함수로도 전달할 수 있다.
*/

greet("Developer", function () {
  console.log("Nice to meet you!");
});


/* =========================================================
   3️⃣ Why Callbacks Matter — Simulating Async Behavior
   ========================================================= */

/*
JavaScript is single-threaded.
비동기 처리를 위해 callback 구조가 사용된다.

setTimeout은 대표적인 비동기 API이다.
*/

console.log("Start");

setTimeout(function () {
  console.log("Executed after 2 seconds");
}, 2000);

console.log("End");

/*
출력 순서:

Start
End
(2초 후)
Executed after 2 seconds

이것이 비동기 실행 흐름이다.
*/


/* =========================================================
   4️⃣ Callback Flow Visualization
   ========================================================= */

/*
Call Stack:

1. console.log("Start")
2. setTimeout 등록 (Web API로 이동)
3. console.log("End")
4. 2초 후 callback이 Event Queue에 들어감
5. Call Stack이 비면 실행

이것이 Event Loop 구조이다.
*/


/* =========================================================
   5️⃣ Callback Example — Simulated Data Fetch
   ========================================================= */

function fetchData(callback) {
  console.log("Fetching data...");

  setTimeout(function () {
    const data = { id: 1, name: "Junyeong" };
    callback(data);
  }, 1500);
}

fetchData(function (result) {
  console.log("Data received:", result);
});


/* =========================================================
   6️⃣ Summary
   ========================================================= */

/*
- Callback은 함수의 인자로 전달되는 함수
- 비동기 작업 완료 후 실행됨
- setTimeout, 이벤트 처리, API 요청 등에 사용됨
- 이후 Promise, async/await의 기초가 되는 개념

콜백은 JavaScript 비동기 구조의 출발점이다.
*/