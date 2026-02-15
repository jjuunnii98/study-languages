# Promise (JavaScript Async — Step 2)

This directory covers **Promise-based asynchronous control flow**
in JavaScript.

It moves beyond basic syntax and focuses on:

- State transitions
- Sequential chaining
- Error propagation
- Clean async pipeline design

콜백 기반 비동기 구조의 한계를 해결하는 Promise 패턴을
문법 수준을 넘어 “설계 관점”에서 다룹니다.

This module bridges:
Callback → Promise → async/await

---

## 🎯 Learning Objectives

- Understand Promise state transitions
- Use resolve / reject properly
- Design clean `.then()` chains
- Handle errors centrally using `.catch()`
- Understand value vs Promise returns
- Build maintainable async pipelines
- Prepare for async/await refactoring

---

## 📂 Files & Progress

### ✅ Day 26 — Promise Basics  
`01_promise_basics.js`

Covers:

- Promise constructor mechanics
- pending → fulfilled / rejected states
- `.then()` / `.catch()` / `.finally()`
- Basic chaining
- Error propagation model

한국어 요약:

- Promise 상태 구조 이해
- resolve / reject 흐름
- 체이닝의 기본 원리
- 에러 전파 모델 이해

---

### ✅ Day 27 — Promise Chaining Patterns  
`02_promise_chain.js`

Covers:

- Returning values vs returning Promises
- Sequential async pipeline design
- Centralized error handling
- Business rule branching inside chains
- Clean replacement of callback-based flows

한국어 요약:

- then()에서 return의 중요성
- 체이닝 기반 파이프라인 설계
- 중앙 집중 에러 처리
- 조건 분기 로직 구현
- 콜백 헬을 구조적으로 해결

---

## 🧠 What is a Promise?

A Promise is:

> An object representing the eventual completion  
> or failure of an asynchronous operation.

Promise는 비동기 작업의 결과 상태를 표현하는 객체입니다.

### States

- **pending**
- **fulfilled**
- **rejected**

상태 전이는 단 한 번만 발생합니다.

---

## 🔄 Conceptual Async Evolution

```text
Callback
    ↓
Callback Hell
    ↓
Promise
    ↓
async / await