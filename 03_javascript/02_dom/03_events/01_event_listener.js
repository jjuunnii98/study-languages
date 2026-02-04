/**
 * Day 15: DOM Events - addEventListener
 *
 * This file demonstrates how to handle user interactions
 * using addEventListener in JavaScript.
 *
 * 이 파일은 JavaScript에서 addEventListener를 사용해
 * 사용자 이벤트(클릭, 입력 등)를 처리하는 기본 방법을 다룬다.
 *
 * 핵심 포인트:
 * - 이벤트는 "행동(action)"과 "반응(handler)"의 연결이다.
 * - addEventListener는 이벤트 처리의 표준 방식이다.
 */

/* --------------------------------------------------
 * 1. Basic Event Listener (Click)
 * --------------------------------------------------
 */

// 버튼 요소 선택
const button = document.getElementById("btn-click");

// 클릭 이벤트 등록
button.addEventListener("click", () => {
  console.log("Button clicked!");
});

/**
 * [한국어 해설]
 * - addEventListener(이벤트타입, 콜백함수)
 * - "click" 이벤트가 발생하면 콜백 함수가 실행된다.
 * - inline onclick보다 분리된 구조로 관리가 가능하다.
 */


/* --------------------------------------------------
 * 2. Accessing Event Object
 * --------------------------------------------------
 */

button.addEventListener("click", (event) => {
  console.log("Event object:", event);
  console.log("Event target:", event.target);
});

/**
 * [한국어 해설]
 * - event 객체는 이벤트에 대한 모든 정보를 담고 있다.
 * - event.target: 실제 이벤트가 발생한 DOM 요소
 * - 디버깅과 조건 분기에 매우 중요하다.
 */


/* --------------------------------------------------
 * 3. Mouse Events
 * --------------------------------------------------
 */

const box = document.getElementById("hover-box");

box.addEventListener("mouseenter", () => {
  box.style.backgroundColor = "lightblue";
});

box.addEventListener("mouseleave", () => {
  box.style.backgroundColor = "white";
});

/**
 * [한국어 해설]
 * - mouseenter / mouseleave는 hover 효과 구현에 자주 사용
 * - UI 피드백(색상, 강조 표시)에 적합
 */


/* --------------------------------------------------
 * 4. Keyboard Events
 * --------------------------------------------------
 */

const input = document.getElementById("text-input");

input.addEventListener("keydown", (event) => {
  console.log(`Key pressed: ${event.key}`);
});

/**
 * [한국어 해설]
 * - keydown / keyup / keypress 이벤트
 * - event.key: 눌린 키 값
 * - 폼 검증, 단축키 구현 등에 사용
 */


/* --------------------------------------------------
 * 5. Multiple Event Listeners
 * --------------------------------------------------
 */

function handleClick() {
  console.log("Handled by named function");
}

button.addEventListener("click", handleClick);

/**
 * [한국어 해설]
 * - 동일한 요소에 여러 이벤트 리스너 등록 가능
 * - 함수 참조 방식은 재사용/제거(removeEventListener)에 유리
 */


/* --------------------------------------------------
 * 6. removeEventListener (Conceptual)
 * --------------------------------------------------
 */

// button.removeEventListener("click", handleClick);

/**
 * [한국어 해설]
 * - 이벤트를 제거하려면 동일한 함수 참조가 필요
 * - 익명 함수는 제거 불가 → named function 권장
 */


/* --------------------------------------------------
 * 7. Summary
 * --------------------------------------------------
 */
/**
 * Day 15 Summary
 * - addEventListener는 이벤트 처리의 표준 API
 * - event 객체로 이벤트 맥락 파악 가능
 * - UI 상호작용은 이벤트 기반으로 설계된다
 * - DOM 조작 + 이벤트 = 동적인 웹 애플리케이션
 */