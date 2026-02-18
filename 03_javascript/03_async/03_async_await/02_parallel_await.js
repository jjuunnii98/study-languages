/**
 * Day 30: Parallel Await (JavaScript Async — async/await)
 *
 * Goal:
 * - Understand when and how to run async tasks in parallel
 * - Compare sequential vs parallel execution time
 * - Learn production patterns:
 *   - Promise.all (fail-fast)
 *   - Promise.allSettled (partial success)
 *   - Concurrency limiting (avoid API rate limits / resource spikes)
 *
 * 목표(한국어):
 * - 비동기 작업을 병렬로 실행해야 하는 상황/방법을 이해한다.
 * - 순차 실행과 병렬 실행의 시간 차이를 비교한다.
 * - 실무 패턴을 익힌다:
 *   - Promise.all(하나라도 실패하면 전체 실패 = fail-fast)
 *   - Promise.allSettled(부분 성공 허용)
 *   - 동시성 제한(concurrency limit)으로 안전하게 병렬 처리
 */

// ---------------------------------------------------------
// 0) Utilities: delay + fake async task
// ---------------------------------------------------------

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * 비동기 작업(예: API 호출)을 흉내내는 함수
 * - name: 작업 이름
 * - ms: 소요 시간
 * - failRate: 실패 확률(0~1)
 */
async function fakeTask(name, ms, failRate = 0) {
  await delay(ms);

  // failRate 확률로 실패 시뮬레이션
  if (Math.random() < failRate) {
    throw new Error(`Task failed: ${name}`);
  }

  return { name, ms, ok: true, ts: new Date().toISOString() };
}

/**
 * 실행 시간 측정 유틸
 * - label: 로그 라벨
 * - fn: async function
 */
async function measure(label, fn) {
  const start = Date.now();
  try {
    const result = await fn();
    const elapsed = Date.now() - start;
    console.log(`✅ ${label} took ${elapsed}ms`);
    return { ok: true, elapsed, result };
  } catch (err) {
    const elapsed = Date.now() - start;
    console.error(`❌ ${label} failed after ${elapsed}ms ->`, err.message);
    return { ok: false, elapsed, error: err };
  }
}

// ---------------------------------------------------------
// 1) Sequential vs Parallel: 속도 차이 체감
// ---------------------------------------------------------

async function sequentialRun() {
  // 순차 실행: 작업이 서로 의존하거나, 순서가 중요할 때 사용
  const a = await fakeTask("A", 300);
  const b = await fakeTask("B", 300);
  const c = await fakeTask("C", 300);
  return [a, b, c];
}

async function parallelRunAll() {
  // 병렬 실행: 서로 독립인 작업이면 Promise.all이 더 효율적
  const tasks = [
    fakeTask("A", 300),
    fakeTask("B", 300),
    fakeTask("C", 300),
  ];
  return Promise.all(tasks);
}

// ---------------------------------------------------------
// 2) Promise.all: fail-fast 전략 (모두 성공해야 의미 있을 때)
// ---------------------------------------------------------

async function parallelFailFast() {
  // 하나라도 실패하면 전체 reject (fail-fast)
  // 예: "유저 + 주문 + 프로필" 모두 필요할 때
  const tasks = [
    fakeTask("User", 250, 0.1),
    fakeTask("Orders", 250, 0.1),
    fakeTask("Profile", 250, 0.1),
  ];

  const results = await Promise.all(tasks); // 여기서 실패하면 throw
  return results;
}

// ---------------------------------------------------------
// 3) Promise.allSettled: 부분 성공 허용 (대체 가능할 때)
// ---------------------------------------------------------

async function parallelPartialSuccess() {
  // 일부 실패해도 결과를 모아서 처리 가능
  // 예: 추천 API 실패해도 메인 화면은 보여줘야 할 때
  const tasks = [
    fakeTask("MainData", 200, 0.05),
    fakeTask("Recommendation", 200, 0.4),
    fakeTask("Ads", 200, 0.2),
  ];

  const settled = await Promise.allSettled(tasks);

  const success = settled
    .filter((r) => r.status === "fulfilled")
    .map((r) => r.value);

  const failed = settled
    .filter((r) => r.status === "rejected")
    .map((r) => r.reason.message);

  return { success, failed };
}

// ---------------------------------------------------------
// 4) Concurrency Limit: 동시성 제한 병렬 처리 (실무 필수)
// ---------------------------------------------------------

/**
 * 동시성 제한 실행기 (concurrency pool)
 *
 * tasks: () => Promise 형태의 함수 배열
 * limit: 동시에 실행할 최대 개수
 *
 * 왜 필요?
 * - 외부 API rate limit 방지
 * - DB 커넥션 폭주 방지
 * - CPU/메모리 스파이크 방지
 */
async function runWithConcurrencyLimit(tasks, limit = 3) {
  const results = [];
  let nextIndex = 0;

  // 워커(worker) 하나가 tasks를 순서대로 가져가 수행
  async function worker(workerId) {
    while (nextIndex < tasks.length) {
      const current = nextIndex;
      nextIndex += 1;

      try {
        const value = await tasks[current]();
        results[current] = { status: "fulfilled", value, workerId };
      } catch (err) {
        results[current] = { status: "rejected", reason: err, workerId };
      }
    }
  }

  // limit 개수만큼 워커를 병렬로 실행
  const workers = Array.from({ length: limit }, (_, i) => worker(i + 1));
  await Promise.all(workers);

  return results;
}

async function concurrencyLimitExample() {
  // 10개 작업을 만들고, 동시에 3개만 실행
  const tasks = Array.from({ length: 10 }, (_, i) => {
    const idx = i + 1;
    const ms = 100 + (idx % 3) * 100; // 100/200/300ms 변동
    const failRate = 0.15;           // 약간의 실패도 섞기
    return () => fakeTask(`Task-${idx}`, ms, failRate);
  });

  const results = await runWithConcurrencyLimit(tasks, 3);

  const summary = results.map((r, i) => {
    const name = `Task-${i + 1}`;
    if (r.status === "fulfilled") {
      return { name, status: "ok", worker: r.workerId };
    }
    return { name, status: "fail", worker: r.workerId, error: r.reason.message };
  });

  return summary;
}

// ---------------------------------------------------------
// ✅ Run Demo
// ---------------------------------------------------------

(async function main() {
  console.log("\n=== Day 30: Parallel Await Demo ===\n");

  await measure("Sequential Run (A->B->C)", sequentialRun);
  await measure("Parallel Run Promise.all (A,B,C)", parallelRunAll);

  await measure("Parallel Fail-fast (Promise.all)", parallelFailFast);
  await measure("Parallel Partial Success (allSettled)", parallelPartialSuccess);

  await measure("Concurrency Limit (pool=3)", concurrencyLimitExample);

  console.log("\n✅ Day 30 complete.\n");
})();

/**
 * Day 30 Summary
 * - 순차 실행: 의존성/순서 필요할 때
 * - 병렬 실행: 독립 작업이면 Promise.all로 성능 개선
 * - fail-fast: 모두 필요할 때 (Promise.all)
 * - partial success: 일부 실패 허용 (Promise.allSettled)
 * - concurrency limit: 실무에서 안전한 병렬 처리의 핵심
 */