/**
 * Day 26 — Promise Basics
 *
 * This file introduces the fundamental mechanics of JavaScript Promises.
 *
 * Covered:
 * 1) Promise state (pending → fulfilled / rejected)
 * 2) resolve / reject
 * 3) .then() chaining
 * 4) .catch() centralized error handling
 * 5) .finally()
 *
 * 이 파일은 Promise의 핵심 구조와 상태 전이를 다룬다.
 * Promise는 "비동기 작업의 결과를 나타내는 객체"이다.
 */

/* =========================================================
   1️⃣ Creating a Promise
   =========================================================
   Promise constructor:
   new Promise((resolve, reject) => { ... })
*/

function asyncTask(success = true) {
  return new Promise((resolve, reject) => {
    console.log("Task started...");

    setTimeout(() => {
      if (success) {
        resolve("Task completed successfully");
      } else {
        reject(new Error("Task failed"));
      }
    }, 1000);
  });
}

/* =========================================================
   2️⃣ Promise States
   =========================================================
   A Promise has three states:

   - pending   (initial state)
   - fulfilled (resolved)
   - rejected  (error occurred)

   상태 전이는 단 한 번만 발생한다.
*/

/* =========================================================
   3️⃣ Using .then() and .catch()
   =========================================================
   then() handles success
   catch() handles errors
*/

asyncTask(true)
  .then((result) => {
    console.log("✅ Success:", result);
  })
  .catch((error) => {
    console.error("❌ Error:", error.message);
  })
  .finally(() => {
    console.log("🔄 Promise settled (success or failure)");
  });

/* =========================================================
   4️⃣ Promise Chaining
   =========================================================
   then() returns a new Promise.
   This allows chaining sequential async operations.
*/

function multiplyAsync(number) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(number * 2);
    }, 500);
  });
}

multiplyAsync(2)
  .then((result) => {
    console.log("Step 1:", result);
    return multiplyAsync(result);
  })
  .then((result) => {
    console.log("Step 2:", result);
    return multiplyAsync(result);
  })
  .then((result) => {
    console.log("Step 3:", result);
  })
  .catch((error) => {
    console.error("Chain error:", error.message);
  });

/* =========================================================
   5️⃣ Error Propagation
   =========================================================
   If any .then() throws an error,
   it will skip remaining .then() blocks
   and jump directly to .catch().
*/

Promise.resolve("Start")
  .then((msg) => {
    console.log(msg);
    throw new Error("Unexpected issue");
  })
  .then(() => {
    console.log("This will NOT run");
  })
  .catch((error) => {
    console.error("Caught error:", error.message);
  });

/* =========================================================
   6️⃣ Summary (KR)
   =========================================================
   ✅ Promise는 비동기 작업의 상태를 표현하는 객체이다.
   ✅ resolve → 성공
   ✅ reject → 실패
   ✅ then() → 성공 처리
   ✅ catch() → 에러 처리
   ✅ finally() → 공통 정리 로직

   Promise는 콜백의 구조적 한계를 해결한다.
   다음 단계는 async/await와 Promise 병렬 처리이다.
*/