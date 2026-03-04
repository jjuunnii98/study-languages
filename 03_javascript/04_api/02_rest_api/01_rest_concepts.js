/**
 * Day 40 — REST API Concepts
 * File: 03_javascript/04_api/02_rest_api/01_rest_concepts.js
 *
 * This file explains the fundamental concepts of REST APIs
 * using JavaScript examples.
 *
 * ---------------------------------------------------------
 * REST란?
 * ---------------------------------------------------------
 * REST (Representational State Transfer)는
 * HTTP 기반으로 서버의 "자원(Resource)"을 관리하는 아키텍처 스타일이다.
 *
 * 핵심 아이디어:
 * 서버의 데이터는 "Resource"로 표현되고
 * HTTP Method로 행동(Action)이 정의된다.
 *
 * Example
 *
 * Resource: users
 * Endpoint: /api/users
 *
 * GET    /users      → 조회
 * POST   /users      → 생성
 * PUT    /users/1    → 수정
 * DELETE /users/1    → 삭제
 *
 * 핵심 구성요소:
 *
 * - Resource (자원)
 * - Endpoint (URL)
 * - HTTP Method
 * - Status Code
 * - Representation (JSON)
 *
 */


/**
 * ======================================================
 * 1️⃣ Resource Concept
 * ======================================================
 *
 * REST에서는 "데이터 객체"를 Resource라고 부른다.
 *
 * 예:
 *
 * users
 * orders
 * products
 *
 * Resource는 URL로 표현된다.
 *
 * Example:
 *
 * /api/users
 * /api/orders
 */

const USERS_ENDPOINT = "/api/users";
const PRODUCTS_ENDPOINT = "/api/products";

console.log("Example REST resources:");
console.log(USERS_ENDPOINT);
console.log(PRODUCTS_ENDPOINT);


/**
 * ======================================================
 * 2️⃣ HTTP Methods
 * ======================================================
 *
 * REST에서는 HTTP Method가 "행동(Action)"을 의미한다.
 *
 * GET    → 데이터 조회
 * POST   → 데이터 생성
 * PUT    → 데이터 전체 수정
 * PATCH  → 데이터 부분 수정
 * DELETE → 데이터 삭제
 *
 * 즉 REST는
 *
 * Resource + HTTP Method
 *
 * 조합으로 동작한다.
 */

const httpMethods = {
  GET: "Read resource (데이터 조회)",
  POST: "Create resource (데이터 생성)",
  PUT: "Replace resource (전체 수정)",
  PATCH: "Update resource partially (부분 수정)",
  DELETE: "Remove resource (삭제)"
};

console.log("HTTP Methods:", httpMethods);


/**
 * ======================================================
 * 3️⃣ REST Endpoint Design
 * ======================================================
 *
 * REST API 설계에서 중요한 규칙:
 *
 * ❌ 동사 사용 금지
 * /getUsers
 * /createUser
 *
 * ✅ 명사 기반 설계
 * /users
 * /users/1
 *
 * Resource 중심 URL 설계가 핵심이다.
 */

function getUserEndpoint(userId) {

  // 특정 사용자 조회 endpoint 생성
  // Example: /api/users/10

  return `/api/users/${userId}`;

}

console.log("Example endpoint:", getUserEndpoint(10));


/**
 * ======================================================
 * 4️⃣ Example REST Call (Fetch)
 * ======================================================
 *
 * REST API는 대부분 JSON 형태로 데이터를 반환한다.
 *
 * Fetch API를 사용하여 데이터를 요청할 수 있다.
 *
 * 주요 단계:
 *
 * 1) 요청 보내기
 * 2) 상태코드 확인
 * 3) JSON 파싱
 * 4) 데이터 사용
 */

async function fetchUsers() {

  try {

    // REST API 호출
    const response = await fetch(
      "https://jsonplaceholder.typicode.com/users"
    );

    /**
     * fetch 특징
     *
     * fetch는 HTTP 오류(404,500)가 발생해도
     * 자동으로 reject하지 않는다.
     *
     * 따라서 반드시 response.ok 확인 필요
     */

    if (!response.ok) {

      throw new Error(`HTTP Error: ${response.status}`);

    }

    // JSON 데이터 변환
    const data = await response.json();

    console.log("Users:", data);

  } catch (error) {

    // 네트워크 오류 또는 HTTP 오류 처리
    console.error("API request failed:", error.message);

  }

}


/**
 * ======================================================
 * 5️⃣ REST Status Codes
 * ======================================================
 *
 * HTTP 상태코드는 서버 응답 상태를 의미한다.
 *
 * 200 OK
 * 요청 성공
 *
 * 201 Created
 * 데이터 생성 성공
 *
 * 204 No Content
 * 성공했지만 반환 데이터 없음
 *
 * 400 Bad Request
 * 잘못된 요청
 *
 * 401 Unauthorized
 * 인증 실패
 *
 * 404 Not Found
 * 리소스 없음
 *
 * 500 Server Error
 * 서버 오류
 */

const statusCodes = {
  200: "Success",
  201: "Created",
  204: "No Content",
  400: "Bad Request",
  401: "Unauthorized",
  404: "Not Found",
  500: "Internal Server Error"
};

console.log("Common HTTP Status Codes:", statusCodes);


/**
 * ======================================================
 * 6️⃣ REST Resource Pattern
 * ======================================================
 *
 * REST API 기본 패턴
 *
 * GET /users
 * → 사용자 목록 조회
 *
 * GET /users/1
 * → 특정 사용자 조회
 *
 * POST /users
 * → 사용자 생성
 *
 * PUT /users/1
 * → 사용자 전체 수정
 *
 * DELETE /users/1
 * → 사용자 삭제
 */

const restExamples = [
  "GET /users",
  "GET /users/1",
  "POST /users",
  "PUT /users/1",
  "DELETE /users/1"
];

console.log("REST examples:", restExamples);


/**
 * ======================================================
 * 7️⃣ REST Best Practices
 * ======================================================
 *
 * REST API 설계 모범 사례
 *
 * ✔ 명사 기반 endpoint 사용
 * ✔ 복수형 resource 사용
 * ✔ 일관된 URL 구조 유지
 * ✔ HTTP status code 정확히 사용
 * ✔ JSON 기반 응답
 */

function restBestPractices() {

  return [

    "Use nouns not verbs",
    "Use plural resources",
    "Use consistent naming",
    "Use HTTP status codes properly",
    "Keep API responses predictable"

  ];

}

console.log("REST Best Practices:", restBestPractices());


/**
 * ======================================================
 * Example Execution
 * ======================================================
 */

fetchUsers();