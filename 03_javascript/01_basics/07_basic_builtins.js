/**
 * Day 7: JavaScript Basic Built-in Objects
 *
 * This file introduces commonly used JavaScript built-in objects
 * and methods that are essential for everyday programming.
 *
 * 이 파일은 JavaScript에서 기본적으로 제공되는
 * 주요 Built-in 객체와 메서드를 다룬다.
 * 실제 개발과 데이터 처리에서 매우 자주 사용된다.
 */

// --------------------------------------------------
// 1. Math Object
// --------------------------------------------------
// Math는 수학 연산과 관련된 정적 메서드를 제공한다.

console.log(Math.PI);              // 원주율
console.log(Math.round(3.7));      // 반올림
console.log(Math.floor(3.7));      // 내림
console.log(Math.ceil(3.1));       // 올림
console.log(Math.max(1, 5, 3));    // 최대값
console.log(Math.min(1, 5, 3));    // 최소값
console.log(Math.random());        // 0 이상 1 미만 난수


// --------------------------------------------------
// 2. String Built-in Methods
// --------------------------------------------------

const message = "  Hello JavaScript World  ";

console.log(message.length);              // 문자열 길이
console.log(message.toUpperCase());        // 대문자 변환
console.log(message.toLowerCase());        // 소문자 변환
console.log(message.trim());               // 앞뒤 공백 제거
console.log(message.includes("JavaScript")); // 포함 여부
console.log(message.replace("World", "JS")); // 문자열 치환


// --------------------------------------------------
// 3. Number Built-in Methods
// --------------------------------------------------

const num = 123.456;

console.log(num.toFixed(2));       // 소수점 고정 (문자열 반환)
console.log(Number.isInteger(num)); // 정수 여부
console.log(Number.parseInt("42")); // 문자열 → 정수
console.log(Number.parseFloat("3.14")); // 문자열 → 실수


// --------------------------------------------------
// 4. Array Built-in Methods
// --------------------------------------------------

const numbers = [1, 2, 3, 4, 5];

numbers.push(6);                   // 요소 추가
numbers.pop();                     // 마지막 요소 제거

console.log(numbers.includes(3));  // 포함 여부
console.log(numbers.indexOf(4));   // 인덱스 조회
console.log(numbers.join("-"));    // 문자열로 결합


// --------------------------------------------------
// 5. Date Object
// --------------------------------------------------
// Date는 날짜와 시간을 다룬다.

const now = new Date();

console.log(now);                  // 현재 날짜/시간
console.log(now.getFullYear());    // 연도
console.log(now.getMonth() + 1);   // 월 (0부터 시작)
console.log(now.getDate());        // 일
console.log(now.getDay());         // 요일 (0=일요일)


// --------------------------------------------------
// 6. Type Conversion Helpers
// --------------------------------------------------

console.log(String(100));          // 숫자 → 문자열
console.log(Number("123"));        // 문자열 → 숫자
console.log(Boolean(1));           // truthy
console.log(Boolean(0));           // falsy


// --------------------------------------------------
// 7. Summary
// --------------------------------------------------
// - JavaScript provides many built-in objects by default
// - Math, String, Number, Array, Date are the most commonly used
// - Built-in methods reduce the need for custom implementations
// - Mastering these improves productivity and code clarity