/**
 * Day 14: DOM Traversing (Parent / Child / Sibling Navigation)
 *
 * This file demonstrates how to navigate the DOM tree
 * using parent, child, and sibling relationships.
 *
 * 이 파일은 DOM 트리에서 요소를 "탐색(traverse)"하는 핵심 방법을 다룬다.
 * 실무에서는 선택한 요소를 기준으로 부모/자식/형제 요소를 찾아
 * UI 상태를 갱신하는 경우가 매우 많다.
 */

/* --------------------------------------------------
 * 0. Setup (Create Demo UI)
 * -------------------------------------------------- */

const app = document.createElement("div");
app.id = "app";
app.style.border = "1px solid #ddd";
app.style.borderRadius = "8px";
app.style.padding = "12px";
app.style.marginBottom = "12px";

document.body.appendChild(app);

const title = document.createElement("h3");
title.textContent = "Day 14: DOM Traversing";
title.style.marginTop = "0";
app.appendChild(title);

const info = document.createElement("p");
info.textContent =
  "Click any item. We will traverse: parent, children, siblings, and closest().";
app.appendChild(info);

const list = document.createElement("ul");
list.id = "menu";
list.style.paddingLeft = "18px";
list.style.lineHeight = "1.8";
app.appendChild(list);

// 리스트 아이템 생성
const items = ["Home", "About", "Projects", "Contact"];
items.forEach((label) => {
  const li = document.createElement("li");
  li.className = "menu-item";
  li.textContent = label;
  li.style.cursor = "pointer";
  list.appendChild(li);
});

// 출력 영역
const output = document.createElement("pre");
output.style.background = "#f8fafc";
output.style.border = "1px solid #e2e8f0";
output.style.borderRadius = "8px";
output.style.padding = "10px";
output.style.whiteSpace = "pre-wrap";
output.textContent = "Output will appear here...";
app.appendChild(output);

/*
[해설]
- DOM 탐색 실습을 위해 UL/LI 구조를 만들고,
  클릭 이벤트에서 탐색 결과를 출력하도록 구성했다.
- pre 태그는 로그를 보기 좋게 출력하기에 좋다.
*/


/* --------------------------------------------------
 * 1. Helper: highlight an element (UI feedback)
 * -------------------------------------------------- */

function highlight(el) {
  // 기존 highlight 제거
  document.querySelectorAll(".is-active").forEach((node) => {
    node.classList.remove("is-active");
    node.style.backgroundColor = "";
    node.style.fontWeight = "";
  });

  // 새로운 highlight 적용
  el.classList.add("is-active");
  el.style.backgroundColor = "#e0f2fe";
  el.style.fontWeight = "600";
}

/*
[해설]
- 선택된 요소가 무엇인지 UI로 즉시 확인할 수 있도록 강조 표시
- 실무에서도 "선택/활성" 상태를 눈에 보이게 만드는 것이 디버깅에 도움
*/


/* --------------------------------------------------
 * 2. DOM Traversing 핵심 API
 * -------------------------------------------------- */
/*
(1) Parent
- element.parentElement : 부모 요소 (Element만)
- element.closest(selector) : 조건에 맞는 가장 가까운 조상 요소

(2) Children
- element.children : 자식 요소들(HTMLCollection)
- element.firstElementChild / lastElementChild

(3) Siblings
- element.previousElementSibling / nextElementSibling
*/


/* --------------------------------------------------
 * 3. Click Event: Traverse from clicked item
 * -------------------------------------------------- */

list.addEventListener("click", (event) => {
  const target = event.target;

  // 이벤트 위임 패턴: ul에서 이벤트를 받고, 실제 클릭 대상이 li인지 검사
  if (!target.classList.contains("menu-item")) return;

  highlight(target);

  // Parent 탐색
  const parent = target.parentElement; // UL
  const closestApp = target.closest("#app"); // 가장 가까운 #app 조상

  // Children 탐색
  const childrenCount = parent.children.length; // UL 아래 LI 수
  const firstChild = parent.firstElementChild;
  const lastChild = parent.lastElementChild;

  // Sibling 탐색
  const prev = target.previousElementSibling;
  const next = target.nextElementSibling;

  // 결과 출력
  output.textContent = [
    `Clicked: ${target.textContent}`,
    "",
    "[Parent Traversing]",
    `- parentElement tag: ${parent.tagName} (#${parent.id || "no-id"})`,
    `- closest('#app') exists: ${Boolean(closestApp)}`,
    "",
    "[Children Traversing]",
    `- parent.children.length: ${childrenCount}`,
    `- firstElementChild: ${firstChild ? firstChild.textContent : "null"}`,
    `- lastElementChild: ${lastChild ? lastChild.textContent : "null"}`,
    "",
    "[Sibling Traversing]",
    `- previousElementSibling: ${prev ? prev.textContent : "null"}`,
    `- nextElementSibling: ${next ? next.textContent : "null"}`,
  ].join("\n");

  console.log("Clicked target:", target);
});

/*
[해설]
- 이벤트 위임(Event Delegation)을 사용했다.
  - UL 하나에만 이벤트 리스너를 달고,
  - 실제 클릭된 요소가 LI인지 검사해서 처리
- DOM Traversing은 이벤트 위임과 결합될 때 실무 효율이 매우 높다.
*/


/* --------------------------------------------------
 * 4. Best Practices (Important)
 * -------------------------------------------------- */
/*
✅ Best Practices
1) DOM 탐색을 남발하기보다는 "명확한 기준점"에서만 탐색
2) parentElement / children / siblings로 해결이 어렵다면 closest()를 활용
3) 이벤트 위임을 사용하면 리스트/테이블 UI가 매우 깔끔해짐
4) nextSibling(텍스트 노드 포함) 대신 nextElementSibling(요소만) 권장

⚠ Common Mistakes
- parentNode, childNodes 사용으로 텍스트 노드까지 포함되어 버그 발생
- className을 통째로 덮어쓰기 (기존 클래스 삭제 위험)
- 이벤트 대상(event.target)을 검증하지 않고 바로 조작
*/