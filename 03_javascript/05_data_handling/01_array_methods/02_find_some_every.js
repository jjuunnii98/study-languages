/*
Day 51 — Array Condition Methods (find / some / every)

File
03_javascript/05_data_handling/01_array_methods/02_find_some_every.js

목표
JavaScript 배열에서 조건 기반으로 데이터를 탐색할 때 사용하는
핵심 메서드 3가지를 이해한다.

1️⃣ find
2️⃣ some
3️⃣ every

이 메서드들은 API 응답 처리, 데이터 검증, 조건 탐색 등에 매우 자주 사용된다.
*/


/* ============================================================
1️⃣ Example Dataset
============================================================ */

/*
API에서 받아온 사용자 데이터라고 가정
*/

const users = [
  { id: 1, name: "Alice", age: 25, active: true },
  { id: 2, name: "Bob", age: 31, active: false },
  { id: 3, name: "Charlie", age: 28, active: true },
  { id: 4, name: "David", age: 35, active: true }
];

console.log("Users:", users);


/* ============================================================
2️⃣ find — 조건에 맞는 첫 번째 요소 찾기
============================================================ */

/*
find는 조건을 만족하는 "첫 번째 요소"를 반환한다.

조건을 만족하는 요소가 없으면 undefined 반환
*/

const userAgeOver30 = users.find(user => user.age > 30);

console.log("First user age > 30:", userAgeOver30);


/*
특정 id 사용자 찾기
*/

const userId3 = users.find(user => user.id === 3);

console.log("User with id=3:", userId3);


/*
핵심 특징

find
→ 조건을 만족하는 "첫 번째 객체" 반환
*/


/* ============================================================
3️⃣ some — 조건을 만족하는 요소가 하나라도 있는지
============================================================ */

/*
some은 조건을 만족하는 요소가
"하나라도 있으면 true"
없으면 false
*/

const hasInactiveUser = users.some(user => user.active === false);

console.log("Any inactive users:", hasInactiveUser);


/*
30세 이상 사용자가 존재하는지 확인
*/

const hasUserOver30 = users.some(user => user.age >= 30);

console.log("Any user age >= 30:", hasUserOver30);


/*
핵심 특징

some
→ 존재 여부 검사
*/


/* ============================================================
4️⃣ every — 모든 요소가 조건을 만족하는지
============================================================ */

/*
every는 배열의 모든 요소가 조건을 만족해야 true
하나라도 실패하면 false
*/

const allUsersAdult = users.every(user => user.age >= 18);

console.log("All users are adults:", allUsersAdult);


/*
모든 사용자가 active인지 확인
*/

const allUsersActive = users.every(user => user.active === true);

console.log("All users active:", allUsersActive);


/*
핵심 특징

every
→ 전체 검증
*/


/* ============================================================
5️⃣ Real-World Example — API Validation
============================================================ */

/*
API에서 주문 데이터를 받았다고 가정
*/

const orders = [
  { id: 1, amount: 120 },
  { id: 2, amount: 80 },
  { id: 3, amount: 200 }
];


/*
금액이 100 이상인 주문이 있는지 확인
*/

const hasLargeOrder = orders.some(order => order.amount >= 100);

console.log("Has large order:", hasLargeOrder);


/*
모든 주문 금액이 양수인지 검증
*/

const allAmountsValid = orders.every(order => order.amount > 0);

console.log("All amounts valid:", allAmountsValid);


/*
특정 주문 찾기
*/

const orderId2 = orders.find(order => order.id === 2);

console.log("Order id=2:", orderId2);


/* ============================================================
Summary
============================================================ */

/*
find
→ 조건을 만족하는 첫 번째 요소 반환

some
→ 조건을 만족하는 요소가 하나라도 있는지 확인

every
→ 모든 요소가 조건을 만족하는지 확인

이 세 가지 메서드는
데이터 검증 / API 응답 처리 / 조건 탐색에서 자주 사용된다.
*/