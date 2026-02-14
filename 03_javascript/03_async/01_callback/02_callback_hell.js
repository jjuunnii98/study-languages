/**
 * Day 24 — Callback Hell (JavaScript Async)
 *
 * This file demonstrates "callback hell":
 * deeply nested callbacks that make async code hard to read,
 * hard to test, and hard to maintain.
 *
 * 이 파일은 콜백 헬(callback hell)을 보여준다.
 * 비동기 로직이 콜백으로 중첩될 때 코드 가독성과 유지보수성이 급격히 떨어지는 문제를 체감한다.
 *
 * Key topics:
 * - Nested async flow
 * - Error-first callback pattern (Node.js style)
 * - Why Promises / async-await exist
 */

/* =========================================================
   1️⃣ Simulated async functions (error-first callbacks)
   =========================================================
   Each function takes a callback like:
   callback(error, result)

   - error가 있으면 error를 전달하고 result는 null
   - 성공이면 error는 null, result에 값

   이런 스타일은 Node.js에서 흔히 쓰이는 패턴이다.
*/

function getUser(userId, cb) {
  setTimeout(() => {
    if (!userId) return cb(new Error("userId is required"), null);

    // pretend we fetched from DB
    cb(null, { id: userId, name: "Junyeong" });
  }, 400);
}

function getOrders(userId, cb) {
  setTimeout(() => {
    // random error simulation
    if (Math.random() < 0.05) return cb(new Error("Orders service timeout"), null);

    cb(null, [
      { orderId: 101, userId, amount: 39.9 },
      { orderId: 102, userId, amount: 12.5 },
    ]);
  }, 400);
}

function getPaymentStatus(orderId, cb) {
  setTimeout(() => {
    if (!orderId) return cb(new Error("orderId is required"), null);

    cb(null, { orderId, paid: true, method: "card" });
  }, 400);
}

function sendEmail(user, paymentInfo, cb) {
  setTimeout(() => {
    // random error simulation
    if (Math.random() < 0.05) return cb(new Error("Email service failed"), null);

    cb(null, `Email sent to ${user.name} for order ${paymentInfo.orderId}`);
  }, 400);
}

/* =========================================================
   2️⃣ Callback Hell Example
   =========================================================
   Goal:
   1) Fetch user
   2) Fetch orders
   3) Pick latest order
   4) Fetch payment status
   5) Send email

   콜백이 계속 안으로 들어가며 "피라미드" 형태가 된다.
*/

console.log("Start: callback hell demo");

getUser(1, (err, user) => {
  if (err) {
    console.error("❌ getUser failed:", err.message);
    return;
  }
  console.log("✅ user:", user);

  getOrders(user.id, (err2, orders) => {
    if (err2) {
      console.error("❌ getOrders failed:", err2.message);
      return;
    }
    console.log("✅ orders:", orders);

    // latest order = last one (simple assumption)
    const latestOrder = orders[orders.length - 1];
    if (!latestOrder) {
      console.error("❌ no orders found");
      return;
    }

    getPaymentStatus(latestOrder.orderId, (err3, payment) => {
      if (err3) {
        console.error("❌ getPaymentStatus failed:", err3.message);
        return;
      }
      console.log("✅ payment:", payment);

      sendEmail(user, payment, (err4, message) => {
        if (err4) {
          console.error("❌ sendEmail failed:", err4.message);
          return;
        }
        console.log("✅", message);
        console.log("End: callback hell demo");
      });
    });
  });
});

/* =========================================================
   3️⃣ Why is this a problem?
   =========================================================
   ✅ 문제점(한국어)

   1) 가독성 문제:
      - 콜백이 중첩될수록 indent(들여쓰기)가 깊어져 읽기 어려움
      - 로직 흐름 파악이 힘들어짐

   2) 에러 처리 복잡:
      - 단계마다 if(err) 처리 반복
      - 어느 단계에서 실패했는지 추적이 어려워짐

   3) 유지보수/확장 어려움:
      - 중간 단계 추가/삭제가 어려움
      - 함수 분리 없이 로직이 한 곳에 뭉치게 됨

   👉 그래서 Promise, async/await가 필요해진다.
*/