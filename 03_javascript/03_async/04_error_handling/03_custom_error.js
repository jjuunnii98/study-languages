/**
 * Day 34 — Custom Error Architecture
 * 파일: 03_custom_error.js
 *
 * 목표:
 * - 기본 Error가 아닌 커스텀 에러 클래스를 설계한다.
 * - 에러에 statusCode, retryable 같은 메타정보를 포함한다.
 * - async/await 환경에서 구조적으로 에러를 throw / catch 한다.
 * - 중앙 집중 에러 핸들링 패턴을 구현한다.
 *
 * 핵심 개념:
 * - 에러는 "메시지 문자열"이 아니라 객체다.
 * - 운영 환경에서는 상태코드 + 재시도 가능 여부가 중요하다.
 */

// --------------------------------------------
// 1️⃣ 기본 커스텀 에러 클래스
// --------------------------------------------

class AppError extends Error {
  constructor(message, statusCode = 500, retryable = false) {
    super(message);

    // 에러 이름 명시
    this.name = this.constructor.name;

    // HTTP 상태 코드
    this.statusCode = statusCode;

    // 재시도 가능 여부
    this.retryable = retryable;

    // 스택 트레이스 유지 (Node.js 환경)
    Error.captureStackTrace(this, this.constructor);
  }
}

// --------------------------------------------
// 2️⃣ 구체적인 도메인 에러 확장
// --------------------------------------------

class ValidationError extends AppError {
  constructor(message) {
    super(message, 400, false);
  }
}

class NotFoundError extends AppError {
  constructor(message) {
    super(message, 404, false);
  }
}

class NetworkError extends AppError {
  constructor(message) {
    super(message, 503, true); // 재시도 가능
  }
}

// --------------------------------------------
// 3️⃣ 비동기 함수 예시
// --------------------------------------------

async function fetchUser(userId) {
  if (!userId) {
    throw new ValidationError("User ID is required.");
  }

  if (userId === 999) {
    throw new NotFoundError("User not found.");
  }

  if (userId === 500) {
    throw new NetworkError("Temporary network failure.");
  }

  // 정상 응답
  return { id: userId, name: "John Doe" };
}

// --------------------------------------------
// 4️⃣ 중앙 에러 핸들링 패턴
// --------------------------------------------

async function handleRequest(userId) {
  try {
    const user = await fetchUser(userId);
    console.log("User fetched successfully:", user);
  } catch (error) {
    handleError(error);
  }
}

function handleError(error) {
  if (error instanceof AppError) {
    console.error(`[${error.statusCode}] ${error.name}: ${error.message}`);

    if (error.retryable) {
      console.log("This error is retryable. Consider retry logic.");
    }
  } else {
    // 예상하지 못한 에러
    console.error("Unexpected error:", error);
  }
}

// --------------------------------------------
// 5️⃣ 테스트 실행
// --------------------------------------------

(async () => {
  await handleRequest();        // ValidationError
  await handleRequest(999);     // NotFoundError
  await handleRequest(500);     // NetworkError
  await handleRequest(1);       // 정상
})();