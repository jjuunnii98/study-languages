/**
 * Day 29: Async/Await Basics (JavaScript Async — Step 3)
 *
 * This file introduces async/await as the modern syntax layer
 * built on top of Promises.
 *
 * 핵심:
 * - async 함수는 항상 Promise를 반환한다.
 * - await는 Promise가 완료될 때까지 "해당 함수 내부" 실행을 잠시 멈춘다.
 * - try/catch로 에러를 중앙에서 처리할 수 있어 구조가 깔끔해진다.
 *
 * NOTE:
 * - await는 "블로킹"이 아니라 "비동기 대기"이며,
 *   이벤트 루프는 다른 작업을 계속 처리한다.
 */

// ---------------------------------------------
// 0) Utilities: delay + fake async fetch
// ---------------------------------------------

/**
 * 지정한 ms 뒤에 resolve되는 Promise를 반환한다.
 * (비동기 흐름을 테스트할 때 자주 쓰는 유틸)
 */
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * 서버 호출을 흉내내는 fake API
 * - payload를 반환하거나
 * - fail=true면 에러를 던진다
 */
async function fakeFetch(endpoint, { ms = 300, fail = false } = {}) {
  await delay(ms);

  if (fail) {
    // 실무에서는 Error 객체로 던지는 게 표준 (stack trace 보존)
    throw new Error(`Request failed: ${endpoint}`);
  }

  return {
    endpoint,
    ok: true,
    ts: new Date().toISOString(),
  };
}

// ---------------------------------------------
// 1) async 함수의 반환값: 항상 Promise
// ---------------------------------------------

async function returnsPromise() {
  // async 함수 내부에서 값을 return하면 "자동으로 Promise.resolve(value)"가 된다.
  return 123;
}

returnsPromise().then((v) => console.log("[1] returnsPromise:", v));

// ---------------------------------------------
// 2) await 기본: 순차 실행 (sequential)
// ---------------------------------------------

/**
 * 순차적으로 실행한다.
 * 장점: 의존성이 있는 단계(예: 토큰 발급 → 데이터 요청)에 적합
 * 단점: 독립 작업이면 느려질 수 있음
 */
async function sequentialExample() {
  console.log("\n[2] sequential start");

  const a = await fakeFetch("/api/a", { ms: 300 });
  console.log("[2] a:", a.endpoint);

  const b = await fakeFetch("/api/b", { ms: 300 });
  console.log("[2] b:", b.endpoint);

  console.log("[2] sequential end");
}

sequentialExample();

// ---------------------------------------------
// 3) 에러 처리: try/catch/finally
// ---------------------------------------------

/**
 * try/catch는 async/await의 핵심 장점 중 하나:
 * - 에러 흐름을 "정상 흐름"과 같은 레벨에서 통제할 수 있다.
 */
async function errorHandlingExample() {
  console.log("\n[3] error handling start");

  try {
    const okRes = await fakeFetch("/api/ok", { ms: 200 });
    console.log("[3] ok:", okRes.ok);

    // 실패를 강제로 발생시켜보자
    const badRes = await fakeFetch("/api/fail", { ms: 200, fail: true });
    console.log("[3] should not reach:", badRes);
  } catch (err) {
    // 실무에서는 err.message, err.stack을 함께 기록하는 패턴이 일반적
    console.error("[3] caught error:", err.message);
  } finally {
    // 항상 실행: 로깅/리소스 정리/로딩 스피너 종료 등
    console.log("[3] finally: cleanup or finalize UI state");
  }

  console.log("[3] error handling end");
}

errorHandlingExample();

// ---------------------------------------------
// 4) 병렬 처리: Promise.all with await
// ---------------------------------------------

/**
 * 독립 작업은 병렬로 실행하는 것이 효율적이다.
 * Promise.all은 "모두 성공해야 성공" (fail-fast)
 */
async function parallelExample() {
  console.log("\n[4] parallel start");

  const tasks = [
    fakeFetch("/api/user", { ms: 300 }),
    fakeFetch("/api/orders", { ms: 300 }),
    fakeFetch("/api/profile", { ms: 300 }),
  ];

  // await Promise.all(...)로 병렬 결과를 한번에 받는다
  const [user, orders, profile] = await Promise.all(tasks);

  console.log("[4] user:", user.endpoint);
  console.log("[4] orders:", orders.endpoint);
  console.log("[4] profile:", profile.endpoint);

  console.log("[4] parallel end");
}

parallelExample();

// ---------------------------------------------
// 5) 실패 전략: allSettled로 부분 성공 허용
// ---------------------------------------------

/**
 * 일부 실패를 허용하고 결과를 수집해야 하는 경우:
 * Promise.allSettled 사용
 */
async function allSettledExample() {
  console.log("\n[5] allSettled start");

  const results = await Promise.allSettled([
    fakeFetch("/api/a", { ms: 150 }),
    fakeFetch("/api/b", { ms: 150, fail: true }),
    fakeFetch("/api/c", { ms: 150 }),
  ]);

  // 결과는 { status: "fulfilled", value } 또는 { status: "rejected", reason }
  const summary = results.map((r) =>
    r.status === "fulfilled"
      ? { status: r.status, endpoint: r.value.endpoint }
      : { status: r.status, error: r.reason.message }
  );

  console.log("[5] summary:", summary);
  console.log("[5] allSettled end");
}

allSettledExample();

// ---------------------------------------------
// 6) Timeout 패턴 (실무 필수 감각)
// ---------------------------------------------

/**
 * Promise에 "시간 제한"을 걸고 싶을 때 흔히 쓰는 패턴:
 * - Promise.race로 timeout Promise와 경쟁시킨다.
 */
function withTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error(`Timeout after ${ms}ms`)), ms)
  );

  return Promise.race([promise, timeout]);
}

async function timeoutExample() {
  console.log("\n[6] timeout start");

  try {
    // 500ms 걸리는 작업에 200ms 타임아웃을 걸면 실패한다.
    const res = await withTimeout(fakeFetch("/api/slow", { ms: 500 }), 200);
    console.log("[6] res:", res);
  } catch (err) {
    console.error("[6] timeout error:", err.message);
  }

  console.log("[6] timeout end");
}

timeoutExample();

// ---------------------------------------------
// ✅ Day 29 Summary
// ---------------------------------------------
/**
 * - async 함수는 항상 Promise를 반환한다.
 * - await는 Promise 완료를 기다리되, 이벤트루프를 막지 않는다.
 * - try/catch로 에러를 중앙에서 처리할 수 있다.
 * - 독립 작업은 Promise.all로 병렬 처리한다.
 * - 부분 성공 허용은 Promise.allSettled를 쓴다.
 * - 실무에서는 timeout/재시도 같은 운영 패턴을 반드시 고려한다.
 */