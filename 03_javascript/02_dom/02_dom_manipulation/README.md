# DOM Manipulation

This section focuses on **manipulating existing DOM elements** after they have been selected.  
It covers creating, removing, traversing, and updating elements dynamically based on user interaction or program logic.

본 섹션은 **이미 선택된 DOM 요소를 실제로 조작하는 방법**에 집중합니다.  
요소 생성, 삭제, 탐색(Traversing), 텍스트/HTML/스타일 변경 등 **동적인 UI 제어의 핵심 개념**을 다룹니다.

---

## 🎯 Learning Objectives

- Create and remove DOM elements dynamically
- Update text and HTML content safely and correctly
- Manipulate classes and inline styles using state-based patterns
- Traverse parent/child/sibling relationships in the DOM tree
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

### `03_class_style_manipulation.js` (Day 13)

**Class & Style Manipulation (State-based UI Pattern)**

- `classList.add/remove/toggle/contains`
- inline `style` 조작 및 reset 전략
- “상태(state)에 따라 UI를 바꾸는” 토글 패턴

📌 핵심 포인트  
- 실무에서는 **class 토글 기반 UI 제어**가 유지보수에 유리
- inline style은 학습용으로 이해하되, 남발은 지양

---

### `04_dom_traversing.js` (Day 14)

**DOM Traversing (Parent / Child / Sibling Navigation)**

- `parentElement`, `children`, `firstElementChild`, `lastElementChild`
- `previousElementSibling`, `nextElementSibling`
- `closest(selector)`를 활용한 조상 탐색
- 이벤트 위임 기반 탐색 패턴(ul에서 li를 처리)

📌 핵심 포인트  
- DOM 탐색은 “기준점 + 최소 탐색”이 안정적
- `nextSibling` 대신 **`nextElementSibling` 권장** (텍스트 노드 혼입 방지)

---

## 🧠 Practical Insights

DOM 조작은 단순 문법이 아니라  
**UI 상태 관리, 보안, 유지보수성**과 직결됩니다.

이 섹션의 목표는 다음 질문에 답할 수 있는 감각을 기르는 것입니다:

- “이 변경은 텍스트인가, 구조인가?”
- “사용자 입력이 포함되는가?”
- “class 기반으로 관리할 수 있는가?”
- “선택한 요소에서 탐색이 필요한가?”

---

## 🚧 Status

**In progress – DOM Manipulation**

- Day 11–14 완료
- 다음 단계: **Events & Interaction** 또는 **DOM Mini Project**

---

## 🔜 Next Topics (Recommended)

- `03_events/01_add_event_listener.js` (이벤트 처리 기초)
- 이벤트 전파 (bubbling / capturing)
- `dataset (data-*)` 활용 및 이벤트 위임 심화
- DOM 기반 mini project (Todo / Filter / Tabs)

---

## 📌 요약 (한국어)

- DOM 요소 생성/삭제/업데이트/스타일 변경을 실전 패턴으로 학습
- `textContent` vs `innerHTML` 차이를 보안 관점에서 이해
- `classList` 토글 기반 UI 제어로 “상태 기반” 사고 확립
- parent/child/sibling/closest를 활용한 DOM 탐색 능력 확보