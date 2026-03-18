/*
Day 55 — Object Mapping Patterns

File
03_javascript/05_data_handling/02_object_transform/03_object_mapping_patterns.js

목표
JavaScript 객체(Object)를 다양한 방식으로 매핑(transform)하는 패턴을 익힌다.

핵심 주제
1) 객체 값(value) 변환
2) key 기반 매핑
3) 조건부 매핑
4) API 응답 → UI/분석용 구조 변환
5) 중첩 객체 일부 변환

한국어 설명
객체 매핑(object mapping)은
기존 객체를 새로운 형태로 가공하는 작업이다.

예:
- 값 단위 변환
- key 이름 변경
- 조건에 따라 일부 필드만 가공
- 화면 표시용 구조로 변경

실무에서는 API 응답, 설정 객체, 사용자 정보, 통계 객체 등을
다시 가공하는 일이 매우 많다.
*/


/* ============================================================
1) Basic Value Mapping
============================================================ */

/*
사용자 점수 객체
*/

const scores = {
  alice: 85,
  bob: 92,
  charlie: 78
};

console.log("Original scores:", scores);

/*
모든 점수에 +5 적용
*/

const boostedScores = Object.fromEntries(
  Object.entries(scores).map(([name, score]) => [name, score + 5])
);

console.log("Boosted scores:", boostedScores);


/* ============================================================
2) Key Mapping Pattern
============================================================ */

/*
key 이름에 prefix 추가
*/

const prefixedScores = Object.fromEntries(
  Object.entries(scores).map(([name, score]) => [`user_${name}`, score])
);

console.log("Prefixed keys:", prefixedScores);


/* ============================================================
3) Conditional Mapping
============================================================ */

/*
점수에 따라 pass/fail 상태 추가
*/

const scoreStatus = Object.fromEntries(
  Object.entries(scores).map(([name, score]) => {
    return [
      name,
      {
        score: score,
        passed: score >= 80
      }
    ];
  })
);

console.log("Score status object:", scoreStatus);


/* ============================================================
4) Mapping Object to Display-Friendly Labels
============================================================ */

/*
내부 key를 사람이 읽기 쉬운 label로 변경
*/

const userProfile = {
  first_name: "Junyeong",
  last_name: "Song",
  job_role: "Data Scientist",
  years_experience: 2
};

const displayLabels = {
  first_name: "First Name",
  last_name: "Last Name",
  job_role: "Job Role",
  years_experience: "Years of Experience"
};

const displayProfile = Object.fromEntries(
  Object.entries(userProfile).map(([key, value]) => {
    return [displayLabels[key] || key, value];
  })
);

console.log("Display profile:", displayProfile);


/* ============================================================
5) API Response Mapping
============================================================ */

/*
API 응답 예시
*/

const apiUser = {
  id: 101,
  username: "junixion_ai",
  email: "jun@example.com",
  is_active: true,
  signup_date: "2026-03-01"
};

/*
UI/프론트엔드 친화적 구조로 매핑
*/

const mappedApiUser = {
  userId: apiUser.id,
  userName: apiUser.username,
  email: apiUser.email,
  status: apiUser.is_active ? "Active" : "Inactive",
  joinedAt: apiUser.signup_date
};

console.log("Mapped API user:", mappedApiUser);


/* ============================================================
6) Mapping with Filtering
============================================================ */

/*
null 값 제거 후 값 변환
*/

const rawMetrics = {
  views: 1200,
  clicks: 85,
  conversions: null,
  revenue: 3400
};

const cleanedMetrics = Object.fromEntries(
  Object.entries(rawMetrics)
    .filter(([key, value]) => value !== null)
    .map(([key, value]) => [key, value])
);

console.log("Cleaned metrics:", cleanedMetrics);


/* ============================================================
7) Mapping to Percentage Format
============================================================ */

/*
비율 데이터를 퍼센트 문자열로 변환
*/

const ratios = {
  openRate: 0.42,
  clickRate: 0.13,
  conversionRate: 0.07
};

const formattedRatios = Object.fromEntries(
  Object.entries(ratios).map(([key, value]) => {
    return [key, `${(value * 100).toFixed(1)}%`];
  })
);

console.log("Formatted ratios:", formattedRatios);


/* ============================================================
8) Nested Object Mapping
============================================================ */

/*
중첩 객체 일부 변환
*/

const order = {
  orderId: 5001,
  customer: {
    name: "Junyeong",
    country: "Korea"
  },
  payment: {
    amount: 120,
    currency: "USD"
  }
};

const mappedOrder = {
  id: order.orderId,
  customerName: order.customer.name,
  customerCountry: order.customer.country,
  paymentLabel: `${order.payment.amount} ${order.payment.currency}`
};

console.log("Mapped order:", mappedOrder);


/* ============================================================
9) Mapping Object to Summary Rows
============================================================ */

/*
객체를 표/리포트용 배열로 변환
*/

const systemStats = {
  cpu: 72,
  memory: 61,
  disk: 80
};

const statRows = Object.entries(systemStats).map(([metric, value]) => {
  return {
    metric: metric,
    value: value,
    warning: value >= 80
  };
});

console.log("Stat rows:", statRows);


/* ============================================================
10) Reusable Object Mapping Helper
============================================================ */

/*
재사용 가능한 helper 함수
*/

function mapObjectValues(obj, mapper) {
  return Object.fromEntries(
    Object.entries(obj).map(([key, value]) => [key, mapper(value, key)])
  );
}

const doubledStats = mapObjectValues(systemStats, (value) => value * 2);
console.log("Doubled stats:", doubledStats);

const labeledStats = mapObjectValues(systemStats, (value, key) => `${key}: ${value}`);
console.log("Labeled stats:", labeledStats);


/* ============================================================
11) Real-World Pattern: Config Mapping
============================================================ */

/*
설정 객체를 환경별로 가공
*/

const appConfig = {
  host: "localhost",
  port: 3000,
  debug: true
};

const envConfig = mapObjectValues(appConfig, (value, key) => {
  if (key === "debug") {
    return value ? "enabled" : "disabled";
  }
  return value;
});

console.log("Environment config:", envConfig);


/* ============================================================
12) Summary
============================================================ */

/*
정리

객체 매핑의 핵심 패턴

1. Object.entries()로 객체를 배열로 변환
2. map/filter로 원하는 형태로 가공
3. Object.fromEntries()로 다시 객체 복원

대표 사용 사례
- 값 변환
- key 변경
- 조건부 가공
- API 응답 정리
- UI 출력용 구조 생성

즉,
object mapping은 JavaScript 데이터 처리에서
매우 중요한 핵심 패턴이다.
*/

console.log("Summary complete.");