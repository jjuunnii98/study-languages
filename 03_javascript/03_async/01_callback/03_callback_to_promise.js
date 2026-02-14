/**
 * Day 25 — Refactor: Callback → Promise
 *
 * This file refactors the Day 24 callback pipeline into Promises.
 * It demonstrates:
 * 1) Promisifying callback-based functions
 * 2) Promise chaining (.then/.catch)
 * 3) async/await (cleaner syntax)
 * 4) Centralized error handling
 *
 * 이 파일은 Day 24의 콜백 기반 비동기 파이프라인을 Promise로 리팩토링한다.
 * - 콜백을 Promise로 변환(promisify)
 * - then/catch 체이닝
 * - async/await로 더 읽기 쉬운 코드 구성
 * - 에러 처리를 한 곳으로 모으는 구조
 */

/* =========================================================
   1️⃣ Callback-style async functions (error-first)
   =========================================================
   callback(err, result) 스타일 (Node.js 관례)
*/

function getUser(userId, cb) {
  setTimeout(() => {
    if (!userId) return cb(new Error("userId is required"), null);
    cb(null, { id: userId, name: "Junyeong" });
  }, 300);
}

function getOrders(userId, cb) {
  setTimeout(() => {
    if (Math.random() < 0.05) return cb(new Error("Orders service timeout"), null);
    cb(null, [
      { orderId: 101, userId, amount: 39.9 },
      { orderId: 102, userId, amount: 12.5 },
    ]);
  }, 300);
}

function getPaymentStatus(orderId, cb) {
  setTimeout(() => {
    if (!orderId) return cb(new Error("orderId is required"), null);
    cb(null, { orderId, paid: true, method: "card" });
  }, 300);
}

function sendEmail(user, paymentInfo, cb) {
  setTimeout(() => {
    if (Math.random() < 0.05) return cb(new Error("Email service failed"), null);
    cb(null, `Email sent to ${user.name} for order ${paymentInfo.orderId}`);
  }, 300);
}

/* =========================================================
   2️⃣ Promisify helper
   =========================================================
   callback 기반 함수를 Promise로 감싸는 유틸 함수.
   - 성공: resolve(result)
   - 실패: reject(error)

   실무에서는 util.promisify(Node.js) 또는 직접 래핑해서 사용한다.
*/

function promisify(fn) {
  return (...args) =>
    new Promise((resolve, reject) => {
      fn(...args, (err, result) => {
        if (err) reject(err);
        else resolve(result);
      });
    });
}

/* callback 함수들을 Promise 버전으로 변환 */
const getUserAsync = promisify(getUser);
const getOrdersAsync = promisify(getOrders);
const getPaymentStatusAsync = promisify(getPaymentStatus);

// sendEmail은 인자가 2개(user, paymentInfo)라 promisify로 바로 감싸면 됨
const sendEmailAsync = promisify(sendEmail);

/* =========================================================
   3️⃣ Promise chaining version
   =========================================================
   then() 체이닝으로 비동기 흐름을 "평평하게(flat)" 만든다.
   콜백헬의 깊은 중첩이 사라지고, 로직 흐름이 위→아래로 읽힌다.
*/

function runWithPromiseChain(userId) {
  console.log("\n=== Run: Promise chaining (.then/.catch) ===");

  let cachedUser;
  let latestOrder;

  return getUserAsync(userId)
    .then((user) => {
      cachedUser = user;
      console.log("✅ user:", user);
      return getOrdersAsync(user.id);
    })
    .then((orders) => {
      console.log("✅ orders:", orders);

      latestOrder = orders[orders.length - 1];
      if (!latestOrder) throw new Error("no orders found");
      return getPaymentStatusAsync(latestOrder.orderId);
    })
    .then((payment) => {
      console.log("✅ payment:", payment);
      return sendEmailAsync(cachedUser, payment);
    })
    .then((message) => {
      console.log("✅", message);
      console.log("Done: Promise chaining");
    })
    .catch((err) => {
      // ✅ 중앙집중 에러 처리 (중간중간 if(err) 반복 제거)
      console.error("❌ Error:", err.message);
    });
}

/* =========================================================
   4️⃣ async/await version (recommended for readability)
   =========================================================
   async/await는 Promise를 더 읽기 쉽게 만든 문법적 설탕(syntax sugar)이다.
   try/catch로 에러를 한 번에 처리한다.
*/

async function runWithAsyncAwait(userId) {
  console.log("\n=== Run: async/await ===");

  try {
    const user = await getUserAsync(userId);
    console.log("✅ user:", user);

    const orders = await getOrdersAsync(user.id);
    console.log("✅ orders:", orders);

    const latestOrder = orders[orders.length - 1];
    if (!latestOrder) throw new Error("no orders found");

    const payment = await getPaymentStatusAsync(latestOrder.orderId);
    console.log("✅ payment:", payment);

    const message = await sendEmailAsync(user, payment);
    console.log("✅", message);

    console.log("Done: async/await");
  } catch (err) {
    console.error("❌ Error:", err.message);
  }
}

/* =========================================================
   5️⃣ Execute demo
   =========================================================
   같은 비즈니스 로직을:
   - Promise chaining
   - async/await
   두 방식으로 실행해본다.
*/

(async function main() {
  console.log("Start: Day 25 refactor callback → promise");

  await runWithPromiseChain(1);
  await runWithAsyncAwait(1);

  console.log("\nEnd: Day 25");
})();

/* =========================================================
   6️⃣ Summary (KR)
   =========================================================
   ✅ 콜백 → Promise로 바꾸면 좋은 점
   1) 중첩 제거: 코드가 위→아래로 읽힌다.
   2) 에러 처리 단순화: catch/try-catch로 중앙 처리 가능
   3) 재사용성 증가: 함수 조합/병렬 처리(Promise.all)로 확장 가능
   4) 유지보수 용이: 단계 추가/삭제가 쉬워진다.

   다음 단계 추천:
   - Promise.all / Promise.race (병렬 실행)
   - async error handling 패턴
   - fetch API와 실전 네트워크 요청
*/