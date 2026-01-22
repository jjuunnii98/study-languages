/**
 * Day 9: DOM Selection — querySelector / querySelectorAll
 *
 * 목표:
 * - CSS 선택자 문법으로 DOM 요소를 선택하는 방법을 익힌다.
 * - querySelector(단일) vs querySelectorAll(다중)의 차이를 이해한다.
 * - 실무에서 자주 쓰는 패턴(존재 확인, 안전한 접근, 반복 처리)을 익힌다.
 *
 * 주의:
 * - 이 코드는 "브라우저 환경"에서 동작한다. (document 객체 필요)
 * - Node.js에서 실행하면 document가 없어 오류가 난다.
 */

/* ------------------------------------------------------------
1) querySelector vs querySelectorAll (개념)
------------------------------------------------------------ */
/**
 * document.querySelector(selector)
 * - selector(CSS 선택자)에 매칭되는 "첫 번째 요소" 1개를 반환
 * - 없으면 null 반환
 *
 * document.querySelectorAll(selector)
 * - 매칭되는 "모든 요소"를 NodeList로 반환
 * - 없으면 길이 0인 NodeList 반환
 *
 * 실무 팁:
 * - 단일 요소는 querySelector
 * - 리스트 요소는 querySelectorAll
 * - 항상 "없을 수 있음"을 고려해 안전하게 코딩한다.
 */

/* ------------------------------------------------------------
2) 테스트를 위한 HTML 구조 (예시)
------------------------------------------------------------ */
/**
 * 아래와 같은 HTML이 있다고 가정하자.
 *
 * <div id="app">
 *   <h1 class="title">DOM Selection</h1>
 *   <p class="desc">querySelector practice</p>
 *
 *   <ul class="menu">
 *     <li class="item">Home</li>
 *     <li class="item active">Docs</li>
 *     <li class="item">Contact</li>
 *   </ul>
 *
 *   <button data-action="save">Save</button>
 * </div>
 *
 * 실행 방법(브라우저):
 * 1) 간단한 index.html을 만들고
 * 2) 이 js 파일을 <script src="02_query_selector.js"></script>로 연결
 * 3) 브라우저 개발자도구(Console)에서 출력 확인
 */

/* ------------------------------------------------------------
3) querySelector: 단일 요소 선택
------------------------------------------------------------ */

// (1) ID로 선택 (#id)
const app = document.querySelector("#app");
console.log("app:", app);

// (2) class로 선택 (.class)
const title = document.querySelector(".title");
console.log("title:", title);

// (3) 태그로 선택 (tag)
const firstParagraph = document.querySelector("p");
console.log("firstParagraph:", firstParagraph);

// (4) 속성 선택자 ([attr=value])
const saveButton = document.querySelector('[data-action="save"]');
console.log("saveButton:", saveButton);

/**
 * 안전 패턴:
 * - 선택 결과는 null일 수 있다.
 * - 따라서 바로 .textContent 같은 걸 쓰기 전에 존재 여부를 확인한다.
 */
if (title) {
  console.log("title text:", title.textContent);
} else {
  console.warn("'.title' 요소를 찾지 못했습니다.");
}

/* ------------------------------------------------------------
4) querySelectorAll: 여러 요소 선택 + 반복 처리
------------------------------------------------------------ */

const menuItems = document.querySelectorAll(".menu .item");
console.log("menuItems(NodeList):", menuItems);
console.log("menuItems length:", menuItems.length);

/**
 * NodeList는 배열처럼 보이지만 완전한 Array는 아니다.
 * - forEach는 지원하는 경우가 많음
 * - map/filter 같은 배열 메서드는 바로는 안 됨 → Array.from으로 변환
 */

// (1) forEach로 순회 (가장 흔한 패턴)
menuItems.forEach((item, idx) => {
  console.log(`[${idx}] item text:`, item.textContent);
});

// (2) NodeList -> Array 변환 후 map 사용
const texts = Array.from(menuItems).map((item) => item.textContent.trim());
console.log("menu item texts:", texts);

/* ------------------------------------------------------------
5) "활성(active) 메뉴" 찾기 (실무 패턴)
------------------------------------------------------------ */

const activeItem = document.querySelector(".menu .item.active");

if (activeItem) {
  console.log("active item:", activeItem.textContent.trim());
} else {
  console.log("활성 메뉴(.active)가 없습니다.");
}

/* ------------------------------------------------------------
6) DOM 선택 실무 팁 (성능/가독성)
------------------------------------------------------------ */
/**
 * (1) 범위를 좁혀서 선택하기
 * - document 전체에서 찾는 대신 특정 컨테이너(app) 안에서 찾으면
 *   가독성과 성능에 도움이 되는 경우가 많다.
 */
if (app) {
  const localTitle = app.querySelector(".title");
  console.log("localTitle within #app:", localTitle?.textContent);
}

/**
 * (2) 선택자 상수화(재사용)
 * - 동일 선택자를 여러 번 쓰면 오타/관리 비용이 증가한다.
 */
const SELECTORS = {
  app: "#app",
  title: ".title",
  menuItems: ".menu .item",
  activeItem: ".menu .item.active",
};

const title2 = document.querySelector(SELECTORS.title);
console.log("title2:", title2?.textContent);

/**
 * (3) "없을 수 있음"을 항상 가정
 * - UI는 화면/상태에 따라 요소가 없을 수 있다.
 * - null 체크는 실무에서 습관이다.
 */

/* ------------------------------------------------------------
7) 요약
------------------------------------------------------------ */
/**
 * - querySelector: 첫 번째 요소 1개 (없으면 null)
 * - querySelectorAll: 매칭 요소 모두 (NodeList, 없으면 length=0)
 * - 안전하게(null 체크), 범위를 좁혀서(app.querySelector), 재사용 가능한 선택자 관리
 */