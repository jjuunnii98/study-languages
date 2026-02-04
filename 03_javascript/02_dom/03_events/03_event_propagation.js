/**
 * Day 17: DOM Events - Event Propagation (Capturing & Bubbling)
 *
 * This file explains how events propagate through the DOM tree.
 * Understanding propagation is critical for:
 * - debugging unexpected event triggers
 * - controlling event flow with stopPropagation()
 * - implementing event delegation correctly
 *
 * 이 파일은 DOM 이벤트 전파(캡처링/버블링)를 다룬다.
 * 이벤트 전파를 이해하면:
 * - 예상치 못한 클릭/핸들러 호출을 디버깅할 수 있고
 * - stopPropagation으로 흐름을 제어할 수 있으며
 * - 이벤트 위임(event delegation)을 정확히 구현할 수 있다.
 *
 * ✅ Event Flow (표준 전파 흐름)
 * 1) Capturing phase (캡처링): window → document → ... → target의 부모 → target
 * 2) Target phase (타겟): target에서 이벤트 처리
 * 3) Bubbling phase (버블링): target → 부모 → ... → document → window
 *
 * ⚠️ 실행을 위해 HTML 구조가 필요하다.
 */

/* --------------------------------------------------
 * 0. Required HTML Structure (예시)
 * --------------------------------------------------
 *
 * <div id="outer" style="padding:20px; border:2px solid black;">
 *   Outer
 *   <div id="middle" style="padding:20px; border:2px solid blue;">
 *     Middle
 *     <button id="inner" style="padding:10px;">Inner Button</button>
 *   </div>
 * </div>
 *
 */

const outer = document.getElementById("outer");
const middle = document.getElementById("middle");
const inner = document.getElementById("inner");

/* --------------------------------------------------
 * 1. Bubbling (default)
 * --------------------------------------------------
 */

outer.addEventListener("click", (event) => {
  console.log("[BUBBLE] outer");
  console.log("  target:", event.target.id);
  console.log("  currentTarget:", event.currentTarget.id);
});

middle.addEventListener("click", (event) => {
  console.log("[BUBBLE] middle");
  console.log("  target:", event.target.id);
  console.log("  currentTarget:", event.currentTarget.id);
});

inner.addEventListener("click", (event) => {
  console.log("[BUBBLE] inner");
  console.log("  target:", event.target.id);
  console.log("  currentTarget:", event.currentTarget.id);
});

/**
 * [한국어 해설]
 * - addEventListener의 기본 동작은 버블링(bubbling)이다.
 * - inner 버튼을 클릭하면:
 *   inner → middle → outer 순서로 핸들러가 실행된다.
 * - target은 '실제로 클릭된 요소'
 * - currentTarget은 '리스너가 붙은 요소'
 */


/* --------------------------------------------------
 * 2. Capturing (useCapture = true)
 * --------------------------------------------------
 */

outer.addEventListener(
  "click",
  (event) => {
    console.log("[CAPTURE] outer");
  },
  true // capture phase에서 실행
);

middle.addEventListener(
  "click",
  (event) => {
    console.log("[CAPTURE] middle");
  },
  true
);

inner.addEventListener(
  "click",
  (event) => {
    console.log("[CAPTURE] inner");
  },
  true
);

/**
 * [한국어 해설]
 * - 세 번째 인자를 true로 주면 캡처링(capturing) 단계에서 실행된다.
 * - inner를 클릭하면:
 *   outer → middle → inner 순서로 캡처링 로그가 먼저 찍힌다.
 * - 이후 버블링 핸들러가 실행되며,
 *   결과적으로 "캡처링 → 타겟 → 버블링" 흐름이 된다.
 */


/* --------------------------------------------------
 * 3. stopPropagation() - stop event flow
 * --------------------------------------------------
 */

inner.addEventListener("click", (event) => {
  console.log("[STOP] inner stops propagation");
  event.stopPropagation();
});

/**
 * [한국어 해설]
 * - stopPropagation()은 이벤트 전파를 중단한다.
 * - 이 inner 핸들러가 실행되면,
 *   inner에서 이벤트가 멈추고 middle/outer 버블링 핸들러가 실행되지 않는다.
 *
 * ⚠️ 주의:
 * - stopPropagation은 "캡처링/버블링 모두"에 영향을 줄 수 있다.
 * - 남발하면 디버깅이 어려워지므로
 *   보통은 이벤트 위임/조건 분기로 해결하는 편이 낫다.
 */


/* --------------------------------------------------
 * 4. stopImmediatePropagation() - advanced
 * --------------------------------------------------
 */

inner.addEventListener("click", (event) => {
  console.log("[IMMEDIATE STOP] inner stops all handlers on same element");
  event.stopImmediatePropagation();
});

inner.addEventListener("click", () => {
  console.log("This will NOT run due to stopImmediatePropagation()");
});

/**
 * [한국어 해설]
 * - stopImmediatePropagation()은
 *   1) 전파를 중단하고
 *   2) 같은 요소(inner)에 등록된 다른 리스너 실행도 막는다.
 * - 하나의 요소에 여러 리스너가 있을 때 강력하게 제어할 수 있지만
 *   실무에서는 사용 빈도가 낮고, 주로 라이브러리/복잡한 UI에서 등장한다.
 */


/* --------------------------------------------------
 * 5. Summary
 * --------------------------------------------------
 */
/**
 * Day 17 Summary
 * - 이벤트 전파는 Capturing → Target → Bubbling 순서로 진행된다.
 * - 기본은 Bubbling이며, capture 옵션으로 Capturing에서 실행 가능하다.
 * - stopPropagation(): 전파 중단
 * - stopImmediatePropagation(): 전파 중단 + 같은 요소의 다른 리스너까지 중단
 *
 * 다음 단계(이벤트 위임)를 위해:
 * - target vs currentTarget 구분
 * - 버블링을 활용하는 사고방식이 매우 중요하다.
 */