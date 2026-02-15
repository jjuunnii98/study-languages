/**
 * Day 27 — Promise Chaining (Practical Patterns)
 *
 * This file focuses on designing robust Promise chains:
 * - returning values vs returning Promises
 * - composing sequential async steps
 * - centralized error propagation
 * - branching logic in chains
 * - converting callback-style flow into a clean chain
 *
 * 이 파일은 Promise 체이닝을 "실전 패턴" 관점에서 다룬다.
 * 단순 then 사용법이 아니라, 유지보수 가능한 비동기 파이프라인을 만드는 것이 목표다.
 */

/* =========================================================
   1️⃣ Helpers: simulate async tasks
   ========================================================= */

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function fetchUser(userId) {
  return delay(200).then(() => {
    if (!userId) throw new Error("userId is required");
    return { id: userId, name: "Junyeong" };
  });
}

function fetchOrders(userId) {
  return delay(250).then(() => {
    // simulate occasional failure
    if (Math.random() < 0.05) throw new Error("Orders service timeout");
    return [
      { orderId: 101, userId, amount: 39.9 },
      { orderId: 102, userId, amount: 12.5 },
    ];
  });
}

function fetchPayment(orderId) {
  return delay(200).then(() => {
    if (!orderId) throw new Error("orderId is required");
    return { orderId, paid: true, method: "card" };
  });
}

function sendReceiptEmail(user, payment) {
  return delay(150).then(() => {
    if (Math.random() < 0.05) throw new Error("Email service failed");
    return `Email sent to ${user.name} for order ${payment.orderId}`;
  });
}

/* =========================================================
   2️⃣ Core rule: always RETURN in then()
   =========================================================
   - then() 안에서 값을 반환하면 다음 then으로 "값"이 전달된다.
   - Promise를 반환하면 다음 then은 그 Promise가 끝날 때까지 기다린다.

   ✅ 핵심: then()에서 return을 안 하면 체인이 끊기거나 undefined가 전달될 수 있다.
*/

function demoReturnRules() {
  console.log("\n=== Demo: return value vs return Promise ===");

  return Promise.resolve(10)
    .then((x) => {
      // return value -> next then gets 20 immediately
      return x * 2;
    })
    .then((x) => {
      console.log("Return value result:", x); // 20

      // return Promise -> next then waits
      return delay(300).then(() => x + 5);
    })
    .then((x) => {
      console.log("Return Promise result:", x); // 25
    });
}

/* =========================================================
   3️⃣ Sequential pipeline with chaining
   =========================================================
   user → orders → payment → email
   콜백헬 구조를 "평평한 체인"으로 바꾼 형태.
*/

function runPipeline(userId) {
  console.log("\n=== Pipeline: user → orders → payment → email ===");

  let cachedUser; // 체인 중간 상태 공유(최소화 권장)
  let latestOrder;

  return fetchUser(userId)
    .then((user) => {
      cachedUser = user;
      console.log("✅ user:", user);
      return fetchOrders(user.id);
    })
    .then((orders) => {
      console.log("✅ orders:", orders);

      latestOrder = orders[orders.length - 1];
      if (!latestOrder) throw new Error("no orders found");

      return fetchPayment(latestOrder.orderId);
    })
    .then((payment) => {
      console.log("✅ payment:", payment);
      return sendReceiptEmail(cachedUser, payment);
    })
    .then((message) => {
      console.log("✅", message);
      console.log("Done: pipeline");
    })
    .catch((err) => {
      // ✅ 중앙 집중 에러 처리 (중간 if(err) 반복 제거)
      console.error("❌ Pipeline error:", err.message);
    });
}

/* =========================================================
   4️⃣ Branching inside a chain (business rules)
   =========================================================
   예: 결제가 unpaid면 이메일을 보내지 않고 종료
*/

function fetchPaymentSometimesUnpaid(orderId) {
  return delay(200).then(() => {
    const paid = Math.random() > 0.2; // 80% paid
    return { orderId, paid, method: paid ? "card" : null };
  });
}

function runBranchingPipeline(userId) {
  console.log("\n=== Pipeline with branching (paid check) ===");

  let userCache;
  let latestOrder;

  return fetchUser(userId)
    .then((user) => {
      userCache = user;
      return fetchOrders(user.id);
    })
    .then((orders) => {
      latestOrder = orders[orders.length - 1];
      if (!latestOrder) throw new Error("no orders found");
      return fetchPaymentSometimesUnpaid(latestOrder.orderId);
    })
    .then((payment) => {
      console.log("✅ payment:", payment);

      if (!payment.paid) {
        // Branch: stop chain early
        console.log("⚠️ Payment not completed. Skip email.");
        return "Skipped email (unpaid)";
      }

      // Branch: continue async
      return sendReceiptEmail(userCache, payment);
    })
    .then((result) => {
      console.log("✅ Result:", result);
      console.log("Done: branching pipeline");
    })
    .catch((err) => {
      console.error("❌ Branching pipeline error:", err.message);
    });
}

/* =========================================================
   5️⃣ Final summary (KR)
   =========================================================
   ✅ Promise 체이닝 실전 핵심

   1) then() 안에서 항상 return을 의식하라
      - 값 반환: 다음 then에 값 전달
      - Promise 반환: 다음 then이 기다렸다가 결과를 받음

   2) catch()로 에러를 한 곳에서 처리하라
      - 중간중간 if(err) 반복 대신 중앙 처리

   3) 비즈니스 규칙은 체인 안에서 "분기"로 구현 가능
      - 조건에 따라 체인을 종료하거나 다음 작업 수행

   다음 단계:
   - Promise.all / Promise.race (병렬 처리)
   - async/await로 같은 파이프라인을 더 깔끔하게 구성
*/

/* =========================================================
   6️⃣ Execute
   ========================================================= */

(async function main() {
  console.log("Start: Day 27 Promise chaining patterns");

  await demoReturnRules();
  await runPipeline(1);
  await runBranchingPipeline(1);

  console.log("\nEnd: Day 27");
})();