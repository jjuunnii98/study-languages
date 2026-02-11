# Forms & Inputs (DOM)

This directory covers **core form and input handling patterns** in the browser
using JavaScript DOM APIs.

Forms are where user interaction becomes real data:
- input values
- validation
- submit control
- UI feedback for errors/success

본 디렉토리는 브라우저 환경에서 JavaScript로
폼(Form)과 입력값(Input)을 다루는 핵심 패턴을 정리합니다.

---

## 🎯 Objectives

- Read and normalize user input values safely
- Handle form submissions with proper event control
- Prevent default browser submit behavior when needed
- Implement basic client-side validation
- Provide user-friendly feedback messages (error/success)

---

## 📂 Structure & Progress

Each file represents one practical topic.
Files are completed incrementally with daily commits.

각 파일은 실무에서 자주 쓰는 주제 하나를 다루며,
일일 학습 단위로 순차적으로 완성됩니다.

---

## ✅ Completed

### ✅ Day 19 — Input Value Handling  
**`01_input_value_handling.js`**

**Key Concepts**
- `value`, `checked`, `selectedIndex`
- `trim()` for normalization
- Input type differences (text / checkbox / select)

**Purpose**
- Convert user input into clean, usable data

---

### ✅ Day 20 — Form Submit Control  
**`02_form_submit_prevent.js`**

**Key Concepts**
- `submit` event
- `event.preventDefault()`
- Controlled form submission flow

**Purpose**
- Prevent unintended submits and build predictable submission logic

---

### ✅ Day 21 — Basic Validation  
**`03_validation_basic.js`**

**Key Concepts**
- Required checks (empty input)
- Basic format validation (email regex example)
- Rule-based validation (password length)
- Error collection pattern (`errors[]`)
- UI feedback rendering (error/success)

**Purpose**
- Validate form inputs before submitting
- Improve user experience with immediate feedback

---

## 🧠 Why Forms & Inputs Matter

Forms are the gateway between users and systems.

Even a simple app needs to handle:
- clean input normalization
- validation rules
- safe submission flow
- user-friendly messaging

Without proper form handling:
- data quality becomes unreliable
- UX becomes frustrating
- errors propagate to backend systems

폼 처리는 프론트엔드 개발의 기본기이자,
데이터 품질과 사용자 경험을 동시에 결정하는 핵심 요소입니다.

---

## 📌 한국어 요약

- Day 19: 입력값을 읽고 정규화하는 패턴
- Day 20: submit 이벤트 제어 및 기본 제출 방지
- Day 21: 기본 검증(필수값/형식/룰) 및 사용자 피드백 출력

이 폴더는
**폼 입력 → 제출 제어 → 검증 → 피드백**의 표준 흐름을 제공합니다.

---

## 🚧 Status

**In progress — Forms & Inputs**

Next recommended topics:
- Real-time validation (`input` event + debounce)
- Advanced validation rules (password strength, custom validators)
- Async validation (API-based checks)
- Accessibility-friendly error messaging