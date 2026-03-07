/**
 * Day 44 — JSON Parse & Stringify
 * File: 03_javascript/04_api/03_json_handling/01_json_parse_stringify.js
 *
 * JSON은 JavaScript Object Notation의 약자로
 * 서버와 클라이언트 간 데이터를 교환할 때 가장 많이 사용되는 형식이다.
 *
 * 핵심 기능:
 * 1️⃣ JSON.parse()     → JSON 문자열을 JavaScript 객체로 변환
 * 2️⃣ JSON.stringify() → JavaScript 객체를 JSON 문자열로 변환
 *
 * 이 과정은 API 통신에서 매우 중요하다.
 * 서버 → JSON 문자열
 * 클라이언트 → 객체로 변환 후 사용
 */

/**
 * ============================================
 * 1️⃣ JavaScript Object → JSON String
 * ============================================
 *
 * JSON.stringify()는 JavaScript 객체를
 * JSON 문자열로 변환한다.
 *
 * API 요청을 보낼 때 자주 사용된다.
 */

const userObject = {
  id: 1,
  name: "Alice",
  age: 28,
  isActive: true
};

// 객체를 JSON 문자열로 변환
const jsonString = JSON.stringify(userObject);

console.log("Original Object:", userObject);
console.log("JSON String:", jsonString);


/**
 * ============================================
 * 2️⃣ JSON String → JavaScript Object
 * ============================================
 *
 * JSON.parse()는 JSON 문자열을
 * JavaScript 객체로 변환한다.
 *
 * API 응답(JSON)을 처리할 때 사용된다.
 */

const apiResponse = '{"id":2,"name":"Bob","age":31,"isActive":false}';

// JSON 문자열을 객체로 변환
const parsedObject = JSON.parse(apiResponse);

console.log("Parsed Object:", parsedObject);
console.log("User name:", parsedObject.name);


/**
 * ============================================
 * 3️⃣ Pretty JSON (가독성 좋은 JSON)
 * ============================================
 *
 * JSON.stringify(object, null, 2)
 *
 * 세 번째 인자는 들여쓰기(space)를 의미한다.
 * 로그 출력이나 파일 저장 시 가독성을 높일 수 있다.
 */

const prettyJson = JSON.stringify(userObject, null, 2);

console.log("Pretty JSON:");
console.log(prettyJson);


/**
 * ============================================
 * 4️⃣ JSON.stringify() 옵션
 * ============================================
 *
 * replacer를 사용하면 특정 속성을 제외하거나
 * 변환할 수 있다.
 */

// password 제외 예시

const account = {
  username: "admin",
  password: "secret123",
  role: "administrator"
};

const safeJson = JSON.stringify(account, (key, value) => {

  // password는 JSON에 포함하지 않음
  if (key === "password") {
    return undefined;
  }

  return value;

});

console.log("Filtered JSON:", safeJson);


/**
 * ============================================
 * 5️⃣ JSON.parse() Error Handling
 * ============================================
 *
 * 잘못된 JSON 문자열을 parse하면
 * SyntaxError가 발생한다.
 *
 * 따라서 try/catch로 처리하는 것이 안전하다.
 */

const invalidJson = "{ name: 'John' }"; // 잘못된 JSON (따옴표 없음)

try {

  const data = JSON.parse(invalidJson);

  console.log(data);

} catch (error) {

  console.error("JSON parsing failed:", error.message);

}


/**
 * ============================================
 * 6️⃣ API Response JSON Handling Example
 * ============================================
 *
 * 실제 API 호출에서는 JSON을 이렇게 처리한다.
 */

async function fetchUser() {

  try {

    const response = await fetch("https://jsonplaceholder.typicode.com/users/1");

    // HTTP 상태코드 검사
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    // JSON 자동 파싱
    const user = await response.json();

    console.log("Fetched User:", user);

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