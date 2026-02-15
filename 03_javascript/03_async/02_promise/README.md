# Promise Architecture (JavaScript Async — Step 2)

This module explores **Promise-based asynchronous system design**
in modern JavaScript.

Rather than focusing on syntax alone, this section treats Promise as:

- A deterministic state machine
- A failure propagation mechanism
- A composable async pipeline abstraction
- A concurrency coordination primitive

콜백 기반 비동기 구조의 한계를 해결하는 Promise 패턴을  
문법 수준이 아닌 **아키텍처(architecture) 관점**에서 다룹니다.

This module forms the structural bridge:

Callback → Promise → async / await

---

## 🎯 Core Learning Objectives

By completing this module, you will:

- Understand Promise as a state machine (`pending → fulfilled / rejected`)
- Model asynchronous flow deterministically
- Design sequential async pipelines using `.then()`
- Centralize failure handling using `.catch()`
- Differentiate between returning values and returning Promises
- Architect composable async flows
- Apply concurrency control (`all`, `race`, `allSettled`, `any`)
- Prepare for async/await refactoring

---

## 📂 Implementation Progress

### ✅ Day 26 — Promise Fundamentals  
`01_promise_basics.js`

**Focus: State & Lifecycle**

- Promise constructor internals
- State transitions
- `.then()` / `.catch()` / `.finally()`
- Error bubbling model

**Architectural Insight:**
Promise enforces a one-time immutable state transition,  
making async flows predictable.

---

### ✅ Day 27 — Promise Chaining Architecture  
`02_promise_chain.js`

**Focus: Sequential Composition**

- Returning values vs Promises
- Chain flattening (avoid nesting)
- Centralized error boundary
- Conditional branching logic
- Async pipeline composition

**Architectural Insight:**
Promise chains behave like deterministic pipelines,  
where each stage transforms or forwards the async result.

---

### ✅ Day 28 — Concurrency & Coordination  
`03_promise_all_race.js`

**Focus: Parallel Execution Strategies**

- `Promise.all()` (fail-fast aggregation)
- `Promise.race()` (first-completion strategy)
- `Promise.allSettled()` (wait-all strategy)
- `Promise.any()` (first-success strategy)

**Architectural Insight:**
Promise introduces concurrency primitives  
that allow explicit control over async coordination.

---

## 🧠 What is a Promise (Architectural View)

A Promise is:

> An object representing the eventual completion  
> or failure of an asynchronous operation.

More precisely:

A Promise is a **controlled state container**
that transitions exactly once and exposes
a composable continuation interface.

Promise는 단순한 비동기 객체가 아니라,  
단 한 번만 상태 전이를 허용하는 **상태 컨테이너**입니다.

---

## 🔄 Async System Evolution

```text
Callback
    ↓
Callback Hell
    ↓
Promise (Deterministic State Model)
    ↓
async / await (Syntactic Refinement)