/**
 * Day 38: Response Parsing (Fetch Basics)
 *
 * 목표:
 * - fetch 응답을 "안전하게" 파싱하는 표준 패턴을 익힌다.
 * - JSON/텍스트/빈 응답(204) 등을 일관된 방식으로 처리한다.
 * - 4xx/5xx에서 fetch가 자동 reject 하지 않는 특성을 반영하여
 *   response.ok 검증 + 에러 바디 파싱까지 포함한 "실무형" 파서를 만든다.
 *
 * 핵심 포인트:
 * - response.json()은 실패할 수 있다(빈 바디, 잘못된 JSON).
 * - Content-Type은 서버마다 다르게 오기도 한다(대소문자/charset 포함).
 * - 에러일 때도 서버가 JSON 에러 바디를 보내는 경우가 많다.
 * - 따라서 "성공/실패"와 "파싱 방식"을 분리해 설계한다.
 */

// -------------------------------
// 0) 커스텀 에러 타입 (실무형)
// -------------------------------

/**
 * HTTP 요청 실패를 표현하는 에러
 * - status, url, responseBody 등을 포함해 디버깅/로그에 유리하게 한다.
 */
class HttpError extends Error {
  /**
   * @param {string} message
   * @param {{ status: number, url: string, body?: any }} meta
   */
  constructor(message, meta) {
    super(message);
    this.name = "HttpError";
    this.status = meta.status;
    this.url = meta.url;
    this.body = meta.body; // 서버가 내려준 에러 바디(JSON 또는 텍스트)
  }
}

// -------------------------------
// 1) 유틸: Content-Type 안전 확인
// -------------------------------

/**
 * Content-Type 헤더에서 mime 타입을 안전하게 가져온다.
 * 예: "application/json; charset=utf-8" -> "application/json"
 */
function getMimeType(response) {
  const ct = response.headers.get("content-type") || "";
  return ct.split(";")[0].trim().toLowerCase();
}

// -------------------------------
// 2) 유틸: 응답 바디를 "가능한 범위에서" 안전 파싱
// -------------------------------

/**
 * 응답을 JSON/텍스트로 안전하게 파싱한다.
 * - 204 No Content 또는 Content-Length 0 같은 케이스를 고려
 * - JSON이라고 주장하지만 실제로는 비어있거나 깨져있을 수 있음
 *
 * @returns {Promise<{ data: any, rawText: string | null, mime: string }>}
 */
async function safeParseBody(response) {
  const mime = getMimeType(response);

  // ✅ 204는 바디가 없다. (표준)
  if (response.status === 204) {
    return { data: null, rawText: null, mime };
  }

  // 먼저 텍스트로 읽어두면:
  // - JSON 파싱 실패 시에도 에러 바디를 유지할 수 있음
  // - 한 번 읽으면 스트림이 소모되므로(Body is a stream), 텍스트로 먼저 읽고 필요 시 JSON 파싱
  const rawText = await response.text();

  // 바디가 진짜 비어있을 수 있다 (서버/프록시 환경에서 흔함)
  if (!rawText) {
    return { data: null, rawText: "", mime };
  }

  // JSON이면 JSON 파싱 시도
  if (mime === "application/json" || mime.endsWith("+json")) {
    try {
      const json = JSON.parse(rawText);
      return { data: json, rawText, mime };
    } catch (e) {
      // JSON이라고 했는데 깨진 경우: 실무에서는 꽤 잦다.
      // 이 경우 rawText를 그대로 남기고 data는 null로 둔다.
      return { data: null, rawText, mime };
    }
  }

  // 그 외는 텍스트로 반환
  return { data: rawText, rawText, mime };
}

// -------------------------------
// 3) 핵심: "검증 + 파싱 + 에러전파"가 포함된 fetch 래퍼
// -------------------------------

/**
 * fetch를 호출하고, 결과를 안전하게 파싱한다.
 * - response.ok를 기준으로 성공/실패를 구분
 * - 실패 시에도 에러 바디를 파싱해 HttpError에 포함
 *
 * @param {string} url
 * @param {RequestInit} [options]
 * @returns {Promise<any>} 파싱된 data (JSON이면 객체, 텍스트면 문자열, 없으면 null)
 */
async function fetchAndParse(url, options = {}) {
  const res = await fetch(url, options);

  // 바디 파싱은 성공/실패 관계없이 해두는 것이 좋다.
  // 이유: 실패일 때도 서버가 내려준 에러 정보를 확보해야 하기 때문.
  const parsed = await safeParseBody(res);

  if (!res.ok) {
    // ✅ 실무형 에러: status + url + body 포함
    const message = `HTTP ${res.status} ${res.statusText} - ${url}`;
    throw new HttpError(message, {
      status: res.status,
      url,
      body: parsed.data ?? parsed.rawText,
    });
  }

  return parsed.data;
}

// -------------------------------
// 4) 데모: JSONPlaceholder로 테스트
// -------------------------------

async function demo() {
  // ✅ 성공 케이스: JSON 파싱
  try {
    const todo = await fetchAndParse("https://jsonplaceholder.typicode.com/todos/1");
    console.log("[SUCCESS] todo:", todo);
  } catch (err) {
    console.error("[ERROR - unexpected]", err);
  }

  // ✅ 실패 케이스: 404 → HttpError로 예외 발생 + 에러 바디(있다면) 포함
  try {
    const unknown = await fetchAndParse("https://jsonplaceholder.typicode.com/unknown-endpoint");
    console.log("[SUCCESS] unknown:", unknown);
  } catch (err) {
    if (err instanceof HttpError) {
      console.error("[HTTP ERROR]", err.message);
      console.error("status:", err.status);
      console.error("url:", err.url);
      console.error("body:", err.body);
    } else {
      console.error("[ERROR]", err);
    }
  }
}

demo();