/**
 * Day 12: DOM Manipulation - Text & HTML Update
 *
 * This file explains how to update text and HTML content
 * in DOM elements using textContent and innerHTML.
 *
 * 이 파일은 DOM 요소의 내용을 수정하는 두 가지 핵심 방식,
 * textContent 와 innerHTML 의 차이와 사용법을 다룬다.
 */

/* --------------------------------------------------
 * 1. Select Target Element
 * -------------------------------------------------- */

// 예제용 컨테이너 생성
const container = document.createElement("div");
container.id = "content-box";
container.style.border = "1px solid #ccc";
container.style.padding = "12px";
container.style.marginBottom = "10px";

// DOM에 추가
document.body.appendChild(container);

/*
[해설]
- 실습을 위해 동적으로 컨테이너를 생성
- 이후 text / HTML 변경 대상이 됨
*/


/* --------------------------------------------------
 * 2. Update Text Content (textContent)
 * -------------------------------------------------- */

container.textContent = "This is plain text content.";

/*
[해설]
- textContent는 문자열을 그대로 텍스트로 처리
- HTML 태그를 넣어도 렌더링되지 않음
- 보안(XSS)에 안전
*/


/* --------------------------------------------------
 * 3. Update HTML Content (innerHTML)
 * -------------------------------------------------- */

// HTML 구조를 포함한 문자열 삽입
container.innerHTML = `
  <h3>Updated with innerHTML</h3>
  <p>This text includes <strong>HTML tags</strong>.</p>
`;

/*
[해설]
- innerHTML은 문자열을 HTML로 파싱하여 DOM에 삽입
- 태그, 스타일, 구조를 함께 변경 가능
- ⚠ 사용자 입력을 그대로 넣으면 XSS 위험
*/


/* --------------------------------------------------
 * 4. Comparison Example
 * -------------------------------------------------- */

// textContent 예제
const textExample = document.createElement("p");
textExample.textContent = "<strong>This is NOT bold</strong>";

// innerHTML 예제
const htmlExample = document.createElement("p");
htmlExample.innerHTML = "<strong>This IS bold</strong>";

document.body.appendChild(textExample);
document.body.appendChild(htmlExample);

/*
[해설]
- textContent: 태그가 문자열로 출력
- innerHTML: 태그가 실제 HTML로 해석
*/


/* --------------------------------------------------
 * 5. Best Practices
 * -------------------------------------------------- */

/*
✔ textContent 사용 권장 상황
- 사용자 입력 출력
- 단순 텍스트 변경
- 보안이 중요한 경우

✔ innerHTML 사용 상황
- 정적 HTML 템플릿 렌더링
- UI 구조를 빠르게 변경해야 할 때
- 데이터가 신뢰 가능한 경우

실무에서는:
- 기본은 textContent
- 꼭 필요할 때만 innerHTML
*/