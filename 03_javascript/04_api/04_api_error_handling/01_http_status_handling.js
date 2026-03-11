/*
========================================================
HTTP Status Handling
========================================================

API 요청을 보낼 때 서버는 항상 HTTP Status Code를 반환한다.

대표적인 상태 코드:

200 OK
→ 요청 성공

201 Created
→ 리소스 생성 성공

400 Bad Request
→ 클라이언트 요청 오류

401 Unauthorized
→ 인증 필요

403 Forbidden
→ 접근 권한 없음

404 Not Found
→ 리소스를 찾을 수 없음

500 Internal Server Error
→ 서버 내부 오류

실무에서는 status code에 따라
로직을 분기해야 한다.
*/

async function fetchUser(userId) {
    const url = `https://jsonplaceholder.typicode.com/users/${userId}`;

    try {
        const response = await fetch(url);

        /*
        ------------------------------------------------
        HTTP Status Code 확인
        ------------------------------------------------
        response.ok 는 status 200~299 범위를 의미
        */

        if (!response.ok) {

            /*
            ------------------------------------------------
            status code 기반 에러 처리
            ------------------------------------------------
            */

            if (response.status === 404) {
                throw new Error("User not found (404)");
            }

            if (response.status === 401) {
                throw new Error("Unauthorized request (401)");
            }

            if (response.status === 500) {
                throw new Error("Server error (500)");
            }

            /*
            기타 에러 처리
            */

            throw new Error(`HTTP error: ${response.status}`);
        }

        /*
        ------------------------------------------------
        정상 응답 처리
        ------------------------------------------------
        */

        const data = await response.json();

        console.log("User Data:");
        console.log(data);

        return data;

    } catch (error) {

        /*
        ------------------------------------------------
        네트워크 오류 / fetch 실패
        ------------------------------------------------
        */

        console.error("API Request Failed:");
        console.error(error.message);

        return null;
    }
}

/*
========================================================
실행 예제
========================================================
*/

fetchUser(1);
fetchUser(999); // 존재하지 않는 사용자