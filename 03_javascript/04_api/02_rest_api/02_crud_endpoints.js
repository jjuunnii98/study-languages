/**
 * Day 41 — REST CRUD Endpoints
 * File: 03_javascript/04_api/02_rest_api/02_crud_endpoints.js
 *
 * This file demonstrates how REST APIs implement
 * CRUD operations using HTTP methods.
 *
 * ---------------------------------------------------------
 * CRUD 의미
 * ---------------------------------------------------------
 *
 * Create  → POST
 * Read    → GET
 * Update  → PUT / PATCH
 * Delete  → DELETE
 *
 * REST에서는 CRUD 작업을 HTTP Method로 표현한다.
 *
 * Example:
 *
 * GET    /users
 * GET    /users/1
 * POST   /users
 * PUT    /users/1
 * DELETE /users/1
 *
 */


const BASE_URL = "https://jsonplaceholder.typicode.com/users";


/**
 * ======================================================
 * 1️⃣ READ — GET
 * ======================================================
 *
 * 데이터 조회
 *
 * GET /users
 *
 * 서버에서 리소스를 조회한다.
 */

async function getUsers() {

  try {

    const response = await fetch(BASE_URL);

    // fetch는 HTTP 오류를 자동 throw 하지 않기 때문에
    // 반드시 response.ok 체크 필요

    if (!response.ok) {

      throw new Error(`HTTP Error: ${response.status}`);

    }

    const users = await response.json();

    console.log("Users list:", users);

  } catch (error) {

    console.error("GET request failed:", error.message);

  }

}



/**
 * ======================================================
 * 2️⃣ READ — GET Single Resource
 * ======================================================
 *
 * 특정 사용자 조회
 *
 * GET /users/1
 */

async function getUserById(userId) {

  try {

    const response = await fetch(`${BASE_URL}/${userId}`);

    if (!response.ok) {

      throw new Error(`HTTP Error: ${response.status}`);

    }

    const user = await response.json();

    console.log("Single user:", user);

  } catch (error) {

    console.error("GET by ID failed:", error.message);

  }

}



/**
 * ======================================================
 * 3️⃣ CREATE — POST
 * ======================================================
 *
 * 데이터 생성
 *
 * POST /users
 *
 * JSON body를 서버에 전달해야 한다.
 */

async function createUser(userData) {

  try {

    const response = await fetch(BASE_URL, {

      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify(userData)

    });

    if (!response.ok) {

      throw new Error(`HTTP Error: ${response.status}`);

    }

    const createdUser = await response.json();

    console.log("Created user:", createdUser);

  } catch (error) {

    console.error("POST request failed:", error.message);

  }

}



/**
 * ======================================================
 * 4️⃣ UPDATE — PUT
 * ======================================================
 *
 * 데이터 전체 수정
 *
 * PUT /users/1
 *
 * PUT은 리소스를 "전체 교체"하는 의미이다.
 */

async function updateUser(userId, updatedData) {

  try {

    const response = await fetch(`${BASE_URL}/${userId}`, {

      method: "PUT",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify(updatedData)

    });

    if (!response.ok) {

      throw new Error(`HTTP Error: ${response.status}`);

    }

    const updatedUser = await response.json();

    console.log("Updated user:", updatedUser);

  } catch (error) {

    console.error("PUT request failed:", error.message);

  }

}



/**
 * ======================================================
 * 5️⃣ DELETE
 * ======================================================
 *
 * 리소스 삭제
 *
 * DELETE /users/1
 */

async function deleteUser(userId) {

  try {

    const response = await fetch(`${BASE_URL}/${userId}`, {

      method: "DELETE"

    });

    if (!response.ok) {

      throw new Error(`HTTP Error: ${response.status}`);

    }

    console.log(`User ${userId} deleted successfully`);

  } catch (error) {

    console.error("DELETE request failed:", error.message);

  }

}



/**
 * ======================================================
 * Example Execution
 * ======================================================
 *
 * 실제 테스트 실행
 */

async function runExamples() {

  await getUsers();

  await getUserById(1);

  await createUser({
    name: "John Doe",
    email: "john@example.com"
  });

  await updateUser(1, {
    name: "Updated User",
    email: "updated@example.com"
  });

  await deleteUser(1);

}


runExamples();