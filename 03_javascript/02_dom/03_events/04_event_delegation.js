/**
 * Day 18: DOM Events - Event Delegation
 *
 * Event delegation attaches ONE listener to a parent element
 * and handles events from many child elements using event bubbling.
 *
 * 이벤트 위임은 "부모 요소 1개에만 이벤트 리스너를 붙이고",
 * 버블링을 이용해 여러 자식 요소의 이벤트를 처리하는 패턴이다.
 *
 * 왜 중요한가?
 * - 리스트/테이블처럼 항목이 많을 때 리스너를 N개 붙이는 것은 비효율적
 * - 항목이 동적으로 추가/삭제될 때도 자동으로 동작한다
 * - 실무 프론트엔드에서 매우 자주 사용되는 구조
 *
 * 핵심 개념
 * - 이벤트는 기본적으로 bubbling(버블링)한다
 * - event.target: 실제 클릭된 요소
 * - event.currentTarget: 리스너가 붙은 요소(부모)
 * - target.closest(selector): "내가 원하는 버튼/아이템인지" 안전하게 판별
 *
 * ⚠️ 실행을 위해 HTML 구조가 필요하다.
 */

/* --------------------------------------------------
 * 0. Required HTML Structure (예시)
 * --------------------------------------------------
 *
 * <div>
 *   <h3>Todo List</h3>
 *   <ul id="todoList">
 *     <li data-id="1">
 *       <span class="title">Read a paper</span>
 *       <button class="btn-done">Done</button>
 *       <button class="btn-remove">Remove</button>
 *     </li>
 *     <li data-id="2">
 *       <span class="title">Write code</span>
 *       <button class="btn-done">Done</button>
 *       <button class="btn-remove">Remove</button>
 *     </li>
 *   </ul>
 *
 *   <button id="addItem">Add Random Item</button>
 * </div>
 *
 */

const todoList = document.getElementById("todoList");
const addItemBtn = document.getElementById("addItem");

/* --------------------------------------------------
 * 1. Delegation: one listener for many buttons
 * --------------------------------------------------
 *
 * 부모(ul)에 click 리스너 1개만 등록하고,
 * 실제 클릭된 요소(event.target)를 검사해서 동작을 분기한다.
 */
todoList.addEventListener("click", (event) => {
  // 1) 실제 클릭된 요소
  const target = event.target;

  // 2) "Done 버튼"을 눌렀는지 판별
  // - 버튼 내부에 아이콘(span/svg)이 들어갈 수 있으므로 closest 사용(안전)
  const doneBtn = target.closest(".btn-done");
  if (doneBtn) {
    const item = doneBtn.closest("li");
    if (!item) return;

    // item 식별 (data-id)
    const id = item.dataset.id;

    // 완료 표시 토글 예시
    item.classList.toggle("done");

    console.log(`[DONE] item id=${id}`);
    return; // 아래 remove 로직까지 내려가지 않게 종료
  }

  // 3) "Remove 버튼"을 눌렀는지 판별
  const removeBtn = target.closest(".btn-remove");
  if (removeBtn) {
    const item = removeBtn.closest("li");
    if (!item) return;

    const id = item.dataset.id;
    item.remove();

    console.log(`[REMOVE] item id=${id}`);
    return;
  }

  // 4) 그 외 영역 클릭 처리(옵션)
  // 예: li의 title을 클릭하면 상세 보기 등
  const title = target.closest(".title");
  if (title) {
    const item = title.closest("li");
    const id = item?.dataset.id;
    console.log(`[CLICK TITLE] item id=${id}`);
  }
});

/**
 * [한국어 해설]
 * - 이 방식은 ul 안에 li가 10개든 1,000개든 이벤트 리스너가 1개만 존재
 * - 항목이 동적으로 추가되어도 부모 리스너가 이벤트를 받아 처리 가능
 * - closest()를 쓰면 "버튼 내부 요소 클릭" 같은 실무 이슈를 안전하게 처리한다
 */


/* --------------------------------------------------
 * 2. Dynamic add item (delegation advantage)
 * --------------------------------------------------
 *
 * delegation을 쓰면 새로 추가된 li에도 별도 리스너가 필요 없다.
 */
let nextId = 3;

addItemBtn?.addEventListener("click", () => {
  const li = document.createElement("li");
  li.dataset.id = String(nextId++);

  li.innerHTML = `
    <span class="title">Random Item ${li.dataset.id}</span>
    <button class="btn-done">Done</button>
    <button class="btn-remove">Remove</button>
  `;

  todoList.appendChild(li);
  console.log(`[ADD] item id=${li.dataset.id}`);
});


/* --------------------------------------------------
 * 3. Common Pitfalls & Best Practices
 * --------------------------------------------------
 *
 * ✅ Best Practices
 * - parent element는 "stable container"로 잡기 (항상 존재하는 요소)
 * - event.target을 그대로 쓰지 말고 closest로 안전하게 매칭하기
 * - 조건 분기(return)로 로직 충돌 방지
 *
 * ⚠️ Pitfalls
 * - stopPropagation을 남발하면 delegation이 깨질 수 있음
 * - 너무 넓은 parent에 붙이면 불필요한 이벤트가 많이 들어올 수 있음
 */


/* --------------------------------------------------
 * 4. Summary
 * --------------------------------------------------
 *
 * - Event delegation = one parent listener + bubbling + target matching
 * - Great for lists/tables/dynamic content
 * - closest() is a practical and safe matching method
 */