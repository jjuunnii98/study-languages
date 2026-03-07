/**
 * Day 46 — Normalize & Flatten JSON
 * File: 03_javascript/04_api/03_json_handling/03_normalize_flatten.js
 *
 * 실제 API 응답은 종종 중첩된 JSON 구조를 가진다.
 *
 * 예:
 * {
 *   id: 1,
 *   user: {
 *     name: "Alice",
 *     address: {
 *       city: "Seoul"
 *     }
 *   }
 * }
 *
 * 이런 구조는 화면 렌더링에는 괜찮을 수 있지만,
 * 테이블 출력 / CSV 저장 / 분석 / 리스트 렌더링에서는
 * 다루기 불편한 경우가 많다.
 *
 * 그래서 "중첩 객체를 평탄화(flatten)" 하는 과정이 필요하다.
 *
 * 핵심 개념:
 * - normalize / flatten = nested JSON → flat object
 * - key path를 점(dot) 형태로 표현
 * - API 응답을 UI/분석 친화적인 구조로 변환
 */


/**
 * ============================================
 * 1️⃣ Example Nested JSON
 * ============================================
 *
 * 실제 API에서 자주 볼 수 있는 구조
 */

const apiResponse = {
  id: 1,
  user: {
    name: "Alice",
    profile: {
      age: 28,
      email: "alice@example.com"
    },
    address: {
      city: "Seoul",
      zipCode: "12345"
    }
  },
  company: {
    name: "Open Data Labs",
    department: {
      team: "Analytics"
    }
  }
};

console.log("Original Nested JSON:");
console.log(apiResponse);


/**
 * ============================================
 * 2️⃣ Flatten Function
 * ============================================
 *
 * 중첩 객체를 재귀(recursion)로 순회하면서
 * 평면 구조로 변환한다.
 *
 * 예:
 * user.profile.age → 28
 * user.address.city → "Seoul"
 */

function flattenObject(obj, parentKey = "", result = {}) {
  for (const key in obj) {
    const value = obj[key];

    // 부모 key가 있다면 dot notation으로 연결
    const newKey = parentKey ? `${parentKey}.${key}` : key;

    // value가 객체이고 null이 아니며 배열이 아닌 경우
    if (
      typeof value === "object" &&
      value !== null &&
      !Array.isArray(value)
    ) {
      flattenObject(value, newKey, result);
    } else {
      result[newKey] = value;
    }
  }

  return result;
}

const flattened = flattenObject(apiResponse);

console.log("Flattened Object:");
console.log(flattened);


/**
 * ============================================
 * 3️⃣ Array Handling Example
 * ============================================
 *
 * 배열은 flatten 전략이 조금 다르다.
 * 여기서는 배열은 그대로 두고,
 * 객체 내부의 구조만 flatten 한다.
 */

const jsonWithArray = {
  id: 2,
  name: "Bob",
  hobbies: ["reading", "coding"],
  contact: {
    email: "bob@example.com",
    phone: "010-1234-5678"
  }
};

const flattenedWithArray = flattenObject(jsonWithArray);

console.log("Flattened Object with Array:");
console.log(flattenedWithArray);


/**
 * ============================================
 * 4️⃣ Normalize Multiple Records
 * ============================================
 *
 * API 응답이 배열 형태라면
 * 각 객체를 순회하면서 flatten 할 수 있다.
 */

const usersResponse = [
  {
    id: 1,
    name: "Alice",
    address: { city: "Seoul", zip: "12345" }
  },
  {
    id: 2,
    name: "Bob",
    address: { city: "Busan", zip: "54321" }
  }
];

const normalizedUsers = usersResponse.map(user => flattenObject(user));

console.log("Normalized Users:");
console.log(normalizedUsers);


/**
 * ============================================
 * 5️⃣ Practical API Example
 * ============================================
 *
 * 실제 fetch API 응답을 받아 flatten 처리하는 예시
 */

async function fetchAndNormalizeUser() {
  try {
    const response = await fetch("https://jsonplaceholder.typicode.com/users/1");

    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    const user = await response.json();

    // 중첩 JSON을 flatten
    const normalizedUser = flattenObject(user);

    console.log("Fetched Original User:");
    console.log(user);

    console.log("Normalized User:");
    console.log(normalizedUser);

  } catch (error) {
    console.error("API request failed:", error.message);
  }
}


/**
 * ============================================
 * 6️⃣ Why Flattening Matters
 * ============================================
 *
 * flatten / normalize가 필요한 이유:
 *
 * 1) 테이블 형태 출력이 쉬워짐
 * 2) CSV / Excel export에 유리
 * 3) 데이터 분석에서 column-based 접근 가능
 * 4) UI 컴포넌트 바인딩 단순화
 */

function explainWhyFlatteningMatters() {
  return [
    "Easier table rendering",
    "Better for CSV/Excel export",
    "Useful for analytics pipelines",
    "Simplifies UI binding"
  ];
}

console.log("Why Flattening Matters:");
console.log(explainWhyFlatteningMatters());


/**
 * ============================================
 * 실행 예시
 * ============================================
 */

fetchAndNormalizeUser();