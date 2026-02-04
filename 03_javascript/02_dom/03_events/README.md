# DOM Events

This directory covers **core DOM event handling concepts** in JavaScript.
Events are the foundation of interactive web applications:

> **UI interaction = DOM events + event handlers + DOM updates**

본 디렉토리는 JavaScript에서 DOM 이벤트를 다루는 핵심 개념을 정리합니다.  
이벤트는 “정적인 화면”을 “사용자와 상호작용하는 UI”로 바꾸는 기반입니다.

---

## 🎯 Objectives

- Understand how to attach event listeners with `addEventListener`
- Learn how to use the **event object** to inspect context and targets
- Master event propagation: **capturing → target → bubbling**
- Control event flow using `preventDefault`, `stopPropagation`, and related patterns
- Build strong fundamentals for **event delegation** (next step)

---

## 📂 Files & Progress

Each file represents a focused topic and is completed incrementally.

### ✅ Day 15 — Event Listener Basics  
**`01_event_listener.js`**

- Register event handlers using `addEventListener`
- Practice common event types: click, keyboard, mouse
- Compare anonymous vs named handlers (removal-ready patterns)

**Key Concepts**
- `addEventListener(type, handler)`
- Multiple listeners on one element
- Handler design for maintainability

---

### ✅ Day 16 — Event Object  
**`02_event_object.js`**

- Explore the `event` object and its practical usage
- Understand `target` vs `currentTarget` clearly
- Use event methods to control default behavior and propagation

**Key Concepts**
- `event.target` vs `event.currentTarget`
- `event.type`, `event.timeStamp`
- `preventDefault()`, `stopPropagation()`

---

### ✅ Day 17 — Event Propagation  
**`03_event_propagation.js`**

- Learn the full DOM event flow:
  - **Capturing → Target → Bubbling**
- Use capture mode (`{ capture: true }` or `true`)
- Stop event flow intentionally and understand side effects

**Key Concepts**
- Capturing vs Bubbling
- `stopPropagation()`
- `stopImmediatePropagation()`

---

## 🧠 Why DOM Events Matter

DOM events enable:
- Buttons, forms, and user interactions
- Dynamic UI updates
- Data input validation
- Complex UI patterns like lists, tables, and modals

Understanding event propagation is especially important because:
- **event delegation** relies on bubbling
- unexpected handler calls are often caused by propagation misunderstandings

---

## 📌 한국어 요약

- Day 15: `addEventListener`로 이벤트 리스너 등록 및 기본 패턴 학습
- Day 16: event 객체 분석 (target/currentTarget, 기본 동작 차단 등)
- Day 17: 이벤트 전파 흐름(캡처링/버블링) 이해 및 전파 제어

이 단계까지 완료하면,
다음 단계인 **이벤트 위임(event delegation)**을 실무 수준으로 구현할 수 있습니다.

---

## 🚧 Status

**Completed (Day 15–17)**  
Next recommended step: **Event Delegation** (handling many items efficiently)