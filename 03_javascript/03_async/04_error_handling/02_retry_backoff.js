/*
====================================================================
Day 33 — Retry with Exponential Backoff
Module: 03_async / 04_error_handling

📌 목표
1) 일시적 실패(transient error) 처리 전략 이해
2) Retry 로직 구현
3) Exponential Backoff 설계
4) 최대 재시도 횟수 제어
5) 실무형 안정성 패턴 학습

이 파일은 네트워크/API 호출 안정성을 위한
재시도 전략 설계 예제입니다.
====================================================================
*/


/* ================================================================
1️⃣ 유틸 함수 — 대기(delay) 함수
================================================================ */

/*
Promise 기반 delay 함수
지정한 시간(ms)만큼 대기 후 resolve
*/

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}



/* ================================================================
2️⃣ 실패를 랜덤으로 발생시키는 Mock API
================================================================ */

/*
70% 확률로 실패, 30% 확률로 성공
실제 환경에서는 네트워크 오류, 500 에러 등을 가정
*/

async function unstableApi() {
  const random = Math.random();

  if (random < 0.7) {
    throw new Error("일시적 서버 오류 발생");
  }

  return "API 호출 성공";
}



/* ================================================================
3️⃣ Retry + Exponential Backoff 구현
================================================================ */

/*
retryWithBackoff 함수 설명:

- fn: 실행할 async 함수
- maxRetries: 최대 재시도 횟수
- baseDelay: 기본 대기 시간(ms)

Backoff 전략:
delay = baseDelay * 2^attempt

예:
1번째 실패 → 500ms
2번째 실패 → 1000ms
3번째 실패 → 2000ms
*/

async function retryWithBackoff(fn, maxRetries = 3, baseDelay = 500) {
  let attempt = 0;

  while (attempt <= maxRetries) {
    try {
      console.log(`🔁 시도 ${attempt + 1}...`);

      const result = await fn();
      console.log("✔ 성공:", result);
      return result;

    } catch (error) {
      console.error(`❌ 실패 (시도 ${attempt + 1}):`, error.message);

      if (attempt === maxRetries) {
        console.error("🚨 최대 재시도 초과. 종료.");
        throw error;
      }

      const backoffTime = baseDelay * Math.pow(2, attempt);
      console.log(`⏳ ${backoffTime}ms 후 재시도...\n`);

      await delay(backoffTime);
      attempt++;
    }
  }
}



/* ================================================================
4️⃣ 실행 테스트
================================================================ */

(async () => {
  try {
    await retryWithBackoff(unstableApi, 3, 500);
  } catch (error) {
    console.error("최종 실패:", error.message);
  }
})();



/*
====================================================================
📌 핵심 정리

1. Retry는 일시적 오류(transient failure)에만 사용해야 한다.
2. 무한 재시도는 시스템을 더 악화시킬 수 있다.
3. Exponential Backoff는 서버 과부하를 방지한다.
4. maxRetries를 반드시 설정해야 한다.
5. 실무에서는 jitter(랜덤 지연)를 추가해 동시 재시도를 분산한다.

이 패턴은 운영 환경에서 API 안정성을 확보하는 핵심 전략이다.
====================================================================
*/