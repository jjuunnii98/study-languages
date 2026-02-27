/**
 * Day 37 — Headers & Query String (Fetch Basics)
 *
 * 목표(Goal)
 * - Query String(쿼리스트링)을 안전하게 만드는 방법(encode 포함)
 * - Headers를 상황별로 설계하는 방법(인증/콘텐츠타입/캐시 등)
 * - fetch GET 요청에 headers + query를 함께 적용하는 패턴
 *
 * 핵심 포인트
 * 1) query string은 문자열 더하기로 만들지 말고 URLSearchParams 사용
 * 2) fetch는 4xx/5xx에서도 resolve될 수 있으므로 response.ok 검증 필수
 * 3) headers는 "필요한 것만" 명확히. 특히 GET에 Content-Type을 무의미하게 넣지 않기
 */

"use strict";

/* -----------------------------
 * 0) 공통 유틸: 에러 메시지 정리
 * -----------------------------
 * 실무에서는 에러를 "삼키지 말고", 의미 있는 메시지로 바꿔서 throw 하는 패턴이 좋다.
 */
function buildHttpErrorMessage(response, bodyText) {
  const base = `HTTP ${response.status} ${response.statusText}`;
  // 서버가 에러 내용을 JSON이 아닌 text로 줄 수 있으니, text를 함께 포함
  if (bodyText) return `${base} - ${bodyText}`;
  return base;
}

/* -----------------------------
 * 1) Query String 만들기 (URLSearchParams)
 * -----------------------------
 * ❌ 안 좋은 예:
 *   const url = base + "?q=" + keyword + "&page=" + page
 * - 공백, 한글, 특수문자 등이 들어오면 URL이 깨질 수 있음
 *
 * ✅ 좋은 예:
 *   new URLSearchParams({ q: keyword, page: "1" }).toString()
 * - 자동 인코딩 + 가독성 + 안전성
 */
function buildQueryString(paramsObj) {
  const sp = new URLSearchParams();

  // paramsObj에서 값이 null/undefined인 것은 제외 (실무에서 흔한 방어 로직)
  for (const [key, value] of Object.entries(paramsObj)) {
    if (value === null || value === undefined) continue;
    sp.set(key, String(value));
  }

  return sp.toString();
}

/* -----------------------------
 * 2) Headers 설계 (필요한 것만)
 * -----------------------------
 * headers는 request의 "메타데이터"
 * - Authorization: 토큰 기반 인증
 * - Accept: 서버에게 "나는 어떤 응답 포맷을 원해" 라고 알림
 * - Content-Type: 요청 body가 있을 때(POST/PUT/PATCH) 주로 필요
 *
 * GET 요청에는 보통 body가 없으므로 Content-Type은 넣지 않는 게 일반적
 */
function buildHeaders({ token } = {}) {
  const headers = {
    // 서버에 "나는 JSON 응답을 기대해" 라고 명확히 알려주기
    Accept: "application/json",
  };

  // 토큰이 있다면 Authorization 헤더 추가
  // Bearer는 가장 흔한 토큰 전달 방식
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  return headers;
}

/* -----------------------------
 * 3) fetch GET: query + headers 적용
 * -----------------------------
 * - baseUrl: 엔드포인트
 * - query: 쿼리 파라미터 객체
 * - token: 인증 토큰(없으면 undefined)
 *
 * ✅ 실무형 포인트
 * - response.ok 검사
 * - 에러 응답 본문(text)도 함께 읽어서 디버깅 가능하게
 */
async function fetchWithQueryAndHeaders({ baseUrl, query, token } = {}) {
  if (!baseUrl) throw new Error("baseUrl is required");

  const qs = query ? buildQueryString(query) : "";
  const url = qs ? `${baseUrl}?${qs}` : baseUrl;

  const headers = buildHeaders({ token });

  const response = await fetch(url, {
    method: "GET",
    headers,
  });

  // fetch는 4xx/5xx에서도 resolve 가능 -> 반드시 ok 체크
  if (!response.ok) {
    const bodyText = await response.text().catch(() => "");
    throw new Error(buildHttpErrorMessage(response, bodyText));
  }

  // 응답이 JSON이 아닐 수도 있으니 try/catch로 안전하게 처리
  // 다만 이 예제에서는 JSON 기반 API를 가정
  const data = await response.json();
  return data;
}

/* -----------------------------
 * 4) 예시 실행 (공개 테스트 API 사용)
 * -----------------------------
 * jsonplaceholder는 테스트용 API로 매우 자주 사용됨
 * - /comments?postId=1 처럼 query로 필터 가능
 *
 * 한국어 포인트:
 * - query에 숫자를 넣어도 URLSearchParams가 문자열로 변환해준다.
 */
async function main() {
  try {
    // (1) Query String 예시: postId로 댓글 필터링
    const comments = await fetchWithQueryAndHeaders({
      baseUrl: "https://jsonplaceholder.typicode.com/comments",
      query: { postId: 1 },
      // token: "YOUR_TOKEN", // 필요하면 사용
    });

    console.log("Fetched comments count:", comments.length);
    console.log("First comment sample:", comments[0]);

    // (2) Query String 인코딩 예시: 공백/한글/특수문자
    // 실제 API가 q 검색을 지원한다는 가정 하에 "URL이 깨지지 않고 만들어지는지"만 시연
    const encodedQs = buildQueryString({
      q: "서울 맛집 + coffee",
      tag: "AI/ML",
      page: 1,
    });
    console.log("Encoded query string:", encodedQs);

    // (3) Headers 예시: token이 있으면 Authorization이 추가됨
    const h1 = buildHeaders();
    const h2 = buildHeaders({ token: "abc123" });
    console.log("Headers without token:", h1);
    console.log("Headers with token:", h2);
  } catch (err) {
    console.error("Error:", err.message);
  }
}

main();