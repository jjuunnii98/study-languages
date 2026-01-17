/**
 * Day 8: DOM Selection — Basic Element Selection
 *
 * This file covers the fundamental ways to select DOM elements in JavaScript.
 * Selecting elements correctly is the first step of DOM manipulation.
 *
 * 본 파일은 JavaScript에서 DOM 요소를 선택하는 가장 기본적인 방법을 다룬다.
 * DOM 조작의 출발점은 "어떤 요소를 정확히 선택하느냐"이다.
 */

// ==================================================
// 1. getElementById
// ==================================================
// Selects a single element by its unique id
// id는 문서 내에서 유일해야 한다.

const titleElement = document.getElementById("title");

console.log(titleElement);

// ⚠️ id가 존재하지 않으면 null을 반환한다.
// 따라서 실제 코드에서는 null 체크가 중요하다.
if (titleElement !== null) {
  titleElement.style.color = "blue";
}

// ==================================================
// 2. getElementsByClassName
// ==================================================
// Selects elements by class name
// 반환값은 HTMLCollection (유사 배열)

const itemsByClass = document.getElementsByClassName("item");

console.log(itemsByClass);

// HTMLCollection은 for...of로 순회 가능
for (const item of itemsByClass) {
  item.style.fontWeight = "bold";
}

// ==================================================
// 3. getElementsByTagName
// ==================================================
// Selects elements by tag name
// 역시 HTMLCollection을 반환한다.

const listItems = document.getElementsByTagName("li");

for (const li of listItems) {
  li.style.backgroundColor = "#f0f0f0";
}

// ==================================================
// 4. Key Characteristics (중요 개념 정리)
// ==================================================
/*
- getElementById:
  - 단일 요소 반환 (Element 또는 null)
  - 가장 빠르고 명확한 선택 방식

- getElementsByClassName / getElementsByTagName:
  - HTMLCollection 반환
  - 실시간(live) 컬렉션 → DOM 변경 시 자동 반영
  - 배열 메서드(map, forEach)는 직접 사용 불가

이러한 특성 때문에,
현대 JavaScript에서는 querySelector 계열이 더 자주 사용된다.
(다음 파일에서 다룰 예정)
*/

// ==================================================
// 5. Summary
// ==================================================
/*
- DOM 조작의 첫 단계는 "정확한 요소 선택"
- id 선택은 단일 요소, class/tag 선택은 복수 요소
- HTMLCollection은 배열과 다르다는 점을 반드시 인지해야 한다
*/