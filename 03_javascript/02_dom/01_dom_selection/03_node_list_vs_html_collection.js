/**
 * Day 10: DOM — NodeList vs HTMLCollection
 *
 * 목표:
 * - NodeList와 HTMLCollection의 차이를 정확히 이해한다.
 * - "live collection" vs "static collection" 개념을 체득한다.
 * - 실무에서 어떤 API를 언제 써야 하는지 판단할 수 있게 한다.
 *
 * 주의:
 * - 이 코드는 브라우저 환경에서 실행해야 한다.
 * - Node.js 환경에서는 document 객체가 없어 실행되지 않는다.
 */

/* ------------------------------------------------------------
1) 테스트용 HTML 구조 (예시)
------------------------------------------------------------ */
/**
 * <ul id="menu">
 *   <li class="item">Home</li>
 *   <li class="item">Docs</li>
 *   <li class="item">Contact</li>
 * </ul>
 */

/* ------------------------------------------------------------
2) HTMLCollection (Live Collection)
------------------------------------------------------------ */

// getElementsByClassName은 HTMLCollection을 반환
const htmlCollection = document.getElementsByClassName("item");

console.log("HTMLCollection:", htmlCollection);
console.log("HTMLCollection length:", htmlCollection.length);

/**
 * HTMLCollection의 특징
 * - live collection (DOM 변경 시 자동 반영)
 * - 배열이 아님 (map, filter 사용 불가)
 * - 오래된 API이지만 여전히 많이 존재
 */

/* ------------------------------------------------------------
3) NodeList (Static Collection)
------------------------------------------------------------ */

// querySelectorAll은 NodeList를 반환
const nodeList = document.querySelectorAll(".item");

console.log("NodeList:", nodeList);
console.log("NodeList length:", nodeList.length);

/**
 * NodeList의 특징
 * - static collection (DOM 변경 시 자동 반영 ❌)
 * - forEach 사용 가능
 * - 최신 DOM API와 함께 가장 많이 사용
 */

/* ------------------------------------------------------------
4) DOM 변경 실험: 차이 확인
------------------------------------------------------------ */

const menu = document.getElementById("menu");

// 새로운 li 요소 추가
const newItem = document.createElement("li");
newItem.className = "item";
newItem.textContent = "Blog";

menu.appendChild(newItem);

console.log("After DOM update:");
console.log("HTMLCollection length:", htmlCollection.length);
console.log("NodeList length:", nodeList.length);

/**
 * 결과 해석:
 * - HTMLCollection: 길이가 자동 증가 (live)
 * - NodeList: 기존 상태 유지 (static)
 */

/* ------------------------------------------------------------
5) 반복 처리 차이
------------------------------------------------------------ */

// NodeList는 forEach 사용 가능
nodeList.forEach((el, idx) => {
  console.log(`NodeList[${idx}]:`, el.textContent);
});

// HTMLCollection은 Array로 변환 후 처리
Array.from(htmlCollection).forEach((el, idx) => {
  console.log(`HTMLCollection[${idx}]:`, el.textContent);
});

/* ------------------------------------------------------------
6) 실무 기준 정리
------------------------------------------------------------ */
/**
 * ✔ querySelector / querySelectorAll 권장
 *   - 코드 가독성 좋음
 *   - static collection → 예측 가능
 *   - 최신 브라우저 표준
 *
 * ⚠ HTMLCollection 주의
 *   - DOM 변경 시 자동 반영되어
 *     의도치 않은 버그를 만들 수 있음
 *
 * ✔ 반복/가공이 필요한 경우
 *   - NodeList 또는 Array로 변환해서 처리
 */

/* ------------------------------------------------------------
7) 요약
------------------------------------------------------------ */
/**
 * - HTMLCollection: live, 자동 반영, 배열 아님
 * - NodeList: static, forEach 가능, 예측 가능
 * - 실무에서는 querySelectorAll + NodeList 조합이 표준
 */