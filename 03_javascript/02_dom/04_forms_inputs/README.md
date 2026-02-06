# Forms & Inputs (JavaScript DOM)

This directory covers **form and input handling patterns** in vanilla JavaScript.
Forms are one of the most common UI surfaces in real-world applications,
and correct handling requires both **technical accuracy** and **robust UX design**.

본 디렉토리는 JavaScript DOM 환경에서 폼과 입력값을 다루는
실무 패턴을 정리합니다.  
폼 처리는 단순 이벤트 처리 수준이 아니라,
**값 추출 → 검증 → 제출 제어 → 피드백**까지 포함하는 핵심 UI 로직입니다.

---

## 🎯 Objectives

- Read and write input values reliably across input types
- Understand `input` vs `change` events for form state updates
- Prevent default form submission and control submission flow
- Validate user inputs and construct clean payloads
- Provide UI feedback (error/success) in a predictable way

---

## 📂 Files & Progress

Each file represents one daily learning milestone.
Later steps build directly on earlier input-handling fundamentals.

### ✅ Day 19 — Input Value Handling  
**`01_input_value_handling.js`**

- Read/write values from:
  - text input, textarea, select
  - checkbox, radio
- Track changes via `input` and `change` events
- Safely parse numeric values and handle empty inputs
- Structure input logic into reusable read/write helpers

**Key Concepts**
- `value` vs `checked`
- `event.target` / `closest()` (conceptual connection)
- `input` (real-time) vs `change` (commit) event differences
- Building a clean JS state object from DOM inputs

---

### ✅ Day 20 — Prevent Default Submit  
**`02_form_submit_prevent.js`**

- Fully control form submission via `event.preventDefault()`
- Validate inputs before action
- Build a standardized payload object for APIs/logging
- Provide success/error feedback to the user

**Key Concepts**
- `submit` event control
- Validation → Payload → Action workflow
- Defensive coding (null/empty/invalid values)
- Reset behavior after submission

---

## 🧠 Why Forms & Inputs Matter

Forms are critical for:
- Authentication and onboarding flows
- Payments and subscription journeys
- Settings and profile management
- Data collection and admin tools

Poor form handling leads to:
- Incorrect data capture
- UX friction and drop-offs
- Fragile code that breaks with small UI changes

Well-structured form logic improves both:
- Data quality
- Product conversion metrics

---

## 📌 한국어 요약

- Day 19: 다양한 입력 타입의 값 추출/반영 + 이벤트 기반 상태 업데이트
- Day 20: submit 기본 동작 차단 + 검증(validation) + payload 구성 + UI 피드백

이 폴더는  
**“폼을 단순 HTML 요소가 아니라, 데이터 처리 파이프라인으로 다루는 방식”**을 정리합니다.

---

## 🚧 Status

**Completed (Day 19–20)**  
Next recommended steps:
- Validation patterns (field-level / form-level, reusable validators)
- Async submit (fetch API integration, loading state, error handling)
- Accessibility and UX improvements (focus management, aria attributes)