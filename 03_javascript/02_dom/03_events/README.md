# DOM Events (JavaScript)

This directory covers **DOM event handling fundamentals and advanced patterns**
used in modern front-end development.

DOM events enable interaction between users and web pages.
Understanding how events work is essential for building
responsive, scalable, and maintainable user interfaces.

본 디렉토리는 JavaScript에서 DOM 이벤트를 다루는
기초 개념부터 실무에서 반드시 필요한 고급 패턴까지를 정리합니다.

---

## 🎯 Objectives

- Understand how DOM events are triggered and handled
- Learn the structure and role of the Event object
- Master event propagation (capturing vs bubbling)
- Apply event delegation for scalable UI design
- Write robust event-handling code for real-world applications

---

## 📂 Files & Progress

Each file represents one daily learning milestone.
Later topics build directly on earlier concepts.

### ✅ Day 15 — Event Listener Basics  
**`01_event_listener.js`**

- 이벤트 리스너 등록 기본 구조
- `addEventListener` 사용법
- 클릭, 입력 등 기본 사용자 이벤트 처리

**Key Concepts**
- Event-driven programming
- Multiple listeners
- Separation of logic and UI

---

### ✅ Day 16 — Event Object  
**`02_event_object.js`**

- Event 객체의 역할과 구조
- `event.target` vs `event.currentTarget`
- 이벤트 정보 접근 방법

**Key Concepts**
- Event metadata
- Target resolution
- Context-aware handlers

---

### ✅ Day 17 — Event Propagation  
**`03_event_propagation.js`**

- 이벤트 전파 메커니즘 이해
- Capturing phase vs Bubbling phase
- `stopPropagation()`의 영향

**Key Concepts**
- Event flow
- Bubbling default behavior
- Controlled propagation

---

### ✅ Day 18 — Event Delegation  
**`04_event_delegation.js`**

- 이벤트 위임(Event Delegation) 패턴
- 부모 요소 하나로 여러 자식 이벤트 처리
- 동적 DOM 요소 처리 전략

**Key Concepts**
- Bubbling-based delegation
- `event.target` + `closest()`
- Performance and scalability

---

## 🧠 Why DOM Events Matter

DOM event handling is central to:
- Interactive UI development
- Form handling and validation
- Dynamic lists and tables
- Performance-optimized front-end architecture

Poor event handling can lead to:
- Memory leaks
- Hard-to-maintain code
- Performance bottlenecks

Well-structured event logic leads to
clean, scalable, and predictable UI behavior.

---

## 📌 한국어 요약

- Day 15: 이벤트 리스너의 기본 구조와 사용법
- Day 16: Event 객체와 이벤트 정보 접근
- Day 17: 이벤트 전파(캡처링/버블링) 이해
- Day 18: 이벤트 위임을 통한 확장 가능한 UI 설계

이 폴더는  
**DOM 이벤트를 단순 사용이 아닌 “설계 관점”에서 다루는 단계**입니다.

---

## 🚧 Status

**Completed (Day 15–18)**  
This module provides a solid foundation for:
- Complex UI interactions
- Dynamic DOM manipulation
- Framework-level event handling (React, Vue, etc.)