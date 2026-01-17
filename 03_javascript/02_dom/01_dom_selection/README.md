# DOM Selection

This module focuses on **selecting elements from the DOM using JavaScript**.
Correct and predictable element selection is the foundation of all DOM manipulation
and event handling.

본 파트는 JavaScript에서 **DOM 요소를 선택하는 방법**을 다룹니다.  
DOM 조작의 시작은 “어떤 요소를 정확히 가져오느냐”이며,
잘못된 선택은 UI 버그와 예측 불가능한 동작의 원인이 됩니다.

---

## 🎯 Learning Objectives

- Understand different DOM selection APIs
- Choose the appropriate selector based on use case
- Recognize the differences between live and static collections
- Avoid common pitfalls in element selection

---

## 📂 Files & Progress

Each file represents a focused concept.
Files are completed incrementally with day-based commits.

각 파일은 하나의 핵심 개념을 다루며,
Day 단위 학습 기록으로 순차적으로 완성됩니다.

---

### ✅ Completed

#### `01_get_element.js` (Day 8)
**Basic DOM selection using legacy APIs**

**Covered topics**
- `document.getElementById`
- `document.getElementsByClassName`
- `document.getElementsByTagName`
- Return values (`Element`, `HTMLCollection`, `null`)
- Iterating over `HTMLCollection`
- Live collection characteristics

**핵심 포인트 (한국어)**
- `getElementById`는 단일 요소 또는 `null` 반환
- `getElementsByClassName`, `getElementsByTagName`은 `HTMLCollection` 반환
- `HTMLCollection`은 실시간(live)으로 DOM 변경을 반영
- 배열 메서드를 바로 사용할 수 없다는 점에 주의

---

### ⏳ Planned

#### `02_query_selector.js`
**Modern DOM selection**
- `querySelector` vs `querySelectorAll`
- CSS selector-based selection
- `NodeList` vs `HTMLCollection`
- Static vs live collections

#### `03_node_list_vs_html_collection.js`
**Collection comparison**
- Practical differences
- Performance and safety considerations
- Real-world usage patterns

---

## 🧠 Why DOM Selection Matters

Accurate DOM selection allows you to:
- Manipulate the correct UI elements
- Avoid unexpected side effects
- Write maintainable and readable front-end code
- Scale interaction logic as the UI grows

DOM 선택은 단순한 문법 문제가 아니라,
**UI 안정성과 코드 품질을 결정하는 핵심 요소**입니다.

---

## 🚧 Status

**In progress — DOM Selection (Day 8 started)**

This module will continue with modern selector APIs
and practical comparison patterns.

본 파트는 Day 8부터 시작되었으며,
이후 현대적인 선택 방식과 실무 패턴으로 확장됩니다.