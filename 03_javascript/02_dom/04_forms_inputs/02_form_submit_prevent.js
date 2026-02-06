/**
 * Day 20: DOM Forms & Inputs - Prevent Default Submit
 *
 * [EN]
 * This file demonstrates how to fully control form submission:
 * - Prevent browser default behavior
 * - Validate user input
 * - Build a clean payload object
 * - Provide UI feedback
 *
 * [KR]
 * 이 파일은 폼 제출(submit)을 완전히 제어하는 방법을 다룹니다.
 * - 브라우저 기본 submit 동작 차단
 * - 입력값 검증(validation)
 * - 서버 전송용 payload 객체 구성
 * - 사용자 피드백(UI 메시지) 처리
 */

/* --------------------------------------------------
 * 0) Required HTML Structure (예시)
 * --------------------------------------------------
 *
 * <form id="profileForm">
 *   <input id="nameInput" type="text" placeholder="Name" />
 *   <input id="ageInput" type="number" placeholder="Age" />
 *
 *   <label>
 *     <input id="subscribeCheckbox" type="checkbox" />
 *     Subscribe
 *   </label>
 *
 *   <button type="submit">Submit</button>
 * </form>
 *
 * <p id="message"></p>
 */

/* --------------------------------------------------
 * 1) DOM References
 * --------------------------------------------------
 */
const form = document.getElementById("profileForm");
const nameInput = document.getElementById("nameInput");
const ageInput = document.getElementById("ageInput");
const subscribeCheckbox = document.getElementById("subscribeCheckbox");
const message = document.getElementById("message");

/* --------------------------------------------------
 * 2) Helper: Validation
 * --------------------------------------------------
 * 실무에서는 validation을 반드시 분리한다.
 * (나중에 재사용/확장 가능)
 */
function validateForm(values) {
  const errors = [];

  if (!values.name) {
    errors.push("이름은 필수 입력값입니다.");
  }

  if (values.age !== null && values.age < 0) {
    errors.push("나이는 0 이상이어야 합니다.");
  }

  return errors;
}

/* --------------------------------------------------
 * 3) Helper: Read form values
 * --------------------------------------------------
 */
function readFormValues() {
  const ageValue = ageInput.value.trim();

  return {
    name: nameInput.value.trim(),
    age: ageValue === "" ? null : Number(ageValue),
    subscribed: subscribeCheckbox.checked,
  };
}

/* --------------------------------------------------
 * 4) Submit Event Handler
 * --------------------------------------------------
 */
form?.addEventListener("submit", (event) => {
  // ✅ 핵심 1: 브라우저 기본 submit 차단
  event.preventDefault();

  // 입력값 읽기
  const values = readFormValues();

  // ✅ 핵심 2: validation 수행
  const errors = validateForm(values);

  if (errors.length > 0) {
    // ❌ 유효성 실패 → 사용자에게 메시지 표시
    message.textContent = errors.join(" ");
    message.style.color = "red";
    return;
  }

  // ✅ 핵심 3: payload 구성
  const payload = {
    ...values,
    submittedAt: new Date().toISOString(),
  };

  // ✅ 핵심 4: 이후 액션
  // - 실제 서비스에서는 fetch / axios로 서버 전송
  console.log("Submitting payload:", payload);

  message.textContent = "폼이 성공적으로 제출되었습니다.";
  message.style.color = "green";

  // 필요 시 초기화
  form.reset();
});

/* --------------------------------------------------
 * 5) Summary (한국어)
 * --------------------------------------------------
 *
 * - submit 이벤트에서는 반드시 event.preventDefault()를 사용한다
 * - validation → payload → action 흐름을 명확히 분리한다
 * - 폼 제출은 '페이지 이동'이 아니라 '데이터 처리'다
 * - 이 패턴은 API 연동, React/Vue 폼 처리로 그대로 확장 가능
 */