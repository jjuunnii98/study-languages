/**
 * Day 35 — Fetch API (GET Request)
 * 파일: 01_fetch_get.js
 *
 * 목표:
 * - fetch 기반 GET 요청 구조 이해
 * - HTTP 상태코드 검증
 * - 네트워크 오류와 HTTP 오류 구분
 * - JSON 파싱 안정성 확보
 * - AbortController를 통한 타임아웃 처리
 * - 재사용 가능한 GET 헬퍼 함수 설계
 */

/**
 * 재사용 가능한 GET 요청 함수
 *
 * @param {string} url - 요청할 API 주소
 * @param {number} timeoutMs - 타임아웃(ms)
 */
async function fetchGet(url, timeoutMs = 5000) {
  // AbortController를 통한 타임아웃 제어
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      signal: controller.signal,
    });

    // HTTP 상태코드 검사
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    // JSON 파싱 (응답이 JSON이라는 가정)
    const data = await response.json();
    return data;

  } catch (error) {
    // 네트워크 에러 / Abort 구분
    if (error.name === "AbortError") {
      console.error("Request timed out.");
      throw new Error("TimeoutError");
    }

    console.error("Fetch failed:", error.message);
    throw error;

  } finally {
    clearTimeout(timeoutId);
  }
}


/**
 * 실제 실행 예시
 */
async function runExample() {
  const url = "https://jsonplaceholder.typicode.com/posts/1";

  try {
    const data = await fetchGet(url, 3000);
    console.log("Success:", data);
  } catch (error) {
    console.error("Request failed:", error.message);
  }
}

// 실행
runExample();