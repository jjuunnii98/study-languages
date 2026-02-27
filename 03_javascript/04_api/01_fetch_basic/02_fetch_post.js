/*
Day 36 — Fetch POST Pattern (Production-Oriented)

📌 목표
- fetch 기반 POST 요청 구조 이해
- JSON body 전송 방식 학습
- HTTP 상태 코드 검증 로직 구현
- AbortController 기반 timeout 처리
- 실무에서 재사용 가능한 API 함수 설계

📌 핵심 포인트
- fetch는 404/500에서도 자동으로 reject하지 않음 → response.ok 직접 검사 필요
- JSON 전송 시 반드시 JSON.stringify 필요
- timeout은 AbortController로 직접 구현
*/

const API_URL = "https://jsonplaceholder.typicode.com/posts";

/**
 * POST 요청을 수행하는 재사용 가능한 함수
 *
 * @param {Object} payload - 서버로 전송할 JSON 객체
 * @param {number} timeoutMs - 요청 제한 시간 (밀리초)
 * @returns {Promise<Object>} - 서버 응답 JSON
 */
async function postData(payload, timeoutMs = 5000) {
  // ⏱ timeout 처리를 위한 AbortController 생성
  const controller = new AbortController();

  // 일정 시간 이후 요청을 강제로 중단
  const timeoutId = setTimeout(() => {
    controller.abort(); // abort 발생 시 fetch는 AbortError throw
  }, timeoutMs);

  try {
    // 📡 fetch POST 요청 실행
    const response = await fetch(API_URL, {
      method: "POST", // HTTP 메서드 지정
      headers: {
        "Content-Type": "application/json", // JSON 전송 명시
      },
      body: JSON.stringify(payload), // JS 객체 → JSON 문자열로 직렬화
      signal: controller.signal, // AbortController 연결
    });

    // 🚨 fetch는 HTTP 에러(404, 500)를 자동 reject하지 않음
    // 따라서 반드시 response.ok 확인 필요
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    // 📥 응답 데이터를 JSON으로 파싱
    const data = await response.json();

    return data; // 성공 시 결과 반환

  } catch (error) {
    // ⛔ timeout으로 인한 abort인지 확인
    if (error.name === "AbortError") {
      console.error("요청이 timeout으로 중단되었습니다.");
      throw new Error("Request Timeout");
    }

    // 일반 네트워크 오류 또는 직접 throw한 에러
    console.error("POST 요청 중 오류 발생:", error.message);
    throw error; // 상위 호출부로 에러 전파

  } finally {
    // 🧹 반드시 타이머 정리 (메모리 누수 방지)
    clearTimeout(timeoutId);
  }
}

/* ===========================
   실행 예제
=========================== */

async function runExample() {
  // 📦 서버로 보낼 데이터 객체
  const newPost = {
    title: "Snowflake Schema",
    body: "Normalized dimension modeling example",
    userId: 1,
  };

  try {
    // POST 요청 실행
    const result = await postData(newPost, 3000);

    // 성공 결과 출력
    console.log("POST 성공:", result);

  } catch (err) {
    // 실패 처리
    console.error("POST 실패:", err.message);
  }
}

// 실제 실행
runExample();