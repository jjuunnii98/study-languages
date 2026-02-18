/**
 * Day 31: Timeout & Abort (async/await)
 *
 * This file covers production-grade timeout and cancellation patterns
 * using AbortController + fetch.
 *
 * 핵심 목표:
 * - 네트워크 요청/비동기 작업에 "시간 제한(timeout)"을 적용한다.
 * - AbortController로 요청을 "취소(abort)"할 수 있게 만든다.
 * - race 기반 timeout vs AbortController 기반 timeout을 비교한다.
 *
 * ✅ 실무 포인트
 * - fetch는 기본적으로 timeout 옵션이 없다 → AbortController로 직접 구현한다.
 * - Promise.race는 "늦게 끝난 요청을 자동 취소"하지 못한다 → abort가 더 안전하다.
 */

/* ------------------------------------------
 * 0) Helpers
 * ------------------------------------------ */

/**
 * sleep(ms): ms 밀리초만큼 기다리는 Promise
 * - 네트워크 지연/타임아웃 테스트를 위해 자주 쓰는 유틸
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * isAbortError(err): abort로 인해 발생한 에러인지 판별
 * - 브라우저/Node 런타임마다 에러 shape이 조금 다를 수 있어 안전하게 처리
 */
function isAbortError(err) {
  return (
    err?.name === "AbortError" ||
    String(err?.message || "").toLowerCase().includes("aborted")
  );
}

/* ------------------------------------------
 * 1) Promise.race 기반 Timeout (주의: 취소는 안 됨)
 * ------------------------------------------ */

/**
 * fetchWithRaceTimeout(url, ms)
 *
 * - Promise.race로 timeout을 만들 수 있지만,
 *   timeout이 발생해도 실제 fetch 요청은 계속 진행될 수 있다.
 *
 * - 따라서 "응답만 무시하고 끝내는" 용도에는 쓸 수 있지만,
 *   리소스 사용/요청 낭비 관점에서는 불리할 수 있다.
 */
async function fetchWithRaceTimeout(url, ms) {
  const timeoutPromise = new Promise((_, reject) => {
    const id = setTimeout(() => {
      clearTimeout(id);
      reject(new Error(`Timeout after ${ms}ms (race)`));
    }, ms);
  });

  // ⚠️ race는 "첫 번째로 끝난 Promise 결과"만 선택한다.
  // ⚠️ timeout이 먼저 끝나도 fetch는 취소되지 않을 수 있다.
  return Promise.race([fetch(url), timeoutPromise]);
}

/* ------------------------------------------
 * 2) AbortController 기반 Timeout (실무 권장)
 * ------------------------------------------ */

/**
 * fetchWithAbortTimeout(url, { timeoutMs, options })
 *
 * - AbortController를 이용해 timeout 시점에 fetch를 "취소"한다.
 * - 실무에서 가장 많이 쓰는 패턴이다.
 *
 * options: fetch 옵션(method, headers, body 등)
 */
async function fetchWithAbortTimeout(url, { timeoutMs = 1000, options = {} } = {}) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(url, {
      ...options,
      signal: controller.signal,
    });

    // HTTP 에러도 명확히 처리(실무에서는 중요)
    if (!res.ok) {
      throw new Error(`HTTP ${res.status} ${res.statusText}`);
    }

    return res;
  } catch (err) {
    if (isAbortError(err)) {
      throw new Error(`Request aborted (timeout ${timeoutMs}ms)`);
    }
    throw err;
  } finally {
    // ✅ 타이머 누수 방지(필수)
    clearTimeout(timeoutId);
  }
}

/* ------------------------------------------
 * 3) AbortController로 "수동 취소" (사용자 액션)
 * ------------------------------------------ */

/**
 * abortableTask(ms, signal)
 *
 * - fetch가 아닌 "일반 비동기 작업"에서도 취소를 구현할 수 있다.
 * - signal이 abort되면 즉시 reject.
 */
function abortableTask(ms, signal) {
  return new Promise((resolve, reject) => {
    const id = setTimeout(() => resolve(`Done in ${ms}ms`), ms);

    // 이미 abort 상태면 즉시 종료
    if (signal?.aborted) {
      clearTimeout(id);
      return reject(new DOMException("Aborted", "AbortError"));
    }

    // abort 이벤트를 수신해 작업 취소
    signal?.addEventListener(
      "abort",
      () => {
        clearTimeout(id);
        reject(new DOMException("Aborted", "AbortError"));
      },
      { once: true }
    );
  });
}

/**
 * runAbortableExample(): 3000ms 작업을 시작하고, 800ms 후 수동 취소
 */
async function runAbortableExample() {
  const controller = new AbortController();

  // 0.8초 후 취소
  setTimeout(() => controller.abort(), 800);

  try {
    const result = await abortableTask(3000, controller.signal);
    console.log("[abortableTask] success:", result);
  } catch (err) {
    if (isAbortError(err)) {
      console.log("[abortableTask] aborted by user/timer");
      return;
    }
    console.log("[abortableTask] error:", err);
  }
}

/* ------------------------------------------
 * 4) Demo Runner
 * ------------------------------------------ */

async function main() {
  console.log("\n--- 1) race timeout demo (no actual cancel) ---");
  try {
    // httpbin 지연 엔드포인트: /delay/2 는 2초 지연
    const res = await fetchWithRaceTimeout("https://httpbin.org/delay/2", 500);
    console.log("race success:", res.status);
  } catch (err) {
    console.log("race failed:", err.message);
  }

  console.log("\n--- 2) abort timeout demo (recommended) ---");
  try {
    const res = await fetchWithAbortTimeout("https://httpbin.org/delay/2", {
      timeoutMs: 500,
    });
    console.log("abort success:", res.status);
  } catch (err) {
    console.log("abort failed:", err.message);
  }

  console.log("\n--- 3) manual abort for generic async task ---");
  await runAbortableExample();

  console.log("\n✅ Day 31 completed: timeout + abort patterns");
}

/**
 * Node에서 실행:
 * node 03_timeout_abort.js
 *
 * ⚠️ 만약 fetch가 없다면(Node 18 미만):
 * - node 버전 올리기 권장
 */
main();