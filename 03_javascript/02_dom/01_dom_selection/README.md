# DOM Selection

This directory covers the fundamentals of **selecting DOM elements** in JavaScript.
DOM selection is the foundation for DOM manipulation, event handling,
and building interactive web interfaces.

본 폴더는 JavaScript에서 **DOM 요소를 선택하는 핵심 기법**을 다룹니다.  
DOM 선택은 이후 DOM 조작, 이벤트 처리, 폼 입력 처리로 이어지는
프론트엔드 개발의 출발점입니다.

---

## 📂 Files

### `01_get_element.js` (Day 8)
Classic DOM selection methods

- `getElementById`
- `getElementsByClassName`
- `getElementsByTagName`
- `getElementsByName`
- HTMLCollection 반환 및 특징(live collection)

**한국어 요약**
- 전통적인 DOM 선택 API 이해
- 단일/복수 요소 선택 방식 차이
- HTMLCollection의 live 특성 파악

---

### `02_query_selector.js` (Day 9)
Modern DOM selection using CSS selectors

- `querySelector`
- `querySelectorAll`
- CSS 선택자 기반 DOM 접근
- NodeList 반환과 특징
- null 체크를 통한 안전한 DOM 접근
- 범위를 제한한 선택 (`container.querySelector`)
- 실무에서 자주 쓰는 active 요소 선택 패턴

**한국어 요약**
- 최신 표준 DOM 선택 방식 학습
- 단일 vs 다중 요소 선택 차이 명확화
- 실무 수준의 안전한 DOM 접근 습관 형성

---

### `03_node_list_vs_html_collection.js` (Day 10)
NodeList vs HTMLCollection

- NodeList (static collection)
- HTMLCollection (live collection)
- DOM 변경 시 두 컬렉션의 동작 차이
- 반복 처리 방식 차이 (`forEach` vs `Array.from`)
- 실무에서 권장되는 선택 기준

**한국어 요약**
- NodeList와 HTMLCollection의 본질적 차이 이해
- DOM 변경에 따른 예상치 못한 버그 방지
- 실무에서는 NodeList 기반 접근을 기본으로 사용

---

## 🎯 Learning Objectives

- DOM 구조와 선택의 개념 정확히 이해
- 상황에 맞는 DOM 선택 API 사용
- 안전한 DOM 접근(null 체크) 습관화
- DOM 조작 및 이벤트 처리로 확장할 수 있는 기반 확보

---

## 🧠 Why DOM Selection Matters

DOM selection enables:
- Dynamic UI updates
- Event handling
- Form validation
- Interactive web applications

Without reliable DOM selection,
DOM manipulation code becomes fragile and error-prone.

DOM 선택은 모든 프론트엔드 로직의 기초이며,  
이 단계가 탄탄해야 이후 코드 품질과 유지보수성이 안정됩니다.

---

## 🚧 Status

**Completed — DOM Selection (Day 8–10)**

Next steps:
- DOM manipulation (create, update, remove elements)
- Event handling (click, input, delegation)
- Forms & input processing