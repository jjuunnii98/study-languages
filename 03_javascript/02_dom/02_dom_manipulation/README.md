# DOM Manipulation

This section focuses on **manipulating existing DOM elements** after they have been selected.  
It covers creating, removing, and updating elements dynamically based on user interaction or program logic.

본 섹션은 **이미 선택된 DOM 요소를 실제로 조작하는 방법**에 집중합니다.  
요소 생성, 삭제, 텍스트/HTML 변경 등 **동적인 UI 제어의 핵심 개념**을 다룹니다.

---

## 🎯 Learning Objectives

- Create and remove DOM elements dynamically
- Update text and HTML content safely and correctly
- Understand differences between text-based and structure-based updates
- Build intuition for real-world UI manipulation patterns

---

## 📂 Files & Progress

각 파일은 하루 단위 학습(Day) 기준으로 구성되어 있으며,  
실무에서 가장 자주 사용되는 DOM 조작 패턴을 단계적으로 다룹니다.

### ✅ Completed

### `01_create_remove_elements.js` (Day 11)

**Create & Remove DOM Elements**

- `document.createElement`
- `appendChild`, `remove`, `removeChild`
- 동적 요소 생성 및 삭제 흐름 이해
- UI 상태 변화에 따른 DOM 제어

📌 핵심 포인트  
- DOM은 정적인 HTML이 아니라 **런타임에 변경 가능한 구조**
- 사용자 이벤트 기반 UI의 기초

---

### `02_text_html_update.js` (Day 12)

**Text vs HTML Content Update**

- `textContent`
- `innerHTML`
- 보안(XSS) 관점에서의 차이
- 언제 어떤 방식을 써야 하는지에 대한 기준 정립

📌 핵심 포인트  
- `textContent` → 안전한 텍스트 출력
- `innerHTML` → 구조 변경 가능하지만 주의 필요
- 실무에서는 **기본은 textContent, 필요 시 innerHTML**

---

## 🧠 Practical Insights

DOM 조작은 단순한 문법 문제가 아니라  
**UI 상태, 보안, 유지보수성**과 직결되는 문제입니다.

이 섹션을 통해 다음과 같은 감각을 기르는 것이 목표입니다:

- “이 변경은 텍스트인가, 구조인가?”
- “사용자 입력이 포함되는가?”
- “이 작업은 JS로 할까, 프레임워크에 맡길까?”

---

## 🚧 Status

**In progress – DOM Manipulation**

- Day 11–12 완료
- 다음 단계: **Events & Interaction**

---

## 🔜 Next Topics

- `03_events/01_add_event_listener.js`
- 이벤트 전파 (bubbling / capturing)
- 실전 UI 인터랙션 패턴

---

## 📌 요약 (한국어)

- DOM 요소를 직접 생성·삭제·수정하는 핵심 방법 학습
- 텍스트 변경과 HTML 구조 변경의 차이 명확히 이해
- 프레임워크 이전 단계에서 반드시 필요한 DOM 기초 완성
- 이후 이벤트 처리 및 인터랙션 학습을 위한 기반 마련