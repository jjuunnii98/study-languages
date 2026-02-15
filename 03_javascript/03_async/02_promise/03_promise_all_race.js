/**
 * Day 28 — Promise.all / Promise.race (Concurrency Patterns)
 *
 * This file covers practical Promise concurrency tools:
 * - Promise.all        : run in parallel, fail-fast if any rejects
 * - Promise.race       : first settled wins (resolve OR reject)
 * - Promise.allSettled : wait for all, regardless of success/failure
 * - Promise.any        : first fulfilled wins (ignores rejects unless all fail)
 *
 * 이 파일은 Promise 병렬 처리 패턴을 다룬다.
 * 비동기 작업을 "동시에" 실행하고 결과를 합치는 설계는
 * API 요청, 데이터 로딩, 배치 처리에서 매우 자주 등장한다.
 */

/* =========================================================
   1️⃣ Helpers: delay + simulated async tasks
   ========================================================= */

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function task(name, ms, shouldFail = false) {
  return delay(ms).then(() => {
    if (shouldFail) throw new Error(`${name} failed`);
    return `${name} done (${ms}ms)`;
  });
}

/* =========================================================
   2️⃣ Promise.all — parallel + fail-fast
   =========================================================
   - 모든 Promise가 성공해야 resolve
   - 하나라도 reject 되면 즉시 reject (fail-fast)
   - "모두 필요"한 상황에 적합 (예: 여러 데이터 소스를 모두 받아야 페이지 렌더 가능)
*/

async function demoPromiseAll() {
  console.log("\n=== Promise.all (parallel, fail-fast) ===");

  try {
    const results = await Promise.all([
      task("A", 300),
      task("B", 500),
      task("C", 200),
    ]);

    console.log("✅ all results:", results);
  } catch (err) {
    console.error("❌ all error:", err.message);
  }

  // fail-fast 예시
  try {
    const results = await Promise.all([
      task("A", 300),
      task("B", 400, true), // 실패
      task("C", 200),
    ]);

    console.log("✅ all results:", results);
  } catch (err) {
    console.error("❌ all error (fail-fast):", err.message);
  }
}

/* =========================================================
   3️⃣ Promise.race — first settled wins (resolve OR reject)
   =========================================================
   - 가장 먼저 "끝난" Promise의 결과를 채택
   - resolve든 reject든 먼저 settled 된 것이 결과가 됨
   - 타임아웃, 가장 빠른 응답 채택 등에 활용
*/

async function demoPromiseRace() {
  console.log("\n=== Promise.race (first settled wins) ===");

  try {
    const winner = await Promise.race([
      task("Fast", 200),
      task("Slow", 600),
    ]);
    console.log("✅ race winner:", winner);
  } catch (err) {
    console.error("❌ race error:", err.message);
  }

  // 첫 번째로 reject가 발생하면 race는 reject가 된다
  try {
    const winner = await Promise.race([
      task("FailFast", 150, true), // reject가 가장 빠름
      task("SlowSuccess", 500),
    ]);
    console.log("✅ race winner:", winner);
  } catch (err) {
    console.error("❌ race error (first is reject):", err.message);
  }
}

/* =========================================================
   4️⃣ Timeout pattern with Promise.race
   =========================================================
   - 특정 시간 안에 작업이 끝나지 않으면 timeout reject
   - 실전에서 API 호출 timeout 구현 시 자주 사용
*/

function withTimeout(promise, timeoutMs) {
  const timeoutPromise = delay(timeoutMs).then(() => {
    throw new Error(`Timeout after ${timeoutMs}ms`);
  });

  return Promise.race([promise, timeoutPromise]);
}

async function demoTimeout() {
  console.log("\n=== Timeout with Promise.race ===");

  try {
    const result = await withTimeout(task("API", 300), 500);
    console.log("✅ within timeout:", result);
  } catch (err) {
    console.error("❌ timeout error:", err.message);
  }

  try {
    const result = await withTimeout(task("API", 800), 400);
    console.log("✅ within timeout:", result);
  } catch (err) {
    console.error("❌ timeout error:", err.message);
  }
}

/* =========================================================
   5️⃣ Promise.allSettled — wait all (no fail-fast)
   =========================================================
   - 모든 Promise가 끝날 때까지 기다림
   - 성공/실패 여부를 전부 수집
   - 배치 처리/리포팅/부분 성공 허용 시 유용
*/

async function demoAllSettled() {
  console.log("\n=== Promise.allSettled (collect all outcomes) ===");

  const results = await Promise.allSettled([
    task("A", 200),
    task("B", 300, true),
    task("C", 150),
  ]);

  console.log("✅ allSettled results:");
  results.forEach((r, idx) => {
    if (r.status === "fulfilled") {
      console.log(`  [${idx}] ✅`, r.value);
    } else {
      console.log(`  [${idx}] ❌`, r.reason.message);
    }
  });
}

/* =========================================================
   6️⃣ Promise.any — first fulfilled wins
   =========================================================
   - 가장 먼저 성공(resolve)한 Promise의 값을 반환
   - reject는 무시하고 계속 기다림
   - 모두 실패하면 AggregateError로 reject
   - "가장 빠른 성공"을 원할 때 적합 (예: 여러 미러 서버 중 성공하는 곳)
*/

async function demoAny() {
  console.log("\n=== Promise.any (first fulfilled wins) ===");

  try {
    const result = await Promise.any([
      task("Fail1", 150, true),
      task("Fail2", 200, true),
      task("Success", 350, false),
    ]);

    console.log("✅ any result:", result);
  } catch (err) {
    console.error("❌ any error:", err.message);
  }

  // 모두 실패하면 AggregateError
  try {
    const result = await Promise.any([
      task("Fail1", 150, true),
      task("Fail2", 200, true),
    ]);
    console.log("✅ any result:", result);
  } catch (err) {
    console.error("❌ any all failed:", err.name); // AggregateError
  }
}

/* =========================================================
   7️⃣ Summary (KR)
   =========================================================
   ✅ 언제 무엇을 쓰나?

   - Promise.all
     "모두 성공"이 필요할 때 (fail-fast)
     예: 페이지 렌더에 필요한 여러 데이터 소스를 모두 받아야 함

   - Promise.race
     "가장 먼저 끝난 것"이 필요할 때
     예: timeout 구현, 가장 빠른 응답 채택

   - Promise.allSettled
     "성공/실패 모두 수집"이 필요할 때
     예: 배치 작업 결과 리포트, 부분 성공 허용

   - Promise.any
     "가장 먼저 성공한 것"이 필요할 때
     예: 미러 서버 / fallback 전략

   다음 단계:
   - fetch API와 병렬 요청 (Promise.all)
   - async/await 기반 실전 네트워크 처리
*/

/* =========================================================
   8️⃣ Execute
   ========================================================= */

(async function main() {
  console.log("Start: Day 28 Promise concurrency patterns");

  await demoPromiseAll();
  await demoPromiseRace();
  await demoTimeout();
  await demoAllSettled();
  await demoAny();

  console.log("\nEnd: Day 28");
})();