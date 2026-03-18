# Object Transform

This module covers how to transform JavaScript objects for real-world data handling.

In JavaScript, objects are the most common structure for:

- API responses
- configuration data
- user profiles
- analytics data

However, objects cannot directly use array methods like `map`, `filter`, or `reduce`.

So we use a core transformation pattern:

```text
Object → Array → Transform → Object
```

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- extract keys, values, and entries from objects
- convert objects into arrays for processing
- transform object structures using `map`, `filter`, `reduce`
- rebuild objects using `Object.fromEntries()`
- design real-world data transformation pipelines

---

# 🔑 Core Methods

## 1. Object.keys()

```javascript
Object.keys(obj)
```

Returns an array of keys.

---

## 2. Object.values()

```javascript
Object.values(obj)
```

Returns an array of values.

---

## 3. Object.entries()

```javascript
Object.entries(obj)
```

Returns an array of `[key, value]`.

👉 Most powerful for transformation.

---

## 4. Object.fromEntries()

```javascript
Object.fromEntries(array)
```

Converts `[key, value]` array back into an object.

---

# 🔁 Core Transformation Pipeline

This is the most important pattern in this module:

```javascript
Object.entries(obj)
  .map(...)
  .filter(...)
  .reduce(...)
→ Object.fromEntries(...)
```

### 한국어 설명

객체를 바로 처리하지 않고:

1. 배열로 변환
2. map / filter로 가공
3. 다시 객체로 복원

이 흐름이 JavaScript 데이터 처리의 핵심이다.

---

# 📂 Module Structure

| File | Description |
|------|------------|
| `01_object_keys_values_entries.js` | Extract keys, values, entries and iterate objects |
| `02_object_from_entries.js` | Convert arrays back into objects |
| `03_object_mapping_patterns.js` | Real-world object transformation patterns |

---

# 🧠 Conceptual Flow

```text
Object (raw data)
   ↓
Object.entries()
   ↓
Array transformation (map / filter / reduce)
   ↓
Object.fromEntries()
   ↓
New Object (processed data)
```

---

# 🔥 Practical Use Cases

## 1. API Response Transformation

```javascript
const apiUser = {
  id: 1,
  username: "jun",
  is_active: true
};

const mappedUser = {
  userId: apiUser.id,
  userName: apiUser.username,
  status: apiUser.is_active ? "Active" : "Inactive"
};
```

---

## 2. Filtering Object Data

```javascript
const cleaned = Object.fromEntries(
  Object.entries(obj).filter(([k, v]) => v !== null)
);
```

---

## 3. Value Transformation

```javascript
const doubled = Object.fromEntries(
  Object.entries(obj).map(([k, v]) => [k, v * 2])
);
```

---

## 4. Key Renaming

```javascript
const renamed = Object.fromEntries(
  Object.entries(obj).map(([k, v]) => [`user_${k}`, v])
);
```

---

# 🚀 Real-World Pattern

```javascript
const result = Object.fromEntries(
  Object.entries(data)
    .filter(([k, v]) => v !== null)
    .map(([k, v]) => [k.toUpperCase(), v])
);
```

---

### 한국어 설명

실무에서는 이 패턴 하나로 대부분 해결된다:

- 데이터 필터링
- 값 변환
- key 변경

---

# ⚠️ Common Mistakes

## ❌ Trying to use map directly on object

```javascript
obj.map(...) // ERROR
```

👉 objects are not arrays

---

## ❌ Forgetting Object.fromEntries()

```javascript
Object.entries(obj).map(...) 
// returns array, not object
```

---

# 💡 Best Practice

Always think:

```text
Object → entries → transform → fromEntries
```

---

# 📊 When to Use What

| Method | Use Case |
|------|--------|
| keys | when only key list is needed |
| values | when only values are needed |
| entries | when transforming object |
| fromEntries | when rebuilding object |

---

# 🧩 Advanced Insight

Object transformation is fundamental for:

- frontend state management
- backend data processing
- API response normalization
- analytics pipelines

---

# 🧠 Mental Model

```text
Object = structured data
Array = transformable data
```

👉 Convert object → array → process → object

---

# 📌 Summary

```text
Object.keys() → get keys
Object.values() → get values
Object.entries() → get [key, value]
Object.fromEntries() → rebuild object
```

---

# 🔥 Final Insight

```text
JavaScript object handling is not about objects.
It's about converting them into arrays and back.
```

---

### 한국어 핵심 정리

이 모듈의 핵심은:

```text
객체 → 배열 → 가공 → 객체
```

이 흐름을 완전히 이해하는 것이다.

이 패턴을 이해하면:

- API 데이터 처리
- UI 데이터 가공
- 분석 데이터 구조 설계

까지 모두 가능해진다.