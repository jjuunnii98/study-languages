/**
 * Day 22: Real-time Input Events (DOM - Forms & Inputs)
 *
 * [EN]
 * This file demonstrates real-time form input handling:
 * - Using `input` event for live updates
 * - Debouncing to reduce unnecessary validation calls
 * - Providing immediate UI feedback (error/success states)
 *
 * [KR]
 * 이 파일은 입력 이벤트를 활용해 실시간(Realtime)으로 폼을 다루는 방법을 다룹니다.
 * - input 이벤트로 사용자가 타이핑할 때마다 상태 업데이트
 * - debounce로 과도한 검증 호출 방지(성능/UX 개선)
 * - 즉시 사용자 피드백(에러/성공 메시지, 버튼 활성화) 제공
 */

"use strict";

// -------------------------------------------
// 0) DOM Elements (assumed to exist in HTML)
// -------------------------------------------
// ✅ HTML 예시(가정)
// <form id="signup-form">
//   <input id="email" />
//   <input id="password" type="password" />
//   <button id="submit-btn" type="submit">Sign Up</button>
//   <div id="message"></div>
// </form>

const form = document.querySelector("#signup-form");
const emailInput = document.querySelector("#email");
const passwordInput = document.querySelector("#password");
const submitBtn = document.querySelector("#submit-btn");
const messageBox = document.querySelector("#message");

// 안전장치: 요소가 없으면 런타임 에러 대신 안내 로그 출력
if (!form || !emailInput || !passwordInput || !submitBtn || !messageBox) {
  console.warn(
    "[Day 22] Required DOM elements not found. Please check your HTML ids: " +
      "#signup-form, #email, #password, #submit-btn, #message"
  );
}

// -------------------------------------------
// 1) Validation Utilities
// -------------------------------------------

function isValidEmail(email) {
  // [KR] 너무 복잡한 RFC 정규식 대신, 학습/실무에서 흔히 쓰는 '기본형' 사용
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return pattern.test(email);
}

function isValidPassword(password) {
  // [KR] 기본 정책: 최소 8자 (추후 강도 정책으로 확장 가능)
  return password.length >= 8;
}

function validateFormState() {
  // [KR] 입력값 정규화: trim()으로 공백 제거
  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();

  const errors = [];

  if (!email) errors.push("Email is required.");
  else if (!isValidEmail(email)) errors.push("Invalid email format.");

  if (!password) errors.push("Password is required.");
  else if (!isValidPassword(password))
    errors.push("Password must be at least 8 characters.");

  return {
    isValid: errors.length === 0,
    errors
  };
}

// -------------------------------------------
// 2) UI Feedback Helpers
// -------------------------------------------

function renderErrors(errors) {
  messageBox.innerHTML = errors.map((e) => `<p>${e}</p>`).join("");
  messageBox.style.color = "red";
}

function renderSuccess(msg) {
  messageBox.textContent = msg;
  messageBox.style.color = "green";
}

function setSubmitEnabled(enabled) {
  submitBtn.disabled = !enabled;

  // [KR] UI 힌트(선택): disabled 상태를 시각적으로 드러내고 싶다면 class를 붙이는 방식도 좋다.
  // submitBtn.classList.toggle("is-disabled", !enabled);
}

// -------------------------------------------
// 3) Debounce Implementation
// -------------------------------------------
// [KR] debounce: 사용자가 입력을 멈춘 뒤 delay(ms) 후에만 검증 실행
//      - 실시간 검증 UX + 과도한 연산 방지
function debounce(fn, delayMs = 300) {
  let timerId;

  return function (...args) {
    clearTimeout(timerId);
    timerId = setTimeout(() => fn.apply(this, args), delayMs);
  };
}

const debouncedLiveValidate = debounce(() => {
  const { isValid, errors } = validateFormState();

  if (!emailInput.value.trim() && !passwordInput.value.trim()) {
    // [KR] 아무 입력이 없을 때는 메시지를 비워서 UX를 깔끔하게 유지
    messageBox.textContent = "";
    setSubmitEnabled(false);
    return;
  }

  if (!isValid) {
    renderErrors(errors);
    setSubmitEnabled(false);
  } else {
    renderSuccess("Looks good. You can submit the form.");
    setSubmitEnabled(true);
  }
}, 300);

// -------------------------------------------
// 4) Live Input Events
// -------------------------------------------

emailInput?.addEventListener("input", debouncedLiveValidate);
passwordInput?.addEventListener("input", debouncedLiveValidate);

// -------------------------------------------
// 5) Submit Control (final gate)
// -------------------------------------------

form?.addEventListener("submit", function (event) {
  event.preventDefault();

  const { isValid, errors } = validateFormState();

  if (!isValid) {
    renderErrors(errors);
    setSubmitEnabled(false);
    return;
  }

  // [KR] 여기서 실제 서버 전송(fetch)로 연결 가능
  // fetch("/signup", { method: "POST", body: JSON.stringify({ ... }) })

  renderSuccess("Submitted successfully! (demo)");
  setSubmitEnabled(false);
});