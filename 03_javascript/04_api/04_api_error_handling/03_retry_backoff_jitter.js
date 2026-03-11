/*
========================================================
Retry + Backoff + Jitter
========================================================

실무 API 환경에서는 요청이 한 번에 항상 성공하지 않는다.

예:
- 네트워크 일시 장애
- 서버 과부하
- 429 Too Many Requests
- 502 / 503 / 504 같은 일시적 서버 오류

이럴 때 무조건 바로 실패시키는 대신,
"잠시 기다렸다가 다시 시도(retry)" 할 수 있다.

하지만 모든 요청이 동시에 재시도하면
서버에 더 큰 부하를 줄 수 있다.

그래서 사용하는 패턴이:

1) Retry
2) Exponential Backoff
3) Jitter

이다.

--------------------------------------------------------
개념 요약
--------------------------------------------------------

Retry
→ 실패 시 다시 시도

Backoff
→ 재시도 간격을 점점 늘림

Jitter
→ 대기 시간에 랜덤성을 추가해서
   모든 클라이언트가 동시에 재시도하는 현상을 방지
*/


/*
========================================================
1️⃣ Sleep Utility
========================================================

지정된 시간(ms)만큼 대기하는 함수
*/

function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}


/*
========================================================
2️⃣ Retryable Error 판별
========================================================

어떤 에러는 재시도할 가치가 있고,
어떤 에러는 즉시 실패해야 한다.

재시도 가능한 대표 상황:
- 네트워크 오류
- 429
- 500, 502, 503, 504

재시도 불필요:
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
*/

function isRetryableStatus(status) {
    return [429, 500, 502, 503, 504].includes(status);
}


/*
========================================================
3️⃣ Fetch with Retry + Backoff + Jitter
========================================================
*/

async function fetchWithRetry(url, options = {}, maxRetries = 3, baseDelay = 500) {
    let attempt = 0;

    while (attempt <= maxRetries) {
        try {
            console.log(`Attempt ${attempt + 1} / ${maxRetries + 1}`);

            const response = await fetch(url, options);

            /*
            ------------------------------------------------
            HTTP 상태 코드 처리
            ------------------------------------------------
            */

            if (!response.ok) {
                /*
                재시도 가능한 상태 코드라면
                throw 해서 catch로 보내고 retry 로직 실행
                */
                if (isRetryableStatus(response.status)) {
                    throw new Error(`Retryable HTTP error: ${response.status}`);
                }

                /*
                재시도 불가능한 상태 코드는 즉시 실패
                */
                throw new Error(`Non-retryable HTTP error: ${response.status}`);
            }

            /*
            ------------------------------------------------
            정상 응답 처리
            ------------------------------------------------
            */
            const data = await response.json();
            console.log("Request succeeded.");
            return data;

        } catch (error) {
            attempt += 1;

            /*
            ------------------------------------------------
            마지막 재시도까지 실패했으면 종료
            ------------------------------------------------
            */
            if (attempt > maxRetries) {
                console.error("All retry attempts failed.");
                console.error(error.message);
                throw error;
            }

            /*
            ------------------------------------------------
            Exponential Backoff
            ------------------------------------------------

            delay = baseDelay * 2^(attempt - 1)

            예:
            attempt 1 -> 500ms
            attempt 2 -> 1000ms
            attempt 3 -> 2000ms
            */

            const backoffDelay = baseDelay * Math.pow(2, attempt - 1);

            /*
            ------------------------------------------------
            Jitter 추가
            ------------------------------------------------

            랜덤 시간(0 ~ 300ms)을 추가해서
            동시에 재시도하는 요청이 몰리지 않게 한다.
            */

            const jitter = Math.floor(Math.random() * 300);

            const totalDelay = backoffDelay + jitter;

            console.warn(`Request failed: ${error.message}`);
            console.warn(`Retrying after ${totalDelay} ms...`);

            await sleep(totalDelay);
        }
    }
}


/*
========================================================
4️⃣ Example Execution
========================================================
*/

/*
정상적으로 성공할 가능성이 높은 API
*/
const SUCCESS_URL = "https://jsonplaceholder.typicode.com/posts/1";

/*
실패 예시용 URL
jsonplaceholder는 404를 반환할 수 있음
404는 retryable이 아니므로 즉시 실패 처리됨
*/
const FAIL_URL = "https://jsonplaceholder.typicode.com/invalid-endpoint";


async function runExamples() {
    try {
        console.log("\n=== Success Example ===");
        const successData = await fetchWithRetry(SUCCESS_URL, {}, 3, 500);
        console.log(successData);

    } catch (error) {
        console.error("Final failure (success example):", error.message);
    }

    try {
        console.log("\n=== Failure Example ===");
        const failData = await fetchWithRetry(FAIL_URL, {}, 3, 500);
        console.log(failData);

    } catch (error) {
        console.error("Final failure (failure example):", error.message);
    }
}

runExamples();