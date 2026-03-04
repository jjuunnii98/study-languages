/**
 * Day 42 — REST API Pagination / Sorting / Filtering
 * File: 03_javascript/04_api/02_rest_api/03_pagination_sort_filter.js
 *
 * This file demonstrates common REST API query patterns:
 *
 * - Pagination (페이지 나누기)
 * - Sorting (정렬)
 * - Filtering (조건 검색)
 *
 * 대부분의 실제 REST API는 다음 형태의 query parameter를 사용한다.
 *
 * Example:
 *
 * GET /users?page=1&limit=10
 * GET /users?sort=name&order=asc
 * GET /users?role=admin
 *
 * Query Parameter는 URL 뒤에 붙는다.
 *
 * Example:
 * /users?page=2&limit=20
 *
 */


/**
 * ======================================================
 * Base API URL
 * ======================================================
 */

const BASE_URL = "https://jsonplaceholder.typicode.com/posts";


/**
 * ======================================================
 * 1️⃣ Pagination
 * ======================================================
 *
 * Pagination은 데이터를 여러 페이지로 나누는 방식이다.
 *
 * 이유:
 *
 * 데이터가 많을 때
 * 한번에 모든 데이터를 가져오면
 *
 * - 네트워크 부담 증가
 * - 응답 속도 저하
 * - 메모리 사용 증가
 *
 * 따라서 API는 보통 다음 query parameter를 제공한다.
 *
 * page
 * limit
 *
 * Example:
 *
 * GET /posts?page=1&limit=10
 */

async function fetchPostsPagination(page = 1, limit = 5) {

  try {

    const url = `${BASE_URL}?_page=${page}&_limit=${limit}`;

    console.log("Pagination URL:", url);

    const response = await fetch(url);

    if (!response.ok) {

      throw new Error(`HTTP Error: ${response.status}`);

    }

    const posts = await response.json();

    console.log(`Page ${page} Posts:`, posts);

  } catch (error) {

    console.error("Pagination request failed:", error.message);

  }

}



/**
 * ======================================================
 * 2️⃣ Sorting
 * ======================================================
 *
 * Sorting은 데이터를 특정 기준으로 정렬하는 기능이다.
 *
 * Example:
 *
 * GET /posts?sort=id&order=desc
 *
 * jsonplaceholder에서는 다음 방식 사용:
 *
 * _sort
 * _order
 */

async function fetchSortedPosts(sortField = "id", order = "desc") {

  try {

    const url = `${BASE_URL}?_sort=${sortField}&_order=${order}`;

    console.log("Sorting URL:", url);

    const response = await fetch(url);

    if (!response.ok) {

      throw new Error(`HTTP Error: ${response.status}`);

    }

    const posts = await response.json();

    console.log("Sorted posts:", posts);

  } catch (error) {

    console.error("Sorting request failed:", error.message);

  }

}



/**
 * ======================================================
 * 3️⃣ Filtering
 * ======================================================
 *
 * Filtering은 특정 조건의 데이터만 조회하는 방식이다.
 *
 * Example:
 *
 * GET /posts?userId=1
 *
 * 즉 특정 필드 값을 기준으로 데이터를 제한한다.
 */

async function fetchFilteredPosts(userId) {

  try {

    const url = `${BASE_URL}?userId=${userId}`;

    console.log("Filtering URL:", url);

    const response = await fetch(url);

    if (!response.ok) {

      throw new Error(`HTTP Error: ${response.status}`);

    }

    const posts = await response.json();

    console.log(`Posts by user ${userId}:`, posts);

  } catch (error) {

    console.error("Filtering request failed:", error.message);

  }

}



/**
 * ======================================================
 * 4️⃣ Combined Query
 * ======================================================
 *
 * 실제 REST API에서는
 *
 * Pagination + Sorting + Filtering
 *
 * 을 동시에 사용하는 경우가 많다.
 *
 * Example:
 *
 * GET /posts?userId=1&_page=1&_limit=5&_sort=id&_order=desc
 */

async function fetchAdvancedQuery(userId, page = 1, limit = 5) {

  try {

    const url =
      `${BASE_URL}?userId=${userId}&_page=${page}&_limit=${limit}&_sort=id&_order=desc`;

    console.log("Advanced query URL:", url);

    const response = await fetch(url);

    if (!response.ok) {

      throw new Error(`HTTP Error: ${response.status}`);

    }

    const posts = await response.json();

    console.log("Advanced query result:", posts);

  } catch (error) {

    console.error("Advanced query failed:", error.message);

  }

}



/**
 * ======================================================
 * Example Execution
 * ======================================================
 */

async function runExamples() {

  // Pagination
  await fetchPostsPagination(1, 5);

  // Sorting
  await fetchSortedPosts("id", "desc");

  // Filtering
  await fetchFilteredPosts(1);

  // Combined Query
  await fetchAdvancedQuery(1, 1, 5);

}

runExamples();