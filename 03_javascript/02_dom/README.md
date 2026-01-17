# JavaScript DOM (Document Object Model)

This module covers **DOM fundamentals**—how JavaScript interacts with HTML elements
to build dynamic user interfaces.

DOM skills are essential for:
- front-end development (interactive UI)
- browser-based data visualization
- building product prototypes and dashboards
- understanding frameworks (React/Vue) at a deeper level

본 파트는 JavaScript로 **DOM(Document Object Model)**을 다루는 방법을 학습합니다.  
DOM은 HTML 문서를 “객체”로 표현한 구조이며, JavaScript는 DOM을 통해 요소를 선택하고,
내용/스타일을 변경하며, 사용자 이벤트를 처리해 동적인 UI를 만듭니다.

---

## 🎯 Learning Objectives

- Select DOM elements reliably using modern APIs
- Manipulate DOM structure and content safely
- Handle user interactions with event-driven programming
- Manage form inputs and validation patterns
- Build reusable patterns that translate to modern frameworks

---

## 📂 Structure

This module is organized into four subtopics:

### 01) DOM Selection (`01_dom_selection/`)
**How to locate elements in the DOM**
- `getElementById`, `getElementsByClassName`, `getElementsByTagName`
- `querySelector`, `querySelectorAll`
- NodeList vs HTMLCollection differences
- Selecting elements safely and predictably

DOM에서 요소를 “어떻게 정확히 가져오는지”를 다룹니다.  
DOM 조작의 출발점이며, 선택 방식의 차이를 이해하면 오류를 크게 줄일 수 있습니다.

---

### 02) DOM Manipulation (`02_dom_manipulation/`)
**How to create, update, and remove elements**
- Create/remove elements dynamically
- Update text vs HTML (`textContent` vs `innerHTML`)
- Manage classes and inline styles
- Traverse DOM relationships (parent/child/sibling)

가져온 요소를 “어떻게 변경하는지”를 다룹니다.  
실무에서는 UI 업데이트(텍스트 변경, 리스트 추가/삭제 등)에 가장 자주 사용됩니다.

---

### 03) Events (`03_events/`)
**How to respond to user behavior**
- `addEventListener`
- Event object usage (`event.target`, `preventDefault`)
- Bubbling vs capturing (propagation model)
- Event delegation pattern (scalable event handling)

사용자 입력(클릭, 키보드, 마우스 등)을 처리하는 이벤트 기반 프로그래밍을 다룹니다.  
특히 **event delegation**은 실무에서 매우 중요합니다.

---

### 04) Forms & Inputs (`04_forms_inputs/`)
**How to work with form inputs and validation**
- Read/write input values
- Handle submit events and prevent page reload
- Basic validation patterns
- Real-time input events (change/input/keyup)

폼과 입력값 처리는 “서비스 기능”과 직결됩니다.  
검색, 로그인, 필터링 UI 등의 기반이 되는 핵심 영역입니다.

---

## ✅ Recommended Study Flow

A suggested progression:

1. Selection → 2. Manipulation → 3. Events → 4. Forms & Inputs

This order matches real product development:
- find elements → update UI → handle user actions → validate user input

추천 학습 순서:
1) 선택 → 2) 조작 → 3) 이벤트 → 4) 폼/입력

실제 서비스 개발 흐름(요소 선택 → UI 변경 → 행동 처리 → 입력 검증)과 동일합니다.

---

## 🧠 Why DOM Matters (for Data + Product)

DOM skills help you:
- build interactive dashboards (tables, filters, charts)
- prototype product ideas quickly
- understand how frameworks work under the hood
- connect data logic with UI behavior

DOM은 데이터 분석 결과를 “사용자에게 보여주는 형태”로 연결해주는 기술입니다.  
즉, 데이터/ML 역량을 서비스로 전환할 때 필수 기반이 됩니다.

---

## 🚧 Status

**In progress — JavaScript DOM module**

This module will be expanded incrementally with day-based commits.

본 모듈은 Day 단위 학습 기록으로 지속적으로 확장됩니다.