/**
 * Day 5: JavaScript Loops
 *
 * This file covers looping constructs in JavaScript.
 * Loops allow repetitive execution of code blocks
 * and are essential for data processing and iteration.
 *
 * 이 파일은 JavaScript의 반복문(loop)을 다룬다.
 * 반복문은 데이터를 순회하거나
 * 동일한 작업을 여러 번 수행할 때 필수적이다.
 */

// ------------------------------------
// 1. for loop
// ------------------------------------
// 가장 기본적인 반복문
// 초기값 → 조건 → 증감 순서로 동작

for (let i = 0; i < 5; i++) {
  console.log("for loop i =", i);
}

// ------------------------------------
// 2. while loop
// ------------------------------------
// 조건이 true인 동안 반복 실행

let count = 0;

while (count < 3) {
  console.log("while loop count =", count);
  count++;
}

// ------------------------------------
// 3. do...while loop
// ------------------------------------
// 조건과 상관없이 최소 한 번은 실행

let number = 0;

do {
  console.log("do...while number =", number);
  number++;
} while (number < 2);

// ------------------------------------
// 4. for...of loop (Arrays)
// ------------------------------------
// 배열 요소를 하나씩 순회 (가장 많이 사용)

let fruits = ["apple", "banana", "orange"];

for (let fruit of fruits) {
  console.log("fruit:", fruit);
}

// ------------------------------------
// 5. for...in loop (Objects)
// ------------------------------------
// 객체의 key를 순회할 때 사용

let person = {
  name: "Junyeong",
  age: 27,
  role: "Student"
};

for (let key in person) {
  console.log(key, ":", person[key]);
}

// ------------------------------------
// 6. break and continue
// ------------------------------------

// break: 반복문 즉시 종료
for (let i = 0; i < 5; i++) {
  if (i === 3) {
    break;
  }
  console.log("break example i =", i);
}

// continue: 현재 반복만 건너뜀
for (let i = 0; i < 5; i++) {
  if (i === 2) {
    continue;
  }
  console.log("continue example i =", i);
}

// ------------------------------------
// 7. Practical example (실무적 예제)
// ------------------------------------
// 점수가 80점 이상인 학생만 출력

let students = [
  { name: "Alice", score: 85 },
  { name: "Bob", score: 72 },
  { name: "Charlie", score: 90 }
];

for (let student of students) {
  if (student.score >= 80) {
    console.log(student.name, "passed");
  }
}

// ------------------------------------
// 8. Summary
// ------------------------------------
/*
- for: 반복 횟수가 명확할 때
- while: 조건 기반 반복
- for...of: 배열 순회 (가장 권장)
- for...in: 객체 key 순회
- break / continue: 반복 제어

요약:
- 반복문은 데이터 처리의 핵심
- 배열에는 for...of
- 객체에는 for...in
- 실무에서는 반복 + 조건문 조합이 가장 흔함
*/