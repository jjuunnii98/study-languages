/*
========================================================
API Timeout Handling with AbortController
========================================================

fetch()는 기본적으로 timeout 기능이 없다.

즉,
서버가 응답하지 않으면
요청이 무한 대기 상태가 될 수 있다.

이를 해결하기 위해 사용하는 것이

AbortController

이다.

AbortController를 사용하면

- 일정 시간 후 요청 취소
- 사용자가 직접 요청 취소
- 오래 걸리는 API 중단

등을 구현할 수 있다.
*/

async function fetchWithTimeout(url, timeout = 5000) {

    /*
    ------------------------------------------------
    AbortController 생성
    ------------------------------------------------
    signal을 fetch에 전달하면
    controller.abort() 호출 시
    요청이 취소된다.
    */

    const controller = new AbortController();
    const signal = controller.signal;

    /*
    ------------------------------------------------
    Timeout 설정
    ------------------------------------------------
    일정 시간이 지나면
    controller.abort() 실행
    */

    const timeoutId = setTimeout(() => {
        controller.abort();
    }, timeout);

    try {

        /*
        ------------------------------------------------
        fetch 요청
        ------------------------------------------------
        signal을 전달해야 abort 가능
        */

        const response = await fetch(url, { signal });

        /*
        ------------------------------------------------
        HTTP 상태 코드 체크
        ------------------------------------------------
        */

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        /*
        ------------------------------------------------
        JSON 데이터 변환
        ------------------------------------------------
        */

        const data = await response.json();

        console.log("API Response:");
        console.log(data);

        return data;

    } catch (error) {

        /*
        ------------------------------------------------
        AbortError 처리
        ------------------------------------------------
        */

        if (error.name === "AbortError") {

            console.error("Request timed out and was aborted.");

        } else {

            /*
            일반 API 에러
            */

            console.error("API Request Failed:");
            console.error(error.message);

        }

        return null;

    } finally {

        /*
        ------------------------------------------------
        timeout 해제
        ------------------------------------------------
        */

        clearTimeout(timeoutId);

    }

}

/*
========================================================
실행 예제
========================================================
*/

const API_URL = "https://jsonplaceholder.typicode.com/posts/1";

/*
정상 요청
*/

fetchWithTimeout(API_URL, 5000);


/*
짧은 timeout 테스트

실제로는 네트워크 상황에 따라
abort 될 수 있다.
*/

fetchWithTimeout(API_URL, 1);