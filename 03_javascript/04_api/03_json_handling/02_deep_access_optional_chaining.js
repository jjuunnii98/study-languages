/**
 * Day 45 — Deep Access & Optional Chaining
 * File: 03_javascript/04_api/03_json_handling/02_deep_access_optional_chaining.js
 *
 * 실제 API 응답(JSON)은 대부분 "중첩 구조(nested object)"로 되어 있다.
 *
 * 예:
 * user → address → geo → lat
 *
 * 이런 데이터를 접근할 때 문제가 되는 것이
 * "undefined 접근 에러"이다.
 *
 * 예:
 * user.address.geo.lat
 *
 * 만약 address가 없다면?
 * → TypeError 발생
 *
 * 이를 해결하기 위해 JavaScript는
 * Optional Chaining (?.) 을 제공한다.
 *
 * Optional Chaining은
 * "존재할 때만 접근하고 없으면 undefined 반환"
 * 하는 안전한 접근 방식이다.
 */

/**
 * ============================================
 * 1️⃣ Example JSON (API Response)
 * ============================================
 *
 * 실제 API에서 자주 볼 수 있는 JSON 구조
 */

const apiResponse = {
  id: 1,
  name: "Alice",
  address: {
    city: "Seoul",
    geo: {
      lat: 37.5665,
      lng: 126.9780
    }
  }
};

console.log("User:", apiResponse);


/**
 * ============================================
 * 2️⃣ Deep Object Access (기본 접근)
 * ============================================
 *
 * 중첩 객체 접근
 */

const latitude = apiResponse.address.geo.lat;

console.log("Latitude:", latitude);


/**
 * ============================================
 * 3️⃣ Problem: Undefined Error
 * ============================================
 *
 * 아래 객체에는 address가 없다.
 */

const userWithoutAddress = {
  id: 2,
  name: "Bob"
};

// 다음 코드는 오류 발생 가능
// userWithoutAddress.address.geo.lat
// → TypeError: Cannot read properties of undefined


/**
 * ============================================
 * 4️⃣ Optional Chaining
 * ============================================
 *
 * ?. 를 사용하면
 * 값이 존재할 때만 접근한다.
 */

const safeLatitude = userWithoutAddress.address?.geo?.lat;

console.log("Safe Latitude:", safeLatitude);


/**
 * ============================================
 * 5️⃣ Optional Chaining with Arrays
 * ============================================
 *
 * 배열 접근에도 사용 가능
 */

const users = [
  { name: "Alice" },
  { name: "Bob", address: { city: "Busan" } }
];

const city = users[1].address?.city;

console.log("User city:", city);


/**
 * ============================================
 * 6️⃣ Optional Chaining with Function Calls
 * ============================================
 *
 * 함수가 존재할 때만 실행 가능
 */

const logger = {
  log(message) {
    console.log("LOG:", message);
  }
};

logger.log?.("Hello Optional Chaining");


/**
 * ============================================
 * 7️⃣ Nullish Coalescing (??)
 * ============================================
 *
 * Optional chaining과 함께 자주 사용되는 연산자
 *
 * ?? → 값이 null 또는 undefined이면 기본값 사용
 */

const userCity = userWithoutAddress.address?.city ?? "Unknown";

console.log("User City:", userCity);


/**
 * ============================================
 * 8️⃣ Practical API Handling Example
 * ============================================
 *
 * 실제 API 데이터 처리 패턴
 */

async function fetchUser() {

  try {

    const response = await fetch("https://jsonplaceholder.typicode.com/users/1");

    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    const user = await response.json();

    // Optional chaining으로 안전 접근
    const city = user.address?.city ?? "No city data";

    console.log("Fetched user:", user.name);
    console.log("City:", city);

  } catch (error) {

    console.error("API request failed:", error.message);

  }

}


/**
 * ============================================
 * 실행 예시
 * ============================================
 */

fetchUser();