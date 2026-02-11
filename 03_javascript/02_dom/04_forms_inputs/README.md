# Forms & Inputs (DOM)

This directory covers **practical form and input handling patterns** in the browser
using JavaScript DOM APIs.

Forms are where user interaction becomes real data:
- reading input values
- controlling submit behavior
- validating data
- providing user-friendly feedback

본 디렉토리는 브라우저 환경에서 JavaScript DOM API를 활용해
**폼(Form)과 입력값(Input)** 을 다루는 실전 패턴을 정리합니다.

---

## 🎯 Objectives

- Read and normalize user inputs safely (trim, type handling)
- Handle form submission with predictable event control
- Prevent default submission when necessary
- Validate input values with clear, reusable rules
- Provide immediate UI feedback (error/success)
- Improve UX with real-time validation using input events + debounce

---

## 📂 Structure & Progress

Each file represents one practical topic.
Files are completed incrementally with daily commits.

각 파일은 실무에서 자주 쓰는 주제 하나를 다루며,
일일 학습 단위로 순차적으로 완성됩니다.

---

## ✅ Completed (Day 19–22)

### ✅ Day 19 — Input Value Handling  
**`01_input_value_handling.js`**

**Key Concepts**
- Reading values: `value`, `checked`, `selectedIndex`
- Normalization: `trim()`
- Input type differences (text / checkbox / select)

**Purpose**
- Convert user input into clean, usable data

---

### ✅ Day 20 — Form Submit Control  
**`02_form_submit_prevent.js`**

**Key Concepts**
- `submit` event
- `event.preventDefault()`
- Controlled submission flow (validation → submit)

**Purpose**
- Prevent unintended submits and build predictable logic

---

### ✅ Day 21 — Basic Validation  
**`03_validation_basic.js`**

**Key Concepts**
- Required checks (empty input)
- Format validation (email pattern example)
- Rule validation (password length policy)
- Error collection pattern (`errors[]`)
- UI feedback rendering (error/success)

**Purpose**
- Validate form inputs before submitting
- Improve user experience with immediate feedback

---

### ✅ Day 22 — Real-time Input Events (Live Validation)  
**`04_real_time_input_events.js`**

**Key Concepts**
- `input` event for live updates
- Debounce pattern to reduce unnecessary validation calls
- Live UI feedback (error/success state)
- Submit button enable/disable control
- Final validation gate on `submit`

**Purpose**
- Provide real-time validation UX
- Keep validation efficient and maintainable

---

## 🧠 Why Forms & Inputs Matter

Forms are the gateway between users and systems.

Even simple apps need:
- clean input normalization
- reliable validation rules
- safe submission control
- clear user feedback

Without proper form handling:
- data quality becomes unreliable
- user experience degrades
- backend systems receive inconsistent inputs

폼 처리는 프론트엔드 개발의 기본기이며,
데이터 품질과 사용자 경험을 동시에 결정하는 핵심 요소입니다.

---

## 📌 한국어 요약

- Day 19: 입력값 읽기 + 정규화(trim) 패턴
- Day 20: submit 이벤트 제어 및 기본 제출 방지
- Day 21: 기본 검증(필수값/형식/룰) + 오류 수집 + 피드백 출력
- Day 22: input 이벤트 + debounce 기반 실시간 검증 UX 구현

이 폴더는
**입력 → 제출 제어 → 검증 → 실시간 피드백**의 표준 흐름을 제공합니다.

---

## 🚀 Next (Recommended)

- Advanced validation rules (password strength, custom validators)
- Async validation (API-based checks, e.g., email duplication)
- Accessibility-friendly error messaging (ARIA)
- Race condition handling for async validation