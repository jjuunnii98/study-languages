/**
 * Day 13: DOM Manipulation - Class & Style Manipulation
 *
 * This file covers how to manipulate CSS classes and inline styles
 * using JavaScript in a practical, UI-friendly way.
 *
 * 이 파일은 JavaScript로 CSS class와 inline style을 조작하는 방법을 다룬다.
 * 실무에서는 "상태(state)에 따라 class를 토글(toggle)하는 패턴"이 매우 중요하다.
 */

/* --------------------------------------------------
 * 0. Setup (Create Demo UI)
 * -------------------------------------------------- */

const app = document.createElement("div");
app.id = "app";
app.style.padding = "12px";
app.style.border = "1px solid #ddd";
app.style.borderRadius = "8px";
app.style.marginBottom = "12px";

document.body.appendChild(app);

const title = document.createElement("h3");
title.textContent = "Day 13: Class & Style Manipulation";
title.style.marginTop = "0";
app.appendChild(title);

const box = document.createElement("div");
box.textContent = "Target Box";
box.className = "box"; // 초기 클래스
box.style.padding = "12px";
box.style.border = "1px solid #ccc";
box.style.borderRadius = "8px";
box.style.transition = "all 150ms ease"; // 시각적 변화가 부드럽게 보이도록
app.appendChild(box);

const btnToggle = document.createElement("button");
btnToggle.textContent = "Toggle Highlight";
btnToggle.style.marginRight = "8px";

const btnReset = document.createElement("button");
btnReset.textContent = "Reset";

app.appendChild(btnToggle);
app.appendChild(btnReset);

/*
[해설]
- 실습용으로 DOM 요소를 직접 만들었다.
- box에 class/style을 적용하고, 버튼으로 상태를 변경하는 UI 패턴을 구성했다.
*/


/* --------------------------------------------------
 * 1. classList Basics
 * -------------------------------------------------- */
/*
classList는 class 조작을 위한 표준 API.
- add(): 클래스 추가
- remove(): 클래스 제거
- toggle(): 있으면 제거, 없으면 추가
- contains(): 특정 클래스 포함 여부 확인
*/

box.classList.add("rounded"); // 예: 의미 있는 class 이름 부여 (실제로 CSS가 없더라도 학습용)
console.log("Has 'rounded' class?", box.classList.contains("rounded"));

box.classList.remove("rounded");
console.log("Has 'rounded' class after remove?", box.classList.contains("rounded"));


/* --------------------------------------------------
 * 2. Toggle Pattern (Most Common in Real UI)
 * -------------------------------------------------- */

function applyHighlight(isOn) {
  // ✅ 실무 팁:
  // "inline style"은 최소화하고, 가능하면 class 토글로 제어하는 것이 유지보수에 좋다.
  // 여기서는 학습 목적상 class + style을 함께 보여준다.

  if (isOn) {
    box.classList.add("is-highlighted");
    box.style.backgroundColor = "#e0f2fe";
    box.style.borderColor = "#0284c7";
    box.style.color = "#0c4a6e";
    box.style.transform = "scale(1.01)";
  } else {
    box.classList.remove("is-highlighted");
    box.style.backgroundColor = "";
    box.style.borderColor = "#ccc";
    box.style.color = "";
    box.style.transform = "";
  }
}

/*
[해설]
- 상태(isOn)에 따라 UI를 바꾸는 "상태 기반 렌더링" 패턴
- 프레임워크(React/Vue)로 가면 이 개념이 그대로 컴포넌트 상태로 연결됨
*/


/* --------------------------------------------------
 * 3. Event Handling: Toggle / Reset
 * -------------------------------------------------- */

btnToggle.addEventListener("click", () => {
  const isOn = box.classList.toggle("is-highlighted"); // toggle 결과(boolean)를 활용
  applyHighlight(isOn);

  console.log("[Toggle] is-highlighted:", isOn);
});

btnReset.addEventListener("click", () => {
  applyHighlight(false);
  console.log("[Reset] highlight cleared");
});

/*
[해설]
- classList.toggle()은 boolean을 반환한다.
  - true: 새로 추가됨(ON)
  - false: 제거됨(OFF)
- 이 반환값으로 스타일 적용을 한 번에 정리할 수 있다.
*/


/* --------------------------------------------------
 * 4. Best Practices (Important)
 * -------------------------------------------------- */
/*
✅ Best Practices
1) 가능한 한 inline style 남발하지 말고 class 기반으로 관리
2) UI는 "상태"로 제어 (isOn 같은 boolean)
3) style을 설정했다면 reset 전략도 함께 설계 (""로 초기화)

⚠ Common Mistakes
- className = "..." 로 통째로 덮어쓰기 (기존 class 사라짐)
- toggle을 쓰면서도 상태를 따로 관리하지 않아 꼬임
- inline style이 너무 많아져서 CSS/디자인 관리가 어려워짐
*/