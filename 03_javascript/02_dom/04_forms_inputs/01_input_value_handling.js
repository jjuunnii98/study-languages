/**
 * Day 19: DOM Forms & Inputs - Input Value Handling
 *
 * [EN]
 * This file covers practical patterns for reading/writing form input values:
 * - text input, textarea, select
 * - checkbox, radio
 * - input vs change events
 * - numeric parsing and safe defaults
 *
 * [KR]
 * 이 파일은 폼 입력값을 다루는 실무 패턴을 정리합니다.
 * - 텍스트 입력/텍스트영역/셀렉트
 * - 체크박스/라디오
 * - input 이벤트 vs change 이벤트 차이
 * - 숫자 변환 및 안전한 기본값 처리
 *
 * ✅ 실행을 위해 아래 예시 HTML 구조가 필요합니다.
 */

/* --------------------------------------------------
 * 0) Required HTML Structure (예시)
 * --------------------------------------------------
 *
 * <form id="profileForm">
 *   <label>
 *     Name:
 *     <input id="nameInput" type="text" placeholder="Enter your name" />
 *   </label>
 *
 *   <label>
 *     Bio:
 *     <textarea id="bioInput" rows="3" placeholder="Short bio"></textarea>
 *   </label>
 *
 *   <label>
 *     Role:
 *     <select id="roleSelect">
 *       <option value="student">Student</option>
 *       <option value="researcher">Researcher</option>
 *       <option value="founder">Founder</option>
 *     </select>
 *   </label>
 *
 *   <label>
 *     Age:
 *     <input id="ageInput" type="number" min="0" max="120" />
 *   </label>
 *
 *   <fieldset>
 *     <legend>Subscription</legend>
 *     <label>
 *       <input id="subscribeCheckbox" type="checkbox" />
 *       Subscribe to newsletter
 *     </label>
 *   </fieldset>
 *
 *   <fieldset>
 *     <legend>Plan</legend>
 *     <label><input type="radio" name="plan" value="free" checked /> Free</label>
 *     <label><input type="radio" name="plan" value="pro" /> Pro</label>
 *     <label><input type="radio" name="plan" value="team" /> Team</label>
 *   </fieldset>
 *
 *   <button type="button" id="fillDemo">Fill Demo Data</button>
 *   <button type="reset">Reset</button>
 * </form>
 *
 * <pre id="output"></pre>
 */

/* --------------------------------------------------
 * 1) DOM References (안전한 참조)
 * --------------------------------------------------
 * - null 체크를 해두면 HTML이 없을 때도 에러를 피할 수 있다.
 */
const form = document.getElementById("profileForm");
const nameInput = document.getElementById("nameInput");
const bioInput = document.getElementById("bioInput");
const roleSelect = document.getElementById("roleSelect");
const ageInput = document.getElementById("ageInput");
const subscribeCheckbox = document.getElementById("subscribeCheckbox");
const fillDemoBtn = document.getElementById("fillDemo");
const output = document.getElementById("output");

/* --------------------------------------------------
 * 2) Helpers: read/write functions
 * --------------------------------------------------
 * 실무에서는 "읽기/쓰기"를 함수화하면 유지보수가 쉬워진다.
 */

// 숫자 입력 안전 변환: 빈 값이면 null, 숫자 아니면 null
function parseNumberOrNull(value) {
  // input.value는 항상 string이므로 Number 변환이 필요
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
}

// 라디오 선택값 읽기
function getRadioValue(name) {
  const checked = document.querySelector(`input[name="${name}"]:checked`);
  return checked ? checked.value : null;
}

// 라디오 선택값 설정
function setRadioValue(name, value) {
  const radio = document.querySelector(`input[name="${name}"][value="${value}"]`);
  if (radio) radio.checked = true;
}

/**
 * 현재 폼 상태를 JS 객체로 읽어오기
 * - 실무에서는 이 객체가 API payload / state 로 이어진다.
 */
function readFormValues() {
  return {
    name: nameInput?.value?.trim() ?? "",
    bio: bioInput?.value?.trim() ?? "",
    role: roleSelect?.value ?? "student",
    age: parseNumberOrNull(ageInput?.value ?? ""),
    subscribed: Boolean(subscribeCheckbox?.checked),
    plan: getRadioValue("plan"),
  };
}

/**
 * JS 객체를 폼에 쓰기
 * - "데모 데이터 채우기", "서버에서 받은 값 반영" 등에 사용
 */
function writeFormValues(values) {
  if (nameInput) nameInput.value = values.name ?? "";
  if (bioInput) bioInput.value = values.bio ?? "";
  if (roleSelect) roleSelect.value = values.role ?? "student";
  if (ageInput) ageInput.value = values.age != null ? String(values.age) : "";
  if (subscribeCheckbox) subscribeCheckbox.checked = Boolean(values.subscribed);

  if (values.plan) setRadioValue("plan", values.plan);
}

/* --------------------------------------------------
 * 3) Render: show current values
 * --------------------------------------------------
 * - 결과를 화면에 출력해두면 학습/디버깅이 쉬움
 */
function render() {
  if (!output) return;
  const data = readFormValues();
  output.textContent = JSON.stringify(data, null, 2);
}

/* --------------------------------------------------
 * 4) Event: input vs change
 * --------------------------------------------------
 * - input: 타이핑하는 즉시 발생 (실시간 반영)
 * - change: 입력이 "확정"되었을 때 발생
 *   (텍스트는 focus out 시, select/checkbox는 값 바뀌는 순간)
 */

// 폼 전체에 input 이벤트를 걸면 대부분 입력을 커버 가능
form?.addEventListener("input", () => {
  // 실시간 값 추적
  render();
});

// change 이벤트는 select/checkbox/radio에 더 직관적인 경우가 많다
form?.addEventListener("change", () => {
  render();
});

/* --------------------------------------------------
 * 5) Demo: fill sample values
 * --------------------------------------------------
 */
fillDemoBtn?.addEventListener("click", () => {
  writeFormValues({
    name: "Junyeong",
    bio: "Preparing for graduate ML research and building data-driven products.",
    role: "founder",
    age: 27,
    subscribed: true,
    plan: "pro",
  });
  render();
});

/* --------------------------------------------------
 * 6) Reset handling
 * --------------------------------------------------
 * reset 버튼을 누르면 form 값이 초기화되지만,
 * 화면 output은 자동으로 갱신되지 않으므로 reset 이벤트에서 render 호출
 */
form?.addEventListener("reset", () => {
  // reset은 즉시 DOM 값이 바뀌지 않을 수 있어 microtask로 한 번 미룸
  setTimeout(render, 0);
});

/* --------------------------------------------------
 * 7) Initial render
 * --------------------------------------------------
 */
render();

/**
 * Day 19 Summary (한국어)
 * - input.value는 항상 문자열(string)이다 → 숫자는 반드시 변환 필요
 * - checkbox는 checked(boolean)로 읽는다
 * - radio는 name 그룹에서 :checked를 찾는다
 * - input 이벤트: 실시간 / change 이벤트: 확정 시점
 * - read/write 함수로 입력 처리 로직을 구조화하면 실무 확장에 유리하다
 */