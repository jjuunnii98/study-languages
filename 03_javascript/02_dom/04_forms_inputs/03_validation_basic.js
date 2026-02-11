/**
 * Day 21: Basic Form Validation
 *
 * This file demonstrates how to implement basic client-side validation
 * using JavaScript before submitting a form.
 *
 * 이 파일은 폼 제출 전에 JavaScript로
 * 기본적인 클라이언트 검증을 수행하는 방법을 다룹니다.
 */

"use strict";

// -------------------------------------------
// 1️⃣ Select DOM Elements
// -------------------------------------------

const form = document.querySelector("#signup-form");
const emailInput = document.querySelector("#email");
const passwordInput = document.querySelector("#password");
const messageBox = document.querySelector("#message");

// -------------------------------------------
// 2️⃣ Utility Validation Functions
// -------------------------------------------

// Simple email pattern (basic example)
function isValidEmail(email) {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return pattern.test(email);
}

// Password rule: minimum 8 characters
function isValidPassword(password) {
  return password.length >= 8;
}

// -------------------------------------------
// 3️⃣ Form Submit Event
// -------------------------------------------

form.addEventListener("submit", function (event) {
  event.preventDefault(); // prevent default form submission

  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();

  let errors = [];

  // --------------------------
  // Validation Logic
  // --------------------------

  if (!email) {
    errors.push("Email is required.");
  } else if (!isValidEmail(email)) {
    errors.push("Invalid email format.");
  }

  if (!password) {
    errors.push("Password is required.");
  } else if (!isValidPassword(password)) {
    errors.push("Password must be at least 8 characters.");
  }

  // --------------------------
  // Display Results
  // --------------------------

  if (errors.length > 0) {
    messageBox.innerHTML = errors.map(err => `<p>${err}</p>`).join("");
    messageBox.style.color = "red";
  } else {
    messageBox.textContent = "Form submitted successfully!";
    messageBox.style.color = "green";

    // Normally you would send data to a server here
    // fetch() or AJAX call
  }
});