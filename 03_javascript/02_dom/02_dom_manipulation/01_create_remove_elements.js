/**
 * Day 11: DOM Manipulation - Create & Remove Elements
 *
 * This file demonstrates how to dynamically create,
 * insert, and remove DOM elements using JavaScript.
 *
 * 이 파일은 JavaScript를 사용하여
 * DOM 요소를 생성(create), 추가(append),
 * 삭제(remove)하는 기본적인 방법을 다룬다.
 */

/* --------------------------------------------------
 * 1. Create an Element
 * -------------------------------------------------- */

// 새로운 div 요소 생성
const box = document.createElement("div");

// 클래스와 텍스트 추가
box.className = "box";
box.textContent = "I am a dynamically created element";

// 스타일 직접 적용 (실무에서는 CSS 권장)
box.style.padding = "10px";
box.style.margin = "10px 0";
box.style.backgroundColor = "#e0f2fe";

/*
[해설]
- document.createElement(): 메모리 상에서만 요소 생성
- 아직 화면(DOM)에 추가되지 않은 상태
- className, textContent, style 등을 통해 속성 설정
*/


/* --------------------------------------------------
 * 2. Append Element to the DOM
 * -------------------------------------------------- */

// body에 요소 추가
document.body.appendChild(box);

/*
[해설]
- appendChild(): 부모 요소의 마지막 자식으로 추가
- 이 시점부터 브라우저 화면에 실제로 렌더링됨
*/


/* --------------------------------------------------
 * 3. Insert Element at a Specific Position
 * -------------------------------------------------- */

// 버튼 생성
const button = document.createElement("button");
button.textContent = "Remove Box";

// body 맨 앞에 버튼 삽입
document.body.prepend(button);

/*
[해설]
- prepend(): 부모 요소의 첫 번째 자식으로 삽입
- appendChild()와 대비되는 메서드
*/


/* --------------------------------------------------
 * 4. Remove an Element
 * -------------------------------------------------- */

// 버튼 클릭 시 box 제거
button.addEventListener("click", () => {
  box.remove();
});

/*
[해설]
- element.remove(): 해당 DOM 요소를 완전히 제거
- 이벤트 기반으로 DOM을 동적으로 제어하는 핵심 패턴
*/


/* --------------------------------------------------
 * 5. Summary
 * -------------------------------------------------- */

/*
핵심 요약:
1. createElement → 요소 생성 (아직 DOM 아님)
2. appendChild / prepend → DOM에 삽입
3. remove → DOM에서 제거
4. 이벤트와 결합하면 인터랙티브 UI 구현 가능

이 패턴은:
- 동적 UI
- 모달, 알림, 리스트 렌더링
- SPA 프레임워크(React/Vue)의 기초 개념
의 핵심이 된다.
*/