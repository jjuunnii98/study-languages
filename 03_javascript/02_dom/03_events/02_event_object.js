/**
 * Day 16: DOM Events - Event Object
 *
 * This file focuses on understanding the event object
 * passed to event handlers in JavaScript.
 *
 * 이 파일은 이벤트 리스너에 전달되는 event 객체의
 * 구조와 실전 활용 방법을 다룬다.
 *
 * 핵심 질문:
 * - 어떤 요소에서 이벤트가 발생했는가?
 * - 어떤 타입의 이벤트인가?
 * - 이벤트는 어떻게 전달되는가?
 */

/* --------------------------------------------------
 * 1. Basic Event Object
 * --------------------------------------------------
 */

const button = document.getElementById("btn-event");

button.addEventListener("click", (event) => {
  console.log(event);
});

/**
 * [한국어 해설]
 * - event 객체는 브라우저가 자동으로 전달한다.
 * - 이벤트 발생 순간의 모든 정보가 담겨 있다.
 * - 디버깅 시 console.log(event)는 필수 습관
 */


/* --------------------------------------------------
 * 2. event.target vs event.currentTarget
 * --------------------------------------------------
 */

const container = document.getElementById("container");

container.addEventListener("click", (event) => {
  console.log("target:", event.target);
  console.log("currentTarget:", event.currentTarget);
});

/**
 * [한국어 해설]
 * - event.target
 *   → 실제로 클릭된 가장 안쪽 요소
 * - event.currentTarget
 *   → 이벤트 리스너가 등록된 요소
 *
 * 👉 이벤트 위임(Event Delegation)의 핵심 개념
 */


/* --------------------------------------------------
 * 3. Event Type and Time
 * --------------------------------------------------
 */

button.addEventListener("click", (event) => {
  console.log("Event type:", event.type);
  console.log("Timestamp:", event.timeStamp);
});

/**
 * [한국어 해설]
 * - event.type: 이벤트 종류(click, keydown 등)
 * - event.timeStamp: 페이지 로드 이후 이벤트 발생 시간(ms)
 * - 사용자 행동 분석에 활용 가능
 */


/* --------------------------------------------------
 * 4. Keyboard Event Object
 * --------------------------------------------------
 */

const input = document.getElementById("text-input");

input.addEventListener("keydown", (event) => {
  console.log("Key:", event.key);
  console.log("Code:", event.code);
});

/**
 * [한국어 해설]
 * - event.key: 실제 입력 문자
 * - event.code: 키보드 물리 키 위치
 * - 단축키, 접근성 기능 구현에 중요
 */


/* --------------------------------------------------
 * 5. Mouse Event Object
 * --------------------------------------------------
 */

const box = document.getElementById("mouse-box");

box.addEventListener("mousemove", (event) => {
  console.log(`X: ${event.clientX}, Y: ${event.clientY}`);
});

/**
 * [한국어 해설]
 * - clientX / clientY: 뷰포트 기준 마우스 좌표
 * - 드래그, 차트, 캔버스 인터랙션 구현의 기초
 */


/* --------------------------------------------------
 * 6. preventDefault()
 * --------------------------------------------------
 */

const link = document.getElementById("external-link");

link.addEventListener("click", (event) => {
  event.preventDefault();
  console.log("Default action prevented");
});

/**
 * [한국어 해설]
 * - 브라우저의 기본 동작을 차단
 * - 폼 제출, 링크 이동 제어 시 필수
 */


/* --------------------------------------------------
 * 7. stopPropagation()
 * --------------------------------------------------
 */

container.addEventListener("click", (event) => {
  event.stopPropagation();
  console.log("Propagation stopped at container");
});

/**
 * [한국어 해설]
 * - 이벤트 버블링 차단
 * - 복잡한 UI 구조에서 의도치 않은 이벤트 방지
 */


/* --------------------------------------------------
 * 8. Summary
 * --------------------------------------------------
 */
/**
 * Day 16 Summary
 * - event 객체는 이벤트의 모든 맥락을 담는다
 * - target vs currentTarget 구분은 매우 중요
 * - preventDefault / stopPropagation은 실무 필수
 * - 이벤트 객체 이해 = DOM 이벤트 마스터의 출발점
 */